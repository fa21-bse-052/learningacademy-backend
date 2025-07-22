import os
import logging
from moviepy import VideoFileClip



logger = logging.getLogger(__name__)
logger.info("Audio module loaded")

def extract_audio(video_path: str, audio_path: str) -> None:
    logger.info(f"extract_audio() start — video_path={video_path}, audio_path={audio_path}")
    if not os.path.isfile(video_path):
        logger.error(f"Video file not found: {video_path}")
        raise FileNotFoundError(f"Video not found: {video_path}")

    clip = VideoFileClip(video_path)
    if clip.audio is None:
        logger.error("No audio track in video")
        raise RuntimeError("No audio track in video")

    clip.audio.write_audiofile(audio_path)
    logger.info(f"Audio extraction succeeded — saved to {audio_path}")
