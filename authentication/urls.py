from django.urls import path
from authentication import views

urlpatterns = [
    path('login/', views.login_for_session, name='login-for-session'),
    path('get-user/', views.get_user, name='get-user'),
]
