from fastapi import APIRouter

router = APIRouter()

@router.post("/analyze")
def analyze_audio(data: dict):
    # TODO: 04번 구현
    return {
        "audio_anger_score": 0.0,
        "audio_stress_score": 0.0,
        "vibe_status": "calm",
        "transcribed_text": "",
        "profanity_detected": False
    }
