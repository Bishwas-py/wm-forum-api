from django.contrib.auth import get_user_model
from ninja import Router

from authentication.extras.tokenizer import Tokenizer
from authentication.models import ForgotUsernameToken
from authentication.schemas.mail_schema import UsernameOutSchema, EmailDetailOut
from generics.schemas import DetailOut
import re

router = Router(tags=["Forgot Username"])


@router.get("/forgot-username", response={200: DetailOut, 429: EmailDetailOut}, auth=None)
def request_username_token(request, email: str):
    # Validate the email
    if re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email) is None:
        return 400, DetailOut(detail="Invalid email.")

    # Get the user or return HttpError
    try:
        user = get_user_model().objects.get(email=email)
    except get_user_model().DoesNotExist:
        return DetailOut(detail="This email is not registered.")

    # Get or create a token
    forgot_username_token = Tokenizer(ForgotUsernameToken, user)
    forgot_username_token.get_or_create_token()

    if forgot_username_token.response:
        return 429, forgot_username_token.response

    # Email the user their token
    user.email_user(
        subject='Forgot Username',
        message=f'Your token to retrieve your username is: {forgot_username_token.token.token_key}',
        from_email='info@blogstorm.ai'
    )

    return DetailOut(detail="Username retrieval email sent successfully.")


@router.post("/retrieve-username", response={200: UsernameOutSchema, 400: DetailOut, 406: DetailOut, 404: DetailOut})
def retrieve_username(request, email: str, token: str):
    try:
        user = get_user_model().objects.get(email=email)
    except get_user_model().DoesNotExist:
        raise

    # Get the token or return HttpError
    try:
        forgot_username_token = ForgotUsernameToken.objects.get(token_key=token, user=user)
    except ForgotUsernameToken.DoesNotExist:
        return 404, DetailOut(detail="Token not found.")

    # Check token validity and expiry
    if forgot_username_token.is_token_expired():
        return 400, DetailOut(detail="Token expired.")
    if not forgot_username_token.is_token_valid(token):
        return 400, DetailOut(detail="Invalid token.")

    # Remove the token and return the username
    forgot_username_token.delete()

    return UsernameOutSchema(username=forgot_username_token.user.username)
