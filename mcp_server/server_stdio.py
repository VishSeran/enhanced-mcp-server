from configuration.logger import get_logger
from configuration.configs import get_relative_path
from pathlib import Path
from mcp_server.server import mcp
from fastmcp import Context
import time


logger = get_logger("server_stdio")

@mcp.tool()
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
        
        path = get_relative_path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        total = len(content)
        chunk_size = max(total//10, 1)
        
        written = 0
        
        with open (path, "w", encoding="utf-8") as f:
            for i in range(0,total, chunk_size):
                f.write(content[i:i+chunk_size])
                written = min(i+chunk_size, total)
                
                await ctx.report_progress(progress=written,
                                          total=total,
                                          message=f"Writing progress: {written}/{total}")
                
                
                time.sleep(0.05)    
            
            await ctx.report_progress(
                progress=total,
                total=total,
                message="Write is completed"
            )
            
            await ctx.info(f"File written successfully to path: {path}")
            return f"File written successfully to: {file_path}"
                
    except ValueError as e:
        await ctx.error(f"Value error: {e}")
        raise
    
    except Exception as e:
        await ctx.error(f"Error in write file: {e}")
        raise
    
    

@mcp.tool()
async def delete_file(file_path:str, ctx: Context) -> str:
    
    """
    Delete a file from the project directory.
    
    Validates that the path points to a file (not a directory) before deletion.
    
    Args:
        file_path: Relative path to the file to delete
        ctx: MCP context for logging
        
    Returns:
        Success or error message describing the operation result
    """
    
    
    try:
        path = get_relative_path(file_path)
        
        if path.is_file():
            path.unlink()
            await ctx.info(f"Successfully deleted file: {file_path}")
            return f"Successfully deleted file: {file_path}"
        
        elif path.is_dir():
            await ctx.warning(f"Error: {file_path} is a directory, not a file")
            return f"Error: {file_path} is a directory, not a file"
        
        else:
            await ctx.warning(f"File not found: {file_path}")
            return f"File not found: {file_path}"
        
        
    except ValueError as e:
        await ctx.error(f"Value error: {e}")
        raise
         
    except Exception as e:
        await ctx.error(f"Error in deleting file: {e}")
        raise
    
    
@mcp.resource("file:///{file_name}")
async def read_file_resources(file_name: str, ctx:Context):
    
    """
    Read the content  of a file  as an  MCP resource
    
    provides  file content  access  through the MCP  resource  protocol using 
    the  file:/// URI schema
    
    Args:
        file_name: Relative path to the file read
        
    Returns:
        Dictionary contains either file_content or error message
    
    """
    
    try:
        
        path = get_relative_path(file_name)
        
        
        
    except ValueError as e:
        await ctx.error(f"Value error in read file resource: {e}")
        raise
    
    except Exception as e:
        await ctx.error(f"Error in read file resource: {e}")
        raise