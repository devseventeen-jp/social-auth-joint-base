import requests
from .base import BaseOAuthAdapter

GOOGLE_AUTH_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_ENDPOINT = "https://www.googleapis.com/oauth2/v3/userinfo"

class GoogleOAuthAdapter(BaseOAuthAdapter):
    provider = "google"

    def get_authorize_url(self, redirect_uri):
        return (
            GOOGLE_AUTH_ENDPOINT+
            f"?client_id={self.config['client_id']}"
            f"&redirect_uri={redirect_uri}"
            f"&response_type=code&scope=openid%20email%20profile"
        )

    def exchange_token(self, code, redirect_uri):
        data = {
            "client_id": self.config["client_id"],
            "client_secret": self.config["client_secret"],
            "code": code,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        }
        resp = requests.post(GOOGLE_TOKEN_ENDPOINT, data=data)
        resp.raise_for_status()
        return res.json()["access_token"]


    def fetch_userinfo(self, token):
        resp = requests.get(
            GOOGLE_USERINFO_ENDPOINT,
            headers={"Authorization": f"Bearer {token}"}
        )
        resp.raise_for_status()
        data = resp.json()
        # Normalize and return
        return {
            "id": data["sub"],
            "email": data.get("email"),
            "name": data.get("name"),
            "avatar": data.get("picture"),
        }