import uvicorn
from fastapi import FastAPI, Query


app = FastAPI()

@app.get("/items1")
async def get_items1(id: str = Query(12)):
    return {"id: ": id}

@app.get("/items2")
async def get_items2(id: str = Query(...)):
    """necessary"""
    return {"id: ": id}

@app.get("/items3")
async def get_items3(id: str = Query(..., min_length=2, max_length=6)):
    return {"id: ": id}

@app.get("/items4")
async def get_items4(id: int = Query(..., gt=6, lt=20)):
    return {"id: ": id}


if __name__ == "__main__":
    uvicorn.run("get_query:app", host="127.0.0.1", port=8000, reload=True)
