from posts.parsers import comment_parser, like_parser

parser = {
    'comments': comment_parser.parse_comment_with_post,
    'likes': like_parser.parse_likes_with_post
}

fields = ['id', 'title', 'body', 'comments', 'likes']
