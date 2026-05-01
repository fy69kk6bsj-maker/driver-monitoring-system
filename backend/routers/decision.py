from fastapi import APIRouter

router = APIRouter()

@router.post("/decide")
def decide(data: dict):
    # TODO: 01번 + 04번 구현
    return {
        "response_text": "",
        "action_type": "monitoring",
        "action_intensity": "soft",
        "system_action": "",
        "ui_notification": "",
        "safety_block": False
    }
