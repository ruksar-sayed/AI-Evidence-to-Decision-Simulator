import json
from pathlib import Path

import pandas as pd
import streamlit as st

from case_generator import create_case_files
from evidence_extractor import extract_folder
from analysis import analyze_evidence, build_timeline, search_evidence
from conflict_detector import detect_conflicts
from llm_handler import ask_ai
from decision_engine import evaluate_decision
from report_generator import generate_report


BASE_DIR = Path(__file__).parent
VISIBLE_DIR = BASE_DIR / "data" / "visible"
HIDDEN_DIR = BASE_DIR / "data" / "hidden"

st.set_page_config(
    page_title="AI Evidence-to-Decision Simulator",
    page_icon="🔎",
    layout="wide"
)

st.title("🔎 AI Evidence-to-Decision Simulator")

st.caption(
    "Investigate shipment discrepancies using traceable evidence."
)

if "initialized" not in st.session_state:
    create_case_files()
    st.session_state.initialized = True

if "released_ids" not in st.session_state:
    st.session_state.released_ids = set()

if "requests" not in st.session_state:
    st.session_state.requests = []

if "attempts" not in st.session_state:
    st.session_state.attempts = []

visible_documents = extract_folder(VISIBLE_DIR)
hidden_documents = extract_folder(HIDDEN_DIR)

released_documents = [
    document
    for document in hidden_documents
    if document["id"] in st.session_state.released_ids
]

available_documents = visible_documents + released_documents

evidence = analyze_evidence(available_documents)

available_ids = {
    item["evidence_id"] for item in evidence
}

conflicts = detect_conflicts(evidence)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Case Workspace",
    "Evidence & Timeline",
    "Investigate with AI",
    "Submit Decision",
    "Final Report"
])

# TAB 1: CASE WORKSPACE

with tab1:
    st.header("Shipment Case")

    col1, col2, col3 = st.columns(3)

    col1.metric("Ordered Quantity", "500")
    col2.metric("Reported Received", "420")
    col3.metric("Reported Difference", "80")

    st.write(
        "The supplier claims that the full shipment was "
        "dispatched. Tracking reports delivery completed, "
        "while the warehouse reports receiving fewer units."
    )

    st.info(
        "These figures describe the synthetic case records. "
        "The reported difference is not proof of responsibility."
    )

    st.subheader("Available Documents")

    for item in evidence:
        with st.expander(
            f"{item['evidence_id']} — {item['source']}"
        ):
            st.write("Date:", item["date"])
            st.write("Type:", item["type"])
            st.write(item["text"])

# TAB 2: EVIDENCE AND TIMELINE

with tab2:
    st.header("Evidence Register")

    if evidence:
        table = pd.DataFrame([
            {
                "Evidence ID": item["evidence_id"],
                "Source": item["source"],
                "Date": item["date"],
                "Type": item["type"],
                "Text": item["text"]
            }
            for item in evidence
        ])

        st.dataframe(table, use_container_width=True)

    st.subheader("Search Evidence")

    query = st.text_input(
        "Search by evidence ID, source, or keyword"
    )

    if query:
        results = search_evidence(evidence, query)

        if results:
            for item in results:
                st.write(
                    f"**{item['evidence_id']} — "
                    f"{item['source']}**"
                )
                st.write(item["text"])
        else:
            st.warning("No matching evidence found.")

    st.subheader("Timeline")

    for item in build_timeline(evidence):
        st.write(
            f"**{item['date']} — {item['evidence_id']}**"
        )
        st.write(item["text"])

    st.subheader("Detected Conflicts")

    for conflict in conflicts:
        with st.expander(conflict["title"]):
            st.write(conflict["details"])
            st.write(
                "Sources: "
                + ", ".join(conflict["evidence_ids"])
            )
            st.write("Status:", conflict["status"])

# TAB 3: INVESTIGATION

with tab3:
    st.header("Ask Questions About the Evidence")

    st.write(
        "The AI receives only records currently available "
        "to the investigator."
    )

    question = st.text_area(
        "Enter your investigation question",
        placeholder=(
            "Does the available evidence prove that all "
            "500 components were received?"
        )
    )

    if st.button("Analyze Evidence"):
        if not question.strip():
            st.warning("Enter a question first.")
        else:
            with st.spinner("Analyzing available evidence..."):
                answer = ask_ai(question, evidence)

            st.subheader("Answer")
            st.write(answer["answer"])

            st.subheader("Cited Evidence")

            if answer["evidence_ids"]:
                for evidence_id in answer["evidence_ids"]:
                    item = next(
                        (
                            e for e in evidence
                            if e["evidence_id"] == evidence_id
                        ),
                        None
                    )

                    if item:
                        st.write(
                            f"**{evidence_id} — {item['source']}**"
                        )
                        st.write(item["text"])
            else:
                st.write("No valid evidence IDs were returned.")

            st.subheader("Uncertainties")

            for uncertainty in answer["uncertainties"]:
                st.write("- ", uncertainty)

