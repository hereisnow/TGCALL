import os
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from google_auth_oauthlib.flow import Flow
from db_manager import save_token  # Импорт функции из твоего db_manager.py

router = APIRouter()

# Загрузка настроек из переменных окружения Railway
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]

def build_flow():
    """Создает объект авторизации Google."""
    return Flow.from_client_config(
        {"web": {
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uris": [GOOGLE_REDIRECT_URI],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }},
        scopes=SCOPES,
    )

@router.get("/auth/google/start")
async def google_start(user_id: str):
    """Шаг 1: Отправляем пользователя на страницу входа Google."""
    flow = build_flow()
    flow.redirect_uri = GOOGLE_REDIRECT_URI
    
    # Передаем user_id в 'state', чтобы получить его обратно в callback
    auth_url, _ = flow.authorization_url(
        access_type="offline", 
        prompt="consent",
        state=user_id 
    )
    return RedirectResponse(auth_url)

@router.get("/auth/google/callback")
async def google_callback(request: Request):
    """Шаг 2: Получаем ответ от Google, сохраняем токен и ID пользователя."""
    code = request.query_params.get("code")
    user_id = request.query_params.get("state")  # Это тот самый ID из шага 1
    
    if not code or not user_id:
        return {"status": "error", "message": "Missing code or user_id"}

    try:
        flow = build_flow()
        flow.redirect_uri = GOOGLE_REDIRECT_URI
        flow.fetch_token(code=code)
        
        # Сохраняем refresh_token в нашу SQLite базу данных
        save_token(user_id, flow.credentials.refresh_token)
        
        return {
            "status": "success", 
            "message": "Календарь успешно привязан! Теперь бот будет напоминать вам о звонках. Вернитесь в Telegram."
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
