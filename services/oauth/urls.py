# oauth/urls.py
from django.urls import path
from . import views
from .views import oauth_callback

urlpatterns = [
    path("providers/", views.get_enabled_providers, name="get_enabled_providers"),   # enable providers
    path("callback/<str:provider_name>/", views.oauth_callback, name="oauth_callback"),
]
