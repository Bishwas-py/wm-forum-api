# Generated by Django 4.2.6 on 2023-10-20 16:16

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0005_remove_post_comments_remove_post_likes'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='polymorphiclike',
            unique_together={('user', 'object_id', 'content_type')},
        ),
    ]
