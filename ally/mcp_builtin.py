import json
import sys
import os
import subprocess

def run_shell_command(command: str) -> str:
    """Executes a shell command and returns the output."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        output = result.stdout
        if result.stderr:
            output += f"\nSTDERR:\n{result.stderr}"
        return output.strip() if output else "Command executed successfully (no output)."
    except Exception as e:
        return f"Error executing command: {e}"

def read_file(path: str) -> str:
    """Reads the content of a local file."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

def write_file(path: str, content: str) -> str:
    """Creates or updates a local file."""
    try:
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote to {path}"
    except Exception as e:
        return f"Error writing file: {e}"

TOOLS = [
    {
        "name": "run_shell_command",
        "description": "Executes a shell command on the user's local machine and returns the stdout and stderr.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The shell command to execute."
                }
            },
            "required": ["command"]
        }
    },
    {
        "name": "read_file",
        "description": "Reads the content of a file on the local filesystem.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The absolute or relative path to the file."
                }
            },
            "required": ["path"]
        }
    },
    {
        "name": "write_file",
        "description": "Creates a new file or overwrites an existing file with the given content.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The absolute or relative path to the file."
                },
                "content": {
                    "type": "string",
                    "description": "The content to write to the file."
                }
            },
            "required": ["path", "content"]
        }
    }
]

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
        except Exception:
            continue
            
        if "method" not in req:
            continue
            
        method = req["method"]
        req_id = req.get("id")
        
        if method == "initialize":
            resp = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "serverInfo": {
                        "name": "ally-builtin",
                        "version": "0.1.0"
                    }
                }
            }
            print(json.dumps(resp), flush=True)
            
        elif method == "tools/list":
            resp = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "tools": TOOLS
                }
            }
            print(json.dumps(resp), flush=True)
            
        elif method == "tools/call":
            name = req.get("params", {}).get("name")
            args = req.get("params", {}).get("arguments", {})
            
            result_text = ""
            if name == "run_shell_command":
                result_text = run_shell_command(args.get("command", ""))
            elif name == "read_file":
                result_text = read_file(args.get("path", ""))
            elif name == "write_file":
                result_text = write_file(args.get("path", ""), args.get("content", ""))
            else:
                result_text = f"Unknown tool: {name}"
                
            resp = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": result_text
                        }
                    ]
                }
            }
            print(json.dumps(resp), flush=True)

if __name__ == "__main__":
    main()
