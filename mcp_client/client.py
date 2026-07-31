from typing import Any

from contextlib import AsyncExitStack
from fastmcp.client.transports import StdioTransport
from fastmcp.client import Client
from fastmcp.client.elicitation import ElicitResult
from fastmcp import Context


from agent.llm_agent import LLMAgent
from configuration.logger import get_logger


logger = get_logger("mcp-client")

class MCPClient:
    
    def __init__(self, tools):
        
        
        try:
            self.stdio_client = None
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
            
            self.stdio_client = Client(
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
        
    
    async def elicitation_handler(self, message:str, response_type:type, ctx:Context):
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
                
            response = response_type(**user_data)
            
            await ctx.info(f"elicitation response if fetched: {response}")
            
            logger.info(
                    "Elicitation response: %s",
                    response
                )
            return response
  
        except ValueError as e:
            logger.error(f"Value error: {e}")
            raise
            
        except Exception as e:
            logger.error(f"Error in elicitation_handler: {e}")
            raise
        
    
    async def progress_handler(self, progress:float, total:float | None, message:str | None) -> None:
        """Handle progress notifications from the MCP server.

        Displays progress updates to the user, showing percentage complete if total is provided.

        Args:
            progress: Current progress value
            total: Total expected progress value (None if unknown)
            message: Optional descriptive message about current progress
        """
        
        try:
            
            if not progress:
                raise ValueError("progress is missing")
            
            if total is not None:
                percentage = (progress/total) * 100
                print(f"Progress: {percentage:.1f}% - {message or ''}")
                
            else:
                print(f"Progress: {progress} - {message or ''}")
            
        except ValueError as e:
            logger.error(f"Value error: {e}")
            raise
            
        except Exception as e:
            logger.error(f"Error in progress_handler: {e}")
            raise
        
        
    async def message_handler(self,message) -> None:
        
        """Handle notification messages from the MCP server.

        Processes server notifications such as tool list changes or resource updates
        and displays appropriate messages to the user.

        Args:
            message: MCP notification message from the server
        """
        
        try:
            
            if not message:
                raise ValueError("message is missing")
            
            if hasattr(message, 'root'):
                method = message.root.method
                print(f"Received: {method}")
                
                if method == "notifications/tools/list_changed":
                    print("Tools have changed - might want to refresh tool cache")
                    
                elif method == "notifications/resources/list_changed":
                    print("Resources have changed - might want to refresh tool cache")
         
        except ValueError as e:
            logger.error(f"Value error: {e}")
            raise
            
        except Exception as e:
            logger.error(f"Error in message_handler: {e}")
            raise
        
        
    async def get_tools(self) -> list[dict[str, Any]]:
        
        try:
            
            tools_list = await self.stdio_client.list_tools()
            logger.info("Tools are fetched")
            
            tools_des = []
            
            tools_des.append(
                {
                    "name": tool.name,
                    "description": tool.description,
                    "input_schema": tool.inputSchema
                    
                } for tool in tools_list
            )
            logger.info(f"tools are fetched: {tools_des}")
            return tools_des
            
        except ValueError as e:
            logger.error(f"Value error: {e}")
            raise
            
        except Exception as e:
            logger.error(f"Error in get tools: {e}")
            raise
        
    
    async def get_resources(self) -> list[dict[str, Any]]:
        try:
            result = await self.stdio_client.list_resources()

            resources_list = [
                {
                    "name": res.name,
                    "description": res.description,
                }
                for res in result.resources
            ]
            logger.info(f"resources are fetched: {resources_list}")
            return resources_list

        except ValueError as e:
            logger.error(f"Value error: {e}")
            raise

        except Exception:
            logger.exception("Error while getting resources")
            raise
        
    async def get_prompt(self):
        
        try:
            
            result = await self.stdio_client.list_prompts()
            logger.info("Prompts list fetched success")
            
            return result
            
        except ValueError as e:
            logger.error(f"Value error: {e}")
            raise
            
        except Exception as e:
            logger.error(f"Error in get prompt: {e}")
            raise
        
    async def get_resource_templates(self):
            
            try:
                
                result = await self.stdio_client.list_resource_templates()
                logger.info("resource templates list fetched success")
                
                return result
                
            except ValueError as e:
                logger.error(f"Value error: {e}")
                raise
                
            except Exception as e:
                logger.error(f"Error in get prompt: {e}")
                raise