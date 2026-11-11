from fastapi import APIRouter, Request
from langchain_cook_assistant.schemas.chat import ChatRequest
from fastapi.responses import StreamingResponse
from langchain_cook_assistant.agents.cook_assistant_agent import search_recipes, get_messages, clear_messages
# get the return msg schema
from langchain_cook_assistant.schemas.chat import ChatMessage


router = APIRouter(prefix="/api", tags=["chat"])

@router.post(path="")
async def send_chat_messages(payload: ChatRequest, request: Request):
    agent = request.app.state.agent
    query = payload.query
    thread_id = payload.thread_id

    return StreamingResponse(
        search_recipes(prompt=query, agent=agent, thread_id=thread_id),
        media_type="text/plain"
    )

@router.delete(path="/{thread_id}")
async def delete_chat_messages(thread_id: str, request: Request):
    checkpointer = request.app.state.checkpointer

    await clear_messages(thread_id=thread_id, checkpointer=checkpointer)

@router.get(path="/{thread_id}")
async def get_chat_messages(thread_id: str, request: Request):
    checkpointer = request.app.state.checkpointer

    messages = await get_messages(thread_id=thread_id, checkpointer=checkpointer)
    return messages

    