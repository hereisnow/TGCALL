import os
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from google_auth_oauthlib.flow import Flow
from db_manager import save_token  # Импортируем функцию для работы с БД

router = APIRouter()

# Загружаем настройки из переменных окружения
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
    """Шаг 1: Начинаем авторизацию, передавая user_id в state."""
    flow = build_flow()
    flow.redirect_uri = GOOGLE_REDIRECT_URI
    
    # state=user_id нужен, чтобы Google вернул нам ID пользователя в callback
    auth_url, _ = flow.authorization_url(
        access_type="offline", 
        prompt="consent",
        state=user_id 
    )
    return RedirectResponse(auth_url)

@router.get("/auth/google/callback")
async def google_callback(request: Request):
    """Шаг 2: Обработка ответа от Google и сохранение токена."""
    code = request.query_params.get("code")
    user_id = request.query_params.get("state")  # Получаем ID обратно
    
    if not code or not user_id:
        return {"status": "error", "message": "Missing code or user_id"}

    try:
        flow = build_flow()
        flow.redirect_uri = GOOGLE_REDIRECT_URI
        flow.fetch_token(code=code)
        
        # Сохраняем refresh_token в базу данных под ID пользователя
        save_token(user_id, flow.credentials.refresh_token)
        
        return {
            "status": "success", 
            "message": "Календарь успешно привязан! Теперь вы можете закрыть это окно."
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
