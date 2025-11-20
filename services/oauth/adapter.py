import importlib
from core import config_loader

PROVIDER_CONFIG = config_loader.load_provider_configs()

def load_adapter(provider: str):
    """
    load <ProviderName>Adapter in providers/<provider>.py
    """
    module = importlib.import_module(f"oauth.providers.{provider}")
    class_name = f"{provider.capitalize()}Adapter"
    cls = getattr(module, class_name)

    cfg = PROVIDER_CONFIG.get(provider, {})
    return cls(cfg)
