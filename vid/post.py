import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

class User(BaseModel):
    name: str
    age: int
    passwd: str | None
    address: str = "here"

@app.post("/users")
async def create_user(user: User):
    return user


if __name__ == "__main__":
    uvicorn.run("post:app", host="127.0.0.1", port=8000, reload=True)
