from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, models
from ..database import get_db



router = APIRouter(
    prefix= "/users",
    tags= ["Users"]
)


@router.post("/", status_code = status.HTTP_201_CREATED, response_model= schemas.UserResponse)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash(user.password)
    user.password = hashed_password

    new_user = models.User(
                        **user.dict()
                        )

    db.add(new_user)
    db.commit()

    db.refresh(new_user)     

    return new_user

@router.get("/{id}", response_model= schemas.UserResponse)
async def get_post(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User does not exist",
        )

    return user