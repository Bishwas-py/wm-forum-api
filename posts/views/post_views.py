from django.views.decorators.csrf import csrf_exempt
from djapy.auth.dec import djapy_login_required
from djapy.data.dec import input_required, field_required
from djapy.pagination.dec import djapy_paginator
from djapy.wrappers.dec import node_to_json_response, method_to_view, model_to_json_node, object_to_json_node

from posts.models import Post
from posts.parsers import post_parser


class CreatePostFields:
    title: str
    tags: list[str]


class ViewPublishableQuery:
    view_content: bool = False


@djapy_login_required
@field_required
@model_to_json_node(['id', 'title'])
def create_post(request, data: CreatePostFields, query: ViewPublishableQuery, *args, **kwargs):
    post = Post.objects.create(
        title=data.title,
        author_id=request.user.id
    )
    if query.view_content:
        post.viewer = request.user
        post.visit_count
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


@csrf_exempt
@djapy_login_required
@node_to_json_response
@model_to_json_node(post_parser.fields, object_parser=post_parser.parser)
def get_post_view(request, post_id, *args, **kwargs):
    return Post.objects.get(id=post_id)
