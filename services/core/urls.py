from django.contrib import admin
from django.urls import path, include
from services.authif.views import get_enable_providers

urlpatterns = [
    path("admin/", admin.site.urls),
    path("authif/", include("social_django.urls", namespace="social")),    # /auth/login/google/ etc.
    path("api/authproviders", get_enable_providers),                     # enable providers
    path("", include("services.authif.urls")),                                    # our custom urls (post_login, register API)
]