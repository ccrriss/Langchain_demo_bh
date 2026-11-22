from langchain.agents.middleware import ModelFallbackMiddleware

model_fallback_middleware = ModelFallbackMiddleware(
    "openai:qwen3.5-flash",
    "openai:qwen3.5-plus",
)
