import os
import json
from typing import Dict, Any

try:
    from google.cloud import secretmanager
except ImportError:
    secretmanager = None


def load_providers(local_path: str, gcp_project: str | None = None) -> Dict[str, Any]:
    """
    Load OAuth provider configuration from local JSON or Secret Manager.
    The source is determined by whether USE_SECRET_MANAGER is enabled.
    """
    use_secret_manager = os.getenv("USE_SECRET_MANAGER", "0") == "1"

    if use_secret_manager:
        if secretmanager is None:
            raise RuntimeError("google-cloud-secret-manager is not installed.")
        providers = _load_from_secret_manager(project_id=gcp_project)
    else:
        providers = _load_from_local_json(json_path=local_path)

    return _normalize_providers(providers)


def _load_from_secret_manager(project_id: str) -> Dict[str, Any]:
    """
    Load provider credentials from Google Secret Manager.
    Assumes a single secret named 'oauth_providers' containing a JSON string.
    """
    if project_id is None:
        raise ValueError("GCP_PROJECT environment variable is required when using Secret Manager.")

    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/oauth_providers/versions/latest"
    response = client.access_secret_version(request={"name": name})
    payload = response.payload.data.decode("utf-8")

    try:
        data = json.loads(payload)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in Secret Manager payload: {e}")

    return data


def _load_from_local_json(json_path: str) -> Dict[str, Any]:
    """
    Load provider credentials from a local JSON file.
    Default path: ./env/oauth_providers.json
    """
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Local provider config not found: {json_path}")

    with open(json_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format in local file: {e}")

    return data


def _normalize_providers(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize structure of provider credentials.
    This allows Secret Manager and local JSON to have slightly different structures.
    Expected output:
        {
            "google": {
                "id": "...",
                "secret": "...",
                "enabled": True
            },
            "github": { ... }
        }
    """
    normalized = {}

    for provider, config in data.items():
        normalized[provider] = {
            "id": config.get("client_id") or config.get("id"),
            "secret": config.get("client_secret") or config.get("secret"),
            "enabled": bool(config.get("enabled", True))
        }

    return normalized


# Optional: quick test runner
if __name__ == "__main__":
    try:
        result = load_providers()
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {e}")
