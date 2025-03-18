from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from zep_cloud.client import Zep
from zep_cloud.errors import BadRequestError
from zep_cloud import Message


class AddMemoryTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        try:
            api_key = self.runtime.credentials["zep_api_key"]

            client = Zep(api_key=api_key)

            try:
                client.user.add(user_id=tool_parameters["user_id"])
            except Exception as e:
                if (
                    isinstance(e, BadRequestError)
                    and "user already exists" in e.body.message
                ):
                    pass
                else:
                    raise e

            try:
                client.memory.add_session(
                    user_id=tool_parameters["user_id"],
                    session_id=tool_parameters["session_id"],
                )
            except Exception as e:
                if (
                    isinstance(e, BadRequestError)
                    and "session already exists" in e.body.message
                ):
                    pass
                else:
                    raise e

            client.memory.add(
                session_id=tool_parameters["session_id"],
                messages=[
                    Message(
                        content=tool_parameters["user_message"],
                        role_type="user",
                    ),
                    Message(
                        content=tool_parameters["assistant_response"],
                        role_type="assistant",
                    ),
                ],
            )

            yield self.create_json_message({"status": "success"})
            yield self.create_text_message("memory added successfully")
        except Exception as e:
            err = str(e)
            yield self.create_json_message({"status": "error", "error": err})
            yield self.create_text_message(f"failed to add memory: {err}")
