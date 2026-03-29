from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

def ingest_docs():
    print("📄 Loading files from docs/ folder...")

    loader = DirectoryLoader("docs/", glob="**/*.txt", loader_cls=TextLoader)
    documents = loader.load()

    if not documents:
        print("❌ No files found in docs/ folder!")
        return None

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = text_splitter.split_documents(documents)
    print(f"✅ Split into {len(chunks)} chunks")

    print("🔄 Creating embeddings (first time may take a minute)...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local("vectorstore/")
    print(f"✅ Done! {len(documents)} docs, {len(chunks)} chunks ingested")

    return vectorstore

if __name__ == "__main__":
    ingest_docs()
