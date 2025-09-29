import uvicorn
from fastapi import FastAPI, Request


app = FastAPI()

@app.get("/client_info")
async def client_info(request: Request):
    return {
        "URL: ": request.url,
        "method: ": request.method,
        "IP: ": request.client.host,
        "params: ": request.query_params,
        "header: ": request.headers,
        # "json: ": await request.json(),
        "cookies: ": request.cookies,
        # "form: ": await request.form()
    }


if __name__ == "__main__":
    uvicorn.run("req:app", host="127.0.0.1", port=8000, reload=True)
