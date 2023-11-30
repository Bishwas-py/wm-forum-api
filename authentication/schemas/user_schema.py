from ninja import Schema, Field


class StatusSchema(Schema):
    is_confirmed: bool


class ProfileSchema(Schema):
    bio: str | None
    location: str | None
    birth_date: str | None
    image: str | None


class UserSchema(Schema):
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
    user_permissions: list[str] = Field(..., alias="get_user_permissions")
