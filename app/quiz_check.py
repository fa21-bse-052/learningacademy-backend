# app/quiz_check.py

import logging
from typing import List
from app.schemas import QuizCheckRequest, QuizCheckResponse, QuizQuestion



# app/quiz_check.py

from typing import List
from app.schemas import QuizCheckRequest, QuizCheckResponse, QuizQuestion

def check_quiz_answers(questions: List[QuizQuestion], answers: List[str]):
    feedback = []
    score = 0

    for i, (question, user_answer) in enumerate(zip(questions, answers)):
        correct = question.answer.strip().lower() == user_answer.strip().lower()
        if correct:
            score += 1
        feedback.append({
    "question": question.question,
    "user_answer": user_answer,     # ✅ correct key
    "correct_answer": question.answer,
    "is_correct": correct
})


    return QuizCheckResponse(score=score, total=len(questions), feedback=feedback)


def check_quiz(payload: QuizCheckRequest) -> QuizCheckResponse:
    return check_quiz_answers(payload.questions, payload.answers)
