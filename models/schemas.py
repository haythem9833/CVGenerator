from pydantic import BaseModel

class UserRegister(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class HistoryCreate(BaseModel):
    user_id: str
    platform: str
    niche: str
    topic: str
    result: str