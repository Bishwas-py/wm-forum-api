from django.urls import path
from posts import views

urlpatterns = [
    path('', views.post_view, name='post-view'),
    path('like/<int:post_id>/', views.like_view, name='like-view'),
    path('comment/<int:post_id>/', views.comment_view, name='comment-view'),
    # path('del-comments/<int:post_id>/', views.delete_comment, name='get-comments'),
]
