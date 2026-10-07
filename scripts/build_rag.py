import os
import shutil

from load_data import load_documents

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

print("="*60)
print("Loading Documents...")
print("="*60)

docs = load_documents()

print("\nSplitting Documents...")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1200,
    chunk_overlap=150,
    separators=["\n\n", "\n", ". ", " ", ""]
)

chunks = text_splitter.split_documents(docs)

print(f"Total Chunks: {len(chunks)}")

print("\nLoading Embedding Model...")

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

DB_PATH = "chromadb"

# Delete previous DB
if os.path.exists(DB_PATH):
    shutil.rmtree(DB_PATH)

print("\nCreating ChromaDB...")

vectordb = Chroma.from_documents(
    documents=chunks,
    embedding=embedding,
    persist_directory=DB_PATH,
    collection_name="soc_rag"
)

print("\n========================================")
print(" ChromaDB Created Successfully!")
print("========================================")
print(f"Saved at : {DB_PATH}")
print(f"Chunks   : {len(chunks)}")