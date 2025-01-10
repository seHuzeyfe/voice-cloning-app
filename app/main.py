from fastapi import FastAPI, UploadFile, HTTPException
from app.services.audio_service import AudioService

app = FastAPI(title = "Voice Cloning API")

# Initialize Services
audio_service = AudioService()

@app.get("/")
async def root():
    return {"message": "Voice Cloning API is running"}

@app.post("/upload-audio")
async def upload_audio(audio_file: UploadFile):
    if not audio_file.content_type.startswith("audio"):
        raise HTTPException(status_code=400, detail="File must be an audio file")

    try:
        file_path = await audio_service.save_audio_file(audio_file)    
        return {"filename": audio_file.filename, "saved_path": str(file_path)}
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))