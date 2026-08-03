import json
from contextlib import AsyncExitStack
from typing import Any
from urllib.parse import quote

from fastmcp import Context
from fastmcp.client import Client
from fastmcp.client.elicitation import ElicitResult
from fastmcp.client.transports import StdioTransport
from langchain_mcp_adapters.tools import load_mcp_tools
from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client
from mcp.types import ClientCapabilities, ElicitationCapability

from agent.llm_agent import LLMAgent
from configurations.logger import get_logger

logger = get_logger("mcp-client")

class MCPClient:
    
    def __init__(self):
        
        
        try:
            self.stdio_client = None
            self.agent = None 
            self.session = None
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
            if self.stdio_client is not None:
                raise RuntimeError(
                    "Already connected to MCP server"
                )
            
            if not server_script_path:
                raise ValueError("server script must have to connect the server!!!")
            
            if (server_script_path.endswith((".py", ".js", ".ts"))):
                
                server_params = StdioServerParameters(
                    command="python",
                    args =[server_script_path]
                )
            
            elif "." in server_script_path:
                server_params = StdioServerParameters(
                    command="python",
                    args=["-m", server_script_path]
                )
                
            else:
                raise ValueError("server script must be a .py or .js or .ts file") 

            read,write = await self.exit_stack.enter_async_context(
                stdio_client(server_params)
            )
            
            self.session = await self.exit_stack.enter_async_context(
                ClientSession(
                    read,
                    write,
                    client_info={
                        "name": "enhanced-mcp-client",
                        "version": "1.0.0"
                    }
                    ,elicitation_callback= self.elicitation_handler
                )
            )
            
            await self.session.initialize()
            logger.info("Client session has initialized")
            
            
        except ValueError as e:
            logger.error(f"Value error: {e}")
            raise
            
        except Exception as e:
            logger.error(f"Error in connect_to_mcp_server: {e}")
            raise
        
    
    async def elicitation_handler(
                                self,
                                context,
                                params):
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
            
            print(f"Server asks: {params.message}")
            schema = params.requestedSchema
            user_data = {}
            
            for field_name, field_schema in schema["properties"].items():
                value = input(f"{field_name}: ")

                if not value:
                    return ElicitResult(action="decline")

                user_data[field_name] = value
            
           
            logger.info(
                    "Elicitation response: %s",
                    user_data
                )
            
            return ElicitResult(
                action="accept",
                content=user_data
            )
  
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
            
            if progress is None:
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
            
            if message is None:
                raise ValueError("message is missing")
            
            if hasattr(message, 'root') and hasattr(message.root, "method"):
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
            
            tools_list = await self.session.list_tools()
            logger.info("Tools are fetched")
        
            tools_des = [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "input_schema": tool.inputSchema
                    
                } for tool in tools_list
            ]
                
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
            result = await self.session.list_resources()

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
            
            result = await self.session.list_prompts()
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
                
                result = await self.session.list_resource_templates()
                logger.info("resource templates list fetched success")
                
                return result
                
            except ValueError as e:
                logger.error(f"Value error: {e}")
                raise
                
            except Exception as e:
                logger.error(f"Error in get prompt: {e}")
                raise
            
            
    async def close(self):
        
        await self.exit_stack.aclose()
        
        self.session = None
        self.agent = None
        
        logger.info(
        "MCP client closed"
    )
            
    async def init_agent(self):
        
        try:
            
            if self.session is None:
                raise RuntimeError(
                    "MCP session is not initialized"
                )
                
            tools = await load_mcp_tools(self.session)
            
            
                
            self.agent = LLMAgent(tools=tools)
            
        except RuntimeError as e:
            logger.error(f"Runtime error: {e}")
            raise
            
        except Exception as e:
            logger.error(f"Error in init_agent: {e}")
            raise
            
    async def get_llm_response(self,query):
        
        try:
            
            if self.agent is None:
                raise RuntimeError(
                    "Agent is not initialized"
                )
            
            response = await self.agent.get_response(query)
            logger.info(f"client llm response is fetched: {response}")
            return response
        
        except RuntimeError as e:
            logger.error(f"runtime error: {e}")
            raise
            
        except Exception as e:
            logger.error(f"Error in get_llm_response: {e}")
            raise
        
        
    async def conversation(self) -> None:
        
        print("\nEntering conversation mode. Type 'quit' or 'q' to exit.")
        
        while (True):
            
            query = input("\nQuery: ").strip()
            
            if query.lower() in ("quit", "q"):
                print("Exit conversation...")
                break
            
            if query is None:
                print("\nPlease enter a query")
                continue
            
            try:
                response = await self.get_llm_response(query)
                print("\n" + response)
                
            except Exception as e:
                logger.error(f"Error in conversation: {e}")
                raise
            
    
    async def prompt(self, prompt_name:str):
        
        try:
            
            prompt_res = await self.get_prompt()
            prompt_result = prompt_res.prompts
            
            prompt_obj = next(
                (prompt for prompt in prompt_result if prompt.name == prompt_name), None
            )
            
            if prompt_obj is None:
                logger.info(f"No matching prompt name: {prompt_name}")
            
            logger.info(f"{prompt_name} prompt extracted success")
            
            print(prompt_obj)
            
            ## get prompt template arguments
            arguments = {}
            
            if prompt_obj.arguments:
                for argument in prompt_obj.arguments:
                    
                    required = "required" if argument.required else "optional"
                    user_input = input(f"{argument.name} - {required}: ")
                    
                    if not user_input and argument.required:
                        print(f"Error in {argument.name} - {required}")  
                        return
                    
                    if user_input:
                        arguments[argument.name] = user_input    
                        
            # Generate the prompt with provided arguments      
            prompt_result = await self.session.get_prompt(prompt_name, arguments)
            prompt = prompt_result.messages[0].content.text
            
            response = await self.get_llm_response(prompt)
            print(response)
        
        except Exception as e:
            logger.error(f"Error in prompt fetching: {e}")
            raise
        
            
    async def read_file(self):
        
        """Read the contents of a file via MCP resource.

        Prompts the user for a file path and retrieves the file content
        through the MCP server's file resource.
        """
        
        try:
            
            file_name = input("Enter the file name you want to read from the mcp server").strip()
            encoded_file_name = quote(file_name, safe="")
            
            # Access file resource using file:/// URI scheme
            resource = await self.session.read_resource(f"file:///{encoded_file_name}")
            file_content = json.loads(resource.contents[0].text)['file_content']
            
            logger.info(f"File Content:\n {file_content}")
            print(f"File Content:\n {file_content}")
            
            return file_content

        except Exception as e:
            logger.error(f"Error in read file: {e}")
            raise
        
    async def read_dir(self):
        
        try:
            response = await self.stdio_client.read_resource("dir://.")
            dir_content = json.loads(response[0].text)['content']
            
            logger.info(f"File Content:\n {dir_content}")
            print(f"File Content:\n {dir_content}")
            
            return dir_content
            
        except Exception as e:
            logger.error(f"Error in read dir: {e}")
            raise
        
    
    def _print_dir_listing(self, items: list[dict]):
        """Format and print a directory listing.

        Args:
            items: List of directory items with metadata (type, size, modified, name)
        """
        print("\nDirectory Listing:\n")
        print(f"{'Type':<10} {'Size':>10} {'Modified':<25} {'Name'}")
        print("-" * 70)
        for item in items:
            # Add icon based on item type
            type_icon = "📁" if item["type"] == "directory" else "📄"
            size = f"{item['size']} B"
            print(f"{type_icon:<2} {item['type']:<8} {size:>10}  {item['modified']:<25} {item['name']}")
            
    
    async def quit(self):
        print("Exiting client...")
        return "quit"
        
            
    async def menu(self):
        
        try:
            
            print("\nMCP Client Started!!!")
            print("Select from the menu or 'quit'/'q' to exit.")
            
            menu_actions = {
                "1": lambda: self.prompt("documentation_generator"),
                "2": lambda: self.prompt("code_review"),
                "3": self.read_file,
                "4": self.read_dir,
                "5": self.conversation,
                "q": self.quit
                
            }
            
            while(True):
            
                choice = input("""
                    Select from the Menu
                    1. Generate Documentation
                    2. Review Code
                    3. Read File
                    4. Read Current Directory
                    5. Converse with Agent
                    q. Quit
                    > """).strip()
                
                
                action = menu_actions.get(choice)
                
                if not action:
                    logger.info(f"invalid actions: {action}")
                    print("Invalid choice. Please try again.")
                    continue
                
                result = await action()
                if result == "quit":
                    break
        
        except Exception as e:
            logger.error(f"Error in menu: {e}")
            raise
           