from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

from zep_cloud.client import Zep


class ZepProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            client = Zep(api_key=credentials["zep_api_key"])
            client.memory.get(session_id="test")
        except Exception as e:
            # TODO: what if the exception is something other than not authorized?
            raise ToolProviderCredentialValidationError(str(e)) from e
