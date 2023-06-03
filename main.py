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

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

@app.get("/")
def root():
    return {"result": "success"}

@app.get("/posts")
def get_posts():
    return {"result": my_posts}

@app.post("/posts")
def create_posts(post: Post):
    new_post = post.dict()
    new_post["id"] = len(my_posts) + 1
    my_posts.append(new_post)
    return {"result": new_post}

@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts) - 1]
    return {"result": post}

@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    return {"result": post}