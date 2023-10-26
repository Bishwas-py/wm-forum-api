import posts.models
from posts.models import PolymorphicLike
from posts.parsers.parser_utils import get_poly


def tags(post: 'posts.models.Post') -> list:
    return [
        parse_tag(tag) for tag in post.tags.all()
    ]


def parse_tag(tag: 'posts.models.Tags') -> dict:
    return {
        'id': tag.id,
        'user': tag.user.username,
        'name': tag.name
    }


parser = {
    'poly': get_poly,
    'user': lambda obj: obj.user.username,
}

basic_fields = ['poly', 'user']
deleted_fields = [*basic_fields, 'soft_deleted_at']
