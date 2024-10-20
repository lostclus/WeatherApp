from enum import StrEnum

from ninja import Schema
from pydantic import Field


class TokenType(StrEnum):
    ACCESS = "a"
    REFRESH = "f"


class TokenPayload(Schema):
    exp: int
    iat: int
    token_type: TokenType = Field(serialization_alias="t")
    user_id: int = Field(serialization_alias="u")


class TokenCreateSchema(Schema):
    email: str
    password: str


class TokenRefreshSchema(Schema):
    token_refresh: str


class TokenOutSchema(Schema):
    email: str
    user_id: int
    token_access: str
    token_refresh: str
    token_access_life_time: int
