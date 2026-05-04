from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class AudioRequest(BaseModel):
    audio_base64: str
    user_id: str
    session_id: str

class AudioResponse(BaseModel):
    audio_anger_score: float
    audio_stress_score: float
    vibe_status: str
    transcribed_text: str
    profanity_detected: bool

@router.post("/analyze", response_model=AudioResponse)
def analyze_audio(data: AudioRequest):
    # TODO: 04번 구현
    return AudioResponse(
        audio_anger_score=0.0,
        audio_stress_score=0.0,
        vibe_status="calm",
        transcribed_text="",
        profanity_detected=False
    )
