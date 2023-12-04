from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from wm_forum_api.api import api

urlpatterns = [
    path('', api.urls),
    path('admin/', admin.site.urls),
    path('posts/', include('posts.urls')),
]

static_urls = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
media_urls = static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static_urls
urlpatterns += media_urls
