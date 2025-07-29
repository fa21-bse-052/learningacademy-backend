from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr
from pymongo import MongoClient
from app.config import settings
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import bcrypt
import logging
import jwt
from datetime import datetime, timedelta

# ─── Logger ─────────────────────────────────────
logger = logging.getLogger("auth")
router = APIRouter()

# ─── MongoDB Setup ──────────────────────────────
client = MongoClient(settings.mongodb_url)
db = client["learning_academy_db"]
user_collection = db["users"]

# ─── JWT Setup ───────────────────────────────────
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = settings.jwt_secret  # from .env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# ─── Schemas ─────────────────────────────────────
class SignupRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# ─── Utility: JWT Token Generation ───────────────
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ─── Signup Endpoint ─────────────────────────────
@router.post("/signup")
async def signup(user: SignupRequest):
    existing_user = user_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered.")

    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    user_collection.insert_one({
        "username": user.username,
        "email": user.email,
        "password": hashed_password.decode('utf-8')
    })
    logger.info(f"User signed up: {user.email}")
    return {"message": "Signup successful"}

# ─── Login & Token Endpoint ──────────────────────
@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = user_collection.find_one({"email": form_data.username})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not bcrypt.checkpw(form_data.password.encode('utf-8'), user["password"].encode('utf-8')):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user["email"]})
    logger.info(f"JWT issued for: {user['email']}")
    return {"access_token": access_token, "token_type": "bearer"}

# ─── Get Current User (optional utility) ─────────
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_collection.find_one({"email": email})
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


