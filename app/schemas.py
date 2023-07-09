from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostRequest(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    user_id: int
    class Config:
        orm_mode = True

class PostResponseWithVote(BaseModel):
    Post: PostResponse
    votes: int
    class Config:
        orm_mode = True

class UserRequest(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Direction(Enum):
    Add = 1
    Delete = 0

class VoteRequest(BaseModel):
    post_id: int
    dir: Direction
    class Config:
        orm_mode = True