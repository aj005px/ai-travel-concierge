import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from tools.weather_tool import get_weather
from tools.search_tool import web_search

def create_travel_agent():
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.7
    )
    tools = [web_search, get_weather]
    llm_with_tools = llm.bind_tools(tools)
    return llm_with_tools, tools

def run_agent(llm_with_tools, tools, user_input, chat_history=[]):
    tool_map = {t.name: t for t in tools}

    system_prompt = """You are an expert AI travel concierge.
Use tools to answer travel questions accurately.
- Weather questions → call get_weather once
- Hotel/visa/trip questions → call web_search once
- Trip planning → call both tools once each
After getting tool results, give a helpful final answer. Do NOT call tools again after getting results."""

    messages = [SystemMessage(content=system_prompt)]
    for msg in chat_history:
        messages.append(msg)
    messages.append(HumanMessage(content=user_input))

    # Pass 1 — get tool calls
    response = llm_with_tools.invoke(messages)
    messages.append(response)

    # If no tool calls just return
    if not response.tool_calls:
        return response.content

    # Execute tools
    for tool_call in response.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        print(f"🔧 Calling: {tool_name} → {tool_args}")

        try:
            result = tool_map[tool_name].invoke(tool_args) if tool_name in tool_map else "Tool not found"
        except Exception as e:
            result = f"Tool error: {str(e)}"

        messages.append(ToolMessage(
            content=str(result),
            tool_call_id=tool_call["id"]
        ))

    # Pass 2 — final answer using base LLM without tools
    base_llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.7
    )
    final = base_llm.invoke(messages)
    return final.content
