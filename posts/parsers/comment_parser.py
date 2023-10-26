import posts.models
from posts.models import PolymorphicComments
from posts.parsers.parser_utils import get_poly


def has_comments(post: 'posts.models.Post') -> list:
    comments = PolymorphicComments.objects.alive().get_all_poly(post)
    return comments.exists()


def parse_comment(comment: 'PolymorphicComments') -> dict:
    return {
        'id': comment.id,
        'user': comment.user.username,
        'comment_text': comment.comment_text,
        'created_at': comment.created_at,
        'poly': get_poly(comment)
    }


parser = {
    'poly': get_poly
}

basic_fields = ['id', 'comment_text', 'created_at', 'poly']
deleted_fields = [*basic_fields, 'soft_deleted_at']
