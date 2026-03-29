import streamlit as st
from groq import Groq
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from rag.retriever import load_retriever


client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.set_page_config(page_title="AI Travel Concierge", page_icon="✈️", layout="wide")

@st.cache_resource
def get_retriever():
    try:
        return load_retriever()
    except Exception as e:
        return None

retriever = get_retriever()

# Sidebar
with st.sidebar:
    st.title("✈️ AI Travel Concierge")
    st.markdown("---")

    if retriever:
        st.success("✅ World travel knowledge base loaded!")
    else:
        st.error("❌ No knowledge base found")
        st.info("Add PDFs to docs/ folder and run:\npython rag/ingest.py")

    st.markdown("---")
    st.markdown("### 💡 Try asking:")
    st.markdown("- Best places to visit in Japan?")
    st.markdown("- What currency is used in Thailand?")
    st.markdown("- Best time to visit Paris?")
    st.markdown("- Visa requirements for Dubai?")
    st.markdown("- Top foods to try in Italy?")
    st.markdown("---")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Main
st.title("✈️ AI Travel Concierge")
st.write("Ask me anything about travel — powered by a real world travel guide!")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": """You are an expert AI travel concierge with knowledge of
destinations all around the world. Help users plan trips, suggest destinations,
explain visa requirements, recommend hotels and food, and give travel tips.
Always be friendly, helpful and specific in your answers.
When given context from travel documents, use it to give accurate answers.
If the context doesnt cover something, use your own knowledge."""
        }
    ]

# Display chat history
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input
user_input = st.chat_input("E.g. What are the must see places in Tokyo?")

if user_input:
    context = ""
    if retriever:
        with st.spinner("🔍 Searching world travel guide..."):
            docs = retriever.invoke(user_input)
            if docs:
                context = "\n\n".join([doc.page_content for doc in docs])

    if context:
        prompt = f"""Use the following travel guide information to answer the question.
If the information is not in the context, use your own travel knowledge.

TRAVEL GUIDE CONTEXT:
{context}

USER QUESTION: {user_input}"""
    else:
        prompt = user_input

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages,
                max_tokens=1024,
            )
            reply = response.choices[0].message.content
            st.write(reply)
            st.session_state.messages.append({
                "role": "assistant",
                "content": reply
            })
