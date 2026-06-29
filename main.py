from fastapi import FastAPI
from routes.auth import router as auth_router
from routes.history import router as history_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth")
app.include_router(history_router, prefix="/api")