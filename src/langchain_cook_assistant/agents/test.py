from dotenv import load_dotenv
load_dotenv()

from langchain.agents import create_agent
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
import os
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer
from langchain_cook_assistant.prompts.system_prompt import system_prompt
from langchain_cook_assistant.schemas.cooking_answer import CookAnswer
from langchain_cook_assistant.middlewares.summarization import summarize_midware
from langchain.messages import HumanMessage
import asyncio


PGSAVER_URI = os.getenv("DOCKER_SAVER_DB")

serde = JsonPlusSerializer(
    allowed_msgpack_modules=[
        ("langchain_cook_assistant.schemas.cooking_answer", "CookAnswer")
    ]
)

async def main():
    async with AsyncPostgresSaver.from_conn_string(PGSAVER_URI, serde=serde) as checkpoint:
        # 1. initialize the checkpoint
        await checkpoint.setup()
        # 2. create the agent
        agent = create_agent(
                "openai:qwen3.6-plus",
                system_prompt=system_prompt,
                # response_format=CookAnswer,
                checkpointer=checkpoint,
                middleware=[summarize_midware],
            )

        response = await agent.astream_events(
            {"messages": [HumanMessage(content="今天哈尔滨天气如何?")]},
            config={
                "configurable": {"thread_id": "1"}
            },
            version="v3"
        )

        # count = 0
        # async for snapshot in response.values:
        #     count += 1
        #     messages = snapshot.get("messages", [])

        #     print("Snapshot:", count)
        #     print("Keys:", snapshot.keys())
        #     print("Message count:", len(messages))
        #     print("Last message type:", type(messages[-1]).__name__ if messages else None)
        #     print("Structured response:", snapshot.get("structured_response"))
        #     print("-" * 40)

        async for message in response.messages:
            print("Node:", message.node)

            async for delta in message.text:
                print(delta, end="", flush=True)

            final_message = await message.output

            print("\nFinal type:", type(final_message))
            print("Final text:", final_message.text())
            print("Tool calls:", final_message.tool_calls)

if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main=main())