from langgraph.runtime import Runtime
from langchain.agents.middleware import after_model, wrap_model_call, ModelRequest, ModelResponse, AgentMiddleware, before_model, hook_config
from langchain.agents.middleware.types import ModelCallResult, ToolCallRequest
from typing import Callable, Any
from langchain.messages import AIMessage, ToolMessage
from langgraph.types import Command

# define the wrap model middleware
@wrap_model_call
def retry_model(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse]
) -> ModelResponse:
    for attempt in range(3):
        try:
            return handler(request)
        except Exception as e:
            print(f"Retry {attempt + 1}/3 after error: {e}")
            if attempt == 2:
                raise

    return None

# 高级用法, 动态修改请求
@wrap_model_call
def dynamic_model_settings(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse]
) -> ModelResponse:
    # get thinking from context
    thinking = request.runtime.context.thinking
    # if thinking is true enable model thinking mode
    thinking_type = "enabled" if thinking else "disabled"

    model_settings = {"extra_body": {"thinking": {"type": thinking_type}}}

    modified_request = request.override(model_settings=model_settings)
    return handler(modified_request)

class LoggingMiddleware(AgentMiddleware):
    def wrap_model_call(
            self, 
            request: ModelRequest, 
            handler: Callable[[ModelRequest], ModelResponse]
    ) -> ModelCallResult:
        try: 
            print(f"\n=======About to call model with {len(request.messages)} messages=======")
            return handler(request)
        except Exception as e:
            print(f"\n=======[错误]: {str(e)}=======")
            return AIMessage("调用模型失败，请重试~")

    def wrap_tool_call(
            self, 
            request: ToolCallRequest, 
            handler: Callable[[ToolCallRequest], ToolMessage | Command]
    ) -> ToolMessage | Command:
        print(f"\n=======调用工具: {request.tool_call['name']}=======")
        print(f"\n=======参数: {request.tool_call['args']}=======")
        try: 
            result = handler(request)
            print("\n=======工具调用成功！=======")
            return result
        except Exception as e:
            print(f"\n=======工具调用失败: {e}=======")
            raise
