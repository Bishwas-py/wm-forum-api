import posts.models
from posts.models import PolymorphicLike
from posts.parsers.parser_utils import get_p


def parse_likes_with_post(post: 'posts.models.Post') -> list:
    likes = PolymorphicLike.objects.get_all_poly(post)
    return [
        parse_comment(like) for like in likes.alive()
    ]


def parse_comment(like: 'PolymorphicLike') -> dict:
    return {
        'id': like.id,
        'user': like.user.username,
        'created_at': like.created_at,
        'p': get_p(like)
    }


parser = {
    'p': get_p,
    'user': lambda obj: obj.user.username,
}

basic_fields = ['p', 'user']
deleted_fields = [*basic_fields, 'soft_deleted_at']
