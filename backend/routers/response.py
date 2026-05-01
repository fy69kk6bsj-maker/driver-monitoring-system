from fastapi import APIRouter

router = APIRouter()

@router.post("/generate")
def generate_response(data: dict):
    # TODO: 01번 구현 (Claude API 연결)
    return {
        "response_text": "안전 운전하세요.",
        "llm_used_flag": False
    }
