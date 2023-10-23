from django.urls import path
from posts.views import post_views, comment_views, like_views

urlpatterns = [
    path('', post_views.post_view, name='post-view'),
    path('like/<int:post_id>/', like_views.like_view, name='like-view'),
    path('likes/<int:post_id>/', like_views.list_post_likes, name='list-post-likes'),
    path('likes/<int:post_id>/count/', like_views.like_post_count, name='like-post-count'),

    path('comment/<int:post_id>/', comment_views.comment_view, name='comment-view'),
    path('comments/<int:post_id>/', comment_views.list_post_comments, name='list-post-comments'),
    path('comments/<int:post_id>/count/', comment_views.like_post_count, name='like-post-count'),
]
