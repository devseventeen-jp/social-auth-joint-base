#from django.conf import settings
#from django.http import JsonResponse, HttpResponseBadRequest
#from oauth.adapter import load_adapter
#from django.contrib.auth import login,get_user_model

from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest, HttpResponse
#from .adapter import get_provider_adapter
from authif.models import Profile

User = get_user_model()

def get_enabled_providers(request):
    """
    Return a list of enabled OAuth providers and their URLs for the frontend.
    """
    providers = []

    for name, data in settings.OAUTH_PROVIDERS.items():
        providers.append({
            "name": name,
            "auth_url": data.get("auth_url"),
            "callback_url": data.get("callback_url"),
        })

    return JsonResponse({"providers": providers})

FRONTEND_ORIGIN = "http://localhost:5173"

@csrf_exempt
def oauth_callback(request: HttpRequest, provider_name: str) -> HttpResponse:
    """
    Handles the OAuth callback from a given provider.
    Creates or retrieves User and associated Profile.
    """
    if "code" not in request.GET:
        return HttpResponseBadRequest("Missing code")

    # 1. get provider adapter
    adapter = load_adapter(provider)

    # 2. get access token
    token_data = adapter.get_access_token(request)
    user_info = adapter.get_user_info(token_data)

    # 3. create or get User
    user, created = User.objects.get_or_create(
        username=user_info["username"],  # unique key
        defaults={
            "email": user_info.get("email", ""),
            "first_name": user_info.get("first_name", ""),
            "last_name": user_info.get("last_name", ""),
        }
    )

    # 4. create or update Profile
    profile, profile_created = Profile.objects.get_or_create(user=user)
    profile.avatar_url = user_info.get("avatar_url", "")
    profile.locale = user_info.get("locale", "")
    profile.save()

    # 5. login session
    login(request, user)

    # 6. redirect 
    return redirect(adapter.get_redirect_url())
