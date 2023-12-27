from django.http import HttpResponse, HttpRequest
from ninja.security import django_auth
from ninja.errors import ValidationError

from collections import defaultdict

from ninja import NinjaAPI

from authentication.apis import auth_api, users_api
from posts.apis import tags_api, posts_api, comment_api
from utils.ninja_exception import MessageValueError
from utils.symbols import detach_message

api = NinjaAPI(
    title='Blogstorm API',
    description=(
        "This API is a powerful, Ninja-powered API for "
        "creating and managing content, users, and more, "
        "and is the core backend of the Webmatrices platform."
    ),
    auth=[django_auth],
    csrf=True,
    docs_url="/"
)

api.add_router("/auth", auth_api.router)
api.add_router("/user", users_api.router)
api.add_router("/tags", tags_api.router)
api.add_router("/posts", posts_api.router)
api.add_router("/comments", comment_api.router)


@api.exception_handler(ValidationError)
def validation_error(request: HttpRequest, exc: ValidationError) -> HttpResponse:
    dict_out = defaultdict(list)
    for error in exc.errors:
        loc = error['loc']
        if loc and loc[0] == 'body':
            loc = loc[2:]
        elif len(loc) > 1:
            loc = loc[1:]
        if '__root__' in loc:
            loc = ['detail']
        msg = detach_message(error['msg'])
        dict_out['.'.join(map(str, loc))] = msg
    return api.create_response(request, {"inline": dict_out}, status=400)


@api.exception_handler(MessageValueError)
def validation_error(request: HttpRequest, exc: MessageValueError) -> HttpResponse:
    return api.create_response(request, {
        "message": exc.message,
        "messages": exc.messages,
        "message_type": exc.message_type,
        "alias": exc.alias,
        "inline": exc.inline
    }, status=400)
