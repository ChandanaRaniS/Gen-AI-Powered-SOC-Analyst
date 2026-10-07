import json
from langchain_community.document_loaders import JSONLoader, PyPDFLoader
from langchain_core.documents import Document


def load_documents():

    # ==========================
    # MITRE
    # ==========================
    print("Loading MITRE...")

    mitre_loader = JSONLoader(
        file_path="data/enterprise-attack.json",
        jq_schema=".objects[]",
        text_content=False
    )

    mitre_docs = mitre_loader.load()

    print(f"MITRE: {len(mitre_docs)}")

    # ==========================
    # NIST
    # ==========================
    print("Loading NIST...")

    nist_loader = PyPDFLoader("data/NIST.pdf")
    nist_docs = nist_loader.load()

    print(f"NIST: {len(nist_docs)}")

    # ==========================
    # CVE
    # ==========================
    print("Loading CVE...")

    with open("data/cve.json", "r", encoding="utf-8") as f:
        cve_json = json.load(f)

    keywords = [
        "ftp",
        "ssh",
        "brute force",
        "authentication bypass",
        "credential",
        "password",
        "login",
        "credential theft",
        "password spraying",
        "remote code execution",
        "privilege escalation",
        "ransomware",
        "malware",
        "command injection",
        "sql injection",
        "buffer overflow"
    ]

    cve_docs = []

    for vuln in cve_json["vulnerabilities"]:

        description = ""

        cve = vuln.get("cve", {})

        for desc in cve.get("descriptions", []):
            if desc.get("lang") == "en":
                description = desc.get("value", "").lower()
                break

        if any(keyword in description for keyword in keywords):

            cve_docs.append(
                Document(
                    page_content=json.dumps(vuln),
                    metadata={
                        "source": "CVE"
                    }
                )
            )

    # Keep only first 5000 relevant CVEs
    cve_docs = cve_docs[:5000]

    print(f"Relevant CVEs: {len(cve_docs)}")

    # ==========================
    # Combine
    # ==========================

    all_docs = mitre_docs + nist_docs + cve_docs

    print(f"TOTAL DOCUMENTS: {len(all_docs)}")

    return all_docs


if __name__ == "__main__":
    load_documents()