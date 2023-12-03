from typing import List

from ninja import Router, Schema
from ninja.pagination import paginate

from posts.models import Post, PolymorphicComments
from posts.schemas import PostSchema, CommentSchema, CreateCommentSchema

router = Router(tags=["Posts"])


@router.get("/get-all", response=List[PostSchema], summary="Get all posts", auth=None)
@paginate
def get_posts(request):
    posts = Post.objects.all().alive()
    return posts


@router.get("/get/{post_slug}", response=PostSchema, summary="Get a post", auth=None)
def get_post(request, post_slug: str, increase_view: bool = True):
    post = Post.objects.alive().get(slug=post_slug)
    post.increment_view_count(request, increase_view)
    return post


@router.get("/get/comments/{post_id}", response=List[CommentSchema], summary="Get all comments on a post", auth=None)
def get_post_comment(request, post_id: int):
    post = Post.objects.alive().get(id=post_id)
    comments = PolymorphicComments.objects.get_all_poly(post).alive()
    return comments


@router.post("/create/comment/{post_id}", response=CommentSchema, summary="Create a comment on a post")
def create_post_comment(request, post_id: int, data: CreateCommentSchema):
    post = Post.objects.alive().get(id=post_id)
    comment = PolymorphicComments.create_comment(user=request.user, content_object=post, comment_text=data.comment_text)
    return comment
