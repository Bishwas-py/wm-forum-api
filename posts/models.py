from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db import models

from generics.abstract_models import GenericModel, Polymorphic
from generics.models import Publishable


class PolymorphicLike(Polymorphic):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'object_id', 'content_type')

    @classmethod
    def create_like(cls, user, content_object):
        like, created = cls.objects.get_or_create(
            user_id=user.id,
            object_id=content_object.id,
            content_type=ContentType.objects.get_for_model(content_object)
        )
        if not created and like.soft_deleted_at:
            like.restore()
        return like


class PolymorphicComments(Polymorphic):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    comment_text = models.TextField()
    likes = models.ManyToManyField(PolymorphicLike, blank=True, related_name='comment_likes')

    @classmethod
    def create_comment(cls, user, content_object, comment_text: str):
        comment = cls.objects.create(
            user=user,
            content_object=content_object,
            comment_text=comment_text
        )
        return comment


class Tags(GenericModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)  # added by
    name = models.TextField()
    iconify_string = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    publishable = models.ManyToManyField(Publishable)


class Post(GenericModel):
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=450)
    body = models.TextField()
    tags = models.ManyToManyField(Tags)
    publishable = models.ManyToManyField(Publishable)

    def view_count(self):
        self.publishable.all().annotate()

    def __str__(self):
        return self.title

