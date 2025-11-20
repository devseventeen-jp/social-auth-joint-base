from django.contrib import admin
from django.urls import path, include
#from authif.views import get_enabled_providers

urlpatterns = [
    path("admin/", admin.site.urls),
    path("authif/", include("social_django.urls", namespace="social")),    # /auth/login/google/ etc.
    path("", include("authif.urls")),
    path("api/auth/", include("oauth.urls")),                                    
]