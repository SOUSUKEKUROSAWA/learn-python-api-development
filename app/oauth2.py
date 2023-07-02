from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "70b3841b672447e142aa8e9811f0bd0ea92b6a0f24a0d1c273f90e0e2a1b55f1" # $ openssl rand -hex 32
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    payload = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expire})
    result = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return result