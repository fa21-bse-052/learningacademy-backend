import logging
from groq import Groq
from .config import settings

#new
from app.schemas import QuizCheckRequest, QuizCheckResponse
from app.quiz_check import check_quiz


logger = logging.getLogger(__name__)
logger.info("Quiz module loaded")

_client = Groq(api_key=settings.groq_api_key)
logger.info("Groq client initialized")

def generate_quiz(transcript: str, num_questions: int, quiz_type: str = "both") -> str:
    prompt = f"""
You are an expert trainer. Generate {num_questions} quiz questions from the following transcript.

Transcript:
\"\"\"
{transcript}
\"\"\"

Instructions:
- Output should be a JSON list of objects with fields: `question`, `options` (list), `answer`, `type`.
- If `type` is "mcq", include `options`.
- If `type` is "short", leave `options` as an empty list.
- Only generate questions, not answers, if possible.

Constraints:
- Only include {quiz_type.upper()} type questions.
- Types can be: "mcq", "short", or "both".
"""
    ...

    resp = _client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    quiz_json = resp.choices[0].message.content
    logger.info("Quiz generation complete")
    return quiz_json
