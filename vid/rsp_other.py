import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

@app.get("/string1")
async def get_string1():
    return "Hello"

@app.get("/string2")
async def get_string2():
    return "<html><h1>Hello</h1></html>"

@app.get("/string3", response_class=HTMLResponse)
async def get_string3():
    return "<html><h1>Hello</h1></html>"

@app.get("/items")
async def get_items(item_id: int):
    return {"id: ": item_id}

@app.get("/redirect1", response_class=RedirectResponse)
async def get_redirect1():
    return RedirectResponse(url="/string1")

@app.get("/redirect2", response_class=RedirectResponse)
async def get_redirect2():
    return RedirectResponse(url="/items?item_id=12")

# 挂 HTML 目录
app.mount('/html2', StaticFiles(directory="html_data", html=True))


if __name__ == "__main__":
    uvicorn.run("rsp_other:app", host="127.0.0.1", port=8000, reload=True)
