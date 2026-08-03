# Enhanced MCP Server

A hands-on implementation of the **Model Context Protocol (MCP)**, featuring a fully-featured Python MCP server and a companion CLI client that connects the server to Claude via the Anthropic API.

---

## Overview

Large Language Models are powerful at generating text, but on their own they can't act on the world. **MCP (Model Context Protocol)** solves this by standardizing how an LLM talks to its environment through three capability types:

- **Tools** — perform actions (write & delete files)
- **Resources** — expose data (read files, list directories)
- **Prompts** — guide structured workflows (code review, documentation generation)

This project implements all three, plus MCP **Context** features (logging, progress reporting, and user elicitation), and ships a CLI client that can converse with Claude using the server's tools.

## Features

### Server (`server.py`)
- **Tools**
  - `write_file` — creates a file (with parent directories) and reports write progress via `ctx.report_progress`
  - `delete_file` — deletes a file with validation and logging via `ctx.info` / `ctx.warning` / `ctx.error`
- **Resources**
  - `file:///{file_name}` — resource template that reads a file's contents
  - `dir://.` — static resource that lists the current directory with metadata (name, path, type, size, timestamps)
- **Prompts**
  - `code_review(file_path)` — builds a structured code-review prompt from a target file
  - `documentation_generator()` — uses **elicitation** (`ctx.elicit`) to ask the user for a file to document and a name for the generated doc, then builds a documentation-generation prompt
- **MCP Context**
  - Logging (`ctx.info`, `ctx.warning`, `ctx.error`)
  - Progress reporting (`ctx.report_progress`)
  - User elicitation (`ctx.elicit`) with a Pydantic schema (`DocumentGeneratorSchema`)

### Client (`client.py`)
- Connects to the server over **STDIO** using `fastmcp.Client`
- Implements handlers for elicitation, progress, and server messages/notifications
- Runs an **agentic loop** with the Anthropic API: sends the user query + available tools to Claude, executes any requested tool calls against the MCP server, feeds results back, and repeats until Claude returns a final answer
- Interactive **CLI menu**:
  1. Generate Documentation
  2. Review Code
  3. Read File
  4. Read Current Directory
  5. Converse with Agent
  6. Quit

## Requirements

- Python 3.10+
- An Anthropic API key (set as an environment variable, typically via a `.env` file)
- Dependencies listed in `requirements.txt` (includes `fastmcp`, `anthropic`, `pydantic`, `python-dotenv`)

## Setup

```bash
# Clone the repo
git clone <this-repo-url>
cd enhanced-mcp-server

# Create and activate a virtual environment
pip install virtualenv
virtualenv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

Create a `.env` file in the project root with your Anthropic API key:

```
ANTHROPIC_API_KEY=your_api_key_here
```

## Usage

Run the client, pointing it at the server script:

```bash
python client.py server.py
```

You'll see:

```
MCP Client Started!
Select from the menu or 'quit'/'q' to exit.

Select from the Menu
1. Generate Documentation
2. Review Code
3. Read File
4. Read Current Directory
5. Converse with Agent
q. Quit
```

From there you can:
- Generate documentation for a code file (via elicitation-driven prompt)
- Request a code review of a given file
- Read file contents or list the current directory via MCP resources
- Have an open-ended, tool-using conversation with Claude

## Project Structure

```
enhanced-mcp-server/
├── server.py         # MCP server: tools, resources, prompts, Context usage
├── client.py         # MCP client: CLI menu, Claude integration, agentic loop
├── requirements.txt  # Python dependencies
└── .env              # Anthropic API key (not committed)
```

## How It Works

1. `client.py` launches `server.py` as a subprocess and connects via STDIO transport.
2. The client fetches the server's tools and passes them to Claude alongside the user's query.
3. If Claude requests a tool call, the client invokes it on the MCP server, returns the result to Claude, and repeats until Claude produces a final text response (the agentic loop).
4. Prompts and resources are invoked directly (via menu selection) rather than through the agentic loop, since they represent user-controlled or passive data-access operations.

## Extending This Project

Ideas for building on this foundation:
- Add new tools (file search, code formatting, database access)
- Expose additional resources (APIs, system metrics)
- Turn prompts into multi-step workflows (debugging, data analysis, automation)
- Explore sandboxing and securing MCP servers for production use

## License

The original lab content this project is based on is licensed under Apache 2.0.


