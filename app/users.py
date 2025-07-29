from typing import Optional
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# In-memory user "database"
users_db = {}

def get_user(email: str) -> Optional[dict]:
    return users_db.get(email)

def create_user(username: str, email: str, password: str) -> dict:
    hashed_password = pwd_context.hash(password)
    user = {"username": username, "email": email, "hashed_password": hashed_password}
    users_db[email] = user
    return user

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
