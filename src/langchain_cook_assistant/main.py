from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Get cross-origin frontend ip
# To avoid that Agent components depending on env variables use only dotenv not pydantic-settings
from dotenv import load_dotenv
import os
import json
# save agent in app.state in lifespan
from contextlib import asynccontextmanager
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langchain_cook_assistant.agents.cook_assistant_agent import serde
from langchain.agents import create_agent
from langchain_cook_assistant.tools.tavily_search import search_tavily
from langchain_cook_assistant.prompts.system_prompt import system_prompt
from langchain_cook_assistant.schemas.cooking_answer import CookAnswer
from langchain_cook_assistant.middlewares.summarization import summarize_midware
from langchain_cook_assistant.api import chat

load_dotenv()

# docker pg uri
PGSAVER_URI = os.getenv("DOCKER_SAVER_DB")

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with AsyncPostgresSaver.from_conn_string(PGSAVER_URI, serde=serde) as checkpoint:
        # 1. initialize the checkpoint
        await checkpoint.setup()
        # 2. create the agent
        agent = create_agent(
                "openai:qwen3.6-plus",
                # tools=[search_tavily],
                system_prompt=system_prompt,
                # response_format=CookAnswer,
                checkpointer=checkpoint,
                middleware=[summarize_midware],
            )

        app.state.agent = agent
        app.state.checkpointer = checkpoint

        yield

app = FastAPI(title="cook assistant", description="AI cook assistant", version="0.1.0", lifespan=lifespan)

BACKEND_CORS_ORIGINS = json.loads(os.getenv("BACKEND_CORS_ORIGINS", '["http://localhost:3000"]'))

app.add_middleware(
    CORSMiddleware,
    allow_origins = BACKEND_CORS_ORIGINS,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

app.include_router(chat.router)