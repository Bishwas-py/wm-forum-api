from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.handlers.wsgi import WSGIRequest
from django.db import models
from django.db.models import QuerySet
from django.utils import timezone

from generics.models import Publishable

VIEW_INCREMENT_MINUTES = 3


class SoftDeleteQuerySet(models.QuerySet):
    def soft_delete(self):
        return self.update(soft_deleted_at=timezone.now())

    def hard_delete(self):
        return super().delete()

    def alive(self):
        return self.filter(soft_deleted_at__isnull=True)

    def dead(self):
        return self.exclude(soft_deleted_at__isnull=True)

    def get_all_poly(self, content_object) -> QuerySet['GenericModel']:
        existing_like = self.filter(
            object_id=content_object.id,
            content_type=ContentType.objects.get_for_model(content_object)
        )
        return existing_like

    def get_poly(self, content_object, _id):
        existing_like = self.get(
            object_id=content_object.id,
            content_type=ContentType.objects.get_for_model(content_object),
            id=_id
        )
        return existing_like


class GenericModel(models.Model):
    """
    Generic model for all the models in the project.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    soft_deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteQuerySet.as_manager()

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def soft_delete(self):
        self.soft_deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.soft_deleted_at = None
        self.save()


class Polymorphic(GenericModel):
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    content_type = models.ForeignKey('contenttypes.ContentType', on_delete=models.PROTECT)

    class Meta:
        abstract = True


class Publishablizer(models.Model):
    publishable = models.ManyToManyField(Publishable, blank=True)

    def increment_view_count(self, request: WSGIRequest, client_ip: str, increase_view=True, increase_by=1):

        if increase_view and increase_by > 0:
            publishable_dict = {"viewer_ip": client_ip}

            if request.user and request.user.is_authenticated:
                publishable_dict.update({"viewer": request.user})

            publishable, created = self.publishable.get_or_create(**publishable_dict)

            # ensure that the view count is only increased once per user or ip in a minute
            if created or not publishable.last_viewed_at or publishable.last_viewed_at < timezone.now() - timezone.timedelta(
                    minutes=VIEW_INCREMENT_MINUTES):
                publishable.last_viewed_at = timezone.now()
                publishable.view_count += increase_by
                publishable.save()

    class Meta:
        abstract = True
