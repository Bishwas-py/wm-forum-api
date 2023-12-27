from typing import List, Optional, Literal

import bleach
from django.utils.html import strip_tags
from ninja import Schema, Field
from pydantic import field_validator

import posts.models
from authentication.schemas.user_schema import GenericUserSchema
from generics.schemas import GenericSchema
from posts.defaults import MIN_TITLE_LENGTH, MAX_TITLE_LENGTH, MIN_BODY_LENGTH, MIN_TAG_COUNT, MAX_TAG_COUNT
from utils.ninja_exception import MessageValueError

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


class PostCreateSchema(Schema):
    body: str
    title: str
    tag_ids: List[int] = []
    slug: Optional[str] = None

    @field_validator('title')
    def validate_title(cls, title):
        if len(title) < MIN_TITLE_LENGTH:
            raise MessageValueError(
                message=f'Your discussion title is too short. Please write at least {MIN_TITLE_LENGTH} characters.',
                alias='title_too_short',
                message_type='warning'
            )
        if len(title) > MAX_TITLE_LENGTH:
            raise MessageValueError(
                message=f'Your discussion title is too long. Please write at most {MAX_TITLE_LENGTH} characters.',
                alias='title_too_long',
                message_type='warning'
            )
        return title

    @field_validator('body')
    def validate_body(cls, body):
        plain_text = strip_tags(body)
        if len(plain_text) < MIN_BODY_LENGTH:
            raise MessageValueError(
                message=f'Your discussion is too short. Please write at least {MIN_BODY_LENGTH} characters.',
                alias='body_too_short',
                message_type='warning'
            )
        return body

    @field_validator('tag_ids')
    def validate_tag_ids(cls, tag_ids):
        if len(tag_ids) < MIN_TAG_COUNT:
            raise MessageValueError(
                message='You have to select at least one tag to post a discussion.',
                alias='tag_not_selected',
                message_type='warning'
            )
        if len(tag_ids) > MAX_TAG_COUNT:
            raise MessageValueError(
                message='You can select at most 3 tags to post a discussion.',
                alias='too_many_tags_selected',
                message_type='warning'
            )
        return tag_ids


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
