from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

@app.get("/")
def root():
    return {"message": "Weocome to my api"}

@app.get("/posts")
def get_posts():
    return {"data": "This is your posts"}

@app.post("/createposts")
def create_posts(post: Post):
    print(post)
    print(post.dict())
    return {"data": post}