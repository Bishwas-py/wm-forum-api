import posts.models


def parse_likes(post: 'posts.models.Post') -> dict:
    data = {
        'count': post.likes.count(),
        'like_ids': [like.id for like in post.likes.all()],
        'liker_usernames': [like.user.username for like in post.likes.all()]
    }

    return data


post_parsers = {
    'likes': lambda post: parse_likes(post)
}
