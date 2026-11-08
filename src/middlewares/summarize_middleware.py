from langchain.agents.middleware import SummarizationMiddleware

summarize_midware = SummarizationMiddleware(
                            model="openai:qwen3.6-27b",
                            trigger=("tokens", 4000),
                            keep=("messages", 20),
                        )
