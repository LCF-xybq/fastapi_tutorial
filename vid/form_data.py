import uvicorn
from fastapi import FastAPI, Form
from pydantic import BaseModel
from typing import Annotated


app = FastAPI()

class User(BaseModel):
    user: str
    passwd: str

@app.post("/login1")
async def create_user(user: Annotated[User, Form(...)]):
    return user


if __name__ == "__main__":
    uvicorn.run("form_data:app", host="127.0.0.1", port=8000, reload=True)
