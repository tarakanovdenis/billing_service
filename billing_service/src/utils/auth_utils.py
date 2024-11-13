from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer
from jwt.exceptions import InvalidTokenError

from src.utils.messages import messages
from src.utils import auth_token_utils


http_bearer = HTTPBearer(auto_error=True)


def get_current_token_payload(
    token: str = Depends(http_bearer)
) -> dict:
    try:
        _, credentials = token
        payload = auth_token_utils.decode_jwt(
            credentials[1]
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=messages.INVALID_TOKEN_ERROR
        )
    return payload


def get_current_auth_user_id_from_or_401(
    payload: dict = Depends(get_current_token_payload),
):
    user_id = payload['user_id']
    return user_id
