from fastapi import FastAPI
from routes.generate import router

app = FastAPI(title="Générateur de CV Professionnel API")

# Inclusion des routes avec le préfixe /api
app.include_router(router, prefix="/api")

@app.get("/")
def health_check():
    return {"status": "ok", "project": "CV Generator Backend"}