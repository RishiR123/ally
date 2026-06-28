# Ally - CLI Coding Agent

Ally is a basic, terminal-native, local-first coding assistant by Orionac. Inspired by tools like Goose, Ally allows you to bring the power of AI into your terminal. It can execute shell commands, read and write files, and help you automate complex engineering workflows directly from your command line.

Ally is built in Python and connects to OpenAI-compatible endpoints, making it perfect for use with local LLMs via tools like [LM Studio](https://lmstudio.ai/) or [Ollama](https://ollama.com/).

## Features

- **Terminal-Native:** Stay in your CLI. Ally works where you work.
- **Local-First Capabilities:** Works beautifully with local models using OpenAI-compatible APIs.
- **File System Access:** Can read, create, and modify files.
- **Shell Execution:** Can run shell commands and read their output.
- **Beautiful UI:** Uses `rich` for elegant markdown rendering and live status indicators.

## Prerequisites

- Python 3.9 or higher

## Installation

You can install Ally globally on macOS or Linux using our installation script. This will set up an isolated environment and create an executable in `~/.local/bin`.

Because this repository is **private**, you cannot use a simple `curl` command to download the script. Instead, please clone the repository and run the script locally:

```bash
git clone https://github.com/RishiR123/ally.git
cd ally
./install.sh
```

**Important:** Make sure `~/.local/bin` is in your system's `PATH`. If it isn't, add this to your `~/.zshrc` or `~/.bashrc`:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

## Setup & Usage

To start Ally and run the interactive setup, simply type:

```bash
ally
```

On your first run, Ally will interactively prompt you for your API provider details (like your LM Studio URL and model name). These settings are saved globally in `~/.ally/.env`.

To update your configuration later, you can run:

```bash
ally --setup
```

Type your requests to Ally in the prompt. Type `exit` or `quit` to close the agent.

## Tools Available

Out of the box, Ally comes with the following tools:
- `run_shell_command(command)`: Executes a command in your terminal.
- `read_file(path)`: Reads the contents of a local file.
- `write_file(path, content)`: Creates or updates a local file.
