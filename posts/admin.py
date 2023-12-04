from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Post, PolymorphicLike, Tags, PolymorphicComments, Publishable

admin.site.register(Post)
admin.site.register(PolymorphicLike)
admin.site.register(PolymorphicComments)
admin.site.register(Tags)


class PublishableAdmin(ModelAdmin):
    list_display = ('viewer', 'viewer_ip', 'last_viewed_at', 'view_count')


admin.site.register(Publishable, PublishableAdmin)
