import time
from fastapi import FastAPI, status, HTTPException, Depends
import psycopg2
from pydantic import BaseModel
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session
load_dotenv()

# create new tables
models.Base.metadata.create_all(bind=engine)

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

@app.get("/")
def root():
    return {"message": "success"}

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    result = db.query(models.Post).all()
    return {"data": result}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    result = models.Post(**post.dict())
    db.add(result)
    db.commit()
    db.refresh(result) # to get result returned
    return {"data": result}

@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    result = db.query(models.Post).filter(models.Post.id == id).first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return {"data": result}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    post.delete(synchronize_session=False)
    db.commit()
    return

@app.put("/posts/{id}")
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    result = db.query(models.Post).filter(models.Post.id == id)
    if not result.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    result.update(post.dict(), synchronize_session=False)
    db.commit()
    return {"data": result.first()}