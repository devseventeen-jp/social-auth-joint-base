#import yaml
#from pathlib import Path
#from django.http import JsonResponse
#from django.conf import settings

#def get_enabled_providers(request):
#    config = yaml.safe_load((Path(settings.BASE_DIR) / "config.yaml").read_text())
#    providers = []
#    for name, data in config.get("auth_providers", {}).items():
#        if data.get("enabled"):
#            providers.append(name)
#    return JsonResponse({"providers": providers})

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# APIs

@login_required
def get_user_profile(request):
    profile = request.user.profile
    return JsonResponse({
        "username": request.user.username,
        "email": request.user.email,
        "display_name": profile.display_name,
        "is_approved": profile.is_approved,
        "company_name": profile.company_name,
        "phone_number": profile.phone_number
    })

import os
from django.shortcuts import redirect
from django.conf import settings
# from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
# from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Post-login redirect handler.
@login_required
def post_login(request):
    """
    After social-auth login, redirect new social users to frontend register page
    with ?provider=...; otherwise redirect to dashboard.
    """
    # Pop session markers set by pipeline
    is_new = request.session.pop("social_is_new", False)
    provider = request.session.pop("social_provider", "")

    # Read frontend targets from env vars (fall back to localhost dev)
    frontend_register = os.getenv("FRONTEND_REGISTER_URL", "http://localhost:5173/register")
    frontend_dashboard = os.getenv("FRONTEND_DASHBOARD_URL", "http://localhost:5173/dashboard")

    if is_new:
        # Append provider param so SPA can prefill provider info
        url = f"{frontend_register}?provider={provider}"
        return redirect(url)
    else:
        return redirect(frontend_dashboard)


# Registration API for initial user data (called from SPA).
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def register_profile(request):
    """
    Accept registration fields from SPA and save to the user's Profile.
    Expects JSON body like { display_name: "...", accept_terms: true, ... }.
    """
    user = request.user

    # Ensure profile exists (if you use post_save signal it should)
    try:
        profile = user.profile
    except Exception:
        # If Profile model not created yet, create a simple one (fallback)
        from .models import Profile
        profile = Profile.objects.create(user=user)

    data = request.data
    # Basic assignments - extend as needed
    display_name = data.get("display_name")
    if display_name is not None:
        profile.display_name = display_name

    # Example: accept_terms stored (if you have such a field)
    if "accept_terms" in data:
        # if profile has accept_terms field add here, otherwise ignore
        try:
            profile.accept_terms = bool(data.get("accept_terms"))
        except Exception:
            pass

    # Mark profile as "registered" if you have such flag (optional)
    # profile.is_registered = True

    profile.save()

    # You can return updated user/profile to SPA
    return Response({
        "ok": True,
        "username": user.username,
        "email": user.email,
        "display_name": getattr(profile, "display_name", "")
    })

# enable providers
def get_enable_providers(request):
    return JsonResponse(settings.OAUTH_PROVIDERS)