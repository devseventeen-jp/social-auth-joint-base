# auth/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("oauth/post_login/", views.post_login, name="post_login"),
    path("api/auth/register/", views.register_profile, name="api_register_profile"),
]
