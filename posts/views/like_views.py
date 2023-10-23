from django.views.decorators.csrf import csrf_exempt

from djapy.auth.dec import djapy_login_required
from djapy.wrappers.dec import node_to_json_response, method_to_view, model_to_json_node, object_to_json_node

from posts.models import Post, PolymorphicLike
from posts.parsers import like_parser


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


@csrf_exempt
@djapy_login_required
@node_to_json_response
@model_to_json_node(like_parser.basic_fields, object_parser=like_parser.parser)
def list_post_likes(request, post_id, *args, **kwargs):
    """
    Unlike a post and return the likes that are unliked.
    """
    post = Post.objects.get(id=post_id)
    likes = PolymorphicLike.objects.get_all_poly(post).alive()
    return likes


@csrf_exempt
@djapy_login_required
@node_to_json_response
@object_to_json_node(['count'])
def like_post_count(request, post_id, *args, **kwargs):
    post = Post.objects.get(id=post_id)
    likes = PolymorphicLike.objects.get_all_poly(post).alive()
    return likes
