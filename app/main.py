from fastapi import FastAPI, UploadFile, HTTPException, Form
from app.services.audio_service import AudioService
from app.models.schemas import TextInput

# Server : uvicorn app.main:app --reload

# Initialize FastAPI
app = FastAPI(title = "Voice Cloning API")

# Initialize Services
audio_service = AudioService()

@app.get("/")
async def root():
    return {"message": "Voice Cloning API is running"}

@app.post("/clone-voice")
async def clone_voice(
    audio_file: UploadFile,
    target_text: str = Form(...),
    reference_text: str = Form(...)
):
    # Validate audio file
    if not audio_file.content_type.startswith("audio"):
        raise HTTPException(status_code=400, detail="File must be an audio file.")

    try:
        # Save audio file
        audio_file_path = await audio_service.save_audio_file(audio_file)

        # Create TextInput model for validation
        text_input = TextInput(
            target_text=target_text,
            reference_text=reference_text
        )

        return {
            "status": "success",
            "audio_file_path": str(audio_file_path),
            "target_text": text_input.target_text,
            "reference_text": text_input.reference_text
        }
    
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))