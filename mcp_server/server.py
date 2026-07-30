from fastmcp import FastMCP
from configuration.logger import get_logger


logger = get_logger("server")

class MCPServer:
    
    def __init__(self):
        
        try:
            
            self.mcp_server = FastMCP(
                name = "FileServer",
                instructions= """
            This MCP server provides tools for interacting with files and directories.

            The server can perform file-related operations such as:
            - Reading file contents safely.
            - Writing and updating files.
            - Listing files and directories.
            - Searching for files within allowed directories.
            - Validating file paths to ensure they remain inside the configured base directory.

            All file operations must follow security rules:
            - Never access files outside the configured base directory.
            - Always validate user-provided paths before performing operations.
            - Do not expose sensitive system files or private information.

            Use the available file tools when the user requests file management,
            document retrieval, file analysis, or directory operations.
            """
            )
            
        except ValueError as e:
            logger.error(f"Value error in mcp server: {e}")
            raise
            
        except Exception as e:
            logger.error(f"Error in mcp server: {e}")
            raise
