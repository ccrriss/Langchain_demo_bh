from langchain.tools import tool, ToolRuntime, BaseTool
from langgraph.graph.state import CompiledStateGraph
from langchain.messages import HumanMessage

"""
    Use closure to get the agent variable while keep the @tool not affected
    or the schema generated for llm will include the agent param that likely will cause error
"""

def create_search_flights_tool(travel_agent: CompiledStateGraph) -> BaseTool:

    @tool
    async def search_flights(runtime: ToolRuntime) -> str:
        """
            travel_agent搜索飞往理想婚礼地点的航班
        """
        origin = runtime.state["origin"]
        destination = runtime.state["destination"]

        content = f"查询从{origin}到{destination}的航班"
        response = await travel_agent.ainvoke(
            {
                "messages": [HumanMessage(content=content)]
            }
        )

        return response["messages"][-1].text

    return search_flights