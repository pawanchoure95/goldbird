import os
from typing import Optional

from django.conf import settings


def firebase_web_config() -> dict:
    return {
        "apiKey": settings.FIREBASE_API_KEY,
        "authDomain": settings.FIREBASE_AUTH_DOMAIN,
        "projectId": settings.FIREBASE_PROJECT_ID,
        "storageBucket": settings.FIREBASE_STORAGE_BUCKET,
        "messagingSenderId": settings.FIREBASE_MESSAGING_SENDER_ID,
        "appId": settings.FIREBASE_APP_ID,
        "measurementId": settings.FIREBASE_MEASUREMENT_ID,
    }


def firebase_is_configured() -> bool:
    required = [
        settings.FIREBASE_API_KEY,
        settings.FIREBASE_AUTH_DOMAIN,
        settings.FIREBASE_PROJECT_ID,
        settings.FIREBASE_APP_ID,
    ]
    return settings.FIREBASE_CHAT_ENABLED and all(required)


def create_firebase_custom_token(uid: str) -> Optional[str]:
    """
    Returns Firebase custom auth token for a Django user UID.
    Returns None when Firebase admin is not configured.
    """
    if not firebase_is_configured():
        return None

    service_account_path = settings.FIREBASE_SERVICE_ACCOUNT_PATH
    if not service_account_path or not os.path.exists(service_account_path):
        return None

    try:
        import firebase_admin
        from firebase_admin import credentials, auth
    except Exception:
        return None

    try:
        firebase_admin.get_app()
    except Exception:
        cred = credentials.Certificate(service_account_path)
        firebase_admin.initialize_app(cred)

    try:
        token = auth.create_custom_token(uid)
        if isinstance(token, bytes):
            return token.decode("utf-8")
        return token
    except Exception:
        return None
