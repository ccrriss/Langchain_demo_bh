from pydantic import BaseModel, Field

class ChatAnswer(BaseModel):
    answer:str = Field(description="The answer based on the user's query")