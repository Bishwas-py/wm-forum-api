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


@djapy_login_required
@field_required
@model_to_json_node(['id', 'title'])
def create_post(request, data: CreatePostFields, *args, **kwargs):
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


class ViewPublishableQuery:
    view_content: bool = False


@csrf_exempt
@djapy_login_required
@node_to_json_response
@model_to_json_node(post_parser.fields, object_parser=post_parser.parser)
@field_required
def get_post_view(request, post_id, query: ViewPublishableQuery, *args, **kwargs):
    post = Post.objects.get(id=post_id)
    if query.view_content:
        post.viewer = request.user
        publishable, created = post.publishable.get_or_create(
            viewer=request.user
        )
        publishable.view_count += 1
        publishable.save()
    return post