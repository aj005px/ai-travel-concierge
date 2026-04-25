import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from tools.weather_tool import get_weather
from tools.search_tool import web_search
from tools.hotels_tool import search_hotels

def create_travel_agent():
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.7
    )
    return llm, [web_search, get_weather, search_hotels]

def generate_itinerary(llm, destination: str, days: int, preferences: str = "") -> str:
    """Generate a detailed travel itinerary."""
    prompt = f"""Create a detailed {days}-day travel itinerary for {destination}.
{f'User preferences: {preferences}' if preferences else ''}

Format the itinerary as:
Day 1: [Title]
- Morning: ...
- Afternoon: ...
- Evening: ...
- Food: ...

Day 2: [Title]
...and so on for all {days} days.

Include specific places, restaurants, tips and estimated costs."""

    response = llm.invoke([
        SystemMessage(content="You are an expert travel planner. Create detailed, practical itineraries."),
        HumanMessage(content=prompt)
    ])
    return response.content

def run_agent(llm, tools, user_input, chat_history=[]):
    tool_results = ""

    # Detect weather intent
    weather_keywords = ["weather", "temperature", "forecast", "climate", "hot", "cold", "rain", "humid"]
    needs_weather = any(w in user_input.lower() for w in weather_keywords)

    # Detect hotel intent
    hotel_keywords = ["hotel", "hotels", "stay", "resort", "accommodation", "lodge", "where to stay"]
    needs_hotels = any(w in user_input.lower() for w in hotel_keywords)

    # Detect itinerary intent
    itinerary_keywords = ["itinerary", "plan", "trip plan", "day plan", "schedule", "days in"]
    needs_itinerary = any(w in user_input.lower() for w in itinerary_keywords)

    # Detect search intent
    search_keywords = ["best", "visa", "flight", "food", "places", "visit", "restaurant", "budget", "cost", "ticket", "cheap", "recommend"]
    needs_search = any(w in user_input.lower() for w in search_keywords)

    if not any([needs_weather, needs_hotels, needs_itinerary, needs_search]):
        needs_search = True

    # Extract city using LLM
    city_response = llm.invoke([
        SystemMessage(content="Extract only the main city or destination name from the user message. Reply with just the city/destination name, nothing else."),
        HumanMessage(content=user_input)
    ])
    city = city_response.content.strip()

    # Call weather tool
    if needs_weather:
        print(f"🌤️ Getting weather for: {city}")
        weather_result = get_weather.invoke({"city": city})
        tool_results += f"\nWEATHER DATA:\n{weather_result}\n"

    # Call hotels tool
    if needs_hotels:
        print(f"🏨 Searching hotels in: {city}")
        hotel_result = search_hotels.invoke({"city": city})
        tool_results += f"\nHOTEL DATA:\n{hotel_result}\n"

    # Call search tool
    if needs_search and not needs_hotels:
        print(f"🔍 Searching for: {user_input}")
        search_result = web_search.invoke({"query": user_input})
        tool_results += f"\nSEARCH RESULTS:\n{search_result}\n"

    # Generate itinerary
    if needs_itinerary:
        import re
        days_match = re.search(r'(\d+)\s*day', user_input.lower())
        days = int(days_match.group(1)) if days_match else 3
        print(f"🗺️ Generating {days}-day itinerary for: {city}")
        itinerary = generate_itinerary(llm, city, days)
        tool_results += f"\nITINERARY:\n{itinerary}\n"

        # Save to database
        from database.db import save_itinerary
        save_itinerary(city, days, itinerary)

    # Build final response
    messages = [
        SystemMessage(content="""You are an expert AI travel concierge.
Use the tool results provided to give accurate, helpful travel advice.
Be friendly, specific and detailed in your response.""")
    ]

    for msg in chat_history:
        messages.append(msg)

    if tool_results:
        messages.append(HumanMessage(content=f"""User asked: {user_input}

Real-time results from our tools:
{tool_results}

Please provide a helpful, friendly response based on this data."""))
    else:
        messages.append(HumanMessage(content=user_input))

    response = llm.invoke(messages)
    return response.content
