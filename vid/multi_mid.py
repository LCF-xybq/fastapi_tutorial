import uvicorn
from fastapi import FastAPI
from fastapi.responses import Response

app = FastAPI()


@app.middleware('http')
async def middleware1(request, call_next):
    print('mid1: before')
    response = await call_next(request)
    print('mid1: after')
    return response

@app.middleware('http')
async def middleware2(request, call_next):
    print('mid2: before')
    response = await call_next(request)
    print('mid2: after')
    return response

@app.get('/middle')
async def get_middle():
    print('logic done')
    return 'mid'

if __name__ == "__main__":
    uvicorn.run("multi_mid:app", host="127.0.0.1", port=8000, reload=True)
