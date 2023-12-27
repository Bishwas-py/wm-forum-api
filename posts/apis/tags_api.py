import time
from typing import List

from ninja import Router, Header, Schema
from ninja.pagination import paginate

from generics.schemas import Inline, MessageOut
from posts.models import Tags
from posts.schemas import TagsSchema, CreateTagsSchema, PostSchema

router = Router(tags=["Tags"])


@router.get("/get-all", response=List[TagsSchema], summary="Get all tags", auth=None)
@paginate
def get_tags(request):
    tags = Tags.objects.all().alive()
    return tags


@router.get("/get-all-posts-by-tag/{tag_slug}", response=List[PostSchema], summary="Get all posts of a tag", auth=None)
@paginate
def get_tags(request, tag_slug: str):
    try:
        tag = Tags.objects.alive().get(slug=tag_slug)
        posts = tag.post_set.all().alive()
        print(posts)
        return posts
    except Tags.DoesNotExist:
        return []


@router.post("/create", response={201: TagsSchema, 400: Inline}, summary="Create a new tag")
def create_tag(request, data: CreateTagsSchema):
    if Tags.objects.filter(name=data.name).exists():
        return 400, Inline({"name": "Tag with this name already exists."})
    if Tags.objects.filter(slug=data.slug).exists():
        return 400, Inline({"slug": "Tag with this slug already exists."})

    tag = Tags.objects.create(
        name=data.name,
        iconify_string=data.iconify_string,
        slug=data.slug,
        description=data.description,
        user=request.auth
    )
    return 201, tag


@router.get("/get/{tag_slug}", response={200: TagsSchema, 404: MessageOut},
            summary="Get a tag by slug", auth=None)
def get_tag(request, tag_slug: str, client_ip: Header[str], increase_view: bool = True):
    try:
        tag = Tags.objects.alive().get(slug=tag_slug)
        tag.increment_view_count(request, client_ip, increase_view)
        return 200, tag
    except Tags.DoesNotExist:
        return 404, {
            "message": "Tag with this slug does not exist.",
            "message_type": "error",
            "alias": "tag_not_found"
        }
