from posts.parsers import comment_parser, like_parser, tag_parse
import posts.models
parser = {
    'has_comments': comment_parser.has_comments,
    'has_likes': like_parser.has_likes,
    'tags': tag_parse.tags,
    'views_count': lambda post: post.publishable.all().view_count()
}

fields = ['id', 'title', 'body', 'has_comments', 'has_likes', 'tags', 'views_count']
