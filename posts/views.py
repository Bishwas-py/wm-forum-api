from django.views.decorators.csrf import csrf_exempt

from djapy.auth.dec import djapy_login_required
from djapy.data.dec import input_required
from djapy.pagination.dec import djapy_paginator
from djapy.wrappers.dec import node_to_json_response, method_to_view, model_to_json_node

from .models import Post


@djapy_login_required
@input_required(['title'])
@model_to_json_node(['id', 'title'])
def create_post(request, data, *args, **kwargs):
    post = Post.objects.create(
        title=data.title,
    )
    return post


@djapy_paginator(['id', 'title', 'body', 'likes'], object_parser={
    'likes': lambda post: post.likes.count()
})
def get_posts(request, *args, **kwargs):
    posts = Post.objects.all()
    return posts


@csrf_exempt
@djapy_login_required
@model_to_json_node(['id', 'title', 'body', 'likes'], object_parser={
    'likes': lambda post: post.likes.count()
})
def like_post(request, post_id, *args, **kwargs):
    post = Post.objects.get(id=post_id)
    post.likes.add(request.user)
    return post


@csrf_exempt
@djapy_login_required
@node_to_json_response
@method_to_view
def post_view(request):
    return {
        'post': create_post,
        'get': get_posts
    }
