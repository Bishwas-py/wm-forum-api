from typing import List

from ninja import Router, Schema
from ninja.pagination import paginate

from posts.models import Post
from posts.schemas import PostSchema

router = Router(tags=["Posts"])


@router.get("/get-all", response=List[PostSchema], summary="Get all posts", auth=None)
@paginate
def get_posts(request):
    posts = Post.objects.all().alive()
    return posts
