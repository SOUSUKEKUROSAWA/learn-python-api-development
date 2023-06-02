from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [
    {
        "title": "title of post 1",
        "content": "content of post 1",
        "id": 1,
    },
    {
        "title": "title of post 2", 
        "content": "content of post 2", 
        "id": 2,
    },
]

@app.get("/")
def root():
    return {"message": "Weocome to my api"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts")
def create_posts(post: Post):
    new_post = post.dict()
    new_post["id"] = len(my_posts) + 1
    my_posts.append(new_post)
    return {"data": new_post}