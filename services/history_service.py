from repositories.history_repo import save_history, get_history_by_user

def add_history(data: dict):
    save_history(data)
    return {"message": "Sauvegardé"}

def fetch_history(user_id: str):
    return get_history_by_user(user_id)