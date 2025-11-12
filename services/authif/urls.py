# auth/urls.py
from django.urls import path
from . import views
from .views import get_enabled_providers

urlpatterns = [
    path("oauth/post_login/", views.post_login, name="post_login"),
    path("api/auth/register/", views.register_profile, name="api_register_profile"),
    path("api/auth/providers/", get_enabled_providers, name="get_enabled_providers"),   # enable providers
]
