from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from zep_cloud.client import Zep
from zep_cloud.core.api_error import ApiError


class RetrieveMemoryTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        try:
            api_key = self.runtime.credentials["zep_api_key"]

            client = Zep(api_key=api_key)

            user_sessions = client.user.get_sessions(user_id=tool_parameters["user_id"])
            if len(user_sessions) > 0:
                most_recently_updated_session = max(
                    user_sessions, key=lambda session: session.updated_at
                )
                session_context = client.memory.get(
                    session_id=most_recently_updated_session.session_id
                ).context

                yield self.create_json_message(
                    {"status": "success", "context": session_context}
                )
                yield self.create_text_message(session_context)
            else:
                yield self.create_json_message({"status": "success", "context": None})
        except Exception as e:
            if isinstance(e, ApiError) and e.status_code == 401:
                raise e
            else:
                err = str(e)
                yield self.create_json_message({"status": "error", "error": err})
                yield self.create_text_message(f"failed to retrieve memory: {err}")
