import posts.models
from posts.models import PolymorphicComments
from posts.parsers.parser_utils import get_p


def parse_comment_with_post(post: 'posts.models.Post') -> list:
    comments = PolymorphicComments.objects.get_all_poly(post)
    return [
        parse_comment(comment) for comment in comments.alive()
    ]


def parse_comment(comment: 'PolymorphicComments') -> dict:
    return {
        'id': comment.id,
        'user': comment.user.username,
        'comment_text': comment.comment_text,
        'created_at': comment.created_at,
        'p': get_p(comment)
    }


parser = {
    'p': get_p
}

basic_fields = ['id', 'comment_text', 'created_at', 'p']
deleted_fields = [*basic_fields, 'soft_deleted_at']
