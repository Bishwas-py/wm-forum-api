from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from ninja import Field, Schema
from pydantic import validator

from authentication.schemas.auth_schema import LoginInline
from utils.symbols import attach_message

email_validator = EmailValidator()


class UserRegisterSchema(Schema):
    username: str
    email: str
    password: str

    @validator('username')
    def username_must_be_valid(cls, value: str):
        if not value.isalnum():
            raise ValueError('Username must be alphanumeric.')
        if value.isdigit():
            raise ValueError('Username must not be only digit.')
        return value

    @validator('email')
    def email_must_be_valid(cls, value: str):
        try:
            email_validator(value)
        except ValidationError:
            raise ValueError(email_validator.message)
        return value

    @validator('password')
    def password_must_be_valid(cls, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise ValueError(attach_message(e.messages))


class AuthOutSchema(Schema):
    is_authenticated: bool
    user_id: int = Field(..., alias="id")
    username: str
    redirect: str | None = None
