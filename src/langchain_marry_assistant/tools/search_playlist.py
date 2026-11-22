from langchain.tools import tool, ToolRuntime, BaseTool
from langgraph.graph.state import CompiledStateGraph
from langchain.messages import HumanMessage

"""
    Use closure to get the agent variable while keep the @tool not affected
    similar to search_flights
"""

def create_search_playlist_tool(playlist_agent: CompiledStateGraph) -> BaseTool:

    @tool
    async def search_playlist(runtime: ToolRuntime) -> str:
        """
            playlist_agent根据类型风格策划播放列表
        """
        genre = runtime.state["genre"]

        content = f"策划符合{genre}风格的婚礼播放列表的曲目"

        response = await playlist_agent.ainvoke(
            {
                "messages": [HumanMessage(content=content)]
            }
        )

        return response["messages"][-1].text

    return search_playlist