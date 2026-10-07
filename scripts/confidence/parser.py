import re


# =====================================================
# Extract Field
# =====================================================

def extract_field(text, field_name):
    """
    Extracts a single field from the report.
    Example:
    - Attack Name: SSH Brute Force
    """

    pattern = rf"-\s*{re.escape(field_name)}:\s*(.*)"

    match = re.search(pattern, text)

    if match:
        return match.group(1).strip()

    return ""


# =====================================================
# Extract Possible Impact
# =====================================================

def extract_possible_impact(text):

    pattern = r"# Possible Impact\s*-\s*(.*?)\n#"

    match = re.search(
        pattern,
        text,
        re.DOTALL
    )

    if match:
        return match.group(1).strip()

    return ""


# =====================================================
# Extract Recommended Actions
# =====================================================

def extract_recommendations(text):

    pattern = r"## Recommended Actions(.*?)## Security Best Practices"

    match = re.search(pattern, text, re.DOTALL)

    if not match:
        return []

    section = match.group(1)

    recommendations = []

    for line in section.splitlines():

        line = line.strip()

        if not line:
            continue

        # Numbered list: 1. 2. 3.
        if re.match(r"^\d+\.", line):

            recommendations.append(
                re.sub(r"^\d+\.\s*", "", line)
            )

        # Bullet list: -
        elif line.startswith("-"):

            recommendations.append(line[1:].strip())

        # Bullet list: •
        elif line.startswith("•"):

            recommendations.append(line[1:].strip())

    return recommendations


# =====================================================
# Parse Complete Report
# =====================================================

def parse_report(report):

    parsed = {

        "attack_name":
            extract_field(
                report,
                "Attack Name"
            ),

        "description":
            extract_field(
                report,
                "Description"
            ),

        "severity":
            extract_field(
                report,
                "Severity Level"
            ),

        "impact":
            extract_possible_impact(
                report
            ),

        "recommendations":
            extract_recommendations(
                report
            )

    }

    return parsed