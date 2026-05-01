from fastapi import APIRouter

router = APIRouter()

@router.post("/calculate")
def calculate_fusion(data: dict):
    # TODO: 01번 구현
    return {
        "anger_score": 0.0,
        "drowsiness_score": 0.0,
        "context_risk": 0.0,
        "final_risk": 0.0,
        "risk_level": "low",
        "primary_risk_type": "low_risk",
        "context_type": "normal",
        "intervention_urgency": 0.0,
        "intervention_feasibility": "rest_limited",
        "driving_context_features": {}
    }
