import uvicorn
from fastapi import FastAPI
from fastapi.responses import Response

app = FastAPI()


@app.middleware('http')
async def middleware1(request, call_next):
    print('before')
    print(request.method, request.url)
    if request.url.path == '/middle':
        print('user visit middle')
        # return Response(content="permission denied")
    response = await call_next(request)
    response.headers['X-Token'] = '123456'
    print('after')
    return response


@app.get('/middle')
async def get_middle():
    print('ing')
    return 'result'


if __name__ == "__main__":
    uvicorn.run("mid:app", host="127.0.0.1", port=8000, reload=True)
