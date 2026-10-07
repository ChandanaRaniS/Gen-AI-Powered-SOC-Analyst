import os
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# Base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ChromaDB path
CHROMA_PATH = os.path.join(BASE_DIR, "chromadb")

# Load embedding model
embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load ChromaDB
vectordb = Chroma(
    persist_directory=CHROMA_PATH,
    embedding_function=embedding,
    collection_name="soc_rag"
)

print("=" * 60)
print("✅ ChromaDB Loaded Successfully!")
print("=" * 60)

while True:

    query = input("\nEnter SOC Query (type 'exit' to quit): ")

    if query.lower() == "exit":
        break

    docs = vectordb.similarity_search(query, k=5)

    print("\n================ RETRIEVED RESULTS ================\n")

    for i, doc in enumerate(docs, start=1):
        print(f"Result {i}")
        print("-" * 60)
        print(doc.page_content[:1200])
        print("\n")