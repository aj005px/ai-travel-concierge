# ✈️ AI Travel Concierge

An AI-powered travel assistant built with **Streamlit**, **Groq (LLaMA 3)**, **LangChain**, and real-time tools for web search, weather, and hotels.

---

## 🚀 Features

* 🌍 Ask travel questions (destinations, visas, food, tips)
* 🔍 Real-time web search using Serper API
* 🌤️ Live weather and 3-day forecast (Open-Meteo, no API key needed)
* 🏨 Hotel search for any destination
* 🗺️ AI-powered itinerary generation
* 💾 SQLite database for saving searches and itineraries
* 📄 RAG from a world travel knowledge base (FAISS + HuggingFace)
* ⚡ Fast responses using Groq LLM (LLaMA 3.3 70B)
* 💬 Chat interface with memory

---

## 📁 Project Structure

```
ai-travel-concierge/
├── app.py                  # Main Streamlit app
├── agents/
│   └── travel_agent.py     # LangChain agent with tool routing
├── tools/
│   ├── weather_tool.py     # Open-Meteo weather tool
│   ├── search_tool.py      # Serper web search tool
│   ├── hotels_tool.py      # Hotel search tool
│   └── test_tools.py       # Tool testing script
├── rag/
│   ├── ingest.py           # Script to ingest documents
│   └── retriever.py        # Loads FAISS vector database
├── database/
│   └── db.py               # SQLite database for searches & itineraries
├── docs/
│   └── world_travel.txt    # World travel knowledge base
├── vectorstore/            # Auto-generated embeddings
├── .streamlit/
│   └── secrets.toml        # API keys (never push this!)
├── .env                    # Local API keys (never push this!)
└── README.md
```

---

## 🛠️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/aj005px/ai-travel-concierge.git
cd ai-travel-concierge
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add API Keys

Create a `.env` file for local development:
```
GROQ_API_KEY=your_groq_key_here
SERPER_API_KEY=your_serper_key_here
```

For Streamlit Cloud, create `.streamlit/secrets.toml`:
```
GROQ_API_KEY = "your_groq_key_here"
SERPER_API_KEY = "your_serper_key_here"
```

Get your free API keys:
- **Groq** → console.groq.com
- **Serper** → serper.dev

---

## 📄 Set Up Knowledge Base

1. Add `.txt` files to the `docs/` folder (world_travel.txt already included)
2. Run the ingestion script:
```bash
python rag/ingest.py
```

This will:
* Load documents from `docs/`
* Split into chunks
* Generate embeddings
* Store them in `vectorstore/`

---

## 🧪 Test Tools

```bash
python tools/test_tools.py
```

---

## ▶️ Run the App

```bash
streamlit run app.py
```

Then open the local URL shown in your terminal.

---

## 💡 Example Questions

* 🌤️ What's the weather in Tokyo?
* 🏨 Best hotels in Bali?
* 🗺️ Plan a 5 day trip to Paris
* 🛂 Visa requirements for Dubai?
* 🍜 Top foods to try in Italy?
* ✈️ Best time to visit Japan?
* 💰 Budget travel tips for Thailand?

---

## 🧹 Reset Chat

Use the **"Clear Chat"** button in the sidebar to restart the conversation.

---

## ⚠️ Notes

* Make sure to run `python rag/ingest.py` before running the app
* If no documents are loaded, the app will still work using general knowledge and web search
* First-time embedding generation may take a minute
* Never push `.env` or `secrets.toml` to GitHub

---

## 📌 Tech Stack

| Tool | Purpose |
|---|---|
| Streamlit | Frontend chat interface |
| Groq API (LLaMA 3.3 70B) | LLM for responses |
| LangChain | Agent and tool orchestration |
| Serper API | Real-time web search |
| Open-Meteo API | Live weather data (free, no key needed) |
| FAISS | Local vector database |
| HuggingFace Embeddings | Document embeddings |
| SQLite | Saving searches and itineraries |

---

## 📜 License

This project is open-source and free to use.
