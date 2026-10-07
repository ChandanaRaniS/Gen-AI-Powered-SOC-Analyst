import os
from openai import OpenAI

# =====================================================
# Hugging Face Client
# =====================================================

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
)

# =====================================================
# Generate AI SOC Report
# =====================================================

def generate_report(

    alert,
    query,
    context,

    primary_mitre,
    primary_nist,
    primary_cve,

    supporting_mitre,
    supporting_nist,
    supporting_cve

):
    prompt = f"""
You are an expert Security Operations Center (SOC) Analyst.

You are given TWO sources of information.

====================================================

SOURCE 1 : WAZUH ALERT

{alert}

====================================================

SOURCE 2 : RAG RETRIEVED KNOWLEDGE

{context}



YOUR TASK

Step 1

Analyze the Wazuh Alert.

Understand:

- Attack Type
- Severity
- Target System
- Destination Port

====================================================

Step 2

Analyze ALL retrieved MITRE ATT&CK,
NIST and CVE knowledge.

The retrieved context contains the Top-3 most relevant
documents from each database.

Read ALL retrieved evidence before making a decision.

====================================================

Step 3

Compare BOTH sources carefully.

Determine whether the retrieved knowledge supports
the Wazuh Alert.

====================================================

====================================================



Generate EXACTLY this report.

# Threat Summary

- Attack Name:

- Description:

# Severity

- Severity Level:



# Possible Impact
- ...

# MITRE ATT&CK Mapping

The Primary MITRE Technique has already been selected by the retrieval engine.

DO NOT choose another Primary Technique.

Use the provided Primary MITRE exactly as given.

Explain why it matches the detected attack.

You may use the supporting techniques only for additional explanation.

Output exactly in this format:

Primary Technique
-----------------

Use the provided Primary MITRE Technique exactly as given.

Do NOT choose another technique.

Summarize it using this format:

Technique ID:
Technique Name:
Tactic:
Reason:

Supporting Retrieved Techniques
-------------------------------

• Technique ID – Technique Name

• Technique ID – Technique Name

Rules:
- Use ONLY retrieved techniques.
- Never invent techniques.
- The Supporting section must NOT include the Primary Technique.
- If only one technique exists, omit the Supporting section.



# Related CVEs
The Primary CVE has already been selected by the retrieval engine.

DO NOT choose another Primary Vulnerability.

Use the provided Primary CVE exactly as given.

Explain why it is relevant to the detected attack.

Use supporting CVEs only as additional evidence.


Output exactly in this format:

Primary Vulnerability
---------------------

Use the provided Primary CVE exactly as given.

Do NOT choose another CVE.

Summarize it using:

CVE ID:
Description:
Reason:
Supporting Retrieved CVEs
-------------------------

• CVE ID

• CVE ID

Rules:
- Never invent CVEs.
- Use ONLY retrieved CVEs.
- Do not repeat the Primary CVE.
- Omit Supporting if only one CVE exists.


# NIST Security Controls and Guidelines

The Primary NIST Security Control has already been selected by the retrieval engine.

DO NOT choose another Primary Security Control.

Use the provided Primary Security Control exactly as given.

Explain why it mitigates the detected attack.

Use supporting controls only as additional evidence.

Output exactly in this format:

Primary Control
---------------

Use the provided Primary NIST Control exactly as given.

Do NOT choose another control.

Summarize it using:

Publication:
Control ID:
Control Name:
Description:
Reason:

Supporting Security Controls
----------------------------

• Control ID – Control Name

• Control ID – Control Name

Rules:
- Never invent controls.
- Use ONLY retrieved controls.
- Do not repeat the Primary Control.
- Omit Supporting if only one control exists.




## Recommended Actions

Generate EXACTLY 3 recommendations.

Rules:

- Use ONLY information explicitly present in the retrieved MITRE, NIST and CVE context.
- Do NOT invent recommendations.
- Do NOT paraphrase if an equivalent recommendation already exists in the retrieved evidence.
- Keep each recommendation to ONE sentence.
- Each recommendation should begin with a verb (Implement, Update, Configure, Restrict, Enable, Monitor, Patch, Disable, etc.).
- Avoid unnecessary explanations.
- Produce recommendations in a consistent style.

## Security Best Practices

Provide EXACTLY 3 unique cybersecurity best practices.

Rules:
- Base them ONLY on the retrieved MITRE ATT&CK, CVE, and NIST information.
- Do NOT repeat any recommendation.
- If information is unavailable, write:
  "Not found in retrieved context."

IMPORTANT:

Return the report EXACTLY ONCE.

Do NOT repeat any section.

Each heading must appear only once.
The final report must contain ONLY these sections:

# Threat Summary

# Severity

# Possible Impact

# MITRE ATT&CK Mapping

# Related CVEs

# NIST Security Controls and Guidelines

## Recommended Actions

## Security Best Practices

# Confidence Assessment

Provide ONLY a concise explanation (3–5 sentences) describing how the retrieved MITRE ATT&CK, CVE, and NIST evidence supports the generated SOC report.

Mention any missing, incomplete, or weak evidence if applicable.

Do NOT state whether the report is reliable or unreliable.
Do NOT calculate any score or percentage.
Do NOT mention confidence levels.
Do NOT output Strong, Partial, Weak or None.



Stop after Security Best Practices.
Do NOT repeat any headings.
"""
    print("Prompt length:", len(prompt))
    completion = client.chat.completions.create(
    model="meta-llama/Llama-3.1-8B-Instruct",
    messages=[
     {
    "role": "system",
    "content": (
        "You are an expert cybersecurity SOC analyst. "
        "The Primary MITRE Technique, Primary CVE, and Primary NIST Security Control "
        "have already been selected by the retrieval engine. "
        "Do NOT replace them, change them, or choose different ones. "
        "Use them exactly as provided. "
        "Use the supporting retrieved evidence only to strengthen your explanation and recommendations. "
        "Never invent information. "
        "Use only the retrieved context. "
        "Follow the required report format exactly and never repeat headings."
    )
},
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0,
    max_tokens=3000
)

    return completion.choices[0].message.content