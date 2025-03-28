from collections.abc import Generator
from typing import Any

import requests

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


class AddSessionMemoryTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        try:
            api_key = self.runtime.credentials["zep_api_key"]
            session_id = tool_parameters["session_id"]

            response = requests.post(
                f"https://api.getzep.com/api/v2/sessions/{session_id}/memory",
                headers={
                    "Authorization": f"Api-Key {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "messages": [
                        {
                            "content": tool_parameters["message"],
                            "role_type": tool_parameters["role_type"],
                        }
                    ]
                },
            )

            response.raise_for_status()
            yield self.create_json_message({"status": "success"})
        except Exception as e:
            err = str(e)
            yield self.create_json_message({"status": "error", "error": err})
