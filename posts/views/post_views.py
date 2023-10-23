from django.views.decorators.csrf import csrf_exempt
from djapy.auth.dec import djapy_login_required
from djapy.data.dec import input_required
from djapy.pagination.dec import djapy_paginator
from djapy.wrappers.dec import node_to_json_response, method_to_view, model_to_json_node

from posts.models import Post
from posts.parsers import post_parser


@djapy_login_required
@input_required(['title'])
@model_to_json_node(['id', 'title'])
def create_post(request, data, *args, **kwargs):
    post = Post.objects.create(
        title=data.title,
        author_id=request.user.id
    )
    return post


@djapy_paginator(post_parser.fields, object_parser=post_parser.parser)
def get_posts(request, *args, **kwargs):
    posts = Post.objects.all()
    return posts


@csrf_exempt
@djapy_login_required
@node_to_json_response
@method_to_view
def post_view(request, *args, **kwargs):
    return {
        'post': create_post,
        'get': get_posts
    }
