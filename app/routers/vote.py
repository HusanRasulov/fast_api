from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils, database, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/vote",
    tags=["votes"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_vote(vote_req: schemas.Vote, db: Session = Depends(database.get_db),
                current_user: models.User = Depends(oauth2.get_current_user)):
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote_req.post_id,
                                              models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if vote_req.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Vote already taken")

        new_vote = models.Vote(user_id=current_user.id, post_id=vote_req.post_id)
        db.add(new_vote)
        db.commit()
        return {"message": "Vote added"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")

        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote"}
