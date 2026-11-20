import time
from langchain_cook_assistant.tools.tavily_search import search_tavily
from langchain_tavily import TavilySearch

search = TavilySearch(
    max_results=3,
    topic="general",
    include_images=True
)

# result = search_tavily.invoke({
#     "query": "酸辣土豆丝 成品图片"
# })

# print("Result type:", type(result))
# print("Images:", result.get("images", []))

from langchain_cook_assistant.tools.tavily_search import (
    search_tool,
    search_tavily
)

print("Original Tavily:", search_tool.args.keys())
print("Wrapped Tool:", search_tavily.args.keys())