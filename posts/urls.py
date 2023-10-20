from django.urls import path
from posts import views

urlpatterns = [
    path('', views.post_view, name='post-view'),
    path('like/<int:post_id>/', views.like_post, name='like-post'),
    path('unlike/<int:post_id>/', views.unlike_post, name='unlike-post'),
]
