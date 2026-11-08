from langchain.tools import tool
from langchain_tavily import TavilySearch
from dotenv import load_dotenv

load_dotenv()

search_tool = TavilySearch(
    max_results = 5,
    topic="general",
)

@tool
def search_tavily(query:str):
    """
    Search the web for information based on the user's query
    """
    return search_tool.invoke(query)
