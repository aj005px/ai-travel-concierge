import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from tools.weather_tool import get_weather
from tools.search_tool import web_search

def test_weather():
    print("=== Testing Weather Tool ===")
    result = get_weather.invoke("Tokyo")
    print(result)
    result2 = get_weather.invoke("InvalidCityXYZ")
    print(result2)

def test_search():
    print("=== Testing Search Tool ===")
    result = web_search.invoke("best time to visit Bali Indonesia")
    print(result[:500])

if __name__ == "__main__":
    test_weather()
    test_search()
    print("✅ All tools tested!")
