import uvicorn
from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],    # 允许的域名
    allow_credentials=True, # 允许携带cookie
    allow_methods=['*'],    # 允许的请求方法
    allow_headers=['*'],    # 允许的请求头
)

# 允许跨源访问
# @app.middleware('http')
# async def add_cors_headers(request, call_next):
#     if request.method == 'OPTIONS':
#         headers = {
#             "Access-Control-Allow-Origin": '*',
#             "Access-Control-Allow-Methods": 'GET, POST, PUT, DELETE, OPTIONS',
#             "Access-Control-Allow-Headers": 'Content-Type, Authorization'
#         }
#         return Response(status_code=200, headers=headers)
#     response = await call_next(request)
#     response.headers['Access-Control-Allow-Origin'] = '*'
#     return response

@app.get('/info')
async def get_info():
    return "content get success!"


if __name__ == "__main__":
    uvicorn.run("cors:app", host="127.0.0.1", port=8000, reload=True)
 