from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def generate_report(
    evidence,
    conflicts,
    attempts,
    conclusion
):
    buffer = BytesIO()

    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    x = 45
    y = height - 50

    def write_line(text):
        nonlocal y

        if y < 55:
            pdf.showPage()
            y = height - 50

        pdf.drawString(x, y, str(text)[:110])
        y -= 18

    pdf.setTitle("AI Evidence-to-Decision Report")

    write_line("AI EVIDENCE-TO-DECISION SIMULATOR")
    write_line("Synthetic Shipment Investigation")
    write_line("")

    write_line("FINAL CONCLUSION")
    write_line(conclusion or "No conclusion submitted.")
    write_line("")

    write_line("EVIDENCE REGISTER")

    for item in evidence:
        write_line(
            f"{item['evidence_id']} | "
            f"{item['source']} | {item['date']}"
        )
        write_line(item["text"])

    write_line("")
    write_line("UNRESOLVED CONFLICTS")

    for conflict in conflicts:
        write_line(conflict["title"])
        write_line(conflict["details"])
        write_line(
            "Sources: " + ", ".join(conflict["evidence_ids"])
        )

    write_line("")
    write_line("DECISION HISTORY")

    for number, attempt in enumerate(attempts, start=1):
        write_line(
            f"Attempt {number}: "
            f"Score {attempt['score']}/100"
        )
        write_line(attempt["conclusion"])

    write_line("")
    write_line("RECOMMENDED NEXT STEP")
    write_line(
        "Verify the received quantity, delivery documentation, "
        "and authorization for any address change."
    )

    pdf.save()

    buffer.seek(0)
    return buffer.getvalue()