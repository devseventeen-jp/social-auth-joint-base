from django.apps import AppConfig

class SocialAuthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "services.authif"

    def ready(self):
        import services.authif.signals
