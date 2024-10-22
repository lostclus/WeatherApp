from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class TokenType(StrEnum):
    ACCESS = "a"
    REFRESH = "f"


class TokenPayload(BaseModel):
    exp: int
    iat: int
    token_type: TokenType = Field(serialization_alias="t")
    user_id: int = Field(serialization_alias="u")


class UserInfo(BaseModel):
    user_id: int


class TokenInfo(BaseModel):
    token_access: str
    token_refresh: str
    token_access_expires_at: datetime
    token_refresh_expires_at: datetime
