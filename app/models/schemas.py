from pydantic import BaseModel, Field

class TextInput(BaseModel):
    target_text: str = Field(..., description="The text to be converted to speech")
    reference_text: str = Field(..., description="The text corresponding to the reference audio")

    class Config:
       schema_extra = {
            "example": {
                "target_text": "This is a test",
                "reference_text": "This is a reference voice sample"
       }
       }