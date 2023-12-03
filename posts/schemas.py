from typing import List

from django.utils.html import strip_tags, strip_spaces_between_tags
from ninja import Schema
import posts.models
from authentication.schemas.user_schema import GenericUserSchema
from generics.schemas import GenericSchema


class PublishableSchema(Schema):
    view_count__sum: int | None
    viewers_count: int | None


class TagsSchema(Schema):
    name: str
    iconify_string: str
    slug: str
    description: str
    discussions_count: int
    publishable: PublishableSchema

    @staticmethod
    def resolve_discussions_count(obj: 'posts.models.Tags'):
        return obj.post_set.count()

    @staticmethod
    def resolve_publishable(obj: 'posts.models.Tags'):
        return obj.publishable.all().view_count()


class CreateTagsSchema(Schema):
    name: str
    iconify_string: str
    slug: str
    description: str


class PostSchema(GenericSchema):
    id: int
    title: str
    slug: str
    body: str
    publishable: PublishableSchema
    author: GenericUserSchema
    tags: list[TagsSchema]
    body_short_escaped: str

    @staticmethod
    def resolve_tags(obj: 'posts.models.Post'):
        return obj.tags.all()

    @staticmethod
    def resolve_body_short_escaped(obj: 'posts.models.Post'):
        return strip_tags(obj.body)[:200] + '...' if len(obj.body) > 200 else strip_tags(obj.body)

    @staticmethod
    def resolve_publishable(obj: 'posts.models.Post'):
        return obj.publishable.all().view_count()


class LikeSchema(GenericSchema):
    user: GenericUserSchema


class CommentSchema(GenericSchema):
    user: GenericUserSchema
    comment_text: str
    likes: List[LikeSchema]

    @staticmethod
    def resolve_likes(obj: 'posts.models.PolymorphicComments'):
        return obj.likes.all()


class CreateCommentSchema(Schema):
    comment_text: str
