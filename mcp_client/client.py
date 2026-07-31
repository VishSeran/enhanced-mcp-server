from contextlib import AsyncExitStack
from fastmcp.client.transports import StdioTransport
from fastmcp.client import Client

from agent.llm_agent import LLMAgent
from configuration.logger import get_logger


logger = get_logger("mcp-client")

class MCPClient:
    
    def __init__(self, tools):
        
        
        try:
            
            self.agent = LLMAgent(tools)
            # AsyncExitStack for managing async context managers
            self.exit_stack = AsyncExitStack()
            
        except ValueError as e:
            logger.error(f"Value error: {e}")
            raise
            
        except Exception as e:
            logger.error(f"Error in mcp client initialization: {e}")
            raise
        
    async def connect_to_mcp_server(self, server_script_path:str):
        
        
        try:
            
            if not server_script_path:
                raise ValueError("server script must have to connect the server!!!")
            
            if not (server_script_path.endswith((".py", ".js", ".ts"))):
                raise ValueError("server script must be a .py or .js or .ts file") 
            
            
            transport = StdioTransport(
                command="python",
                args =[server_script_path]
            )
            
            stdio_client = Client(
                transport,
                elicitation_handler = self.elicitation_handler,
                progress_handler = self.progree_handler,
                message_handler = self.message_handler
            )
            
            await self.exit_stack.enter_async_context(stdio_client)
            
            
        except ValueError as e:
            logger.error(f"Value error: {e}")
            raise
            
        except Exception as e:
            logger.error(f"Error in connect_to_mcp_server: {e}")
            raise