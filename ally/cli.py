import sys
import argparse
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt

from .agent import AllyAgent
from .setup import setup, is_configured

console = Console()

def print_welcome():
    welcome_text = """
# Welcome to Ally 🤖
*Your basic CLI coding agent, by Orionac.*

Type your request below. Type `exit` or `quit` to stop.
    """
    console.print(Panel(Markdown(welcome_text), style="bold blue", expand=False))

def main():
    parser = argparse.ArgumentParser(description="Ally CLI Coding Agent")
    parser.add_argument("--setup", action="store_true", help="Run the interactive setup")
    args = parser.parse_args()

    if args.setup:
        setup()
        return

    if not is_configured():
        console.print("[yellow]It looks like Ally is not configured yet. Running setup...[/yellow]\n")
        setup()
        # Reload config after setup
        from .config import Config
        Config.load()
        
    from .config import Config
    Config.load()
        
    print_welcome()
    
    # We initialize the agent here AFTER setup and dotenv reload so it gets the right config
    agent = AllyAgent()
    
    while True:
        try:
            # Get user input
            user_input = Prompt.ask("\n[bold green]You[/bold green]")
            
            if user_input.strip().lower() in ['exit', 'quit']:
                console.print("[bold yellow]Goodbye![/bold yellow]")
                break
            
            if not user_input.strip():
                continue
                
            agent.add_user_message(user_input)
            
            # Show a spinner while the agent processes the turn
            with console.status("[bold cyan]Ally is thinking...[/bold cyan]", spinner="dots") as status:
                
                # Callback to update the spinner text when a tool is called
                def update_status(text: str):
                    status.update(f"[bold cyan]{text}[/bold cyan]")
                
                try:
                    response_text = agent.process_turn(status_callback=update_status)
                except Exception as e:
                    response_text = f"**An error occurred during processing:**\n```\n{e}\n```"

            # Print the final response
            console.print("\n[bold blue]Ally[/bold blue]")
            console.print(Markdown(response_text))
            
        except KeyboardInterrupt:
            console.print("\n[bold yellow]Goodbye![/bold yellow]")
            break
        except EOFError:
            break
            
    agent.cleanup()

if __name__ == "__main__":
    main()
