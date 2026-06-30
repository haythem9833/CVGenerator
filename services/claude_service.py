import os
from google import genai
from dotenv import load_dotenv
from fastapi import HTTPException
from prompts.templates import get_prompt

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

async def generate_cv_content(fullname: str, job_title: str, experience_years: int, skills: str, background: str) -> str:
    try:
        # On génère le prompt en lui passant les nouvelles variables du CV
        prompt = get_prompt(
            fullname=fullname,
            job_title=job_title,
            experience_years=experience_years,
            skills=skills,
            background=background
        )

        # Appel à l'API Gemini
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        error_msg = str(e)

        if "API_KEY_INVALID" in error_msg or "API key not valid" in error_msg:
            raise HTTPException(status_code=401, detail="Clé API Gemini invalide. Vérifie ton .env")

        if "RESOURCE_EXHAUSTED" in error_msg or "quota" in error_msg.lower():
            raise HTTPException(status_code=429, detail="Quota Gemini dépassé. Réessaie dans quelques secondes")

        if "DEADLINE_EXCEEDED" in error_msg or "timeout" in error_msg.lower():
            raise HTTPException(status_code=504, detail="Gemini API timeout. Réessaie")

        raise HTTPException(status_code=500, detail=f"Erreur inattendue : {error_msg}")