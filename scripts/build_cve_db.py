import os
import json
import shutil

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

print("=" * 60)
print("Building Structured CVE Database")
print("=" * 60)

# =====================================================
# Load NVD CVE JSON
# =====================================================

with open("data/cve.json", "r", encoding="utf-8") as f:
    cve_json = json.load(f)

print(f"\nTotal CVEs in Dataset : {len(cve_json['vulnerabilities'])}")

docs = []

# =====================================================
# Process CVEs
# =====================================================

for item in cve_json["vulnerabilities"]:

    cve = item.get("cve", {})

    # ---------------------------------------------
    # Skip rejected CVEs
    # ---------------------------------------------
    if cve.get("vulnStatus", "").lower() == "rejected":
        continue

    # ---------------------------------------------
    # CVE ID
    # ---------------------------------------------
    cve_id = cve.get("id", "Unknown")

    # ---------------------------------------------
    # English Description
    # ---------------------------------------------
    description = "Not Available"

    for desc in cve.get("descriptions", []):
        if desc.get("lang") == "en":
            description = desc.get("value", "").strip()
            break

    # ---------------------------------------------
    # Create Structured Document
    # ---------------------------------------------
    page_content = f"""
CVE ID: {cve_id}

Description:
{description}
"""

    metadata = {
        "source": "CVE",
        "cve_id": cve_id
    }

    docs.append(
        Document(
            page_content=page_content.strip(),
            metadata=metadata
        )
    )

print(f"\nValid CVEs Indexed : {len(docs)}")

# =====================================================
# Load Embedding Model
# =====================================================

print("\nLoading Embedding Model...")

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# =====================================================
# Delete Existing Database
# =====================================================

DB_PATH = "cve_db"

if os.path.exists(DB_PATH):
    shutil.rmtree(DB_PATH)

# =====================================================
# Create Chroma Database
# =====================================================

print("\nCreating CVE Vector Database...")

vectordb = Chroma.from_documents(
    documents=docs,
    embedding=embedding,
    persist_directory=DB_PATH,
    collection_name="cve"
)

print("\n==========================================")
print("Structured CVE Database Created Successfully!")
print("==========================================")
print(f"Total Documents : {len(docs)}")
print(f"Database Path   : {DB_PATH}")