import logging
from typing import List, Optional
from pydantic import BaseModel
from typing import List

# ─── Logging ───────────────────────────────────────────────────────────────────
logger = logging.getLogger(__name__)
logger.info("Schemas module imported")

# ─── Models ────────────────────────────────────────────────────────────────────


class QuizQuestion(BaseModel):
    question: str
    options: Optional[List[str]] = []
    answer: Optional[str] = ""
    type: str

class QuizCheckRequest(BaseModel):
    transcript: str
    questions: List[QuizQuestion]
    answers: List[str]

class QuizCheckResponse(BaseModel):
    score: int
    total: int
    feedback: List[dict]

class VideoToQuizRequest(BaseModel):
    transcript: str
    num_questions: int
    quiz_type: str

class VideoToQuizResponse(BaseModel):
    transcript: str
    quiz: List[QuizQuestion]
