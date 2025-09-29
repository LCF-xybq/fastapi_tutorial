import uvicorn
from typing import List, Optional
from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    id: int
    name: str
    price: float
    category: str

class Pagination(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int

class ListResponse(BaseModel):
    status: str = "success"
    data: List[Item]
    pagination: Pagination


DB = [Item(id=i, name=f"A{i}", price=100 * i, category="U" if i % 2 ==0 else "H") for i in range(1, 101)]

@app.get("/items1")
async def get_items1():
    return ["A1", "A2", "A3"]

@app.get("/items2")
async def get_items2():
    return DB

@app.get("/items3")
async def get_items3(category: Optional[str]=Query(None, description="fen lei")):
    temp = []
    if category:
        for item in DB:
            if item.category == category:
                temp.append(item)

    return temp

@app.get("/items4")
async def get_items4(page: int = Query(1, ge=1, description="page"),
                     page_size: int = Query(10, ge=1, le=100, description="size"),
                     category: Optional[str]=Query(None, description="fen lei")):
    
    filter_items = DB
    if category:
        filter_items = [item for item in DB if item.category == category]
    
    total = len(filter_items)
    total_page = (total + page_size - 1) // page_size
    start = (page - 1) * page_size
    end = start + page_size

    return ListResponse(data=filter_items[start: end],
                        pagination=Pagination(total=total,
                                              page=page,
                                              page_size=page_size,
                                              total_pages=total_page))



if __name__ == "__main__":
    uvicorn.run("rsp_list:app", host="127.0.0.1", port=8000, reload=True)
