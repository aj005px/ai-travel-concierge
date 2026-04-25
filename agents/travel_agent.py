import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from tools.weather_tool import get_weather
from tools.search_tool import web_search

def create_travel_agent():
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.7
    )
    return llm, [web_search, get_weather]

def run_agent(llm, tools, user_input, chat_history=[]):
    tool_results = ""

    # Detect weather intent
    weather_keywords = ["weather", "temperature", "forecast", "climate", "hot", "cold", "rain", "humid"]
    needs_weather = any(w in user_input.lower() for w in weather_keywords)

    # Detect search intent
    search_keywords = ["hotel", "hotels", "cheap", "best", "visa", "flight", "food", "places", "visit", "trip", "plan", "restaurant", "budget", "cost", "ticket", "resort", "stay", "book"]
    needs_search = any(w in user_input.lower() for w in search_keywords)

    # If neither detected, default to search
    if not needs_weather and not needs_search:
        needs_search = True

    # Call weather tool
    if needs_weather:
        # Extract city name using LLM
        city_response = llm.invoke([
            SystemMessage(content="Extract only the city name from the user message. Reply with just the city name, nothing else."),
            HumanMessage(content=user_input)
        ])
        city = city_response.content.strip()
        print(f"🌤️ Getting weather for: {city}")
        weather_result = get_weather.invoke({"city": city})
        tool_results += f"\nWEATHER DATA:\n{weather_result}\n"

    # Call search tool
    if needs_search:
        print(f"🔍 Searching for: {user_input}")
        search_result = web_search.invoke({"query": user_input})
        tool_results += f"\nSEARCH RESULTS:\n{search_result}\n"

    # Build final prompt
    messages = [
        SystemMessage(content="""You are an expert AI travel concierge.
Use the tool results provided to give accurate, helpful travel advice.
Be friendly, specific and detailed in your response.""")
    ]

    for msg in chat_history:
        messages.append(msg)

    if tool_results:
        messages.append(HumanMessage(content=f"""User asked: {user_input}

Here are the real-time results from our tools:
{tool_results}

Please provide a helpful, friendly response based on this data."""))
    else:
        messages.append(HumanMessage(content=user_input))

    response = llm.invoke(messages)
    return response.content
