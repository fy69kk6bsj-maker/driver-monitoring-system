from fastapi import APIRouter

router = APIRouter()

@router.get("/{user_id}/profile")
def get_profile(user_id: str):
    # TODO: 03번 Firebase 연결
    return {"user_id": user_id}

@router.post("/{user_id}/update")
def update_profile(user_id: str, data: dict):
    # TODO: 03번 Firebase 연결
    return {"status": "ok"}

@router.post("/intervention/log")
def log_intervention(data: dict):
    # TODO: 03번 Firebase 연결
    return {"status": "ok"}
