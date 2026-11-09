from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer
from langchain.messages import HumanMessage, AIMessage
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
# declare the type of agent
from langgraph.graph.state import CompiledStateGraph
from collections.abc import AsyncIterator


serde = JsonPlusSerializer(
    allowed_msgpack_modules=[
        ("langchain_cook_assistant.schemas.cooking_answer", "CookAnswer")
    ]
)

# agent logic(stream)

async def search_recipes(prompt: str, thread_id: str, agent: CompiledStateGraph) -> AsyncIterator:
    message = HumanMessage(
        content= prompt
    )
    stream = await agent.astream_events(
        {"messages": [message]},
        config={
            "configurable": {"thread_id": thread_id}
        },
        version="v3"
    )

    async for message in stream.messages:
        async for delta in message.text:
                yield delta


async def clear_messages(thread_id: str, checkpointer: AsyncPostgresSaver):
    await checkpointer.adelete_thread(thread_id=thread_id)

async def get_messages(thread_id: str, checkpointer: AsyncPostgresSaver):
    checkpoint = await checkpointer.aget(
        config= {
            "configurable": {"thread_id": thread_id}
        }
    )

    if not checkpoint:
        return []
    
    channel_values = checkpoint.get("channel_values")
    if not channel_values:
        return []
    
    messages = channel_values.get("messages", [])
    if not messages:
        return []

    # convert the format of messages
    AI_messages = []
    for msg in messages:
        if not msg.content:
            continue
        if isinstance(msg, AIMessage):
            AI_messages.append(msg.content)

    return AI_messages