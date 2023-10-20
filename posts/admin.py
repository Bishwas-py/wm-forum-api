from django.contrib import admin
from .models import Post, PolymorphicLike

admin.site.register(Post)
admin.site.register(PolymorphicLike)