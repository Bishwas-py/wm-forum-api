from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models

from generics.models import GenericModel


class PolymorphicLike(GenericModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content_type = models.ForeignKey('contenttypes.ContentType', on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()


class Post(GenericModel):
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=450)
    body = models.TextField()
    likes = models.ManyToManyField(PolymorphicLike, blank=True, related_name='post_likes')

    def __str__(self):
        return self.title
