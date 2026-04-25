from langchain_core.tools import tool
from langchain_community.utilities import GoogleSerperAPIWrapper

@tool("web_search", return_direct=False)
def web_search(query: str) -> str:
    """Search the web for travel info, hotels, visa requirements and destination guides. Input should be a search query string."""
    try:
        search = GoogleSerperAPIWrapper()
        return search.run(query)
    except Exception as e:
        return f"Search error: {str(e)}"

def get_search_tool():
    return web_search
