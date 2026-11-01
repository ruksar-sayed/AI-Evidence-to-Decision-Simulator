import re


def analyze_evidence(documents):
    results = []

    for document in documents:
        text = document.get("text", "")

        quantities = [
            int(value)
            for value in re.findall(
                r"\b\d+\b", text
            )
        ]

        results.append({
            "evidence_id": document.get("id", "UNKNOWN"),
            "source": document.get("source", "Unknown"),
            "date": document.get("date", "Unknown"),
            "type": document.get("type", "Unknown"),
            "text": text,
            "quantities": quantities
        })

    return results


def build_timeline(evidence):
    return sorted(
        evidence,
        key=lambda item: item.get("date", "Unknown")
    )


def search_evidence(evidence, query):
    query = query.lower().strip()

    if not query:
        return []

    return [
        item for item in evidence
        if query in item.get("text", "").lower()
        or query in item.get("source", "").lower()
        or query in item.get("evidence_id", "").lower()
    ]