from fastapi import FastAPI, UploadFile, HTTPException

app = FastAPI(title = "Voice Cloning API")

@app.get("/")
async def root():
    return {"message": "Voice Cloning API is running"}

@app.post("/upload-audio")
async def upload_audio(audio_file: UploadFile):

    if not audio_file.content_type.startswith("audio"):
        raise HTTPException(status_code=400, detail="File must be an audio file")
    
    return {"filename": audio_file.filename}