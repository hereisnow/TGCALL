import os
import sys

# Добавляем корневую папку в путь, чтобы видеть db_manager
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from google_auth_oauthlib.flow import Flow
from db_manager import save_token 

router = APIRouter()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]

def build_flow():
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
    flow = build_flow()
    flow.redirect_uri = GOOGLE_REDIRECT_URI
    auth_url, _ = flow.authorization_url(access_type="offline", prompt="consent", state=user_id)
    return RedirectResponse(auth_url)

@router.get("/auth/google/callback")
async def google_callback(request: Request):
    code = request.query_params.get("code")
    user_id = request.query_params.get("state")
    
    if not code or not user_id:
        return {"error": "Нет кода или ID пользователя"}

    try:
        flow = build_flow()
        flow.redirect_uri = GOOGLE_REDIRECT_URI
        flow.fetch_token(code=code)
        
        save_token(user_id, flow.credentials.refresh_token)
        return {"status": "success", "message": "Всё работает! Закройте окно."}
    except Exception as e:
        return {"error": str(e)}
