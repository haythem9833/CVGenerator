from repositories.user_repo import create_user, get_user_by_email
from core.security import hash_password, verify_password, create_token
from fastapi import HTTPException

def register_user(email: str, password: str):
    existing = get_user_by_email(email)
    if existing:
        raise HTTPException(status_code=400, detail="Email déjà utilisé")
    hashed = hash_password(password)
    create_user(email, hashed)
    return {"message": "Compte créé"}

def login_user(email: str, password: str):
    user = get_user_by_email(email)
    if not user or not verify_password(password, user["password"]):
        raise HTTPException(status_code=401, detail="Identifiants incorrects")
    token = create_token(user["id"])
    return {"token": token}