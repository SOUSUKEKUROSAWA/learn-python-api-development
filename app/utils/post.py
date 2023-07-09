from fastapi import status, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import models

def get_post_by_id_or_404(id: int, db: Session):
    result = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return result

def check_post_ownership(post: models.Post, current_user: int):
    if post.Post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")