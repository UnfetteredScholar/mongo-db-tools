import base64

from core.config import settings
from fastapi import HTTPException, status
from jose import ExpiredSignatureError, JWTError, jwt
from schemas.token import ClientIdentifier, TokenData

KEYS = {
    ClientIdentifier.QUEST_AI.value: settings.QUEST_AI_SECRET_KEY,
}

PUBLIC_KEY = base64.b64decode(settings.PUBLIC_KEY_B64)

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def verify_access_token(
    token: str,
    audience: str | None = settings.SERVICE_ID,
) -> TokenData:
    """
    Verifies an access token

    Args:
        token: the jwt token string

    Returns:
        TokenData object containing the data in the token
    """
    try:
        version = jwt.get_unverified_claims(token).get("version", 1)
        client_id = jwt.get_unverified_claims(token).get("client_id")

        if version == 1:
            payload = jwt.decode(token, KEYS[client_id], algorithms=["HS256"])
        else:
            payload = jwt.decode(token, PUBLIC_KEY, algorithms=["RS256"], audience=audience)

        email: str = payload.get("sub")
        id: str = payload.get("id")
        token_type: str = payload.get("type")
        role: str = payload.get("role")

        if email is None or id is None:
            raise credentials_exception

        return TokenData(email=email, id=id, type=token_type, role=role, client_id=client_id, access_token=token)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token expired",
        )
    except JWTError as ex:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
        )
