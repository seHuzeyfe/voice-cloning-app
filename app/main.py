from fastapi import FastAPI

app = FastAPI(title = "Voice Cloning API")

@app.get("/")
async def root():
    return {"message": "Voice Cloning API is running"}