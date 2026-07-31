
import os
import dotenv

from langchain_groq import ChatGroq
from langchain.agents import create_agent

from configuration.configs import MODEL_NAME
from configuration.logger import get_logger


logger = get_logger("llm-agent")
dotenv.load_dotenv()

class LLMAgent:
    
    def __init__(self, tools, model_name=MODEL_NAME):
        
        
        try:
            GROQ_API = os.getenv("groq_api")
            
            self.llm = ChatGroq(
                api_key=GROQ_API,
                model=model_name,
                temperature=0.5
            )
            
            self.llm_agent = create_agent(
                model=self.llm,
                tools=tools,
                system_prompt="""
                            You are a useful AI agent.
                            You have access to the tools that provided.
                            Use the relevant tools if needed when answering the user questions.
                """
            )
            
        except ValueError as e:
            logger.error(f"Value error: {e}")
            raise
            
        except Exception as e:
            logger.error(f"Error in llm agent initialization: {e}")
            raise
        