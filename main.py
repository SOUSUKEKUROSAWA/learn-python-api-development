from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

posts = [
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
    for post in posts:
        if post["id"] == id:
            return post

@app.get("/")
def root():
    return {"message": "success"}

@app.get("/posts")
def get_posts():
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    result = post.dict()
    result["id"] = len(posts) + 1
    posts.append(result)
    return {"data": result}

@app.get("/posts/{id}")
def get_post(id: int):
    result = find_post(id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return {"data": result}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    posts.remove(post)
    return

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    result = find_post(id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    result.update(post.dict())
    return {"data": result}