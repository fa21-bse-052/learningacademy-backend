import json
import logging
from typing import List
from groq import Groq

from app.schemas import QuizCheckRequest, QuizCheckResponse, QuizQuestion
from .config import settings

logger = logging.getLogger(__name__)
logger.info("LLM-based quiz checking module loaded")

_client = Groq(api_key=settings.groq_api_key)


def check_quiz_answers_llm(questions: List[QuizQuestion], answers: List[str]) -> QuizCheckResponse:
    questions_data = [
        {
            "question": q.question,
            "answer": q.answer
        }
        for q in questions
    ]

    prompt = f"""
You are a quiz evaluator.

For each question, compare the user's answer to the correct answer and return JSON in this format:

[
  {{
    "question": "question text",
    "user_answer": "user's answer",
    "correct_answer": "correct answer",
    "is_correct": true or false
  }},
  ...
]

Questions:
{json.dumps(questions_data, indent=2)}

User Answers:
{json.dumps(answers, indent=2)}
"""

    logger.info("Starting LLM-based quiz checking...")
    response = _client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    content = response.choices[0].message.content.strip()
    logger.debug("LLM raw output:\n%s", content)

    try:
        result = json.loads(content)
        score = sum(1 for item in result if item.get("is_correct"))
        return QuizCheckResponse(score=score, total=len(questions), feedback=result)

    except json.JSONDecodeError as e:
        logger.error("Failed to parse LLM response: %s", e)
        logger.debug("Raw LLM output:\n%s", content)
        # 🛑 Fallback to manual comparison
        logger.warning("Falling back to manual answer checking...")
        return check_quiz_answers_manual(questions, answers)


def check_quiz_answers_manual(questions: List[QuizQuestion], answers: List[str]) -> QuizCheckResponse:
    feedback = []
    score = 0

    for q, user_ans in zip(questions, answers):
        correct = q.answer.strip().lower() == user_ans.strip().lower()
        if correct:
            score += 1
        feedback.append({
            "question": q.question,
            "user_answer": user_ans,
            "correct_answer": q.answer,
            "is_correct": correct
        })

    return QuizCheckResponse(score=score, total=len(questions), feedback=feedback)


def check_quiz(payload: QuizCheckRequest) -> QuizCheckResponse:
    logger.info("check_quiz called")
    return check_quiz_answers_llm(payload.questions, payload.answers)
