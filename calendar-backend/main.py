from fastapi import FastAPI
from .auth_google import router as google_router

app = FastAPI()

# Подключаем маршруты Google
app.include_router(google_router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}
