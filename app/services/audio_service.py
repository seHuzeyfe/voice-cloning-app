import os
from pathlib import Path
from fastapi import UploadFile

class AudioService:
    def __init__(self):
        self.upload_dir = Path("uploads")
        self.upload_dir.mkdir(exist_ok=True)

    async def save_audio_file(self, audio_file: UploadFile) -> Path:
        """
        Saves an uploaded audio file to disk.
        Returns the path to the saved file.
        """
        try:
            file_path = self.upload_dir / audio_file.filename

            with open(file_path, "wb") as f:
                content = await audio_file.read()
                f.write(content)
            return file_path
        except Exception as e:
            raise RuntimeError(f"Failed to save audio file: {str(e)}")
