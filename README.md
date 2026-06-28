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

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ally.git
cd ally
```
*(Replace `YOUR_USERNAME` with your actual GitHub username)*

### 2. Create a Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install the package

Install the package in editable mode so you can easily modify it:

```bash
pip install -e .
```

## Configuration

Ally uses a `.env` file for configuration.

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Open the `.env` file and configure it to point to your AI provider. For example, if you are using LM Studio locally:
   ```env
   ALLY_API_BASE_URL=http://localhost:1234/v1
   ALLY_API_KEY=lm-studio
   ALLY_MODEL=local-model
   ```
   *Note: Even for local providers, an API key is sometimes required by the OpenAI client, so a dummy string like `lm-studio` is used.*

## Usage

Once installed and configured, you can start Ally by simply running:

```bash
ally
```

Or, alternatively, you can run the module directly:

```bash
python3 main.py
```

Type your requests to Ally in the prompt. Type `exit` or `quit` to close the agent.

## Tools Available

Out of the box, Ally comes with the following tools:
- `run_shell_command(command)`: Executes a command in your terminal.
- `read_file(path)`: Reads the contents of a local file.
- `write_file(path, content)`: Creates or updates a local file.
