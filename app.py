import streamlit as st
from dotenv import load_dotenv
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from agents.travel_agent import create_travel_agent, run_agent
from rag.retriever import load_retriever
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY", "")
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY") or st.secrets.get("SERPER_API_KEY", "")

st.set_page_config(page_title="AI Travel Concierge", page_icon="✈️", layout="wide")

@st.cache_resource
def get_agent():
    try:
        return create_travel_agent()
    except Exception as e:
        st.error(f"Agent error: {e}")
        return None, []

@st.cache_resource
def get_retriever():
    try:
        return load_retriever()
    except:
        return None

agent, tools = get_agent()
retriever = get_retriever()

# Sidebar
with st.sidebar:
    st.title("✈️ AI Travel Concierge")
    st.markdown("---")
    st.markdown("### 🛠️ Active Tools")
    st.success("🔍 Web Search — ON")
    st.success("🌤️ Weather — ON")
    if retriever:
        st.success("📚 Travel Knowledge Base — ON")
    else:
        st.warning("📚 Knowledge Base — OFF")
    st.markdown("---")
    st.markdown("### 💡 Try asking:")
    st.markdown("- 🌤️ What's the weather in Tokyo?")
    st.markdown("- 🗺️ Plan a 5 day trip to Paris")
    st.markdown("- 🛂 Visa requirements for Dubai?")
    st.markdown("- 🏨 Best hotels in Bali?")
    st.markdown("- ✈️ Best time to visit Japan?")
    st.markdown("---")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.rerun()

# Main
st.title("✈️ AI Travel Concierge")
st.write("Your smart travel assistant with real-time web search and weather! 🌍")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input
user_input = st.chat_input("Ask me anything about travel...")

if user_input:
    full_input = user_input
    if retriever:
        try:
            docs = retriever.invoke(user_input)
            if docs:
                context = "\n\n".join([doc.page_content for doc in docs])
                full_input = f"{user_input}\n\nContext from travel guide:\n{context[:1000]}"
        except:
            pass

    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("🤔 Searching and thinking..."):
            try:
                reply = run_agent(agent, tools, full_input, st.session_state.chat_history)
            except Exception as e:
                reply = f"Sorry, I hit an error: {str(e)}. Please try again!"

            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.session_state.chat_history.extend([
                HumanMessage(content=user_input),
                AIMessage(content=reply)
            ])
