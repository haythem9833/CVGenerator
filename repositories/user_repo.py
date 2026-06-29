from db.supabase import supabase

def create_user(email: str, hashed_password: str):
    return supabase.table("users").insert({
        "email": email,
        "password": hashed_password
    }).execute()

def get_user_by_email(email: str):
    result = supabase.table("users").select("*").eq("email", email).execute()
    return result.data[0] if result.data else None