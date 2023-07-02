import time
from typing import List
from fastapi import FastAPI, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from . import models, schemas, utils
from .database import engine, get_db
from sqlalchemy.orm import Session
load_dotenv()

# create new tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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

@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    result = db.query(models.Post).all()
    return result

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    result = models.Post(**post.dict())
    db.add(result)
    db.commit()
    db.refresh(result) # to get result returned
    return result

@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    result = db.query(models.Post).filter(models.Post.id == id).first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return result

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    post.delete(synchronize_session=False)
    db.commit()
    return

@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    result = db.query(models.Post).filter(models.Post.id == id)
    if not result.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    result.update(post.dict(), synchronize_session=False)
    db.commit()
    return result.first()

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user_dict = user.dict()
    # hash the password - user.password
    hashed_password = utils.hash(user.password)
    user_dict['password'] = hashed_password
    # create user in db
    result = models.User(**user_dict)
    db.add(result)
    db.commit()
    db.refresh(result)
    return result