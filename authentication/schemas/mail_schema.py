from ninja import Schema

from generics.schemas import DetailOut


class EmailDetailOut(DetailOut):
    time_left: int = None


class UsernameOutSchema(Schema):
    username: str
