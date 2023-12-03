from django.contrib import admin
from .models import Post, PolymorphicLike, Tags, PolymorphicComments

admin.site.register(Post)
admin.site.register(PolymorphicLike)
admin.site.register(PolymorphicComments)
admin.site.register(Tags)
