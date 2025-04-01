from collections.abc import Generator
from typing import Any

import requests

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


class InitSessionTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        try:
            api_key = self.runtime.credentials["zep_api_key"]
            headers = {
                "Authorization": f"Api-Key {api_key}",
                "Content-Type": "application/json",
            }
            data = {
                "session_id": tool_parameters["session_id"],
                "user_id": tool_parameters["user_id"],
            }

            response = requests.post(
                "https://api.getzep.com/api/v2/sessions", headers=headers, json=data
            )

            if response.status_code == 400:
                # 400 status code means the session already exists, which is fine
                pass
            elif not response.ok:
                response.raise_for_status()

            yield self.create_json_message({"status": "success"})
        except Exception as e:
            err = str(e)
            yield self.create_json_message({"status": "error", "error": err})
