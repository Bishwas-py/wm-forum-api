from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver

from generics.abstract_models import GenericModel, Polymorphic, Publishablizer
from generics.models import Publishable
from posts.defaults import MAX_TITLE_LENGTH, MAX_SLUG_LENGTH


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


class Tags(GenericModel, Publishablizer):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)  # added by
    name = models.TextField()
    iconify_string = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=100, null=True, blank=True, unique=True)

    def __str__(self):
        return self.name


class Post(GenericModel, Publishablizer):
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=MAX_TITLE_LENGTH)
    body = models.TextField()
    tags = models.ManyToManyField(Tags)
    slug = models.SlugField(max_length=MAX_SLUG_LENGTH, null=True, blank=True, unique=True)

    def __str__(self):
        return self.title


@receiver(post_save, sender=Post)
def create_post_slug(sender, instance: Post, created, **kwargs):
    if created:
        instance.slug = slugify(f'{instance.title}-{instance.id}')
        instance.save()
