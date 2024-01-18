from fastapi import FastAPI
from pathlib import Path
from fastapi import Request, Response
from fastapi.responses import FileResponse


app = FastAPI(reload=True)
video_path = Path('4K.mp4')


@app.get('/hello')
async def hello():
    return 'welcome'

@app.get("/video")
async def video_endpoint():
    return FileResponse(video_path)


    