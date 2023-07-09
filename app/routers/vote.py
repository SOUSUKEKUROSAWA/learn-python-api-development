from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, database, models, oauth2
from ..utils.post import get_post_by_id_or_404

router = APIRouter(
    prefix = "/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.VoteRequest, db: database.SessionLocal = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    get_post_by_id_or_404(vote.post_id, db)
    query_get_vote_by_post_id_and_user_id = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = query_get_vote_by_post_id_and_user_id.first()
    if (vote.dir == schemas.Direction.Add):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exist")
        query_get_vote_by_post_id_and_user_id.delete(synchronize_session=False)
        db.commit()
        return {"message": "Successfully deleted vote"}

    