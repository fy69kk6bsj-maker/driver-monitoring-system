from fastapi import APIRouter

router = APIRouter()

@router.post("/analyze")
def analyze_image(data: dict):
    # TODO: 02번 구현
    return {
        "visual_anger_score": 0.0,
        "visual_drowsiness_score": 0.0,
        "blink_rate": 0.0,
        "eye_closed_duration": 0.0,
        "yawn_score": 0.0,
        "anger_trend": "stable",
        "persistent_risk": False
    }
