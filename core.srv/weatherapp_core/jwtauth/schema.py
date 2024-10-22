from datetime import datetime

from ninja import Schema


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
    token_access_expires_at: datetime
