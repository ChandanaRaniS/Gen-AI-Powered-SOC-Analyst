import os
import re
import json
import shutil

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

print("=" * 60)
print("Building Structured NIST Database")
print("=" * 60)

JSON_PATH = "data/NIST_SP-800-53_rev5_catalog-min.json"

with open(JSON_PATH, "r", encoding="utf-8") as f:
    catalog = json.load(f)

groups = catalog["catalog"]["groups"]

print(f"\nControl Families Found : {len(groups)}")

# ==========================================================
# Helper Functions
# ==========================================================

def clean_text(text):
    """
    Remove OSCAL placeholders and extra spaces.
    """

    if not text:
        return ""

    text = re.sub(r"\{\{.*?\}\}", "", text)
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def extract_statement(part):
    """
    Recursively extract ONLY the control statement.
    """

    collected = []

    prose = part.get("prose")

    if prose:

        cleaned = clean_text(prose)

        if cleaned:
            collected.append(cleaned)

    for child in part.get("parts", []):

        collected.extend(
            extract_statement(child)
        )

    return collected


# ==========================================================
# Create Documents
# ==========================================================

documents = []

total_controls = 0
# ==========================================================
# Traverse NIST Families
# ==========================================================

for family in groups:

    family_name = family.get("title", "Unknown Family")

    controls = family.get("controls", [])

    print(f"Processing {family_name} ({len(controls)} controls)")

    for control in controls:

        control_id = control.get("id", "").upper()

        # --------------------------------------------------
        # Skip Control Enhancements
        # Example:
        # AC-2(1)
        # IA-2(12)
        # --------------------------------------------------

        if "(" in control_id:
            continue

        control_name = control.get("title", "").strip()

        statement = ""

        # --------------------------------------------------
        # Search only the "statement" section
        # --------------------------------------------------

        for part in control.get("parts", []):

            if part.get("name") == "statement":

                lines = extract_statement(part)

                statement = "\n".join(lines)

                break

        # Skip empty controls

        if statement.strip() == "":
            continue

        # --------------------------------------------------
        # Build RAG Document
        # --------------------------------------------------

        page_content = f"""
Control ID: {control_id}

Control Name: {control_name}

Control Family: {family_name}

Description:
{statement}
""".strip()

        metadata = {
            "source": "NIST",
            "control_id": control_id,
            "control_name": control_name,
            "family": family_name,
        }

        documents.append(
            Document(
                page_content=page_content,
                metadata=metadata,
            )
        )

        total_controls += 1


print("\n==========================================")
print(f"Structured Controls Indexed : {total_controls}")
print("==========================================")
# ==========================================================
# Load Embedding Model
# ==========================================================

print("\nLoading Embedding Model...")

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# ==========================================================
# Delete Existing Database
# ==========================================================

DB_PATH = "nist_db"

if os.path.exists(DB_PATH):
    print("\nRemoving old NIST database...")
    shutil.rmtree(DB_PATH)

# ==========================================================
# Create Chroma Database
# ==========================================================

print("\nCreating NIST Vector Database...")

vectordb = Chroma.from_documents(
    documents=documents,
    embedding=embedding,
    persist_directory=DB_PATH,
    collection_name="nist"
)

print("\n==========================================")
print("Structured NIST Database Created Successfully!")
print("==========================================")

print(f"Total Controls Indexed : {len(documents)}")

# ==========================================================
# Display Sample Controls
# ==========================================================

print("\n================ SAMPLE CONTROLS ================\n")

for i, doc in enumerate(documents[:3], start=1):

    print(f"----- Control {i} -----\n")
    print(doc.page_content)
    print("\n" + "-" * 70 + "\n")

print(f"Database saved at : {DB_PATH}")

print("\nDone.")