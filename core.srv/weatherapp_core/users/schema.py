from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from ninja import ModelSchema
from pydantic import EmailStr, field_validator

from .models import User


class UserCreateSchema(ModelSchema):
    email: EmailStr
    password: str

    class Config:
        model = User
        model_fields = ["email"]

    @field_validator("password")
    @classmethod
    def _validate_password(cls, value: str) -> str:
        try:
            validate_password(value)
        except ValidationError as error:
            error_str = " ".join(str(e) for e in error)
            raise ValueError(error_str) from error
        return value


class UserUpdateSchema(ModelSchema):
    default_location_id: int | None = None

    class Config:
        model = User
        model_fields = [
            "timezone",
            "temperature_unit",
            "wind_speed_unit",
            "precipitation_unit",
            "date_format",
            "time_format",
        ]
        fields_optional = "__all__"


class UserOutSchema(ModelSchema):
    default_location_id: int | None

    class Config:
        model = User
        model_fields = [
            "id",
            "email",
            "timezone",
            "temperature_unit",
            "wind_speed_unit",
            "precipitation_unit",
            "date_format",
            "time_format",
        ]
