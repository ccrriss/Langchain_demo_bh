import time
from langchain_cook_assistant.tools.tavily_search import search_tavily

start = time.perf_counter()

result = search_tavily.invoke({
    "query": "西红柿炒鸡蛋的做法"
})

print("Elapsed:", round(time.perf_counter() - start, 2))
print("Result type:", type(result))
print("Result has error:", isinstance(result, dict) and "error" in result)