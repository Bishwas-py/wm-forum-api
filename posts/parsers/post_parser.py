from posts.parsers import comment_parser, like_parser, tag_parse

parser = {
    'has_comments': comment_parser.has_comments,
    'has_likes': like_parser.has_likes,
    'tags': tag_parse.tags
}

fields = ['id', 'title', 'body', 'has_comments', 'has_likes', 'tags']
