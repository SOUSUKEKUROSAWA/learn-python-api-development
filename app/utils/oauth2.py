from datetime import datetime, timedelta
from jose import JWTError, jwt
from .. import schemas
from ..config import settings

def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        id: str = payload.get("user_id")
        if id is None:
            raise credential_exception
        result = schemas.TokenData(id=id) # veridation & formatting
        return result
    except JWTError:
        raise credential_exception

def create_payload(data: dict):
    result = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    result.update({"exp": expire})
    return result