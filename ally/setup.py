import os
import sys
from rich.console import Console
from rich.prompt import Prompt

console = Console()

def get_config_path():
    return os.path.expanduser("~/.ally/.env")

def is_configured():
    config_path = get_config_path()
    return os.path.exists(config_path)

def setup():
    console.print("\n[bold blue]Welcome to Ally Setup![/bold blue]")
    console.print("Let's configure your AI provider so Ally can connect to a model.\n")
    
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
        
    config_content = f"""# Ally Configuration
ALLY_API_BASE_URL={base_url}
ALLY_API_KEY={api_key}
ALLY_MODEL={model}
"""
    with open(get_config_path(), 'w', encoding='utf-8') as f:
        f.write(config_content)
        
    console.print(f"\n[bold green]Configuration saved successfully to {get_config_path()}![/bold green]")
    console.print("You are now ready to use Ally. Run [bold cyan]ally[/bold cyan] to start.\n")

if __name__ == "__main__":
    setup()
