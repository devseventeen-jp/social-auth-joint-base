from .adapters.google import exchange_code_for_token as google_exchange
from .adapters.google import fetch_userinfo as google_userinfo

PROVIDER_MAP = {
    "google": {
        "exchange": google_exchange,
        "userinfo": google_userinfo,
    },
    # "github": {...}
    # "twitter": {...}
}


def get_oauth_profile(provider, code, redirect_uri, client_id, client_secret):
    if provider not in PROVIDER_MAP:
        raise ValueError("Unknown provider")

    adapter = PROVIDER_MAP[provider]

    # code => token
    token = adapter["exchange"](code, redirect_uri, client_id, client_secret)

    # token => profile
    profile = adapter["userinfo"](token)

    return profile
