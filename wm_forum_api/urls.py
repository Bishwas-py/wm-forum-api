from django.contrib import admin
from django.urls import path, include

from wm_forum_api.api import api

urlpatterns = [
    path('', api.urls),
    path('admin/', admin.site.urls),
    path('posts/', include('posts.urls')),
]
