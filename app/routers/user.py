from fastapi import status, HTTPException, Depends, APIRouter
from typing import List
from .. import models, schemas, utils
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix = "/users",
)

@router.get("/", response_model=List[schemas.UserOut])
def get_users(db: Session = Depends(get_db)):
    result = db.query(models.User).all()
    return result

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user_dict = user.dict()
    # hash the password - user.password
    hashed_password = utils.hash(user.password)
    user_dict['password'] = hashed_password
    # create user in db
    result = models.User(**user_dict)
    db.add(result)
    db.commit()
    db.refresh(result)
    return result

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    result = db.query(models.User).filter(models.User.id == id).first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} was not found")
    return result