from langchain.tools import tool, ToolRuntime, BaseTool
from langgraph.graph.state import CompiledStateGraph
from langchain.messages import HumanMessage

"""
    Use closure to get the agent variable while keep the @tool not affected
    similar to search_flights
"""

def create_search_venues_tool(venue_agent: CompiledStateGraph) -> BaseTool:

    @tool
    async def search_venues(runtime: ToolRuntime) -> str:
        """
            venue_agent根据给定的地点和宾客数量寻找最佳的婚礼场地
        """
        destination = runtime.state["destination"]
        capacity = runtime.state["guest_count"]

        content = f"在{destination}寻找适合{capacity}宾客的婚礼场地"

        response = await venue_agent.ainvoke(
            {
                "messages": [HumanMessage(content=content)]
            }
        )

        return response["messages"][-1].text

    return search_venues