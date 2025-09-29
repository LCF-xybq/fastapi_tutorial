import uvicorn
from fastapi import FastAPI


app = FastAPI()


@app.get("/query1")
async def get_query(id: int, name: str):
    return {"id: ": id, "name: ": name}


if __name__ == "__main__":
    uvicorn.run("query:app", host="127.0.0.1", port=8000, reload=True)
