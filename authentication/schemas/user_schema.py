from django.http import HttpRequest
from ninja import Schema, Field


class StatusSchema(Schema):
    is_confirmed: bool


class ProfileSchema(Schema):
    bio: str | None
    location: str | None
    birth_date: str | None
    image: str | None

    @staticmethod
    def resolve_image(obj, context):
        request: HttpRequest = context["request"]
        site = request.scheme + "://" + request.get_host()
        if obj.image:
            return site + obj.image.url
        return None


class GenericUserSchema(Schema):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    is_staff: bool
    is_superuser: bool
    is_active: bool
    status: StatusSchema
    profile: ProfileSchema


class UserSchema(GenericUserSchema):
    user_permissions: list[str] = Field(..., alias="get_user_permissions")
