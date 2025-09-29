import uvicorn
from fastapi import FastAPI, Path
from typing import Annotated
from pydantic import BeforeValidator


app = FastAPI()

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
