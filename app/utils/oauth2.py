from datetime import datetime, timedelta
import os
from jose import JWTError, jwt
from . import schemas

def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        id: str = payload.get("user_id")
        if id is None:
            raise credential_exception
        result = schemas.TokenData(id=id) # veridation & formatting
        return result
    except JWTError:
        raise credential_exception

def create_payload(data: dict):
    result = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    result.update({"exp": expire})
    return result