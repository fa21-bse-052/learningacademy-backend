import logging
from typing import List, Optional
from pydantic import BaseModel, EmailStr  # ✨ Added EmailStr
from typing import List
from typing import List, Union

# ─── Logging ───────────────────────────────────────────────────────────────────
logger = logging.getLogger(__name__)
logger.info("Schemas module imported")

# ─── Models ────────────────────────────────────────────────────────────────────



class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    answer: Union[str, int]  # Accepts either string or integer
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

# ─── Authentication Schemas ────────────────────────────────────────────────────

class UserSignup(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
