# auth_app/auth_utils.py
import jwt
from datetime import datetime, timedelta
from django.conf import settings

ACCESS_TOKEN_LIFETIME_MINUTES = 60
REFRESH_TOKEN_LIFETIME_DAYS = 7

def generate_access_token(payload: dict) -> str:
    """
    payload should contain identifying fields, e.g. {"email": "..."}
    """
    data = payload.copy()
    now = datetime.utcnow()
    data.update({
        "exp": now + timedelta(minutes=ACCESS_TOKEN_LIFETIME_MINUTES),
        "iat": now,
        "type": "access"
    })
    token = jwt.encode(data, settings.SECRET_KEY, algorithm="HS256")
    # pyjwt >=2 returns str; older returned bytes
    if isinstance(token, bytes):
        token = token.decode()
    return token

def generate_refresh_token(payload: dict) -> str:
    data = payload.copy()
    now = datetime.utcnow()
    data.update({
        "exp": now + timedelta(days=REFRESH_TOKEN_LIFETIME_DAYS),
        "iat": now,
        "type": "refresh"
    })
    token = jwt.encode(data, settings.SECRET_KEY, algorithm="HS256")
    if isinstance(token, bytes):
        token = token.decode()
    return token

def verify_access_token(token: str) -> dict | None:
    try:
        data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        # optionally check type
        if data.get("type") != "access":
            return None
        return data
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
