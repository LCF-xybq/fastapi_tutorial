import uvicorn
import aiofiles
from pathlib import Path
from fastapi import FastAPI, File, UploadFile, HTTPException, Form


app = FastAPI()

@app.post("/upload1")
async def upload_file1(file: bytes = File(...)):
    with open("./file.jpg", "wb") as f:
        f.write(file)
    return {"msg: ": "success"}

@app.post("/upload2")
async def upload_file2(file: UploadFile):
    async with aiofiles.open(f"./{file.filename}", "wb") as f:
        # chunk = await file.read(1024 * 1024)
        # while chunk:
        #     await f.write(chunk)
        #     chunk = await file.read(1024 * 1024)
        while chunk := await file.read(1024 * 1024):
            await f.write(chunk)

    return {"msg: ": "success"}

@app.post("/batch_upload")
async def batch_upload(files: list[UploadFile] = File(...)):
    return {"count: ": len(files), "names: ": [f.filename for f in files]}

ALLOWED_EXTENSIONS = {'.jpg', '.png'}

@app.post("/upload_image")
async def upload_image(file: UploadFile):
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, "not support")
    
    return {"msg: ": "success"}

@app.post("/submit_form")
async def submit_form(uname: str=Form(...),
                      file: UploadFile = File(...)):
    return {"uname: ": uname, "filename: ": file.filename}


if __name__ == '__main__':
    uvicorn.run("up_file:app", host="127.0.0.1", port=8000, reload=True)
