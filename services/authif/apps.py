from django.apps import AppConfig

class SocialAuthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "authif"

    def ready(self):
        import authif.signals
