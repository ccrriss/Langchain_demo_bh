from pydantic import BaseModel, Field

class Reference(BaseModel):
    title: str = Field(description="The title of the page cited in the answer")
    url:str = Field(description="The url of the page cited in the answer")

class AnswerInfo(BaseModel):
    answer: str = Field(description="The final answer for user")
    reference_list: list[Reference] = Field(description="The web pages cited in the answer")