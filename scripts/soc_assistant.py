
from confidence.parser import parse_report
from report import generate_pdf
import multi_retriever
from llama import generate_report
import os
import json




print("=" * 70)
print("GenAI Powered SOC Analyst Assistant")
print("=" * 70)


# =====================================================
# Load Retrieved Data
# =====================================================

alert = multi_retriever.retrieved_alert
query = multi_retriever.retrieved_query
context = multi_retriever.retrieved_context

print("Sending Wazuh Alert and RAG Context to Llama...\n")

# =====================================================
# Generate SOC Report
# =====================================================

report = generate_report(

    alert,
    query,
    context,

    multi_retriever.retrieved_primary_mitre,
    multi_retriever.retrieved_primary_nist,
    multi_retriever.retrieved_primary_cve,

    multi_retriever.retrieved_supporting_mitre,
    multi_retriever.retrieved_supporting_nist,
    multi_retriever.retrieved_supporting_cve

)
parsed_report = parse_report(report)

print("\nParsed Report")
print("=" * 60)
print(parsed_report)
from confidence.confidence_score import *

attack_score = validate_attack_name(
    parsed_report["attack_name"],
    alert["attack_type"],
    str(alert),
    multi_retriever.retrieved_primary_mitre,
    multi_retriever.retrieved_primary_cve
)

print("Attack Validation:", attack_score)
# =====================================================
# =====================================================
# Description Validation
# =====================================================

description_score = validate_description(

    parsed_report["description"],

    str(alert),

    multi_retriever.retrieved_primary_mitre,

    multi_retriever.retrieved_primary_nist

)

print("\nDescription Validation")
print("=" * 60)
print(f"Description Score : {description_score:.4f}")

# =====================================================
# Severity Validation
# =====================================================

severity_score = validate_severity(

    parsed_report["severity"],

    alert["severity"],

    str(alert)

)

print("\nSeverity Validation")
print("=" * 60)
print(f"Severity Score : {severity_score:.4f}")

# =====================================================
# Impact Validation
# =====================================================

impact_score = validate_impact(

    parsed_report["impact"],

    multi_retriever.retrieved_primary_mitre,

    multi_retriever.retrieved_primary_nist

)

print("\nImpact Validation")
print("=" * 60)
print(f"Impact Score : {impact_score:.4f}")
# =====================================================
# Threat Validation (TV)
# =====================================================

tv = calculate_tv(
    attack_score,
    description_score,
    severity_score,
    impact_score
)

print("\nThreat Validation")
print("=" * 60)
print(f"TV Score : {tv:.4f}")
# =====================================================
# Recommendation Validation
# =====================================================

recommendations = parsed_report["recommendations"]

print("\nRecommendations extracted:")
print(recommendations)
print("Count:", len(recommendations))

rec1_score = validate_recommendation(
    recommendations[0],
    multi_retriever.retrieved_primary_nist,
    multi_retriever.retrieved_primary_mitre
)

rec2_score = validate_recommendation(
    recommendations[1],
    multi_retriever.retrieved_primary_nist,
    multi_retriever.retrieved_primary_mitre
)

rec3_score = validate_recommendation(
    recommendations[2],
    multi_retriever.retrieved_primary_nist,
    multi_retriever.retrieved_primary_mitre
)

print("\nRecommendation Validation")
print("=" * 60)
print(f"Recommendation 1 : {rec1_score:.4f}")
print(f"Recommendation 2 : {rec2_score:.4f}")
print(f"Recommendation 3 : {rec3_score:.4f}")
# =====================================================
# Recommendation Validation Score
# =====================================================

rv = calculate_rv(
    rec1_score,
    rec2_score,
    rec3_score
)

print("\nRecommendation Validation (RV)")
print("=" * 60)
print(f"RV Score : {rv:.4f}")
# =====================================================
# Cyber Evidence Validation Framework (CEVF)
# =====================================================

cevf = calculate_cevf(
    tv,
    rv
)

print("\nCyber Evidence Validation Framework")
print("=" * 60)
print(f"CEVF Score : {cevf:.4f}")
# =====================================================
# Final Confidence Score
# =====================================================

confidence = calculate_confidence_score(
    cevf
)

print("\nOverall Confidence")
print("=" * 60)
print(f"Confidence : {confidence:.2f}%")
# =====================================================
# Reliability
# =====================================================

reliability = classify_confidence(
    confidence
)

print(f"Reliability : {reliability}")
# =====================================================
# Display Report
# =====================================================






print(f"Attack Validation Score : {attack_score*100:.2f}%")

# =====================================================
# Append Confidence Score
# =====================================================

# =====================================================
# Insert Overall Confidence Score
# =====================================================

confidence_heading = "# Confidence Assessment"

if confidence_heading in report:

    report = report.replace(

        confidence_heading,

        f"""# Confidence Assessment

Overall Confidence Score: {confidence:.2f}%

Reliability: {reliability}

Evidence Summary:
""",

        1
    )
print(report)
# =====================================================
# Save RAG Results for Dashboard
# =====================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

rag_path = os.path.join(
    BASE_DIR,
    "data",
    "rag_results.json"
)

rag_results = {
    "summary": report,
    "confidence": round(confidence, 2),
    "reliability": reliability,

    "alert": {
        "id": alert.get("id"),
        "timestamp": alert.get("timestamp"),
        "description": alert.get("description"),
        "agent": alert.get("agent"),
        "mitre": alert.get("mitre", []),
        "technique": alert.get("technique", []),
        "full_log": alert.get("full_log"),
        "attack_type": alert.get("attack_type"),
        "severity": alert.get("severity"),
        "system": alert.get("system"),
        "destination_port": alert.get("destination_port")
    },

    "mitre": {
        "primary": multi_retriever.retrieved_primary_mitre,
        "supporting": multi_retriever.retrieved_supporting_mitre
    },

    "cves": {
        "primary": multi_retriever.retrieved_primary_cve,
        "supporting": multi_retriever.retrieved_supporting_cve
    },

    "nist": {
        "primary": multi_retriever.retrieved_primary_nist,
        "supporting": multi_retriever.retrieved_supporting_nist
    },

    "evidence": [],
    "healthcare_context": [],
    "retrieval_statistics": {}
}
with open(rag_path, "w", encoding="utf-8") as f:
    json.dump(rag_results, f, indent=4)

print(" rag_results.json updated")

# =====================================================
# Generate PDF
# =====================================================

generate_pdf(
    report,
    "SOC_Report.pdf"
)



