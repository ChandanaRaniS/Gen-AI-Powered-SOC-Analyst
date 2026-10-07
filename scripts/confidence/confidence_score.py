from sentence_transformers import SentenceTransformer, util

# =====================================================
# Load Embedding Model
# =====================================================

embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

# =====================================================
# Semantic Similarity
# =====================================================

def semantic_similarity(text1, text2):
    """
    Computes semantic similarity between two texts.
    Returns a value between 0 and 1.
    """

    if not str(text1).strip() or not str(text2).strip():
        return 0.0

    emb1 = embedding_model.encode(
        str(text1),
        convert_to_tensor=True
    )

    emb2 = embedding_model.encode(
        str(text2),
        convert_to_tensor=True
    )

    similarity = util.cos_sim(
        emb1,
        emb2
    ).item()

    # Convert [-1,1] → [0,1]
    similarity = (similarity + 1) / 2

    return round(similarity, 4)
# =====================================================
## =====================================================
# Attack Name Validation (V1)
# =====================================================

def validate_attack_name(
        ai_attack_name,
        alert_attack_type,
        alert_description,
        mitre_text="",
        cve_text=""
):

    evidence = " ".join(filter(None, [
        alert_attack_type,
        alert_description,
        mitre_text,
        cve_text
    ]))

    score = semantic_similarity(
        ai_attack_name,
        evidence
    )

    return score
# =====================================================
# Description Validation (V2)
# =====================================================

def validate_description(
        ai_description,
        alert_description,
        mitre_text="",
        nist_text=""
):

    evidence = " ".join(filter(None, [
        alert_description,
        mitre_text,
        nist_text
    ]))

    score = semantic_similarity(
        ai_description,
        evidence
    )

    return score
# =====================================================
# Severity Validation (V3)
# =====================================================

def validate_severity(
        ai_severity,
        alert_severity,
        alert_description=""
):

    if str(ai_severity).strip().lower() == str(alert_severity).strip().lower():
        return 1.0

    return 0.0
# =====================================================
# Possible Impact Validation (V4)
# =====================================================

def validate_impact(
        ai_impact,
        mitre_text="",
        nist_text=""
):
    """
    Validate AI-generated impact using
    MITRE and NIST evidence.
    """

    evidence = " ".join(filter(None, [
        mitre_text,
        nist_text
    ]))

    score = semantic_similarity(
        ai_impact,
        evidence
    )

    return score

# =====================================================
# Recommendation Validation
# =====================================================

def validate_recommendation(
        recommendation,
        nist_text="",
        mitre_text=""
):
    """
    Validate AI-generated recommendation
    against NIST controls and MITRE mitigations.
    """

    evidence = " ".join(filter(None, [
        nist_text,
        mitre_text
    ]))

    score = semantic_similarity(
        recommendation,
        evidence
    )

    return score
# =====================================================
# Threat Assessment Validation (TV)
# =====================================================

def calculate_tv(
        attack_score,
        description_score,
        severity_score,
        impact_score
):

    tv = (
        attack_score +
        description_score +
        severity_score +
        impact_score
    ) / 4

    return round(tv, 4)
# =====================================================
# Recommendation Validation (RV)
# =====================================================

def calculate_rv(
        rec1_score,
        rec2_score,
        rec3_score
):

    rv = (
        rec1_score +
        rec2_score +
        rec3_score
    ) / 3

    return round(rv, 4)
# =====================================================
# Cyber Evidence Validation Framework
# =====================================================

def calculate_cevf(
        tv,
        rv
):

    cevf = (
        tv +
        rv
    ) / 2

    return round(cevf, 4)
# =====================================================
# Final Confidence Score
# =====================================================

def calculate_confidence_score(
        cevf
):

    confidence = round(
        cevf * 100,
        2
    )

    return confidence
# =====================================================
# Reliability Classification
# =====================================================

def classify_confidence(score):

    if score < 60:
        return "Low"

    elif score < 75:
        return "Moderate"

    else:
        return "High"