from fastapi import APIRouter
from fastapi import Request
from langchain_cook_assistant.schemas.chat import ChatRequest
from fastapi.responses import StreamingResponse
from langchain_cook_assistant.agents.cook_assistant_agent import search_recipes, get_messages, clear_messages
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

router = APIRouter(prefix="/api", tags=["chat"])

@router.post(path="")
async def send_chat_messages(payload: ChatRequest, request: Request, checkpointer: AsyncPostgresSaver):
    agent = request.app.state.agent
    query = payload.query
    thread_id = payload.thread_id

    return StreamingResponse(
        search_recipes(prompt=query, agent=agent, thread_id=thread_id),
        media_type="text/event-stream"
    )
    
@router.delete(path="")
async def delete_chat_messages(payload: ChatRequest, request: Request):
    thread_id = payload.thread_id
    checkpointer = request.app.state.checkpointer

    await clear_messages(thread_id=thread_id, checkpointer=checkpointer)
    
@router.get(path="")
async def get_chat_messages(payload: ChatRequest, request: Request):
    thread_id = payload.thread_id
    checkpointer = request.app.state.checkpointer

    messages = await get_messages(thread_id=thread_id, checkpointer=checkpointer)
    return messages
    