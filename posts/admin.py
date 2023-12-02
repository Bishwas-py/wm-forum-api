from django.contrib import admin
from .models import Post, PolymorphicLike, Tags

admin.site.register(Post)
admin.site.register(PolymorphicLike)
admin.site.register(Tags)
