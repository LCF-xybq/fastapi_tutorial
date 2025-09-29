import uvicorn
from enum import Enum
from fastapi import FastAPI, Path
from typing import Annotated
from pydantic import BeforeValidator


app = FastAPI()

@app.get("/items1/{item_id}")
async def read_items1(item_id: int):
    return {"item_id: ": item_id}

@app.get("/items2/{item_id}")
async def read_items2(item_id: str = Path(..., regex='^a\d{2}$')):
    return {"item_id: ": item_id}

class ClassName(str, Enum):
    aa = "aa"
    bb = "bb"
    cc = "cc"

@app.get("/items3/{model}")
async def read_items3(model: ClassName):
    return {"model_name: ": model}


def validate(value):
    if not value.startswith("P-"):
        raise ValueError("must startswith P-")
    return value

Item = Annotated[str, BeforeValidator(validate)]
    
@app.get("/items4/{item_id}")
async def read_items4(item_id: Item):
    return {"item_id: ": item_id}


if __name__ == "__main__":
    uvicorn.run("path_query:app", host="127.0.0.1", port=8000, reload=True)
