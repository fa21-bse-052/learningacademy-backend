from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional
from app.db import progress_collection  # MongoDB collection for video progress

router = APIRouter()

class SaveProgressRequest(BaseModel):
    user_email: EmailStr
    video_id: str
    progress_time: float  # in seconds

class GetProgressResponse(BaseModel):
    progress_time: float

@router.post("/save-progress")
async def save_progress(data: SaveProgressRequest):
    # Upsert the progress (insert if not exists, else update)
    result = await progress_collection.update_one(
        {"user_email": data.user_email, "video_id": data.video_id},
        {"$set": {"progress_time": data.progress_time}},
        upsert=True
    )
    return {"message": "Progress saved successfully."}

@router.get("/get-progress", response_model=GetProgressResponse)
async def get_progress(user_email: EmailStr, video_id: str):
    record = await progress_collection.find_one({"user_email": user_email, "video_id": video_id})
    if not record:
        raise HTTPException(status_code=404, detail="No progress found for this video.")
    return {"progress_time": record["progress_time"]}
