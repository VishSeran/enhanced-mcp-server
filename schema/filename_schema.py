from pydantic import BaseModel


class DocumentGeneratorSchema(BaseModel):
    
    file_path:str
    name:str