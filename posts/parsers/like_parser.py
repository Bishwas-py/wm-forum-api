import posts.models
from posts.models import PolymorphicLike
from posts.parsers.parser_utils import get_poly


def parse_likes_with_post(post: 'posts.models.Post') -> list:
    likes = PolymorphicLike.objects.get_all_poly(post)
    return [
        parse_like(like) for like in likes.alive()
    ]


def parse_like(like: 'PolymorphicLike') -> dict:
    return {
        'id': like.id,
        'user': like.user.username,
        'created_at': like.created_at,
        'poly': get_poly(like)
    }


parser = {
    'poly': get_poly,
    'user': lambda obj: obj.user.username,
}

basic_fields = ['poly', 'user']
deleted_fields = [*basic_fields, 'soft_deleted_at']
