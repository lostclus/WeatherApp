from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from weatherapp.jwtauth import JWTAuthenticator, TokenPayload, TokenType

from ..settings import settings

bearer_credentials = HTTPBearer()


def jwt_credentials(
    bearer: Annotated[HTTPAuthorizationCredentials, Depends(bearer_credentials)]
) -> TokenPayload:
    authenticator = JWTAuthenticator(secret_key=settings.secret_key)
    return authenticator.decode_token(bearer.credentials, assert_type=TokenType.ACCESS)
