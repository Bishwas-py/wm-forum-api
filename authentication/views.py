from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.models import User
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from djapy.auth.dec import djapy_login_required
from djapy.data.dec import input_required, field_required
from djapy.utils.response_format import create_response
from djapy.wrappers.dec import node_to_json_response, object_to_json_node

from authentication.fields import RegisterField


@csrf_exempt
@node_to_json_response
@object_to_json_node(['session_key', 'is_authenticated', 'expiry_age', 'csrf_token', 'id'], exclude_null_fields=True)
@input_required(['username', 'password'])
def login_for_session(request, data, *args, **kwargs):
    user = authenticate(username=data.username, password=data.password)
    if user:
        login(request, user)
    return {
        'session_key': request.session.session_key,
        'is_authenticated': user.is_authenticated if user else False,
        'expiry_age': request.session.get_expiry_age(),
        'csrf_token': request.COOKIES.get('csrftoken'),
        'id': user.id if user else None,
    }


@csrf_exempt
@djapy_login_required
@node_to_json_response
@object_to_json_node(['username', 'email', 'first_name', 'last_name', 'is_authenticated', 'id'])
def get_user(request, *args, **kwargs):
    return request.user


@csrf_exempt
@node_to_json_response
@object_to_json_node(['session_key', 'is_authenticated', 'expiry_age', 'csrf_token', 'id'], exclude_null_fields=True)
@field_required
def register_with_session(request, data: RegisterField, *args, **kwargs):
    users = get_user_model().objects.filter(Q(username=data.username) | Q(email=data.email))
    if users.exists():
        return create_response(
            'error',
            'user_exists',
            'User with the given information already exits.',
            field_name='username',
            field_type='payload'
        )
    user = get_user_model().objects.create(
        username=data.username,
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email
    )
    if user:
        login(request, user)
    return {
        'session_key': request.session.session_key,
        'is_authenticated': user.is_authenticated if user else False,
        'expiry_age': request.session.get_expiry_age(),
        'csrf_token': request.COOKIES.get('csrftoken'),
        'id': user.id if user else None,
    }
