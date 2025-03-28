from typing import Any
import requests

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class ZepProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            headers = {"Authorization": f"Api-Key {credentials['zep_api_key']}"}
            session_id = "test"
            response = requests.get(
                f"https://api.getzep.com/api/v2/sessions/{session_id}/memory",
                headers=headers,
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise ToolProviderCredentialValidationError(str(e)) from e
