import json
import os

from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# ===============================
# Load Embedding Model
# ===============================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_PATH = os.path.join(BASE_DIR, "chromadb")

embedding = HuggingFaceEmbeddings(import json
import os

from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# ===============================
# Load Embedding Model
# ===============================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_PATH = os.path.join(BASE_DIR, "chromadb")

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectordb = Chroma(
    persist_directory=DB_PATH,
    embedding_function=embedding,
    collection_name="soc_rag"
)

print("=" * 60)
print("ChromaDB Loaded Successfully!")
print("=" * 60)

# ===============================
# Load Healthcare Alerts
# ===============================

alerts = []

with open(os.path.join(BASE_DIR, "data", "healthcare_alerts.json"), "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line:
            alerts.append(json.loads(line))

print(f"Loaded {len(alerts)} alerts")

# ===============================
# Select First Alert
# ===============================

alert = alerts[0]["data"]

print("\nALERT\n")
print(alert)

# ===============================
# Build Query
# ===============================

# ===============================
# Build Better Query
# ===============================

attack = alert["attack_type"].replace("_", " ")

query = f"""
Healthcare Cyber Attack

Attack Type: {attack}

System: {alert["system"]}

Severity: {alert["severity"]}

Port: {alert["destination_port"]}

MITRE ATT&CK technique
NIST Cybersecurity Framework
CVE vulnerability
"""

print("\nGenerated Query:")
print(query)

print("\nSearching RAG...\n")

docs = vectordb.similarity_search_with_score(query, k=5)
print("=" * 60)
print("RETRIEVED DOCUMENTS")
print("=" * 60)

for i, (doc, score) in enumerate(docs, start=1):

    print(f"\nResult {i}")
    print(f"Similarity Score : {score:.4f}")
    print("-" * 60)

    print(doc.page_content[:1500])
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectordb = Chroma(
    persist_directory=DB_PATH,
    embedding_function=embedding,
    collection_name="soc_rag"
)

print("=" * 60)
print("ChromaDB Loaded Successfully!")
print("=" * 60)

# ===============================
# Load Healthcare Alerts
# ===============================

alerts = []

with open(os.path.join(BASE_DIR, "data", "healthcare_alerts.json"), "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line:
            alerts.append(json.loads(line))

print(f"Loaded {len(alerts)} alerts")

# ===============================
# Select First Alert
# ===============================

alert = alerts[0]["data"]

print("\nALERT\n")
print(alert)

# ===============================
# Build Query
# ===============================

# ===============================
# Build Better Query
# ===============================

attack = alert["attack_type"].replace("_", " ")

query = f"""
Healthcare Cyber Attack

Attack Type: {attack}

System: {alert["system"]}

Severity: {alert["severity"]}

Port: {alert["destination_port"]}

MITRE ATT&CK technique
NIST Cybersecurity Framework
CVE vulnerability
"""

print("\nGenerated Query:")
print(query)

print("\nSearching RAG...\n")

docs = vectordb.similarity_search_with_score(query, k=5)
print("=" * 60)
print("RETRIEVED DOCUMENTS")
print("=" * 60)

for i, (doc, score) in enumerate(docs, start=1):

    print(f"\nResult {i}")
    print(f"Similarity Score : {score:.4f}")
    print("-" * 60)

    print(doc.page_content[:1500])