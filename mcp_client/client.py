from typing import Type

from contextlib import AsyncExitStack
from fastmcp.client.transports import StdioTransport
from fastmcp.client import Client
from fastmcp.client.elicitation import ElicitResult


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
                args =["-m", server_script_path]
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
        
    
    async def elicitation_handler(self, message:str, response_type:type, params, context):
        """Handle elicitation requests from the MCP server.
    
                When the server needs user input, this handler prompts the user,
                collects their response, and returns it in the expected format.
    
                Args:
                    message: The question or prompt from the server
                    response_type: Pydantic model defining the expected response structure
                    params: Additional parameters for the elicitation
                    context: Elicitation context information
    
                Returns:
                    ElicitResult with action="decline" if no response, or response_type instance with user input
                """
        try:
            if not message:
                raise ValueError("Server message is missing")
            
            print(f"Server asks: {message}")
            user_data = {}
            
            for field_name, field_type in response_type.__annotations__.items():
                user_input = input(f"Enter value for '{field_name}' ({field_type.__name__}): "). strip()
                
                if not user_input:
                    return ElicitResult(action="decline")
            
                user_data[field_name] = user_input
                
            logger.info("elicitation response if fetched")
            return response_type(**user_data)
  
        except ValueError as e:
            logger.error(f"Value error: {e}")
            raise
            
        except Exception as e:
            logger.error(f"Error in elicitation_handler: {e}")
            raise