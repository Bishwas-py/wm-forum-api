from django.views.decorators.csrf import csrf_exempt
from djapy.auth.dec import djapy_login_required
from djapy.data.dec import input_required
from djapy.pagination.dec import djapy_paginator
from djapy.wrappers.dec import model_to_json_node, node_to_json_response, method_to_view, object_to_json_node

from posts.models import Post, PolymorphicComments
from posts.parsers import comment_parser


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
@djapy_paginator(comment_parser.basic_fields, object_parser=comment_parser.parser)
def list_post_comments(request, post_id, *args, **kwargs):
    """
    Unlike a post and return the likes that are unliked.
    """
    post = Post.objects.get(id=post_id)
    likes = PolymorphicComments.objects.get_all_poly(post).alive()
    return likes


@csrf_exempt
@djapy_login_required
@node_to_json_response
@object_to_json_node(['count'])
def comment_post_count(request, post_id, *args, **kwargs):
    post = Post.objects.get(id=post_id)
    likes = PolymorphicComments.objects.get_all_poly(post).alive()
    return likes
