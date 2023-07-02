import time
from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from . import models
from .database import engine
from .routers import post, user, auth

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

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)