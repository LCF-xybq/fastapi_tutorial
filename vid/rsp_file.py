import uvicorn
import aiofiles
from fastapi import FastAPI
from fastapi.responses import Response, FileResponse, StreamingResponse


app = FastAPI()


@app.get("/custom_file")
async def get_custom_file():
    info = b"File Content"
    return Response(
        content=info,
        media_type="text/plain",
        headers={'Content-Disposition': 'attachment;filename="file.txt"'}
    )

@app.get("/download_pdf")
async def get_custom_file():
    path = "./data/1.pdf"
    return FileResponse(
        path=path,
        media_type="application/pdf",
        headers={'Content-Disposition': 'attachment;filename="file.pdf"'}
    )

# 分段返回
def generate_chunks(file_path: str, chunk_size: int = 1024 * 1024 * 10):
    with open(file_path, "rb") as f:
        while chunk := f.read(chunk_size):
            yield chunk


@app.get("/download_mp4")
async def get_custom_file():
    path = "./data/1.mp4"
    return StreamingResponse(
        content=generate_chunks(path),
        media_type="video/mp4",
        headers={'Content-Disposition': 'attachment;filename="file.mp4"'}
    )

# 分段返回 - async
async def generate_chunks2(file_path: str, chunk_size: int = 1024 * 1024 * 10):
    async with aiofiles.open(file_path, "rb") as f:
        while chunk := await f.read(chunk_size):
            yield chunk


@app.get("/download_mp4_2")
async def get_custom_file():
    path = "./data/1.mp4"
    return StreamingResponse(
        content=generate_chunks2(path),
        media_type="video/mp4",
        headers={'Content-Disposition': 'attachment;filename="file.mp4"'}
    )



if __name__ == "__main__":
    uvicorn.run("rsp_file:app", host="127.0.0.1", port=8000, reload=True)
