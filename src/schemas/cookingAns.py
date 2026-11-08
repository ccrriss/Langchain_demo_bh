from pydantic import BaseModel, Field

class CookAnswer(BaseModel):
    answer:str = Field(description="The answer of how to cook based on the user's query")