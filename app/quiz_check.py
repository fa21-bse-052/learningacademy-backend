# app/quiz_check.py

import json
import logging
import re
from typing import List
from groq import Groq

from app.schemas import QuizCheckRequest, QuizCheckResponse, QuizQuestion
from .config import settings

logger = logging.getLogger(__name__)
logger.info("LLM-based quiz checking module loaded")

_client = Groq(api_key=settings.groq_api_key)

def clean_llm_response(content: str) -> str:
    """Remove markdown code block formatting like ```json ... ``` or ```...```."""
    if "```json" in content:
        match = re.search(r"```json\s*(.*?)\s*```", content, re.DOTALL)
        if match:
            return match.group(1).strip()
    elif "```" in content:
        match = re.search(r"```(.*?)```", content, re.DOTALL)
        if match:
            return match.group(1).strip()
    return content.strip()

def check_quiz_answers_llm(questions: List[QuizQuestion], answers: List[str], transcript: str) -> QuizCheckResponse:
    prompt = f"""
You are an intelligent quiz evaluator.

You are provided with:
- A transcript from a presentation
- A list of quiz questions (without correct answers)
- A list of user-provided answers

Your task is to:
- Evaluate each answer based only on the transcript
- For each question, compare the user's answer to the relevant content in the transcript
- Decide if the user's answer is correct

Return the result in this format and respond with ONLY this JSON:
[
  {{
    "question": "question text",
    "user_answer": "user's answer",
    "correct_answer": "best match from transcript",
    "is_correct": true or false
  }},
  ...
]

Transcript:
\"\"\"
{transcript}
\"\"\"

Questions:
{json.dumps([q.question for q in questions], indent=2)}

User Answers:
{json.dumps(answers, indent=2)}
"""

    logger.info("Starting LLM-based quiz checking using transcript context...")
    response = _client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    raw_content = response.choices[0].message.content.strip()
    logger.debug("LLM raw output:\n%s", raw_content)

    cleaned_content = clean_llm_response(raw_content)

    try:
        result = json.loads(cleaned_content)
        score = sum(1 for item in result if item.get("is_correct"))
        return QuizCheckResponse(score=score, total=len(questions), feedback=result)

    except json.JSONDecodeError as e:
        logger.error("Failed to parse LLM response: %s", e)
        logger.debug("Cleaned LLM output:\n%s", cleaned_content)
        raise ValueError("LLM response could not be parsed as JSON")

def check_quiz(payload: QuizCheckRequest) -> QuizCheckResponse:
    logger.info("check_quiz called")
    return check_quiz_answers_llm(payload.questions, payload.answers, payload.transcript)
