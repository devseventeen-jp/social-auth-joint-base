import os
import json
from pathlib import Path
from typing import Dict, Any

try:
    from google.cloud import secretmanager
except ImportError:
    secretmanager = None


def load_provider_configs() -> Dict[str, Any]:
    """
    Load OAuth provider configuration from local JSON or Secret Manager.
    The source is determined by whether USE_SECRET_MANAGER is enabled.
    """

    base_dir = Path(__file__).resolve().parent.parent
    config_path = base_dir / "oauth_config.json"
    secret_path = base_dir / "env" / "oauth_providers.json"

    # --- Step 1: Read config info (non-secret, URLs etc.) ---
    config_data = {}
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            config_data = json.load(f)

    # --- Step 2: Determine which source to use for credentials ---
    use_secret_manager = os.getenv("USE_SECRET_MANAGER", "0") == "1"
    gcp_project = os.getenv("GCP_PROJECT", "")
    if use_secret_manager:
        if secretmanager is None:
            raise RuntimeError("google-cloud-secret-manager is not installed.")
        providers = _load_from_secret_manager(project_id=gcp_project)
    else:
        providers = _load_from_local_json(json_path=secret_path)

    # --- Step 3: Merge both sets (config + secrets) ---
    provider_configs = {}
    for provider, cfg in providers.items():
        provider_configs[provider] = {
            **config_data.get(provider, {}),
            **cfg
        }

    return provider_configs


def _load_from_secret_manager(project_id: str) -> Dict[str, Any]:
    """
    Load provider credentials from Google Secret Manager.
    Assumes a single secret named 'oauth_providers' containing a JSON string.
    """
    if project_id is None:
        raise ValueError("GCP_PROJECT environment variable is required when using Secret Manager.")

    client = secretmanager.SecretManagerServiceClient()
    providers = {}

    possible_providers = ["google", "facebook", "twitter", "github"]

    for provider in possible_providers:
        secret_name = f"projects/{project_id}/secrets/{provider}_oauth_credentials/versions/latest"
        try:
            response = client.access_secret_version(name=secret_name)
            payload = response.payload.data.decode("utf-8")
            providers[provider] = json.loads(payload)
        except Exception as e:
            print(f"[WARN] Failed to load secret for {provider}: {e}")

    return providers


def _load_from_local_json(json_path: str) -> Dict[str, Any]:
    """
    Load provider credentials from a local JSON file.
    Default path: ./env/oauth_providers.json
    """
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Local provider config not found: {json_path}")

    with open(json_path, "r", encoding="utf-8") as f:
        try:
            raw = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format in local file: {e}")

    # Remove disabled providers
    return {
        name: data
        for name, data in raw.items()
        if data.get("enabled", True)
    }

def load_providers() -> Dict[str, Any]:
    """
    Return only enabled providers, merged with static config data if needed.
    """
    all_providers = load_provider_configs()

    # enabled == true のみを残す
    enabled = {
        name: info
        for name, info in all_providers.items()
        if info.get("enabled", True)
    }

    return enabled

# Optional: quick test runner
if __name__ == "__main__":
    try:
        result = load_provider_configs()
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {e}")
