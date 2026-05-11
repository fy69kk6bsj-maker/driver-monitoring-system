from fastapi import APIRouter
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv

TEST_MODE = True  # API 키 발급 후 False로 변경
load_dotenv()

router = APIRouter()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ResponseRequest(BaseModel):
    user_id: str
    session_id: str
    action_type: str
    action_intensity: str
    risk_level: str
    primary_risk_type: str
    nearest_rest_area: str
    user_profile: dict

class ResponseResult(BaseModel):
    response_text: str
    llm_used_flag: bool

@router.post("/generate", response_model=ResponseResult)
def generate_response(data: ResponseRequest):

    # HIGH면 LLM 안 씀 → Decision에서 이미 처리
    if data.risk_level == "high":
        return ResponseResult(
            response_text="",
            llm_used_flag=False
        )

    # 사용자 프로필 꺼내기
    profile = data.user_profile
    music = profile.get("preferred_music_genre", "")
    style = profile.get("conversation_style", "casual")
    hobby = profile.get("hobby", "")
    anger_trigger = profile.get("anger_trigger_context", "")

    # 시스템 프롬프트
    system_prompt = """당신은 운전자의 안전을 돕는 AI 동반자입니다.
운전 중 대화하므로 반드시 짧고 자연스럽게 말해야 합니다.
- 한 문장 또는 두 문장 이내로만 답하세요.
- 딱딱하지 않고 친근하게 말하세요.
- 운전에 집중할 수 있도록 가볍게 말하세요."""

    # 상황별 프롬프트
    if data.action_type == "calming_prompt":
        user_prompt = f"""운전자가 분노 또는 스트레스 상태입니다.
운전자 정보:
- 대화 스타일: {style}
- 분노 유발 상황: {anger_trigger if anger_trigger else '알 수 없음'}
- 취미: {hobby if hobby else '알 수 없음'}

위 정보를 참고해서 운전자를 안정시키는 짧은 한마디를 한국어로 생성해주세요."""

    elif data.action_type == "conversation":
        user_prompt = f"""운전자가 안전한 상태입니다. 가볍게 대화를 시작해주세요.
운전자 정보:
- 대화 스타일: {style}
- 취미: {hobby if hobby else '알 수 없음'}
- 좋아하는 음악: {music if music else '알 수 없음'}

위 정보를 참고해서 자연스러운 대화 시작 문장을 한국어로 생성해주세요."""

    elif data.action_type == "alert":
        user_prompt = f"""운전자에게 피로 또는 졸음 주의를 부드럽게 알려주세요.
가까운 휴게소: {data.nearest_rest_area if data.nearest_rest_area else '없음'}
짧고 친근하게 한국어로 말해주세요."""

    else:
        return ResponseResult(response_text="", llm_used_flag=False)

    # OpenAI API 호출
    try:
        # TEST_MODE일 때 LLM 호출 스킵
    if TEST_MODE:
        return ResponseResult(
            response_text="[테스트 모드] LLM 응답 생략",
            llm_used_flag=False
        )
    
        response = client.chat.completions.create(
            model="gpt-4o",
            max_tokens=100,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        response_text = response.choices[0].message.content.strip()
        return ResponseResult(response_text=response_text, llm_used_flag=True)

    except Exception as e:
        print(f"OpenAI API 오류: {e}")
        return ResponseResult(response_text="", llm_used_flag=False)
