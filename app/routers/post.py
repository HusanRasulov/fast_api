from typing import Optional

from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)


@router.get("/")
def get_posts(
        db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user),
        page_size: int = 10,
        page: int = 0,
        search: Optional[str] = ""
):
    post_out_list = []

    res = (
        db.query(
            models.Post,
            func.count(models.Vote.post_id).label("votes")  # Add the vote count as a column
        )
        .outerjoin(models.Vote, models.Post.id == models.Vote.post_id)
        .group_by(models.Post.id)
        .all()
    )

    for post, vote_count in res:
        post = {
            "id": post.id,
            "title": post.title,
            "votes": vote_count
        }
        post_out_list.append(post)

    return res


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(user_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}")
async def get_post(id: int, db: Session = Depends(get_db), current_user: object = Depends(oauth2.get_current_user)):
    post, vote_count = (
        db
        .query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .outerjoin(models.Vote, models.Post.id == models.Vote.post_id)
        .group_by(models.Post.id).filter(models.Post.id == id).first()
    )

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post is not found with this id: {id}")

    post_out = {
        "id": post.id,
        "title": post.title,
        "votes": vote_count
    }

    return post_out


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db), current_user: object = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post is not found with this id: {id}")

    if post.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this action")

    post.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostResponse)
async def update_post(
        id: int,
        updated_post: schemas.PostCreate,
        db: Session = Depends(get_db),
        current_user: object = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post is not found with this id: {id}")

    if post.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this action")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
