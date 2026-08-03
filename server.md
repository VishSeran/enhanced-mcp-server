# Server Documentation
## Overview
The server is built using the FastMCP framework and provides tools for interacting with files and directories.
## Features
* Reading file contents safely
* Writing and updating files
* Listing files and directories
* Searching for files within allowed directories
* Validating file paths to ensure they remain inside the configured base directory
## Security Rules
* Never access files outside the configured base directory
* Always validate user-provided paths before performing operations
* Do not expose sensitive system files or private information
## Usage
The server can be used for file management, document retrieval, file analysis, or directory operations.
## Error Handling
The server logs errors using the logger module and raises exceptions for any errors that occur during initialization.