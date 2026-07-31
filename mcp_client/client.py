from contextlib import AsyncExitStack

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
        
    async def connect_to_mcp_server(self, server_script:str):
        
        
        try:
            
        except ValueError as e:
            logger.error(f"Value error: {e}")
            raise
            
        except Exception as e:
            logger.error(f"Error in llm agent initialization: {e}")
            raise