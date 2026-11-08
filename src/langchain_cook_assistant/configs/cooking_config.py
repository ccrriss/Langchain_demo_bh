from langchain_core.runnables import RunnableConfig

cooking_cfg: RunnableConfig = {
    "configurable": {"thread_id": "cooking_thread"}
}
