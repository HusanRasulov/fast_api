from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, conint


class PostBase(BaseModel):
    name: str
    content: str
    is_published: bool = True


class PostCreate(PostBase):
    pass


class UserCreateResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime


class PostResponse(PostBase):
    id: int
    user: UserCreateResponse

    class Config:
        from_attributes = True


class PostOut(PostResponse):
    Post: PostResponse
    votes: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime


class login(BaseModel):
    email: EmailStr
    password: str


class TokenData(BaseModel):
    id: Optional[int] = None


class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)

