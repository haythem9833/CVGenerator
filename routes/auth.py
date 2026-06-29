from fastapi import APIRouter
from models.schemas import UserRegister, UserLogin
from services.auth_service import register_user, login_user

router = APIRouter()

@router.post("/register")
def register(data: UserRegister):
    return register_user(data.email, data.password)

@router.post("/login")
def login(data: UserLogin):
    return login_user(data.email, data.password)