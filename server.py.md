# Server Documentation
## Overview
The server.py file contains the implementation of the MCPServer class, which provides tools for interacting with files and directories.
## Class Description
The MCPServer class initializes a FastMCP server with a set of instructions that describe its purpose and functionality.
## Instructions
The server provides tools for:
* Reading file contents safely
* Writing and updating files
* Listing files and directories
* Searching for files within allowed directories
* Validating file paths to ensure they remain inside the configured base directory
## Security Rules
All file operations must follow these security rules:
* Never access files outside the configured base directory
* Always validate user-provided paths before performing operations
* Do not expose sensitive system files or private information
## Usage
To use the server, create an instance of the MCPServer class and access the mcp_server attribute.
## Error Handling
The server catches and logs any ValueErrors or Exceptions that occur during initialization, and raises them to prevent further execution.