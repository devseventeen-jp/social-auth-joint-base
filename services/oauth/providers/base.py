import requests
from django.conf import settings

class BaseOAuthAdapter:
    provider = None  # set provides name in the delivered class

    def __init__(self, config: dict):
        """
        config = {
            "client_id": "...",
            "client_secret": "...",
            "auth_url": "...",
            "token_url": "...",
            "userinfo_url": "..."
        }
        """
        self.config = config

    def get_authorize_url(self, redirect_uri):
        """ return authorize url in the derivered class """
        raise NotImplementedError

    def exchange_token(self, code: str, redirect_uri: str):
        """ return access token in the derivered class """
        raise NotImplementedError

    def fetch_userinfo(self, token: str):
        """ get user info in the derivered class """
        raise NotImplementedError
