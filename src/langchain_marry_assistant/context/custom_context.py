from dataclasses import dataclass
from langchain.tools import tool, ToolRuntime

# whether the thinking mode is on or off
@dataclass
class ThinkingMode:
    """
        Thinking mode on or off
    """
    thinking: bool

"""
to get the val from context:

get the context from ToolRuntime

"""