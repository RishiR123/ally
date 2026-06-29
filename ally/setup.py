import os
import sys
import yaml
from rich.console import Console
from rich.prompt import Prompt

console = Console()

def get_config_path():
    return os.path.expanduser("~/.ally/config.yaml")

def is_configured():
    config_path = get_config_path()
    return os.path.exists(config_path)

def setup():
    console.print("\n[bold blue]Welcome to Ally 2.0 Setup![/bold blue]")
    console.print("Let's configure your AI provider and MCP servers.\n")
    
    # Default values suitable for LM Studio
    default_base_url = "http://localhost:1234/v1"
    default_api_key = "lm-studio"
    default_model = "local-model"
    
    base_url = Prompt.ask("API Base URL (e.g., for LM Studio or Ollama)", default=default_base_url)
    api_key = Prompt.ask("API Key (leave as default for most local models)", default=default_api_key)
    model = Prompt.ask("Model Name", default=default_model)
    
    config_dir = os.path.dirname(get_config_path())
    if not os.path.exists(config_dir):
        os.makedirs(config_dir, exist_ok=True)
        
    config_data = {
        "llm": {
            "provider": "local",
            "base_url": base_url,
            "api_key": api_key,
            "model": model
        },
        "mcp_servers": {
            "builtin": {
                "command": "python",
                "args": ["-m", "ally.mcp_builtin"]
            }
        }
    }
    
    with open(get_config_path(), 'w', encoding='utf-8') as f:
        yaml.dump(config_data, f, default_flow_style=False, sort_keys=False)
        
    console.print(f"\n[bold green]Configuration saved successfully to {get_config_path()}![/bold green]")
    console.print("You are now ready to use Ally. Run [bold cyan]ally[/bold cyan] to start.\n")

if __name__ == "__main__":
    setup()
