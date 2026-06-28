import json
from openai import OpenAI
from typing import List, Dict, Any, Callable

from .config import Config
from .tools import TOOLS_SCHEMA, TOOL_FUNCTIONS

class AllyAgent:
    def __init__(self):
        self.client = OpenAI(**Config.get_openai_client_kwargs())
        self.model = Config.MODEL
        
        # System prompt defines the persona and rules
        self.system_prompt = """You are Ally, a helpful and powerful CLI coding agent created by Orionac.
You have access to tools to interact with the local filesystem and terminal.
Use your tools to accomplish the user's tasks. Always explain what you are doing.
When executing commands, wait for the output before proceeding.
"""
        
        self.history: List[Dict[str, Any]] = [
            {"role": "system", "content": self.system_prompt}
        ]

    def add_user_message(self, message: str):
        self.history.append({"role": "user", "content": message})

    def process_turn(self, status_callback: Callable[[str], None] = None) -> str:
        """
        Sends the current history to the model, executes any requested tools,
        and loops until a final text response is returned.
        
        status_callback is an optional function to update the CLI UI during tool execution.
        """
        while True:
            if status_callback:
                status_callback("Thinking...")
                
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.history,
                tools=TOOLS_SCHEMA,
                tool_choice="auto"
            )

            message = response.choices[0].message
            
            # If the model wants to call tools
            if message.tool_calls:
                # Add the model's tool call message to history
                # We need to convert it to a dictionary format expected by the API for history
                message_dict = message.model_dump(exclude_none=True)
                self.history.append(message_dict)

                for tool_call in message.tool_calls:
                    function_name = tool_call.function.name
                    if status_callback:
                        status_callback(f"Executing tool: {function_name}...")
                        
                    try:
                        arguments = json.loads(tool_call.function.arguments)
                        
                        if function_name in TOOL_FUNCTIONS:
                            func = TOOL_FUNCTIONS[function_name]
                            result = func(**arguments)
                        else:
                            result = f"Error: Unknown tool {function_name}"
                            
                    except Exception as e:
                        result = f"Error parsing arguments or executing tool: {e}"

                    # Append tool result to history
                    self.history.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": function_name,
                        "content": str(result)
                    })
                # Loop back to let the model see the tool outputs
            else:
                # Final text response
                content = message.content or ""
                self.history.append({"role": "assistant", "content": content})
                return content
