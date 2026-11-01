def detect_conflicts(evidence):
    conflicts = []

    order = next(
        (
            item for item in evidence
            if item["evidence_id"] == "E001"
        ),
        None
    )

    supplier = next(
        (
            item for item in evidence
            if item["evidence_id"] == "E002"
        ),
        None
    )

    warehouse = next(
        (
            item for item in evidence
            if item["evidence_id"] == "E004"
        ),
        None
    )

    tracking = next(
        (
            item for item in evidence
            if item["evidence_id"] == "E003"
        ),
        None
    )

    if order and supplier and warehouse:
        conflicts.append({
            "title": "Ordered quantity versus received quantity",
            "evidence_ids": ["E001", "E002", "E004"],
            "details": (
                "The order specifies 500 components, the supplier "
                "claims 500 were dispatched, and the warehouse "
                "reports receiving 420. The reported difference "
                "is 80 components."
            ),
            "status": "Unresolved"
        })

    if tracking:
        conflicts.append({
            "title": "Delivery status does not establish quantity",
            "evidence_ids": ["E003", "E004"],
            "details": (
                "Tracking reports delivery completed, but this "
                "does not establish that all 500 components "
                "were physically received."
            ),
            "status": "Quantity not independently verified"
        })

    address_email = next(
        (
            item for item in evidence
            if item["evidence_id"] == "E005"
        ),
        None
    )

    if address_email:
        conflicts.append({
            "title": "Delivery-address authorization",
            "evidence_ids": ["E005", "E007"],
            "details": (
                "An address change is mentioned, but the available "
                "email does not establish whether it was authorized. "
                "Review the authorization record if released."
            ),
            "status": "Unverified"
        })

    return conflicts