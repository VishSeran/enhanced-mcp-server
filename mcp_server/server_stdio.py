from configuration.logger import get_logger
from configuration.configs import get_logger
from mcp_server.server import mcp
from fastmcp import Context


logger = get_logger("server_stdio")

@mcp.tool
async def write_file(file_path:str, content:str, ctx:Context):
    
    """
    create a new file with specific content.
    
    create a parent dictionaries if they dont exists. Write content to the file using  
    UTF-8 encoding.
    
    Args:
        file_path: Relative path where the file should be created.
        content: Content to write to the file.
        ctx: MCP Context for logging
        
    returns:
        Success messages with file path
    
    Raises:
        Exception: If file creation fails (logged to context)
    """
    
    try:
        
        path = 
        
    except ValueError as e:
        ctx.error(f"Value error: {e}")
        raise
    
    except Exception as e:
        ctx.error(f"Error in write file:" {e})
        raise

