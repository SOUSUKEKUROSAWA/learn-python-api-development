import time
from fastapi import FastAPI, status, HTTPException
import psycopg2
from pydantic import BaseModel
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

load_dotenv()

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

end_time = datetime.now() + timedelta(seconds=30)

while True:
    if datetime.now() > end_time:
        raise Exception("Could not connect to the database within 30 seconds")

    try:
        conn = psycopg2.connect(host=os.getenv("DB_HOST"), database=os.getenv("DB_NAME"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"), cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Database connection failed")
        print(error)
        time.sleep(2)

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
    cursor.execute(
        """
        select 
            * 
        from 
            posts
        """
    )
    result = cursor.fetchall()
    return {"data": result}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute(
        """
        insert
        into
            posts
            (title, content, published)
        values
            (%s, %s, %s) returning *
        """,
        (post.title, post.content, post.published)
    )
    result = cursor.fetchone()
    conn.commit()
    return {"data": result}

@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute(
        """
        select 
            * 
        from 
            posts
        where
            id = %s
        """,
        (id,)
    )
    result = cursor.fetchone()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return {"data": result}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(
        """
        delete
        from 
            posts
        where
            id = %s returning *
        """,
        (id,)
    )
    post = cursor.fetchone()
    conn.commit()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(
        """
        update
            posts
        set
            title = %s, content = %s, published = %s
        where
            id = %s returning *
        """,
        (post.title, post.content, post.published, id)
    )
    result = cursor.fetchone()
    conn.commit()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return {"data": result}