import uvicorn
from typing import Union, TypeVar, Generic
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

class Item(BaseModel):
    id: int
    name: str
    tags: list[str] = []

@app.get("/items/dict")
async def get_items_dict():
    return {"name: ": "Alex", "age: ": 12}

@app.get("/items/model1")
async def get_items_model1():
    return Item(id=2, name="Joe")

@app.get("/items/model2", response_model=Item, response_model_exclude_unset=True)
async def get_items_model2():
    return Item(id=2, name="Joe")

# 定义泛型模型
T = TypeVar("T")
class SuccessResponse(BaseModel, Generic[T]):
    status: str = "Success"
    data: T

class ErrorResponse(BaseModel):
    status: str = "Error"
    message: str
    code: int

@app.get("/items/{item_id}", response_model=Union[SuccessResponse[Item], ErrorResponse])
async def get_items_model3(item_id: int):
    if item_id == 1:
        item = Item(id=1, name="HH", tags=["red", "black"])
        return SuccessResponse[Item](data=item)
    else:
        return ErrorResponse(message="Item not found", code=500)


if __name__ == "__main__":
    uvicorn.run("rsp_json:app", host="127.0.0.1", port=8000, reload=True)
