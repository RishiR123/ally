import json
import subprocess
import threading
import queue
import time
from typing import Dict, Any, List, Optional

class MCPClient:
    """A lightweight, synchronous MCP client over stdio."""
    
    def __init__(self, command: str, args: List[str]):
        self.command = command
        self.args = args
        self.process = None
        self._msg_id = 0
        self._responses: Dict[int, Any] = {}
        self._events = queue.Queue()
        self._running = False
        
    def start(self):
        self.process = subprocess.Popen(
            [self.command] + self.args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, # We can log stderr or ignore
            text=True,
            bufsize=1 # Line buffered
        )
        self._running = True
        
        # Start a reader thread
        self.read_thread = threading.Thread(target=self._read_loop, daemon=True)
        self.read_thread.start()
        
        # Send initialize request
        init_req = {
            "jsonrpc": "2.0",
            "id": self._get_id(),
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "ally",
                    "version": "0.1.0"
                }
            }
        }
        self._send(init_req)
        resp = self._wait_for_response(init_req["id"])
        
        # Send initialized notification
        self._send({
            "jsonrpc": "2.0",
            "method": "notifications/initialized",
            "params": {}
        })
        
    def stop(self):
        self._running = False
        if self.process:
            self.process.terminate()
            self.process.wait()
            
    def get_tools(self) -> List[Dict[str, Any]]:
        req_id = self._get_id()
        self._send({
            "jsonrpc": "2.0",
            "id": req_id,
            "method": "tools/list",
            "params": {}
        })
        resp = self._wait_for_response(req_id)
        if "result" in resp and "tools" in resp["result"]:
            return resp["result"]["tools"]
        return []
        
    def call_tool(self, name: str, arguments: Dict[str, Any]) -> str:
        req_id = self._get_id()
        self._send({
            "jsonrpc": "2.0",
            "id": req_id,
            "method": "tools/call",
            "params": {
                "name": name,
                "arguments": arguments
            }
        })
        resp = self._wait_for_response(req_id)
        
        if "error" in resp:
            return f"Error: {resp['error'].get('message', str(resp['error']))}"
            
        if "result" in resp and "content" in resp["result"]:
            content = resp["result"]["content"]
            if isinstance(content, list):
                return "\n".join([c.get("text", str(c)) for c in content if c.get("type") == "text"])
            return str(content)
            
        return str(resp.get("result", ""))
        
    def _get_id(self) -> int:
        self._msg_id += 1
        return self._msg_id
        
    def _send(self, msg: Dict[str, Any]):
        if not self.process or not self.process.stdin:
            raise RuntimeError("MCP process not running")
        line = json.dumps(msg) + "\n"
        self.process.stdin.write(line)
        self.process.stdin.flush()
        
    def _read_loop(self):
        while self._running and self.process and self.process.stdout:
            line = self.process.stdout.readline()
            if not line:
                break
            try:
                msg = json.loads(line)
                if "id" in msg:
                    self._responses[msg["id"]] = msg
            except json.JSONDecodeError:
                pass # Ignore non-json output
                
    def _wait_for_response(self, msg_id: int, timeout: float = 30.0) -> Dict[str, Any]:
        start = time.time()
        while time.time() - start < timeout:
            if msg_id in self._responses:
                return self._responses.pop(msg_id)
            time.sleep(0.05)
        raise TimeoutError(f"Timeout waiting for response to message {msg_id}")
