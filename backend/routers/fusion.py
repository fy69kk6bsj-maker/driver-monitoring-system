
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class GPSFeatures(BaseModel):
    speed_norm: float
    traffic_density_score: float
    driving_duration_norm: float
    night_driving_risk: float
    rest_area_distance_norm: float

class FusionRequest(BaseModel):
    visual_anger_score: float
    visual_drowsiness_score: float
    audio_anger_score: float
    audio_stress_score: float
    gps_features: GPSFeatures
    user_id: str
    session_id: str

class FusionResponse(BaseModel):
    anger_score: float
    drowsiness_score: float
    context_risk: float
    final_risk: float
    risk_level: str
    primary_risk_type: str
    context_type: str
    intervention_urgency: float
    intervention_feasibility: str

@router.post("/calculate", response_model=FusionResponse)
def calculate_fusion(data: FusionRequest):
    # 가중치 초기값
    a1, a2 = 0.6, 0.4
    g1, g2, g3, g4, g5 = 0.30, 0.20, 0.15, 0.25, 0.10
    d1, d2, d3 = 0.40, 0.40, 0.20
    n1, n2, n3 = 0.60, 0.30, 0.10

    # TODO: 01번 Fusion 수식 구현
    anger_score = a1 * data.visual_anger_score + a2 * data.audio_anger_score
    drowsiness_score = data.visual_drowsiness_score
    context_risk = (
        g1 * data.gps_features.speed_norm +
        g2 * data.gps_features.traffic_density_score +
        g3 * data.gps_features.driving_duration_norm +
        g4 * data.gps_features.night_driving_risk +
        g5 * data.gps_features.rest_area_distance_norm
    )
    final_risk = d1 * anger_score + d2 * drowsiness_score + d3 * context_risk
    intervention_urgency = n1 * drowsiness_score + n2 * anger_score + n3 * context_risk

    # risk_level 분류
    if final_risk >= 0.7:
        risk_level = "high"
    elif final_risk >= 0.3:
        risk_level = "medium"
    else:
        risk_level = "low"

    # primary_risk_type
    if anger_score >= 0.7 and drowsiness_score >= 0.7:
        primary_risk_type = "mixed"
    elif drowsiness_score >= 0.7:
        primary_risk_type = "drowsiness"
    elif anger_score >= 0.7:
        primary_risk_type = "anger"
    else:
        primary_risk_type = "low_risk"

    # context_type
    g = data.gps_features
    if drowsiness_score >= 0.7 and g.night_driving_risk >= 0.7 and g.driving_duration_norm >= 0.6:
        context_type = "fatigue_night_longdrive"
    elif anger_score >= 0.7 and g.traffic_density_score >= 0.7:
        context_type = "anger_congested_traffic"
    elif drowsiness_score >= 0.7 and g.rest_area_distance_norm <= 0.3:
        context_type = "fatigue_rest_available"
    else:
        context_type = "normal"

    # intervention_feasibility
    if g.rest_area_distance_norm <= 0.3:
        feasibility = "rest_possible"
    elif g.rest_area_distance_norm <= 0.6:
        feasibility = "rest_possible_soon"
    else:
        feasibility = "rest_limited"

    return FusionResponse(
        anger_score=round(anger_score, 4),
        drowsiness_score=round(drowsiness_score, 4),
        context_risk=round(context_risk, 4),
        final_risk=round(final_risk, 4),
        risk_level=risk_level,
        primary_risk_type=primary_risk_type,
        context_type=context_type,
        intervention_urgency=round(intervention_urgency, 4),
        intervention_feasibility=feasibility
    )
