from fastapi import Security, status
from fastapi.exceptions import HTTPException
from fastapi.security import APIKeyHeader

from cgn_ec_api.config import settings

api_key_header = APIKeyHeader(name=settings.API_KEY_HEADER)


def require_local_api_key(api_key: str = Security(api_key_header)) -> str:
    for local_key in settings.API_KEYS:
        if api_key == local_key:
            return

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Not authenticated"
    )
