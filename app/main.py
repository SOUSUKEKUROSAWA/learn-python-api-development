from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from . import models
from .database import engine
from .routers import post, user, vote, auth

app = FastAPI()

@app.get("/")
def root():
    return RedirectResponse(url="/docs")

app.include_router(post.router)
app.include_router(user.router)
app.include_router(vote.router)
app.include_router(auth.router)