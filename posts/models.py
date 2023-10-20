from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from generics.models import GenericModel


class PolymorphicLike(GenericModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content_type = models.ForeignKey('contenttypes.ContentType', on_delete=models.PROTECT)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    @classmethod
    def create_like(cls, user, content_object):
        existing_like = cls.objects.filter(
            user=user,
            object_id=content_object.id,
            content_type=ContentType.objects.get_for_model(content_object)
        )
        if not existing_like:
            like = cls.objects.create(
                user=user,
                content_object=content_object
            )
            return like
        else:
            first_like = existing_like.first()
            existing_like.exclude(id=first_like.id).delete()
            return first_like

    @classmethod
    def get_like(cls, user, content_object):
        existing_like = cls.objects.filter(
            user=user,
            object_id=content_object.id,
            content_type=ContentType.objects.get_for_model(content_object)
        )
        if existing_like:
            return existing_like.first()
        else:
            return None


class PolymorphicComments(GenericModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content_type = models.ForeignKey('contenttypes.ContentType', on_delete=models.PROTECT)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    comment = models.TextField()
    likes = models.ManyToManyField(PolymorphicLike, blank=True, related_name='comment_likes')

    @classmethod
    def create_comment(cls, user, content_object, comment):
        comment = cls.objects.create(
            user=user,
            content_object=content_object,
            comment=comment
        )
        return comment


class Post(GenericModel):
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=450)
    body = models.TextField()
    likes = models.ManyToManyField(PolymorphicLike, blank=True, related_name='post_likes')
    comments = models.ManyToManyField(PolymorphicComments, blank=True, related_name='post_comments')

    def __str__(self):
        return self.title

    def likes_count(self):
        return self.likes.count()
