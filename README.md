# ✈️ AI Travel Concierge

A simple AI-powered travel assistant built with **Streamlit**, **Groq (LLM)**, and **LangChain RAG**.
It answers travel-related questions using both general knowledge and a custom document-based knowledge base.

---

## 🚀 Features

* 🌍 Ask travel questions (destinations, visas, food, tips)
* 📄 Retrieval-Augmented Generation (RAG) from your own documents
* ⚡ Fast responses using Groq LLM (LLaMA 3)
* 🧠 Local vector database using FAISS
* 💬 Chat interface with memory

---

## 📁 Project Structure

```
.
├── app.py                # Main Streamlit app
├── rag/
│   ├── ingest.py        # Script to ingest documents
│   └── retriever.py     # Loads vector database
├── docs/                # Add your .txt files here
├── vectorstore/         # Auto-generated embeddings
└── README.md
```

---

## 🛠️ Setup Instructions

### 1. Clone the repository

```
git clone <your-repo-url>
cd <repo-folder>
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Add API Key

Create a `.streamlit/secrets.toml` file:

```
GROQ_API_KEY = "your_api_key_here"
```

---

## 📄 Add Knowledge Base

1. Add `.txt` files to the `docs/` folder
2. Run the ingestion script:

```
python rag/ingest.py
```

This will:

* Load documents
* Split into chunks
* Generate embeddings
* Store them in `vectorstore/`

---

## ▶️ Run the App

```
streamlit run app.py
```

Then open the local URL shown in your terminal.

---

## 💡 Example Questions

* Best places to visit in Japan?
* What currency is used in Thailand?
* Best time to visit Paris?
* Visa requirements for Dubai?
* Top foods to try in Italy?

---

## 🧹 Reset Chat

Use the **"Clear Chat"** button in the sidebar to restart the conversation.

---

## ⚠️ Notes

* Make sure `vectorstore/` exists before running the app
* If no documents are loaded, the app will still work using general knowledge
* First-time embedding may take a minute

---

## 📌 Tech Stack

* Streamlit
* Groq API (LLaMA 3)
* LangChain
* FAISS
* HuggingFace Embeddings

---

## 📜 License

This project is open-source and free to use.
