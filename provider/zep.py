from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError
from tools.retrieve_memory import RetrieveMemoryTool


class ZepProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            tool = RetrieveMemoryTool.from_credentials(credentials)
            for _ in tool._invoke({"user_id": "test"}):
                pass
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e)) from e
