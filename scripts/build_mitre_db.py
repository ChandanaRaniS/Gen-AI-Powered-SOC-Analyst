import os
import json
import shutil

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

print("=" * 60)
print("Building Structured MITRE ATT&CK Database")
print("=" * 60)

# ==========================================================
# Configuration
# ==========================================================

MITRE_JSON = "data/enterprise-attack.json"
DB_PATH = "mitre_db"

# ==========================================================
# Load Official MITRE ATT&CK STIX Bundle
# ==========================================================

print("\nLoading MITRE ATT&CK JSON...")

with open(MITRE_JSON, "r", encoding="utf-8") as f:
    bundle = json.load(f)

objects = bundle["objects"]

print(f"Total STIX Objects : {len(objects)}")

# ==========================================================
# Extract ATT&CK Techniques
# ==========================================================

documents = []

for obj in objects:

    if obj.get("type") != "attack-pattern":
        continue

    # Skip revoked / deprecated techniques
    if obj.get("revoked", False):
        continue

    if obj.get("x_mitre_deprecated", False):
        continue

    # ------------------------------------------------------
    # Technique ID
    # ------------------------------------------------------

    technique_id = "Unknown"

    for ref in obj.get("external_references", []):

        if ref.get("source_name") == "mitre-attack":

            technique_id = ref.get("external_id", "Unknown")
            break

    # ------------------------------------------------------
    # Technique Name
    # ------------------------------------------------------

    technique_name = obj.get("name", "Unknown")

    # ------------------------------------------------------
    # Description
    # ------------------------------------------------------

    description = obj.get("description", "Not Available")

    # Keep only the first paragraph
    description = description.split("\n\n")[0].strip()

    # ------------------------------------------------------
    # Tactics
    # ------------------------------------------------------

    tactics = []

    for phase in obj.get("kill_chain_phases", []):

        if phase.get("kill_chain_name") == "mitre-attack":

            tactics.append(phase.get("phase_name"))

    

    

    

    # ======================================================
    # Structured Text for Embedding
    # ======================================================

    page_content = f"""
Technique ID: {technique_id}

Technique Name: {technique_name}

Tactics:
{", ".join(tactics) if tactics else "Not Available"}

Description:
{description}


"""

    # ======================================================
    # Metadata
    # ======================================================

    metadata = {
        "source": "MITRE",
        "technique_id": technique_id,
        "technique_name": technique_name,
        "tactics": ", ".join(tactics),
        "stix_id": obj.get("id")
    }

    documents.append(
        Document(
            page_content=page_content.strip(),
            metadata=metadata
        )
    )

print(f"\nStructured Techniques : {len(documents)}")

# ==========================================================
# Embedding Model
# ==========================================================

print("\nLoading Embedding Model...")

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# ==========================================================
# Remove Existing Database
# ==========================================================

if os.path.exists(DB_PATH):
    shutil.rmtree(DB_PATH)

# ==========================================================
# Build ChromaDB
# ==========================================================

print("\nCreating Chroma Database...")

vectordb = Chroma.from_documents(
    documents=documents,
    embedding=embedding,
    persist_directory=DB_PATH,
    collection_name="mitre"
)

print("\n==============================================")
print("Structured MITRE Database Created Successfully")
print("==============================================")
print(f"Database Location : {DB_PATH}")
print(f"Techniques Stored : {len(documents)}")