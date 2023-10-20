from django.views.decorators.csrf import csrf_exempt

from djapy.auth.dec import djapy_login_required
from djapy.data.dec import input_required
from djapy.pagination.dec import djapy_paginator
from djapy.wrappers.dec import node_to_json_response, method_to_view, model_to_json_node

from .models import Post, PolymorphicLike, PolymorphicComments
from posts.parsers import like_parser, comment_parser, post_parser


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


@model_to_json_node(like_parser.basic_fields, object_parser=like_parser.parser)
def like_post(request, post_id, *args, **kwargs):
    post = Post.objects.get(id=post_id)
    like = PolymorphicLike.create_like(request.user, post)
    return like


@model_to_json_node(like_parser.deleted_fields, object_parser=like_parser.parser)
def unlike_post(request, post_id, *args, **kwargs):
    """
    Unlike a post and return the likes that are unliked.
    """
    post = Post.objects.get(id=post_id)
    likes = PolymorphicLike.objects.get_all_poly(post).filter(user=request.user)
    likes.soft_delete()
    return likes


@csrf_exempt
@djapy_login_required
@node_to_json_response
@method_to_view
def like_view(request, *args, **kwargs):
    return {
        'post': like_post,
        'delete': unlike_post
    }


@model_to_json_node(comment_parser.basic_fields, object_parser=comment_parser.parser)
@input_required(['comment_text'])
def comment_on_post(request, post_id, data, *args, **kwargs):
    """
    Comment on a post and return the comment that is created.
    """
    post = Post.objects.get(id=post_id)
    comment = PolymorphicComments.create_comment(request.user, post, data.comment_text)
    return comment


@model_to_json_node(comment_parser.deleted_fields, object_parser=comment_parser.parser)
@input_required([], ['comment_id'])
def delete_comment(request, post_id, query, *args, **kwargs):
    """
    Delete a comment on a post and return the comment that is deleted.
    """
    post = Post.objects.get(id=post_id)
    comment = PolymorphicComments.objects.get_poly(post, query.comment_id)
    comment.soft_delete()
    return comment


@csrf_exempt
@djapy_login_required
@node_to_json_response
@method_to_view
def comment_view(request, *args, **kwargs):
    return {
        'post': comment_on_post,
        'delete': delete_comment
    }


@csrf_exempt
@djapy_login_required
@node_to_json_response
@method_to_view
def post_view(request, *args, **kwargs):
    return {
        'post': create_post,
        'get': get_posts
    }
