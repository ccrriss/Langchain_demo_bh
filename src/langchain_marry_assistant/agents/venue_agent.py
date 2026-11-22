"""
    This subagent includes tavily_search for searching the venue
    Used async def to get agent to keep same as travel_agent although is's actually a sync function
"""

from langchain_tavily import TavilySearch
from langchain.agents import create_agent
from langchain_marry_assistant.middlewares.model_fallback_middleware import model_fallback_middleware

search_tool = TavilySearch(
    max_results=5,
    topic="general"
)

async def get_venue_agent():
    venue_agent = create_agent(
        model="openai:qwen3.5-flash", 
        tools=[search_tool],
        middleware=[model_fallback_middleware],
        system_prompt="""
        你是场地专家, 你在指定的位置搜索满足要求的场地.
        你不能再追问任何后续问题.
        标准如下:
        - 价格(尽量低)
        - 容量(完全匹配)
        - 评价(尽可能高)
        你可能需要进行多次搜索以迭代地找到相对最佳选项.
        """
    )

    return venue_agent