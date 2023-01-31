from fastapi import FastAPI
from fastapi.params import Body

from pydantic import BaseModel
from typing import Optional


# data schema
class some_scehma(BaseModel):
    a: int
    b: int

    # default values
    c: bool = True

    # optional values
    d: Optional[int] = None


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "FastAPI, Hello World"}

@app.post("/some_post_method")
async def some_post_method(payload: dict = Body(...)):
    return {"message": "a: {}, b: {}".format(payload['a'], payload['b'])}

@app.post("/some_post_method1")
async def some_post_method(payload: some_scehma):
    print(payload.a, payload.b, payload.c)

    return {"message": payload}