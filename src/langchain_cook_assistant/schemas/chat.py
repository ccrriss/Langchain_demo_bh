from pydantic import BaseModel, Field
from typing import Literal

class ChatRequest(BaseModel):
    query: str = Field(description="The query of the user")
    thread_id: str = Field(description="the thread id of checkpoint")

class ChatMessage(BaseModel):
    role: Literal["ai", "human"] = Field(description="The chat message")
    message: str = Field(description="The chat message from ai or user")