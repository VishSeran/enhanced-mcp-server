from configuration.logger import get_logger
from configuration.configs import get_relative_path, Base_dir
from pathlib import Path
from mcp_server.server import mcp
from fastmcp import Context
import time
from datetime import datetime

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
async def read_file_resources(file_name: str, ctx:Context) -> dict:
    
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
        
        if not path.exists() or not path.is_file():
            ctx.warning(f"error: file is missinng: {file_name}")
            return{
                "error": f"file is missinng: {file_name}"
            }
        
        ctx.info(f"read file successful: {file_name}")
        
        return {
            "file_content": path.read_text(encoding="utf-8")
        }
        
        
    except ValueError as e:
        await ctx.error(f"Value error in read file resource: {e}")
        raise
    
    except Exception as e:
        await ctx.error(f"Error in read file resource: {e}")
        raise
    

@mcp.resource("dir://.")
async def list_files_resource(ctx: Context) -> dict:
    
    try:
        
        path = get_relative_path(".")
        
        if not path.exists():
            raise ValueError(f"file directory not exists: {path}")
        
        items = []
        
        for item in path.iterdir():
            status = item.stat()
            
            items.append({
                "name": item.name,
                "path": str(item.relative_to(Base_dir)),
                "type": "dictonary" if item.is_dir() else "file",
                "size": status.st_size,
                "modified": datetime.fromtimestamp(status.st_mtime).isoformat(),
                "created": datetime.fromtimestamp(status.st_ctime).isoformat()
            })
            
        return {
            "items" : items
        }

    except ValueError as e:
        await ctx.error(f"Value error in list files resource: {e}")
        raise
    
    except Exception as e:
        await ctx.error(f"Error in list files resource: {e}")
        raise
    

@mcp.prompt()
async def code_review(file_path: str, ctx: Context) -> str:
    
    """Generate a prompt for code review  and quality evaluation.
    
        Reads a code file and generate a prompt for groq support to perform a comprehensive 
        code review.
        
        Args:
            file_path: the file path for a file that contains the code.
            ctx: MCP context that manages logging and communication.
            
        Returns:
            Formatted prompt string for code review.
            
        Raises:
            FileNotFoundError: if the specified file doesn't exist 
    """
    
    try:
        
        path = get_relative_path(file_path)
        
        if not path.is_file() or not path.exists():
            await ctx.warning(f"Error: {file_path} is not a valid file")
            raise FileNotFoundError(f"Error: {file_path} is not a valid file")
        
        
    except FileNotFoundError as e:
        await ctx.error(f"Value error in code review: {e}")
        raise
    
    except Exception as e:
        await ctx.error(f"Error in code review: {e}")
        raise