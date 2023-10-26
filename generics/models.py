from django.contrib.auth import get_user_model
from django.db import models


class Publishable(models.Model):
    viewer = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    view_count = models.PositiveIntegerField(default=0)
