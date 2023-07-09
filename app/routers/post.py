from fastapi import status, HTTPException, Depends, APIRouter
from typing import List
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix = "/posts",
    tags = ["Posts"]
)

@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    result = db.query(models.Post).all()
    return result

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostRequest, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    result = models.Post(**post.dict(), user_id=current_user.id)
    db.add(result)
    db.commit()
    db.refresh(result) # to get result returned
    return result

@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    result = db.query(models.Post).filter(models.Post.id == id).first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return result

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    query_get_post_by_id = db.query(models.Post).filter(models.Post.id == id)
    post = query_get_post_by_id.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    query_get_post_by_id.delete(synchronize_session=False)
    db.commit()
    return

@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostRequest, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    query_get_post_by_id = db.query(models.Post).filter(models.Post.id == id)
    post = query_get_post_by_id.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    query_get_post_by_id.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    result = query_get_post_by_id.first()
    return result