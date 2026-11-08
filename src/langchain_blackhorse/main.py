from dotenv import load_dotenv
from langchain.agents import create_agent

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from pydantic import BaseModel, Field
from typing import Annotated

# database with short-term memory
from langgraph.checkpoint.postgres import PostgresSaver
import os
# tools
from tools.searchTool import search_tavily
# schemas
from schemas.answerInfo import AnswerInfo
from schemas.cookingAns import CookAnswer
from schemas.chat import ChatAnswer
# summarize middleware
from middlewares.summarize_middleware import summarize_midware
# config
from configs.thread_one_config import chat_config
from configs.cooking_config import cooking_cfg
# register the return type
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer

serde = JsonPlusSerializer(
    allowed_msgpack_modules=[
        ("schemas.chat", "ChatAnswer"), ("schemas.cookingAns", "CookAnswer")
    ]
)

load_dotenv()

# docker pg uri
PGSAVER_URI = os.getenv("DOCKER_SAVER_DB")
print(PGSAVER_URI)

with PostgresSaver.from_conn_string(PGSAVER_URI) as checkpoint:
    checkpoint.serde = serde
    checkpoint.setup()
    
    agent = create_agent(
        "openai:qwen3.6-plus",
        tools=[search_tavily],
        system_prompt="以厨房助手的口吻回答问题",
        response_format=CookAnswer,
        checkpointer=checkpoint,
        middleware=[summarize_midware],
    )

    response = agent.invoke(
        {"messages": [HumanMessage(
            content=[
                {"type": "text", "text": "你好我是小贾, 请告诉我图片中的菜如何做?"},
                {"type": "image", "url": "https://aisearch.cdn.bcebos.com/pic_create/2026-04-10/10/74d52055e4947f8c.jpg"}
            ]),
        ],},
        config=cooking_cfg
    )
    
    for message in response['messages']:
        message.pretty_print()