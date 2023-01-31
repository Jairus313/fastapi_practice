from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas
from .database import engine, get_db
from .utils import hash
from .routers import post, user



models.base.metadata.create_all(bind = engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)


@app.get("/")
async def root():
    return "Server is up"