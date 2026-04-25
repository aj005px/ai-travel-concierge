from langchain_core.tools import tool
from langchain_community.utilities import GoogleSerperAPIWrapper
import os

@tool
def web_search(query: str) -> str:
    """Search the web for travel information, visa requirements, hotels, flights, and destination guides."""
    try:
        search = GoogleSerperAPIWrapper()
        return search.run(query)
    except Exception as e:
        return f"Search error: {str(e)}"

def get_search_tool():
    return web_search
