from langchain.agents import AgentState
from langchain.tools import tool, ToolRuntime
from langgraph.types import Command
from langchain.messages import ToolMessage

class WeddingState(AgentState):
    origin: str  
    destination: str
    guest_count: str
    genre: str  # style of the wedding

@tool
def update_wedding_state(origin: str, destination: str, guest_count: str, genre: str, runtime: ToolRuntime) -> Command:
    """
        询问用户, 知道下列所有值时更新State: origin, destination, guest_count, genre
    """
    update = {
        "origin": origin,
        "destination": destination,
        "guest_count": guest_count,
        "genre": genre,
        "messages": [
            ToolMessage(
                content="Successfully updated state",
                tool_call_id = runtime.tool_call_id
            )
        ]
    }
    return Command(update=update)