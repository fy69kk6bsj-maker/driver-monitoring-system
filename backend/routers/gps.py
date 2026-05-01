from fastapi import APIRouter

router = APIRouter()

@router.post("/analyze")
def analyze_gps(data: dict):
    # TODO: 03번 구현
    return {
        "speed_norm": 0.0,
        "traffic_density_score": 0.0,
        "driving_duration_norm": 0.0,
        "night_driving_risk": 0.0,
        "rest_area_distance_norm": 0.0,
        "nearest_rest_area": ""
    }
