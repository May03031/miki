from google.oauth2 import id_token as google_id_token
from google.auth.transport import requests as google_requests
from fastapi import HTTPException, status
from config import settings

async def verify_google_token(id_token: str) -> dict:
    try:
        payload = google_id_token.verify_oauth2_token(
            id_token,
            google_requests.Request(),
            settings.GOOGLE_CLIENT_ID,
        )

        if not payload.get("email_verified"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Google email not verified"
            )

        return payload  # chứa email, sub, name, picture...

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Google Token"
        )

