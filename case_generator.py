import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
VISIBLE_DIR = BASE_DIR / "data" / "visible"
HIDDEN_DIR = BASE_DIR / "data" / "hidden"


def create_case_files():
    VISIBLE_DIR.mkdir(parents=True, exist_ok=True)
    HIDDEN_DIR.mkdir(parents=True, exist_ok=True)

    visible_documents = [
        {
            "id": "E001",
            "source": "purchase_order.json",
            "date": "2026-10-01",
            "type": "Purchase Order",
            "text": (
                "The buyer ordered 500 electronic components "
                "with a total stated value of INR 1800000."
            )
        },
        {
            "id": "E002",
            "source": "supplier_email.json",
            "date": "2026-10-03",
            "type": "Supplier Email",
            "text": (
                "The supplier claims that all 500 components "
                "were dispatched."
            )
        },
        {
            "id": "E003",
            "source": "courier_tracking.json",
            "date": "2026-10-05",
            "type": "Courier Record",
            "text": (
                "Courier tracking reports delivery completed. "
                "This record does not specify the quantity "
                "physically received by the warehouse."
            )
        },
        {
            "id": "E004",
            "source": "warehouse_report.json",
            "date": "2026-10-05",
            "type": "Warehouse Report",
            "text": (
                "The warehouse reports receiving 420 components. "
                "The remaining quantity has not been reconciled."
            )
        },
        {
            "id": "E005",
            "source": "address_change_email.json",
            "date": "2026-10-04",
            "type": "Email",
            "text": (
                "An email mentions a delivery-address change. "
                "The available record does not establish whether "
                "the change was properly authorized."
            )
        }
    ]

    hidden_documents = [
        {
            "id": "E006",
            "source": "delivery_receipt.json",
            "date": "2026-10-05",
            "type": "Delivery Receipt",
            "text": (
                "Synthetic supplemental record: a delivery receipt "
                "is available for further investigation. Its "
                "contents must be reviewed before conclusions "
                "can be drawn."
            )
        },
        {
            "id": "E007",
            "source": "address_authorization.json",
            "date": "2026-10-04",
            "type": "Authorization Record",
            "text": (
                "Synthetic supplemental record: an address-change "
                "authorization record is available for review. "
                "Its contents must be verified before authorization "
                "can be established."
            )
        }
    ]

    for folder, documents in [
        (VISIBLE_DIR, visible_documents),
        (HIDDEN_DIR, hidden_documents)
    ]:
        for document in documents:
            path = folder / document["source"]

            with open(path, "w", encoding="utf-8") as file:
                json.dump(document, file, indent=4)

    return len(visible_documents), len(hidden_documents)


if __name__ == "__main__":
    visible, hidden = create_case_files()
    print(f"Created {visible} visible documents.")
    print(f"Created {hidden} hidden documents.")