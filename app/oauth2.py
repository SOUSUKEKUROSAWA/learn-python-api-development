from fastapi import status, HTTPException, Depends
from jose import jwt
from dotenv import load_dotenv
import os
from . import models
from sqlalchemy.orm import Session
from .database import get_db
from fastapi.security import OAuth2PasswordBearer
from .utils.oauth2 import create_payload, verify_access_token

load_dotenv()

# HTTPリクエストから認証トークン（通常は Authorization ヘッダーから）を抽出する
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict):
    payload = create_payload(data)
    result = jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))
    return result

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token = verify_access_token(token, HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials", headers={"WWW-Authenticate": "Bearer"}))
    result = db.query(models.User).filter(models.User.id == valid_token.id).first()
    return result