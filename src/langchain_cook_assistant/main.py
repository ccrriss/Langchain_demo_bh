from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
# database with short-term memory
from langgraph.checkpoint.postgres import PostgresSaver
import os
# tools
from langchain_cook_assistant.tools.tavily_search import search_tavily
# schemas
from langchain_cook_assistant.schemas.cooking_answer import CookAnswer
# summarize middleware
from langchain_cook_assistant.middlewares.summarization import summarize_midware
# config
from langchain_cook_assistant.configs.cooking_config import cooking_cfg
# register the return type
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer
# prompt
from langchain_cook_assistant.prompts.system_prompt import system_prompt

serde = JsonPlusSerializer(
    allowed_msgpack_modules=[
        ("langchain_cook_assistant.schemas.cooking_answer", "CookAnswer")
    ]
)

load_dotenv()

# docker pg uri
PGSAVER_URI = os.getenv("DOCKER_SAVER_DB")
print(PGSAVER_URI)

with PostgresSaver.from_conn_string(PGSAVER_URI) as checkpoint:
# 1. initialize the checkpoint
    checkpoint.serde = serde
    checkpoint.setup()
# 2. create the agent
    agent = create_agent(
        "openai:qwen3.6-plus",
        tools=[search_tavily],
        system_prompt=system_prompt,
        response_format=CookAnswer,
        checkpointer=checkpoint,
        middleware=[summarize_midware],
    )

    # response = agent.invoke(
    #     {"messages": [HumanMessage(
    #         content=[
    #             {"type": "text", "text": "你好我是小贾, 请告诉我图片中的菜能做什么?"},
    #             {"type": "image", "url": "https://aisearch.cdn.bcebos.com/pic_create/2026-04-10/10/74d52055e4947f8c.jpg"}
    #         ]),
    #     ],},
    #     config=cooking_cfg
    # )

    response = agent.invoke(
        {'messages': [HumanMessage(
            content="我更喜欢第三道菜, 可以说的更详细一点吗?"
        )]},
        config=cooking_cfg        
    )
    
    for message in response['messages']:
        message.pretty_print()