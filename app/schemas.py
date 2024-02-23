from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint


# create a class and make a template for the user and bound him/her. Use the pydantic lib "All this is for validation purpose".


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class UsersCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime 

    class Config:
        orm_mode = True

class Post(PostBase):
    id: int
    owner_id: int
    owner: UserOut
    created_at: datetime 

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None


class Votes(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)