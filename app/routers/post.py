from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import schemas, models, oauth2
from ..database import get_db



router = APIRouter(
    prefix= "/posts",
    tags= ["Posts"]
)


@router.get("/", response_model = List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10, offset: int = 0, search: Optional[str] = ""):
    posts = db.query(models.Post).filter(
                models.Post.owner_id == current_user.id,
                models.Post.title.contains(search)).limit(limit).offset(offset).all()
    
    if not posts:
        raise HTTPException(
            status_code= status.HTTP_204_NO_CONTENT,
            detail= "No Posts were found"
        )

    return posts

@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.PostResponse)
async def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), 
    current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(
                        owner_id = current_user.id,
                        **post.dict()
                        )

    db.add(new_post)
    db.commit()

    db.refresh(new_post)     

    return new_post

@router.get("/{id}", response_model = schemas.PostResponse)
async def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Post does not exist",
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Not Authorized"
        )

    return post

@router.delete("/{id}", response_model = schemas.PostResponse)
async def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)
    
    if not post.first():
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Post does not exist"
        )

    if post.first().owner_id != current_user.id:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Not Authorized"
        )

    post.delete(synchronize_session = False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model = schemas.PostResponse)
async def update_post(id: int, post: schemas.PostBase, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if not post_query.first():
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Post does not exist"
        )

    if post_query.first().owner_id != current_user.id:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Not Authorized"
        )

    post_query.update(post.dict(), synchronize_session= False)

    db.commit()

    return post_query.first()