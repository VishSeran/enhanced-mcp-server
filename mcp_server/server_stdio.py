from configuration.logger import get_logger
from mcp_server.server import mcp
from fastmcp import Context


logger = get_logger("server_stdio")

@mcp.tool
async def write_file(file_path:str, content:str, ctx:Context):
    
    

