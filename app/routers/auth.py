from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..utils import auth
from ..database import get_db
from .. import models, oauth2, schemas
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
    tags=["Authentication"],
)

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    if not auth.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    result = oauth2.create_access_token(data = {"user_id": user.id})
    return {"access_token": result, "token_type": "bearer"} # リクエストの度に新しいシグネチャが生成される