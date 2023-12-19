from typing import List

from ninja import Router, Schema, Header
from ninja.pagination import paginate

from generics.schemas import MessageOut
from posts.models import Post, PolymorphicComments, Tags
from posts.schemas import PostSchema, CommentSchema, CreateCommentSchema, PostCreateSchema

router = Router(tags=["Posts"])


@router.get("/get-all", response=List[PostSchema], summary="Get all posts", auth=None)
@paginate
def get_posts(request):
    posts = Post.objects.all().alive()
    return posts


@router.get("/get/{post_slug}", response=PostSchema, summary="Get a post", auth=None)
def get_post(request, post_slug: str, client_ip: Header[str], increase_view: bool = True):
    post = Post.objects.alive().get(slug=post_slug)
    post.increment_view_count(request, client_ip, increase_view)
    return post


@router.post("/create", response={201: PostSchema, 400: MessageOut}, summary="Create a post")
def create_post(request, data: PostCreateSchema):
    tags = Tags.objects.filter(id__in=data.tag_ids)
    if Post.objects.filter(slug=data.slug).exists():
        return 400, {
            'message': 'Post with this slug already exists',
            'message_type': 'warning',
            'alias': 'post_slug_exists'
        }

    if not tags.exists():
        return 400, {
            'message': 'No tags found',
            'message_type': 'warning',
            'alias': 'no_tags_found'
        }

    if Post.objects.filter(title=data.title, author=request.user, tags__in=tags).exists():
        return 400, {
            'message': 'An exact same post is already created by you',
            'message_type': 'warning',
            'alias': 'duplicate_post'
        }

    post = Post.objects.create(
        title=data.title,
        body=data.body,
        author=request.user,
        slug=data.slug,
    )
    post.tags.set(tags)
    return 201, post


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
