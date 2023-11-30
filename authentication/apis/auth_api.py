from django.contrib.auth import get_user_model, login
from django.db import IntegrityError
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from ninja import Router
from authentication.extras import openapi_extra
from authentication.extras.tokenizer import Tokenizer
from authentication.schemas.auth_schema import LoginInline, LoginSchema
from authentication.models import ConfirmMailToken
from authentication.schemas import UserRegisterSchema, AuthOutSchema
from generics.schemas import ActionMessageOut, MessageOut
from utils.constant_handler import FRONTEND_URL

router = Router(tags=["Authentication"])


@router.post("register", response={201: AuthOutSchema, 400: LoginInline}, auth=None,
             summary="Register and login user", openapi_extra=openapi_extra.auth_in_extra)
@csrf_exempt
def register(request, user_payload: UserRegisterSchema):
    """
    If user is registered successfully, user will be logged in, and email will be sent to user's email
    with confirmation link. Also, login token will be returned in response headers.
    ```
    Set-Cookie: sessionid=<session_string>; expires=<time>; HttpOnly; Max-Age=<time>; Path=/; SameSite=Lax
    ```
    """
    try:
        user = get_user_model().objects.create_user(
            username=user_payload.username,
            password=user_payload.password,
            email=user_payload.email,
        )

        confirm_email_token = Tokenizer(ConfirmMailToken, user)
        confirm_email_token.get_or_create_token()

        user.status.set_token_and_save(confirm_email_token.token)

        user.email_user(
            subject='Confirm your email',
            message=f'Please click on the link below to confirm your email:'
                    f' {FRONTEND_URL}/account-confirmation/{confirm_email_token.token.token_key}.',
            from_email='no-reply@blogstorm.ai'
        )
    except IntegrityError:
        return 400, LoginInline(inline={"username": "User with this username already exists."})

    login(request, user)
    auth_out = AuthOutSchema.from_orm(request.user)
    auth_out.redirect = "/"

    return 201, auth_out


@router.post("/login", response={200: MessageOut, 400: LoginInline}, auth=None,
             summary="Login user", openapi_extra=openapi_extra.auth_in_extra)
@csrf_exempt
def login_user(request, data: LoginSchema):
    """
    If user is logged in successfully, login token will be returned in response headers.
    ```
    Set-Cookie: sessionid=<session_string>; expires=<time>; HttpOnly; Max-Age=<time>; Path=/; SameSite=Lax
    ```
    """
    user = get_user_model().objects.filter(username=data.username).first()

    if not user:
        return 400, LoginInline(
            inline={
                "username": "User with this username does not exist."
            }
        )

    if not user.check_password(data.password):
        return 400, LoginInline(
            inline={
                "password": "Password is incorrect."
            }
        )

    login(request, user)
    return 200, MessageOut(
        message="User logged in successfully.",
        message_type="success",
        alias="login_success"
    )


@router.get("logout", response={200: AuthOutSchema}, summary="Logout user")
def logout_user(request):
    """
    Logout user
    """
    request.user.auth_token.delete()
    return 200, request


@router.get("assign-csrf", summary="Assign CSRF token", openapi_extra=openapi_extra.csrf_token_extra)
@ensure_csrf_cookie
def assign_csrf_token(request):
    """
    Assign CSRF token;
    ```
    Set-Cookie: csrftoken=<csrf_token>; expires=<time>; HttpOnly; Max-Age=<time>; Path=/; SameSite=Lax
    ```
    """
    return HttpResponse()
