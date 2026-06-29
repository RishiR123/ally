import json
from openai import OpenAI
from typing import List, Dict, Any, Callable

from .config import Config
from .mcp_client import MCPClient

class AllyAgent:
    def __init__(self):
        self.client = OpenAI(**Config.get_openai_client_kwargs())
        self.model = Config.get_model()
        
        # System prompt defines the persona and rules
        self.system_prompt = """You are Ally 2.0, a helpful and powerful CLI coding agent created by Orionac.
You have access to tools via the Model Context Protocol (MCP).
Use your tools to accomplish the user's tasks. Always explain what you are doing.
When executing commands, wait for the output before proceeding.
"""
        self.history: List[Dict[str, Any]] = [
            {"role": "system", "content": self.system_prompt}
        ]
        self.mcp_clients: Dict[str, MCPClient] = {}
        self.tools_schema = []
        self._initialize_mcp()

    def _initialize_mcp(self):
        mcp_servers = Config.get_mcp_servers()
        for server_name, server_config in mcp_servers.items():
            client = MCPClient(command=server_config["command"], args=server_config["args"])
            client.start()
            self.mcp_clients[server_name] = client
            
            # Fetch tools and convert to OpenAI schema format
            mcp_tools = client.get_tools()
            for t in mcp_tools:
                self.tools_schema.append({
                    "type": "function",
                    "function": {
                        "name": f"{server_name}__{t['name']}",
                        "description": t.get("description", ""),
                        "parameters": t.get("inputSchema", {})
                    }
                })

    def add_user_message(self, message: str):
        self.history.append({"role": "user", "content": message})
        self._truncate_context()

    def _truncate_context(self):
        """A simple context truncation strategy for local models: keep system prompt and last 20 messages."""
        if len(self.history) > 21:
            # keep system prompt, and last 20
            self.history = [self.history[0]] + self.history[-20:]

    def process_turn(self, status_callback: Callable[[str], None] = None) -> str:
        """
        Sends the current history to the model, executes any requested tools,
        and loops until a final text response is returned.
        """
        while True:
            if status_callback:
                status_callback("Thinking...")
                
            kwargs = {
                "model": self.model,
                "messages": self.history,
            }
            if self.tools_schema:
                kwargs["tools"] = self.tools_schema
                kwargs["tool_choice"] = "auto"
                
            response = self.client.chat.completions.create(**kwargs)
            message = response.choices[0].message
            
            if message.tool_calls:
                message_dict = message.model_dump(exclude_none=True)
                self.history.append(message_dict)

                for tool_call in message.tool_calls:
                    function_name = tool_call.function.name
                    if status_callback:
                        status_callback(f"Executing tool: {function_name}...")
                        
                    try:
                        arguments = json.loads(tool_call.function.arguments)
                        # The function name is serverName__toolName
                        if "__" in function_name:
                            server_name, actual_tool_name = function_name.split("__", 1)
                            if server_name in self.mcp_clients:
                                client = self.mcp_clients[server_name]
                                result = client.call_tool(actual_tool_name, arguments)
                            else:
                                result = f"Error: MCP Server '{server_name}' not found."
                        else:
                            result = f"Error: Malformed tool name '{function_name}'"
                    except Exception as e:
                        result = f"Error parsing arguments or executing tool: {e}"

                    self.history.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": function_name,
                        "content": str(result)
                    })
                # Loop back to let the model see the tool outputs
                self._truncate_context()
            else:
                content = message.content or ""
                self.history.append({"role": "assistant", "content": content})
                return content
                
    def cleanup(self):
        for client in self.mcp_clients.values():
            client.stop()
