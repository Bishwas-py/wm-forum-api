from ninja import Router
from authentication.extras.tokenizer import Tokenizer
from authentication.models import ConfirmMailToken
from generics.schemas import DetailOut, TitledDetailOut, ActionMessageOut
from authentication.schemas.mail_schema import EmailDetailOut
from utils.constant_handler import FRONTEND_URL

router = Router(tags=["Confirm Email"])


@router.get("/confirm-email", summary="Send a new confirmation email to the user",
            response={200: DetailOut, 208: ActionMessageOut, 429: EmailDetailOut})
def send_confirmation_email(request):
    user = request.auth
    if user.status.is_confirmed:
        return 208, ActionMessageOut(
            message="The user's email is already confirmed.",
            alias="already_confirmed",
            message_type="success",
            redirect="/"
        )
    confirm_email_token = Tokenizer(ConfirmMailToken, user)
    confirm_email_token.get_or_create_token()

    user.status.token = confirm_email_token.token
    user.status.save()

    if confirm_email_token.response:
        return 429, confirm_email_token.response

    user.email_user(
        subject='Confirm your email',
        message=f'Please click on the link below to confirm your email:'
                f' {FRONTEND_URL}/account-confirmation/{confirm_email_token.token.token_key}.',
        from_email='no-reply@blogstorm.ai'
    )
    return DetailOut(detail="Email sent successfully.")


@router.get("/confirm-email/{confirmation_token}", summary="Confirm the user's email",
            response={200: TitledDetailOut, 400: DetailOut})
def confirm_email(request, confirmation_token: str):
    user = request.auth
    if user.status.is_confirmed:
        return 200, TitledDetailOut(
            detail="Email already confirmed.",
            detail_title="Email Confirmed",
            detail_description=f"You [{user.username}] have already been confirmed."
        )
    if not user.status.token:
        return 400, TitledDetailOut(
            detail="User does not have a confirmation token.",
            detail_title="Invalid Token",
            detail_description="The token may have expired or been deleted, "
                               "or the user may have already been confirmed."
        )
    if not user.status.token.is_token_valid(confirmation_token):
        return 400, TitledDetailOut(detail="Invalid confirmation token.", detail_title="Invalid Token")
    if user.status.token.is_token_expired():
        return 400, TitledDetailOut(detail="Confirmation token expired.", detail_title="Expired Token")

    success, message = user.status.set_confirmed()
    if success:
        return 200, TitledDetailOut(detail=message, detail_title="Email Confirmed")
    return 400, TitledDetailOut(detail="Not able to set user status to confirmed.", detail_title="Invalid Token")
