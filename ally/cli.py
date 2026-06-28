import sys
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt

from .agent import AllyAgent

console = Console()

def print_welcome():
    welcome_text = """
# Welcome to Ally 🤖
*Your basic CLI coding agent, by Orionac.*

Type your request below. Type `exit` or `quit` to stop.
    """
    console.print(Panel(Markdown(welcome_text), style="bold blue", expand=False))

def main():
    print_welcome()
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

if __name__ == "__main__":
    main()
