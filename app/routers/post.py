from fastapi import status, Depends, APIRouter
from typing import List
from sqlalchemy import func
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from ..utils.post import get_post_by_id_or_404, check_post_ownership

router = APIRouter(
    prefix = "/posts",
    tags = ["Posts"]
)

@router.get("/", response_model=List[schemas.PostResponseWithVote])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: str = ""):
    result = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return result

@router.get("/my", response_model=List[schemas.PostResponseWithVote])
def get_my_posts(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    result = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.user_id == current_user.id).all()
    return result

@router.get("/{id}", response_model=schemas.PostResponseWithVote)
def get_post(id: int, db: Session = Depends(get_db)):
    result = get_post_by_id_or_404(id, db)
    return result

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostRequest, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    result = models.Post(**post.dict(), user_id=current_user.id)
    db.add(result)
    db.commit()
    db.refresh(result) # to get result returned
    return result

@router.put("/{id}", response_model=schemas.PostResponseWithVote)
def update_post(id: int, updated_post: schemas.PostRequest, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    post = get_post_by_id_or_404(id, db)
    check_post_ownership(post, current_user)
    db.query(models.Post).filter(models.Post.id == id).update(updated_post.dict(), synchronize_session=False)
    db.commit()
    result = get_post_by_id_or_404(id, db)
    return result

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    post = get_post_by_id_or_404(id, db)
    check_post_ownership(post, current_user)
    db.delete(post.Post)
    db.commit()
    return
