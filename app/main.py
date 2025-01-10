import os
os.environ["TORCH_INDUCTOR_USE_LLVM"] = "0"  # Disable Inductor backend

import torch
import torch._dynamo
torch._dynamo.config.suppress_errors = True

from fastapi import FastAPI, UploadFile, HTTPException, Form
from pathlib import Path
import shutil

from app.services.voice_clone import VoiceCloneService
from app.services.audio_service import AudioService

app = FastAPI(title="Voice Cloning API")

# Initialize services
voice_clone_service = VoiceCloneService(use_cuda=False)
audio_service = AudioService()

@app.post("/clone-voice")
async def clone_voice(
    audio_file: UploadFile,
    target_text: str = Form(...),
    reference_text: str = Form(...)
):
    """
    Clone voice from reference audio and generate new speech with target text
    """
    try:
        # 1. Validate and save input audio
        if not audio_file.content_type.startswith("audio"):
            raise HTTPException(status_code=400, detail="File must be an audio file")
        
        # Save uploaded file
        upload_dir = Path("uploads")
        upload_dir.mkdir(exist_ok=True)

        input_path = upload_dir / audio_file.filename
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(audio_file.file, buffer)

        # Process voice cloning
        try:
            output_path = await voice_clone_service.clone_voice(
                input_audio_path=input_path,
                target_text=target_text,
                reference_text=reference_text,
            )
            return {
                "status": "success",
                "message": "Voice cloning successful",
                "output_path": str(output_path),
            }
        
        finally:
            # Clean up uploaded file
            input_path.unlink(missing_ok=True)

    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
