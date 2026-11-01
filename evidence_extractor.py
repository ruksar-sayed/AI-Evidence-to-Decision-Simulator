import json
from pathlib import Path
from pypdf import PdfReader


def extract_document(path):
    path = Path(path)
    suffix = path.suffix.lower()

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    if suffix == ".json":
        with open(path, "r", encoding="utf-8") as file:
            document = json.load(file)

        if not isinstance(document, dict):
            raise ValueError("JSON document must contain an object.")

        return {
            "id": document.get("id", ""),
            "source": str(path),
            "date": document.get("date", "Unknown"),
            "type": document.get("type", "Unknown"),
            "text": document.get("text", "")
        }

    if suffix == ".pdf":
        reader = PdfReader(str(path))
        text = "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        )

        return {
            "id": "",
            "source": str(path),
            "date": "Unknown",
            "type": "PDF",
            "text": text
        }

    if suffix in {".txt", ".eml"}:
        text = path.read_text(encoding="utf-8", errors="replace")

        return {
            "id": "",
            "source": str(path),
            "date": "Unknown",
            "type": "Email" if suffix == ".eml" else "Text",
            "text": text
        }

    raise ValueError(f"Unsupported file type: {suffix}")


def extract_folder(folder):
    folder = Path(folder)
    evidence = []

    if not folder.exists():
        return evidence

    supported = {".json", ".pdf", ".txt", ".eml"}

    for path in sorted(folder.iterdir()):
        if path.is_file() and path.suffix.lower() in supported:
            try:
                evidence.append(extract_document(path))
            except Exception as error:
                evidence.append({
                    "id": "",
                    "source": str(path),
                    "date": "Unknown",
                    "type": "Extraction Error",
                    "text": f"Could not extract document: {error}"
                })

    return evidence