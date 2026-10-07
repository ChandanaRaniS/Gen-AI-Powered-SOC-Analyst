import os
import json

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# ==========================
# Load Databases
# ==========================

mitre_db = Chroma(
    persist_directory=os.path.join(BASE_DIR, "mitre_db"),
    embedding_function=embedding,
    collection_name="mitre"
)

nist_db = Chroma(
    persist_directory=os.path.join(BASE_DIR, "nist_db"),
    embedding_function=embedding,
    collection_name="nist"
)

cve_db = Chroma(
    persist_directory=os.path.join(BASE_DIR, "cve_db"),
    embedding_function=embedding,
    collection_name="cve"
)

print("All Databases Loaded Successfully!\n")

# ==========================
# Load Alert
# ==========================

current_alert = os.path.join(
    BASE_DIR,
    "data",
    "current_alert.json"
)

with open(current_alert, "r", encoding="utf-8") as f:
    alert = json.load(f)


print("ALERT")

print(alert)

# ==========================
# Build Query
# ==========================

attack = alert.get("attack_type")

if attack:
    attack = attack.replace("_", " ")
else:
    attack = alert.get("description", "Unknown Attack")

query = (
    f"{alert.get('description', '')} "
    f"Severity {alert.get('severity', '')} "
    f"{' '.join(alert.get('mitre', []))} "
    f"{' '.join(alert.get('technique', []))} "
    f"{alert.get('full_log', '')}"
)

# ==========================
# Retrieve Top-3 Documents
# ==========================

mitre = mitre_db.similarity_search_with_score(query, k=3)
nist = nist_db.similarity_search_with_score(query, k=3)
cve = cve_db.similarity_search_with_score(query, k=3)
# ==========================================================
# ==========================================================
# Primary Evidence + Distance Scores
# ==========================================================

primary_mitre = mitre[0][0].page_content
primary_mitre_distance = mitre[0][1]

primary_nist = nist[0][0].page_content
primary_nist_distance = nist[0][1]

primary_cve = cve[0][0].page_content
primary_cve_distance = cve[0][1]

# ==========================================================
# Supporting Evidence
# ==========================================================

supporting_mitre = [doc.page_content for doc, score in mitre[1:]]
supporting_nist = [doc.page_content for doc, score in nist[1:]]
supporting_cve = [doc.page_content for doc, score in cve[1:]]
# ==========================
# Build Combined Context
# ==========================

context = "================ MITRE ================\n\n"

for i, (doc, distance) in enumerate(mitre, start=1):

    context += f"----- Result {i} -----\n"
    context += f"Distance Score: {distance:.4f}\n\n"
    context += doc.page_content
    context += "\n\n"

context += "\n================ NIST ================\n\n"

for i, (doc, distance) in enumerate(nist, start=1):

    context += f"----- Result {i} -----\n"
    context += f"Distance Score: {distance:.4f}\n\n"
    context += doc.page_content
    context += "\n\n"
context += "\n================ CVE ================\n\n"

for i, (doc, distance) in enumerate(cve, start=1):

    context += f"----- Result {i} -----\n"
    context += f"Distance Score: {distance:.4f}\n\n"
    context += doc.page_content
    context += "\n\n"

# ==========================
# Export Variables
# ==========================

retrieved_alert = alert
retrieved_query = query
retrieved_context = context

retrieved_primary_mitre = primary_mitre
retrieved_primary_mitre_distance = primary_mitre_distance

retrieved_primary_nist = primary_nist
retrieved_primary_nist_distance = primary_nist_distance

retrieved_primary_cve = primary_cve
retrieved_primary_cve_distance = primary_cve_distance

retrieved_supporting_mitre = supporting_mitre
retrieved_supporting_nist = supporting_nist
retrieved_supporting_cve = supporting_cve
# ==========================
# Print
# ==========================

print("\n==============================")
print("Combined Context Ready")
print("==============================")

print(context)

print("\n==============================")
print("\n==============================")