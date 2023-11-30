from typing import List

from ninja import Router, Schema
from ninja.pagination import paginate

from generics.schemas import Inline
from posts.models import Tags

router = Router(tags=["Tags"])


class TagsSchema(Schema):
    name: str
    iconify_string: str
    slug: str
    description: str
    discussions_count: int

    @staticmethod
    def resolve_discussions_count(obj: Tags):
        return obj.post_set.count()


class CreateTagsSchema(Schema):
    name: str
    iconify_string: str
    slug: str
    description: str


@router.get("/get-all", response=List[TagsSchema], summary="Get all tags")
@paginate
def get_tags(request):
    tags = Tags.objects.all().alive()
    return tags


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
