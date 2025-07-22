# app/transcribe.py

import os
import logging
from groq import Groq
from .config import settings

logger = logging.getLogger(__name__)
logger.info(f"Transcribe module loaded (using Groq Whisper: whisper-large-v3)")

# Initialize a single Groq client for transcription
_groq_client = Groq(api_key=settings.groq_api_key)

def transcribe(audio_path: str) -> str:
    """
    Transcribe an audio file via Groq's Whisper-large-v3 model.
    
    Args:
        audio_path: Path to the local audio file (.mp3, .m4a, etc.)
    
    Returns:
        The transcribed text.
    """
    logger.info(f"Beginning transcription via Groq: {audio_path}")
    if not os.path.exists(audio_path):
        logger.error(f"Audio file not found: {audio_path}")
        raise FileNotFoundError(f"Audio not found: {audio_path}")

    # Read file bytes
    with open(audio_path, "rb") as f:
        audio_bytes = f.read()

    # Call Groq transcription endpoint
    transcription = _groq_client.audio.transcriptions.create(
        file=(os.path.basename(audio_path), audio_bytes),
        model="whisper-large-v3",
        response_format="verbose_json"
    )

    text = transcription.text
    logger.info("Transcription completed via Groq")
    return text
