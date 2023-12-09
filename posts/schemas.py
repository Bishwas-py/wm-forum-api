from typing import List

import bleach
from django.utils.html import strip_tags, escape
from ninja import Schema
import posts.models
from authentication.schemas.user_schema import GenericUserSchema
from generics.schemas import GenericSchema

BLEACH_ALLOWED_TAGS = ['p', 'b', 'i', 'u', 'em', 'strong', 'a',
                       'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li', 'br',
                       'hr', 'img', 'blockquote', 'pre', 'code', 'table', 'thead',
                       'tr', 'th', 'td', 'tbody', 'strike', 'del', 'sup', 'sub',
                       ]

BLEACH_ALLOWED_ATTRIBUTES = ['href', 'title', 'src', 'alt', 'rel', 'target']


def set_nofollow(attrs, new=False):
    attrs[(None, 'rel')] = 'nofollow'
    return attrs


def set_target(attrs, new=False):
    attrs[(None, 'target')] = '_blank'
    return attrs


class PublishableSchema(Schema):
    view_count__sum: int | None
    viewers_count: int | None


class TagsSchema(GenericSchema):
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
    def resolve_body(obj: 'posts.models.Post'):
        linkified_body = bleach.linkify(obj.body, callbacks=[set_nofollow, set_target])
        return bleach.clean(linkified_body,
                            tags=BLEACH_ALLOWED_TAGS,
                            attributes=BLEACH_ALLOWED_ATTRIBUTES,
                            strip=False)

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
