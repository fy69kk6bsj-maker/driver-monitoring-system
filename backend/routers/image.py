from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ImageRequest(BaseModel):
    image_base64: str
    user_id: str
    session_id: str

class ImageResponse(BaseModel):
    visual_anger_score: float
    visual_drowsiness_score: float
    blink_rate: float
    eye_closed_duration: float
    yawn_score: float
    anger_trend: str
    persistent_risk: bool

@router.post("/analyze", response_model=ImageResponse)
def analyze_image(data: ImageRequest):
    # TODO: 02번 구현
    return ImageResponse(
        visual_anger_score=0.0,
        visual_drowsiness_score=0.0,
        blink_rate=0.0,
        eye_closed_duration=0.0,
        yawn_score=0.0,
        anger_trend="stable",
        persistent_risk=False
    )
