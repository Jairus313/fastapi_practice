from fastapi import FastAPI
from fastapi.params import Body

from pydantic import BaseModel
from typing import Optional


class post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


app = FastAPI()

my_posts = [
    {
        "title": "post 1",
        "content": "post 1 content",
        "id": 1
    },
    {
        "title": "post 2",
        "content": "post 2 content",
        "id": 2 
    }
]

@app.get("/")
async def root():
    return {"message": "FastAPI, Hello World"}

# for references
# @app.post("/posts")
# async def get_posts(payload: dict = Body(...)):
#     return {"message": "a: {}, b: {}".format(payload['a'], payload['b'])}

@app.get("/posts")
async def get_posts():
    return {"data": my_posts}

@app.post("/posts")
async def create_posts(payload: post):
    payload = payload.dict()
    payload["id"] = len(my_posts) + 1

    my_posts.append(payload)

    return {"data": payload}