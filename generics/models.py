from django.db import models
from django.utils import timezone


class SoftDeleteQuerySet(models.QuerySet):
    def soft_delete(self):
        return self.update(soft_deleted_at=timezone.now())

    def hard_delete(self):
        return super().delete()

    def alive(self):
        return self.filter(soft_deleted_at__isnull=True)

    def dead(self):
        return self.exclude(soft_deleted_at__isnull=True)


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
