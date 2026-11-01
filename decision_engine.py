def evaluate_decision(
    conclusion,
    supporting_ids,
    counter_ids,
    confidence,
    next_action,
    available_ids
):
    feedback = []
    score = 0

    supporting_ids = list(dict.fromkeys(supporting_ids))
    counter_ids = list(dict.fromkeys(counter_ids))

    valid_support = [
        item for item in supporting_ids
        if item in available_ids
    ]

    valid_counter = [
        item for item in counter_ids
        if item in available_ids
    ]

    if not conclusion.strip():
        feedback.append("Provide a clear conclusion.")
    else:
        score += 20
        feedback.append("Conclusion provided.")

    if valid_support:
        score += 25
        feedback.append(
            "Supporting evidence references are valid."
        )
    else:
        feedback.append(
            "Select at least one valid supporting evidence ID."
        )

    if valid_counter:
        score += 20
        feedback.append(
            "Counterevidence has been identified."
        )
    else:
        feedback.append(
            "Consider relevant counterevidence."
        )

    if 1 <= confidence <= 5:
        score += 15
        feedback.append("Confidence level recorded.")
    else:
        feedback.append(
            "Select a confidence level from 1 to 5."
        )

    if next_action.strip():
        score += 20
        feedback.append("Next investigative step provided.")
    else:
        feedback.append(
            "Recommend a specific next investigative step."
        )

    invalid_ids = (
        set(supporting_ids + counter_ids) - available_ids
    )

    if invalid_ids:
        feedback.append(
            "Rejected unavailable evidence IDs: "
            + ", ".join(sorted(invalid_ids))
        )

    return {
        "score": score,
        "maximum_score": 100,
        "feedback": feedback,
        "valid_supporting_ids": valid_support,
        "valid_counterevidence_ids": valid_counter,
        "invalid_ids": sorted(invalid_ids)
    }