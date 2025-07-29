import os
import uuid
import json
import logging
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from typing import List
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.certificate_utils import generate_certificate  # Correct relative import
from fastapi import APIRouter


# ─── FastAPI App ───────────────────────────────────────────────────────────────
app = FastAPI(title="Video→Quiz API")

# ─── Routers ───────────────────────────────────────────────────────────────────
from app.auth import router as auth_router
from app.video_progress import router as video_progress_router

# ─── Imports ───────────────────────────────────────────────────────────────────
from app.schemas import (
    VideoToQuizRequest,
    VideoToQuizResponse,
    QuizCheckRequest,
    QuizCheckResponse,
    QuizQuestion
)
from .audio import extract_audio
from .transcribe import transcribe
from .quiz import generate_quiz
from app.quiz_check import check_quiz

# ─── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(name)s — %(levelname)s — %(message)s"
)
logger = logging.getLogger(__name__)
logger.info("Starting FastAPI app")

# ─── Temporary Directory ───────────────────────────────────────────────────────
TEMP_DIR = "tmp"
os.makedirs(TEMP_DIR, exist_ok=True)
logger.info(f"Temporary dir ready at {TEMP_DIR}")

# ─── Include Routers ───────────────────────────────────────────────────────────
app.include_router(auth_router)
app.include_router(video_progress_router)

# ─── Health Check ──────────────────────────────────────────────────────────────
@app.get("/health")
def health_check():
    logger.info("Health check ping")
    return {"status": "ok"}

# ─── Video to Quiz ─────────────────────────────────────────────────────────────
@app.post("/video-to-quiz", response_model=VideoToQuizResponse)
async def video_to_quiz(
    num_questions: int = Form(...),
    quiz_type: str = Form("both"),
    video_file: UploadFile = File(...)
):
    logger.info(f"video-to-quiz called — num_questions={num_questions}, quiz_type={quiz_type}, filename={video_file.filename}")
    valid_types = {"mcq", "short", "both"}
    if quiz_type.lower() not in valid_types:
        raise HTTPException(status_code=400, detail=f"Invalid quiz_type. Must be one of: {valid_types}")

    uid = uuid.uuid4().hex
    video_path = os.path.join(TEMP_DIR, f"{uid}.mp4")
    logger.info(f"Saving uploaded video to {video_path}")
    with open(video_path, "wb") as f:
        f.write(await video_file.read())

    audio_path = os.path.join(TEMP_DIR, f"{uid}.mp3")
    try:
        extract_audio(video_path, audio_path)
    except Exception as e:
        logger.exception("Audio extraction failed")
        raise HTTPException(status_code=400, detail=str(e))

    try:
        transcript = transcribe(audio_path)
    except Exception as e:
        logger.exception("Transcription failed")
        raise HTTPException(status_code=500, detail=f"Transcription error: {e}")

    try:
        raw_quiz = generate_quiz(transcript, num_questions, quiz_type)
        logger.info(f"Raw quiz output: {repr(raw_quiz)}")

        if "```json" in raw_quiz:
            raw_quiz = raw_quiz.split("```json")[1].split("```")[0].strip()
        elif "```" in raw_quiz:
            raw_quiz = raw_quiz.split("```")[1].strip()
    except Exception as e:
        logger.exception("Quiz generation failed")
        raise HTTPException(status_code=500, detail=f"Quiz generation error: {e}")

    try:
        quiz_list = json.loads(raw_quiz)
        quiz_objs: List[QuizQuestion] = [QuizQuestion(**q) for q in quiz_list]
    except Exception as e:
        logger.exception("Quiz parsing failed")
        raise HTTPException(status_code=500, detail=f"Quiz parsing error: {e}")

    logger.info("video-to-quiz completed successfully")
    return VideoToQuizResponse(transcript=transcript, quiz=quiz_objs)

# ─── Quiz Check ────────────────────────────────────────────────────────────────
@app.post("/check-quiz", response_model=QuizCheckResponse)
def check_quiz_endpoint(payload: QuizCheckRequest):
    logger.info("check-quiz called")
    try:
        return check_quiz(payload)
    except Exception as e:
        logger.error("Quiz checking failed", exc_info=e)
        raise HTTPException(status_code=500, detail=str(e))
# certificate

from app.certificate_utils import generate_certificate  # Correct relative import
from fastapi import APIRouter
from fastapi.responses import FileResponse

class CertificateRequest(BaseModel):
    name: str
      

@app.post("/certificate")
async def assign_certificate(data: CertificateRequest):
    

    pdf_path = generate_certificate(data.name)

    return FileResponse(
        pdf_path,
        media_type='application/pdf',
        filename=os.path.basename(pdf_path)
    )
