import json
from typing import Any

from openai import OpenAI

from config import Settings
from tools import TOOL_FUNCTIONS, TOOL_SCHEMAS


SYSTEM_PROMPT = """You are a practical assistant with tools.
Use a tool whenever it gives a more reliable answer than guessing.
After a tool returns, inspect the observation and continue reasoning.
Do not invent tool results.
Keep the final answer concise and useful.
"""


class ToolCallingAgent:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.client = OpenAI(
            api_key=settings.api_key,
            base_url=settings.base_url,
        )

    def _execute_tool(self, name: str, arguments: str) -> str:
        function = TOOL_FUNCTIONS.get(name)
        if function is None:
            return json.dumps({"error": f"Unknown tool: {name}"}, ensure_ascii=False)

        try:
            kwargs: dict[str, Any] = json.loads(arguments or "{}")
            result = function(**kwargs)
            return json.dumps({"ok": True, "result": result}, ensure_ascii=False)
        except Exception as exc:
            return json.dumps(
                {"ok": False, "error": f"{type(exc).__name__}: {exc}"},
                ensure_ascii=False,
            )

    def run(self, user_input: str) -> str:
        messages: list[dict[str, Any]] = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input},
        ]

        for _ in range(self.settings.max_steps):
            response = self.client.chat.completions.create(
                model=self.settings.model,
                messages=messages,
                tools=TOOL_SCHEMAS,
                tool_choice="auto",
                temperature=self.settings.temperature,
            )

            message = response.choices[0].message
            tool_calls = message.tool_calls or []

            assistant_message: dict[str, Any] = {
                "role": "assistant",
                "content": message.content or "",
            }

            if tool_calls:
                assistant_message["tool_calls"] = [
                    {
                        "id": call.id,
                        "type": "function",
                        "function": {
                            "name": call.function.name,
                            "arguments": call.function.arguments,
                        },
                    }
                    for call in tool_calls
                ]

            messages.append(assistant_message)

            if not tool_calls:
                return message.content or ""

            for call in tool_calls:
                observation = self._execute_tool(
                    call.function.name,
                    call.function.arguments,
                )
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": call.id,
                        "content": observation,
                    }
                )

        return "Agent stopped because it reached AGENT_MAX_STEPS."
