from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import QuerySet
from django.utils import timezone


class SoftDeleteQuerySet(models.QuerySet):
    def soft_delete(self):
        return self.update(soft_deleted_at=timezone.now())

    def hard_delete(self):
        return super().delete()

    def alive(self) -> QuerySet['GenericModel']:
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
