from ninja import Router

from authentication.schemas.user_schema import UserSchema

router = Router(tags=["User"])


@router.get("/info", response=UserSchema)
def user_view(request):
    user = request.user
    return user
