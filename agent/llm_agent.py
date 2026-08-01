
import os

import dotenv
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import InMemorySaver

from configurations.configs import MODEL_NAME
from configurations.logger import get_logger

logger = get_logger("llm-agent")
dotenv.load_dotenv()

class LLMAgent:
    
    def __init__(self, tools, model_name=MODEL_NAME):
        
        
        try:
            GROQ_API = os.getenv("groq_api")
            
            if not model_name:
                raise ValueError("Model name is empty")
            
            if not GROQ_API:
                raise ValueError("GROQ_API_KEY is missing from environment")
            
            
            if not tools:
                raise ValueError("tools list is missing or empty")
            
            checkpointer = InMemorySaver()
            
            self.config = {
                "configurable": {
                    "thread_id": "conversational_id"
                }
            }
            
            self.llm = ChatGroq(
                api_key=GROQ_API,
                model=model_name,
                temperature=0.5,
                max_tokens=4000
            )
            
            logger.info(f"{model_name} model initiated")
            
            self.llm_agent = create_agent(
                model=self.llm,
                tools=tools,
                checkpointer=checkpointer,
                system_prompt="""
                            You are a useful AI agent.
                            You have access to the tools that provided.
                            Use the relevant tools if needed when answering the user questions.
                """
            )
            
            logger.info("LLM Agent initiated")
            
        except ValueError as e:
            logger.error(f"Value error: {e}")
            raise
            
        except Exception as e:
            logger.error(f"Error in llm agent initialization: {e}")
            raise
        
    
    async def get_response(self, query:str):
        
        try:
            
            if not query:
                raise ValueError("Query is missing")
            
            response = await self.llm_agent.ainvoke({
                "messages": [
                    {
                        "role": "user",
                        "content": query
                        
                    }
                ]
            }, config=self.config)
            
            logger.info("Reponse is fetched")
            return response['messages'][-1].content
  
            
        except ValueError as e:
            logger.error(f"Value error: {e}")
            raise
            
        except Exception as e:
            logger.error(f"Error in get response: {e}")
            raise    
        