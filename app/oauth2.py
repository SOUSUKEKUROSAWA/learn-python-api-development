from fastapi import status, HTTPException, Depends
from jose import JWTError, jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from . import schemas, models
from sqlalchemy.orm import Session
from .database import get_db
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

# HTTPリクエストから認証トークン（通常は Authorization ヘッダーから）を抽出する
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict):
    payload = create_payload(data)
    result = jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))
    return result

def verify_access_token(token: str, credential_exception):
    # tokenが不正または期限切れである可能性があるためtryで囲う（decodeプロセスは外部入力に依存する）
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        id: str = payload.get("user_id")
        if id is None:
            raise credential_exception
        result = schemas.TokenData(id=id) # veridation & formatting
        return result
    except JWTError: # JWTErrorが発生したときのみ以下を実行
        raise credential_exception

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token = verify_access_token(token, create_credential_exception())
    result = db.query(models.User).filter(models.User.id == valid_token.id).first()
    return result

def create_payload(data: dict):
    result = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    result.update({"exp": expire})
    return result

def create_credential_exception():
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials", headers={"WWW-Authenticate": "Bearer"})