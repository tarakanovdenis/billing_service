from datetime import datetime, timezone, timedelta

import jwt
# from jwt.exceptions import ExpiredSignatureError

from src.core.config import settings
# from src.utils.messages import messages


def decode_jwt(
    jwt_token: str | bytes,
    key: str = settings.jwt_settings.public_key_path.read_text(),
    algorithm: str = settings.jwt_settings.algorithm,
):
    # try:
    decoded = jwt.decode(jwt_token, key=key, algorithms=[algorithm])
    # except ExpiredSignatureError:
    #     return {
    #         'detail': messages.TOKEN_IS_EXPIRED_OR_USER_IS_INACTIVE
    #     }
    return decoded