# TAB 4: CONTROLLED REQUESTS AND DECISION

with tab4:
    st.header("Request Additional Evidence")

    st.write(
        "Hidden documents are unavailable until you request "
        "them and provide a reason."
    )

    for document in hidden_documents:
        if document["id"] in st.session_state.released_ids:
            st.success(
                f"{document['id']} has been released."
            )
            continue

        with st.expander(
            f"Request {document['id']} — "
            f"{document['type']}"
        ):
            st.write(
                "Source: " + document["source"]
            )

            reason = st.text_area(
                "Why do you need this document?",
                key=f"reason_{document['id']}"
            )

            if st.button(
                f"Request {document['id']}",
                key=f"request_{document['id']}"
            ):
                if not reason.strip():
                    st.warning(
                        "Provide a reason before requesting "
                        "the document."
                    )
                else:
                    st.session_state.requests.append({
                        "evidence_id": document["id"],
                        "reason": reason
                    })

                    st.session_state.released_ids.add(
                        document["id"]
                    )

                    st.rerun()

    st.divider()

    st.header("Submit Investigation Decision")

    conclusion = st.text_area(
        "Your conclusion",
        placeholder=(
            "The records show a quantity discrepancy, but "
            "the available evidence does not establish "
            "where or why it occurred."
        )
    )

    supporting_ids = st.multiselect(
        "Supporting evidence",
        options=sorted(available_ids)
    )

    counter_ids = st.multiselect(
        "Counterevidence",
        options=sorted(available_ids)
    )

    confidence = st.slider(
        "Confidence level",
        min_value=1,
        max_value=5,
        value=3
    )

    next_action = st.text_area(
        "Recommended next investigative action"
    )

    if st.button("Evaluate and Save Decision"):
        result = evaluate_decision(
            conclusion=conclusion,
            supporting_ids=supporting_ids,
            counter_ids=counter_ids,
            confidence=confidence,
            next_action=next_action,
            available_ids=available_ids
        )

        attempt = {
            "conclusion": conclusion,
            "supporting_ids": result["valid_supporting_ids"],
            "counter_ids": result["valid_counterevidence_ids"],
            "confidence": confidence,
            "next_action": next_action,
            "score": result["score"],
            "feedback": result["feedback"]
        }

        st.session_state.attempts.append(attempt)

        st.success(
            f"Decision saved. Score: {result['score']}/100"
        )

        for feedback in result["feedback"]:
            st.write("- ", feedback)

    st.subheader("Previous Attempts")

    for number, attempt in enumerate(
        st.session_state.attempts,
        start=1
    ):
        with st.expander(f"Attempt {number}"):
            st.write(attempt["conclusion"])
            st.write(f"Score: {attempt['score']}/100")
            st.write("Next action:", attempt["next_action"])

# TAB 5: FINAL REPORT

with tab5:
    st.header("Investigation Report")

    if st.session_state.attempts:
        latest = st.session_state.attempts[-1]

        st.write("Latest conclusion:")
        st.write(latest["conclusion"])

        st.metric(
            "Latest Decision Score",
            f"{latest['score']}/100"
        )
    else:
        latest = None
        st.info("No decision has been submitted yet.")

    st.subheader("Outstanding Issues")

    for conflict in conflicts:
        st.write(f"**{conflict['title']}**")
        st.write(conflict["details"])

    report_conclusion = (
        latest["conclusion"] if latest else ""
    )

    pdf_bytes = generate_report(
        evidence=evidence,
        conflicts=conflicts,
        attempts=st.session_state.attempts,
        conclusion=report_conclusion
    )

    st.download_button(
        label="Download Final Report (PDF)",
        data=pdf_bytes,
        file_name="investigation_report.pdf",
        mime="application/pdf"
    )

    st.download_button(
        label="Download Evidence Register (JSON)",
        data=json.dumps(
            evidence,
            indent=2,
            ensure_ascii=False
        ),
        file_name="evidence_register.json",
        mime="application/json"
    )