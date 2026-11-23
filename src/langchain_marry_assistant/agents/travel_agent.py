"""
    This subagent includes kiwi and time MCP of flight and time
"""

from langchain_marry_assistant.mcp.kiwi_mcp import KIWI_MCP_CONNECTION
from langchain_marry_assistant.mcp.time_mcp import TIME_MCP_CONNECTION
from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.tools import BaseTool
from langchain_marry_assistant.middlewares.model_fallback_middleware import model_fallback_middleware

async def get_tools() -> list[BaseTool]:
    client = MultiServerMCPClient(
        connections={
            **KIWI_MCP_CONNECTION,
            **TIME_MCP_CONNECTION
        }
    )

    tools = await client.get_tools()
    return tools

async def get_travel_agent():
    """
        1. get the tools
        2. create the agent with the tools and the model_fallback_middleware(unnecessary)
    """
    tools = await get_tools()

    travel_agent = create_agent(
        model="openai:qwen3.5-flash",  
        tools=tools,
        middleware=[model_fallback_middleware],
        system_prompt="""
        你是一个旅行助手agent, 为用户搜索到达婚礼地点的理想航班, 你不能再追问任何后续问题.
        标准如下:
        - 价格(尽量低, 经济舱为主)
        - 持续时间(越短越好)
        - 日期(你认为该地点举行婚礼的最佳时间)
        你不会得到额外的信息, 只有出发地和目的地.
        请让用户知道你的候选列表.
        """
    )

    return travel_agent
