from ninja import Schema
import posts.models
from authentication.schemas.user_schema import GenericUserSchema


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


class PostSchema(Schema):
    author: GenericUserSchema
    title: str
    slug: str
    body: str
    publishable: PublishableSchema
    tags: list[TagsSchema]

    @staticmethod
    def resolve_tags(obj: 'posts.models.Post'):
        return obj.tags.all()

    @staticmethod
    def resolve_publishable(obj: 'posts.models.Post'):
        return obj.publishable.all().view_count()
