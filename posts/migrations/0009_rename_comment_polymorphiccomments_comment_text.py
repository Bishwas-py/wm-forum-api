# Generated by Django 4.2.6 on 2023-10-20 16:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_alter_polymorphiclike_unique_together'),
    ]

    operations = [
        migrations.RenameField(
            model_name='polymorphiccomments',
            old_name='comment',
            new_name='comment_text',
        ),
    ]
