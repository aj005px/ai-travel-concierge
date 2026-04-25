from langchain_core.tools import tool
from langchain_community.utilities import GoogleSerperAPIWrapper

@tool("search_hotels", return_direct=False)
def search_hotels(city: str) -> str:
    """Search for best hotels in a city. Input should be a city name string."""
    try:
        search = GoogleSerperAPIWrapper()
        result = search.run(f"best hotels in {city} with prices and ratings")
        return f"🏨 Hotels in {city}:\n\n{result}"
    except Exception as e:
        return f"Hotel search error: {str(e)}"
