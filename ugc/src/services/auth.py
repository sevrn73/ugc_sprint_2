import jwt
import httpx
from http import HTTPStatus
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core.config import settings


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Invalid authentication scheme.")

            is_token_valid = await self.verify_jwt(credentials.credentials)
            if not is_token_valid:
                raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid token or expired token.")
            return jwt.decode(credentials.credentials, algorithms="HS256", options={"verify_signature": False})["jti"]
        else:
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Invalid authorization code.")

    async def verify_jwt(self, jwtoken: str) -> bool:
        async with httpx.AsyncClient() as client:
            response = await client.get(settings.VERIFY_JWT_URL, headers={"Authorization": "Bearer " + jwtoken})
        if response.status_code == HTTPStatus.OK:
            return True
        else:
            return False
