from fastapi import status, HTTPException, Depends, APIRouter
from typing import List
from .. import models, schemas
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix = "/posts",
    tags = ["Posts"]
)

@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    result = db.query(models.Post).all()
    return result

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    result = models.Post(**post.dict())
    db.add(result)
    db.commit()
    db.refresh(result) # to get result returned
    return result

@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    result = db.query(models.Post).filter(models.Post.id == id).first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return result

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    query_get_post_by_id = db.query(models.Post).filter(models.Post.id == id)
    if not query_get_post_by_id.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    query_get_post_by_id.delete(synchronize_session=False)
    db.commit()
    return

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    query_get_post_by_id = db.query(models.Post).filter(models.Post.id == id)
    if not query_get_post_by_id.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    query_get_post_by_id.update(post.dict(), synchronize_session=False)
    db.commit()
    result = query_get_post_by_id.first()
    return result