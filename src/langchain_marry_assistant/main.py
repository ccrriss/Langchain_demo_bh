from langchain.tools import tool, ToolRuntime
from langchain.agents import create_agent
from langchain.messages import HumanMessage, ToolMessage, AIMessage
from dotenv import load_dotenv

# since the ModelFallbackMiddleware creates model obj, so load_dotenv before import
load_dotenv()

from langgraph.graph.state import CompiledStateGraph
from langgraph.checkpoint.memory import InMemorySaver
import asyncio

# import the tools to create tools with subagents
from langchain_marry_assistant.tools.search_flights import create_search_flights_tool
from langchain_marry_assistant.tools.search_playlist import create_search_playlist_tool
from langchain_marry_assistant.tools.search_venues import create_search_venues_tool
# import the get agent functions to get subagents then use them to create tools
from langchain_marry_assistant.agents.playlist_agent import get_playlist_agent
from langchain_marry_assistant.agents.travel_agent import get_travel_agent
from langchain_marry_assistant.agents.venue_agent import get_venue_agent
# import the customized state
from langchain_marry_assistant.state.wedding_state import WeddingState, update_wedding_state

async def tools_initialize():
    travel_agent = await get_travel_agent()
    playlist_agent = await get_playlist_agent()
    venue_agent = await get_venue_agent()

    search_flights = create_search_flights_tool(travel_agent=travel_agent)
    search_playlist = create_search_playlist_tool(playlist_agent=playlist_agent)
    search_venue = create_search_venues_tool(venue_agent=venue_agent)

    return [search_flights, search_playlist, search_venue]

async def main() -> CompiledStateGraph:
    tools = await tools_initialize()

    # Using langgraph server doesn't need the InMemorySaver
    agent: CompiledStateGraph = create_agent(
        model="openai:qwen3.5-flash",
        tools=[*tools, update_wedding_state],
        state_schema=WeddingState,
        system_prompt="""
        你是婚礼协调员. 你负责与用户沟通, 找到更新状态所需的所有信息, 并更新到state.
        一旦完成你就可以委派任务了. 将查找航班, 搜索场地和策划播放列表的任务委派给你的专家agent.
        当你收到他们的答案, 设计一场婚礼方案.
        """
    )

    return agent




