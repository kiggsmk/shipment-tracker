from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import decode_token

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    payload = decode_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = payload.get("user_id")

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    return user_id