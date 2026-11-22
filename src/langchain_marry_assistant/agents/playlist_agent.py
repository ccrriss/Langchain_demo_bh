"""
    This subagent includes database tool to get the playlist from database
    Used async def to get agent to keep same as travel_agent although is's actually a sync function
"""

from langchain_community.utilities import SQLDatabase
from pathlib import Path
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_marry_assistant.middlewares.model_fallback_middleware import model_fallback_middleware

CURRENT_DIR = Path(__file__).resolve().parent
BASE_DIR = CURRENT_DIR.parent

db = SQLDatabase.from_uri(f"sqlite:///{BASE_DIR}/resources/Chinook.db")

@tool
def query_playlist_db(query: str) -> str:
    """
        Query the database for playlist information
    """
    try:
        return db.run(query)
    except Exception as e:
        return f"Error querying database: {e}"

async def get_playlist_agent():
    playlist_agent = create_agent(
        model="openai:qwen3.5-flash",
        tools=[query_playlist_db],
        middleware=[model_fallback_middleware],
        system_prompt="""
        你是播放列表专家. 查询sql数据库并为给定类型的婚礼策划完美的播放列表.
        一旦你有了你的播放列表, 计算播放列表的总时长和成本, 每首歌都有一个相关的价格.
        如果在查询数据库时遇到错误, 请尝试通过更改查询来修复它们.
        不要空手而归, 继续查询数据库, 直到你找到一个歌曲列表.
        你可能需要进行多个查询以迭代地找到最佳选项.
        """
    )

    return playlist_agent