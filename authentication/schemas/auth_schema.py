from ninja import Schema


class LoginSchema(Schema):
    username: str
    password: str


class LoginInlineParam(Schema):
    """
    Inline errors are used to return errors in the response body. Usually to be displayed inline with the form.
    """
    username: str | list[str] = None
    password: str | list[str] = None


class LoginInline(Schema):
    inline: LoginInlineParam

