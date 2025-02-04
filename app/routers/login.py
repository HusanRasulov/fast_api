from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import schemas, models, utils, oauth2
from ..database import get_db

router = APIRouter(
    tags=['authentication']
)


@router.post("/login")
async def login(user_credentials: schemas.login, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="password or email is incorrect")

    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="password or email is incorrect")

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return schemas.AccessTokenResponse(access_token=access_token, token_type="Bearer")
