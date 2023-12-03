from typing import Literal
from ninja import Schema
from pydantic.schema import datetime


class MessageOut(Schema):
    """
    Message errors are used to return errors in the response body. Usually to be displayed in a toast.
    """
    message: str = None
    messages: list[str] = None
    message_type: Literal["error", "warning", "success", "info"]
    alias: str = None

    @classmethod
    def from_exception(cls, e):
        return cls(messages=str(e), message_type="error", alias="server_error")

    class Config:
        from_attributes = False


class ActionMessageOut(MessageOut):
    redirect: str = None


class DetailOut(Schema):
    """
    Detail errors are used to return errors in the response body. Usually to be displayed after a action.
    """
    detail: str

    class Config:
        from_attributes = False


class TitledDetailOut(DetailOut):
    """
    Detail errors are used to return errors in the response body. Usually to be displayed after a action.
    """
    detail_title: str
    detail_description: str | None = None

    class Config:
        from_attributes = False


class Inline(Schema):
    """
    Inline errors are used to return errors in the response body. Usually to be displayed inline with the form.
    """
    inline: dict[str, str | list[str]]

    class Config:
        from_attributes = False

    def __init__(self, inline: dict[str, str | list[str]]):
        super().__init__(inline=inline)


class InlineMessageOut(MessageOut, Inline):
    pass


class DetailMessageOut(MessageOut, DetailOut):
    pass


class GenericSchema(Schema):
    id: int
    created_at: datetime
    updated_at: datetime
    soft_deleted_at: datetime | None = None
