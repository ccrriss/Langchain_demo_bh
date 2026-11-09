from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    query: str = Field(description="The query of the user")
    thread_id: str = Field(description="the thread id of checkpoint")