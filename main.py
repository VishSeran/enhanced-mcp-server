import asyncio

from configurations.logger import get_logger
from mcp_client.client import MCPClient

logger = get_logger("main")

async def main():
    
    try:
        mcp_client = MCPClient()
        logger.info("MCP Client has initiated")
        
        logger.info("MCP Client is connceting to server...")
        await mcp_client.connect_to_mcp_server("mcp_server.server_stdio")
        
        logger.info("LLM agent is initializing...")
        await mcp_client.init_agent()
        
        await mcp_client.menu()
    
    except ValueError as e:
        logger.error(f"Value error: {e}")
        raise
        
    except Exception as e:
        logger.error(f"Error in main: {e}")
        raise
    
    
if __name__ == "__main__":
    asyncio.run(main())
    