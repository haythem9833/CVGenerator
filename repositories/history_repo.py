from db.supabase import supabase

def save_history(data: dict):
    return supabase.table("history").insert(data).execute()

def get_history_by_user(user_id: str):
    result = supabase.table("history").select("*").eq("user_id", user_id).execute()
    return result.data