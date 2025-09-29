import uvicorn
from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator


app = FastAPI()

class User(BaseModel):
    name: str = Field(default="joe")
    age: int = Field(...)

@app.post("/users/")
async def create_user(user: User):
    return user

class Account(BaseModel):
    name: str = Field(..., min_length=2, max_length=12)
    passwd: str = Field(..., pattern='^\w{6, 32}$')

@app.post("/account")
async def set_account(account: Account):
    return account

class Email(BaseModel):
    email: str

    @field_validator('email')
    def email_validator(cls, v):
        if not "@" in v:
            raise ValueError("e-mail format error!")
        return v
    
@app.post("/users2")
async def create_users2(user: Email):
    return user 

class order(BaseModel):
    items: list = Field(..., min_length=1, max_length=4)
    address: str = Field(..., description="pei song di zhi")

@app.post("/orders/")
async def create_order(order: order):
    return order

class Status(str, Enum):
    ACTIVATE = "activate"
    INACTIVATE = 'inactivate'

class Task(BaseModel):
    status: Status = Field(default=Status.ACTIVATE)

@app.post("/task/")
async def get_task():
    return Task()


if __name__ == "__main__":
    uvicorn.run("field_valid:app", host="127.0.0.1", port=8000, reload=True)
