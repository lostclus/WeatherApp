from datetime import UTC, datetime, timedelta

import jwt

from .errors import JWTDecodeError, JWTExpiredSignatureError, JWTInvalidType
from .models import TokenInfo, TokenPayload, TokenType, UserInfo


class JWTAuthenticator:
    def __init__(
        self,
        secret_key: str,
        algorithm: str = "HS256",
        access_token_life_time: timedelta = timedelta(minutes=15),
        refresh_token_life_time: timedelta = timedelta(hours=3),
    ) -> None:
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_life_time = access_token_life_time
        self.refresh_token_life_time = refresh_token_life_time

    def encode_token(self, payload: TokenPayload) -> str:
        return jwt.encode(
            payload.model_dump(), self.secret_key, algorithm=self.algorithm
        )

    def decode_token(
        self, token: str, assert_type: TokenType | None = None
    ) -> TokenPayload:
        try:
            decoded = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except jwt.DecodeError as error:
            raise JWTDecodeError("JWT token decode error") from error
        except jwt.ExpiredSignatureError as error:
            raise JWTExpiredSignatureError("JWT signature has expired") from error

        payload = TokenPayload(**decoded)

        if assert_type:
            if payload.token_type != assert_type:
                raise JWTInvalidType("Invalid token type")

        return payload

    def create_token_for_user(
        self, user: UserInfo, now: datetime | None = None
    ) -> TokenInfo:
        now = (now or datetime.now(UTC)).replace(microsecond=0)
        exp_access = now + self.access_token_life_time
        exp_refresh = now + self.refresh_token_life_time

        access_payload = TokenPayload(
            exp=int(exp_access.timestamp()),
            iat=int(now.timestamp()),
            token_type=TokenType.ACCESS,
            **user.model_dump(),
        )
        refresh_payload = TokenPayload(
            exp=int(exp_refresh.timestamp()),
            iat=int(now.timestamp()),
            token_type=TokenType.REFRESH,
            **user.model_dump(),
        )

        token_access = self.encode_token(access_payload)
        token_refresh = self.encode_token(refresh_payload)

        return TokenInfo(
            token_access=token_access,
            token_refresh=token_refresh,
            token_access_expires_at=exp_access,
            token_refresh_expires_at=exp_refresh,
        )
