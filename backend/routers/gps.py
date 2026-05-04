
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class GPSRequest(BaseModel):
    latitude: float
    longitude: float
    driving_duration_min: float
    user_id: str
    session_id: str

class GPSResponse(BaseModel):
    speed_norm: float
    traffic_density_score: float
    driving_duration_norm: float
    night_driving_risk: float
    rest_area_distance_norm: float
    nearest_rest_area: str

@router.post("/analyze", response_model=GPSResponse)
def analyze_gps(data: GPSRequest):
    # TODO: 03번 구현
    return GPSResponse(
        speed_norm=0.0,
        traffic_density_score=0.2,
        driving_duration_norm=0.0,
        night_driving_risk=0.0,
        rest_area_distance_norm=0.0,
        nearest_rest_area=""
    )
