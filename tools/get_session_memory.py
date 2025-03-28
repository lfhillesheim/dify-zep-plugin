from collections.abc import Generator
from typing import Any
import requests

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


class GetSessionMemoryTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        try:
            api_key = self.runtime.credentials["zep_api_key"]
            session_id = tool_parameters["session_id"]

            headers = {"Authorization": f"Api-Key {api_key}"}

            params = {}
            if "lastn" in tool_parameters:
                params["lastn"] = tool_parameters["lastn"]
            if "min_rating" in tool_parameters:
                params["min_rating"] = tool_parameters["min_rating"]

            response = requests.get(
                f"https://api.getzep.com/api/v2/sessions/{session_id}/memory",
                headers=headers,
                params=params,
            )
            response.raise_for_status()

            memory_data = response.json()

            yield self.create_json_message({"status": "success", "memory": memory_data})
            yield self.create_text_message(memory_data.get("context", ""))
        except Exception as e:
            err = str(e)
            yield self.create_json_message({"status": "error", "error": err})
            yield self.create_text_message(f"failed to retrieve memory: {err}")
