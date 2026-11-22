from langchain.tools import tool, ToolRuntime
from langchain.agents import create_agent
from langchain.messages import HumanMessage, ToolMessage, AIMessage
from dotenv import load_dotenv
from langgraph.checkpoint.memory import InMemorySaver
from langchain_marry_assistant.middlewares.custom_middleware import dynamic_model_settings, ModelCallLimitMiddleware
from langchain_marry_assistant.context.custom_context import ThinkingMode
# MCP
from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent

CUSTOM_MCP_SERVER_PATH = BASE_DIR / "mcp" / "custom_mcp.py"

load_dotenv()

# # Agent
agent = create_agent(
    model="openai:qwen3.5-flash",
    checkpointer=InMemorySaver(),
)


