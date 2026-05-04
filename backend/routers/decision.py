from fastapi import APIRouter
from pydantic import BaseModel
import time

router = APIRouter()

# 마지막 질문 시간 (메모리에 유지)
last_question_time: dict = {}

class FusionResult(BaseModel):
    anger_score: float
    drowsiness_score: float
    context_risk: float
    final_risk: float
    risk_level: str
    primary_risk_type: str
    context_type: str
    intervention_urgency: float
    intervention_feasibility: str

class DecisionRequest(BaseModel):
    fusion_result: FusionResult
    user_id: str
    session_id: str
    nearest_rest_area: str
    anger_trend: str

class DecisionResponse(BaseModel):
    response_text: str
    action_type: str
    action_intensity: str
    system_action: str
    ui_notification: str
    safety_block: bool

def can_ask_question(user_id: str, final_risk: float, intervention_urgency: float) -> bool:
    # 위험도 높으면 질문 차단
    if final_risk >= 0.7:
        return False
    if intervention_urgency >= 0.7:
        return False
    # 60초 쿨다운
    now = time.time()
    last = last_question_time.get(user_id, 0)
    if now - last < 60:
        return False
    return True

@router.post("/decide", response_model=DecisionResponse)
def decide(data: DecisionRequest):
    f = data.fusion_result
    rest = data.nearest_rest_area
    trend = data.anger_trend

    # 기본값
    response_text = ""
    action_type = "monitoring"
    action_intensity = "soft"
    system_action = "none"
    ui_notification = ""
    safety_block = False

    # ── HIGH 위험 → Rule-based 즉각 대응 ──
    if f.risk_level == "high":
        safety_block = True

        if f.primary_risk_type == "drowsiness":
            action_type = "alert"
            action_intensity = "strong"
            system_action = "alert_sound"
            if rest:
                response_text = f"졸음이 감지되었습니다. {rest}에서 잠시 휴식을 취하세요."
                ui_notification = f"⚠️ 졸음 감지 — {rest} 휴식 권장"
            else:
                response_text = "졸음이 감지되었습니다. 안전한 곳에 차를 세우고 휴식을 취하세요."
                ui_notification = "⚠️ 졸음 감지 — 즉시 휴식 필요"

        elif f.primary_risk_type == "anger":
            action_type = "calming_prompt"
            action_intensity = "strong"
            system_action = "none"
            response_text = "심호흡을 해보세요. 잠시 여유를 가지면 더 안전하게 운전할 수 있어요."
            ui_notification = "⚠️ 분노 감지 — 안정이 필요해요"

        elif f.primary_risk_type == "mixed":
            action_type = "alert"
            action_intensity = "strong"
            system_action = "alert_sound"
            response_text = "졸음과 긴장이 동시에 감지되었습니다. 가까운 휴게소에서 휴식을 취해주세요."
            ui_notification = "⚠️ 위험 감지 — 즉시 휴식 필요"

    # ── MEDIUM 위험 → 부드러운 개입 ──
    elif f.risk_level == "medium":

        if f.primary_risk_type == "drowsiness":
            action_type = "alert"
            action_intensity = "moderate"
            system_action = "none"
            if rest:
                response_text = f"피로가 쌓이고 있어요. {rest}이 가까이 있으니 잠깐 쉬어가는 건 어떨까요?"
            else:
                response_text = "피로가 쌓이고 있어요. 창문을 열거나 스트레칭을 해보세요."
            ui_notification = "졸음 주의"

        elif f.primary_risk_type == "anger":
            action_type = "calming_prompt"
            action_intensity = "moderate"
            system_action = "none"
            if trend == "rising":
                response_text = "많이 힘드시죠? 잠깐 심호흡 한 번 해볼게요."
            else:
                response_text = "교통 상황이 불편하시죠. 조금만 더 여유를 가져볼까요?"
            ui_notification = "분노 주의"

        elif f.primary_risk_type == "mixed":
            action_type = "calming_prompt"
            action_intensity = "moderate"
            system_action = "none"
            response_text = "피로와 긴장이 함께 느껴지네요. 잠깐 쉬어가는 게 좋을 것 같아요."
            ui_notification = "피로 + 긴장 주의"

    # ── LOW 위험 → 모니터링 + 대화 가능 ──
    elif f.risk_level == "low":
        if can_ask_question(data.user_id, f.final_risk, f.intervention_urgency):
            action_type = "conversation"
            action_intensity = "soft"
            # 질문 시간 업데이트
            last_question_time[data.user_id] = time.time()
            # TODO: LLM으로 대화 생성 (현재는 고정 텍스트)
            response_text = ""  # LLM 연결 후 채울 예정
        else:
            action_type = "monitoring"
            action_intensity = "soft"

    return DecisionResponse(
        response_text=response_text,
        action_type=action_type,
        action_intensity=action_intensity,
        system_action=system_action,
        ui_notification=ui_notification,
        safety_block=safety_block
    )
