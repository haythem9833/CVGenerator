from fastapi import APIRouter
from models.schemas import HistoryCreate
from services.history_service import add_history, fetch_history

router = APIRouter()

@router.post("/history")
def save(data: HistoryCreate):
    return add_history(data.dict())

@router.get("/history/{user_id}")
def get_history(user_id: str):
    return fetch_history(user_id)