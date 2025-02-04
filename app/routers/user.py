from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils
from sqlalchemy.orm import Session

from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserCreateResponse)
async def create_user(user: schemas.UserBase, db: Session = Depends(get_db)):
    user.password = utils.get_password_hash(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserResponse)
async def read_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user is not found with this id: {id}")

    return user

