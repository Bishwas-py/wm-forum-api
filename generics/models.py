from django.contrib.auth import get_user_model
from django.db import models


class PublishableQuery(models.QuerySet):
    def view_count(self):
        return self.aggregate(view_count__sum=models.Sum('view_count'), viewers_count=models.Count('viewer'))


class Publishable(models.Model):
    viewer = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    view_count = models.PositiveIntegerField(default=0)

    objects = PublishableQuery.as_manager()
