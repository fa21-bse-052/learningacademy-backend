import logging
from typing import List, Optional
from pydantic import BaseModel
from typing import List

# ─── Logging ───────────────────────────────────────────────────────────────────
logger = logging.getLogger(__name__)
logger.info("Schemas module imported")

# ─── Models ────────────────────────────────────────────────────────────────────
class VideoToQuizRequest(BaseModel):
    num_questions: int 

class QuizQuestion(BaseModel):
    question: str
    options: Optional[List[str]] = None  # <-- make optional
    answer: str
    type: str  # "MCQ" or "Short-answer"


class VideoToQuizResponse(BaseModel):
    transcript: str
    quiz: List[QuizQuestion]


# New ones
# For quiz checking
class QuizFeedback(BaseModel):
    question: str
    correct_answer: str
    user_answer: str
    is_correct: bool

class QuizCheckRequest(BaseModel):
    questions: List[QuizQuestion]
    answers: List[str]

class QuizCheckResponse(BaseModel):
    score: int
    total: int
    feedback: List[QuizFeedback]