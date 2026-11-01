# AI Evidence to Decision Simulator

An interactive Streamlit app that simulates how an investigator turns scattered evidence into a decision, using a **missing shipment** case. Users query an AI assistant, gather evidence from case records, and make a final call. The app then scores how well that decision is supported by the evidence.

## Overview

A shipment has gone missing. The case records are only partly visible. Some of the key records are hidden and surface only when the user asks the right questions. The user must:

1. Review the evidence that's available
2. Ask the AI assistant questions to uncover more information
3. Decide what most likely happened to the shipment
4. Get scored on the quality of the decision and the reasoning behind it

## Features

- **AI-assisted investigation:** ask questions about the case and get answers from an LLM grounded in the case records
- **Hidden records:** some evidence is revealed only through relevant queries
- **Decision workflow:** submit a final conclusion with supporting reasons
- **Scoring:** the decision is evaluated against the available evidence
- **Streamlit interface:** simple, browser-based UI

## Tech Stack

- Python
- Streamlit
- LLM API (add the provider you used, e.g. OpenAI / Gemini / Anthropic)

## Project Structure

```
AI-Evidence-to-Decision-Simulator/
├── app.py              # Main Streamlit app
├── data/               # Case records
├── requirements.txt    # Dependencies
└── README.md
```

*(Adjust to match your actual files.)*

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/ruksar-sayed/AI-Evidence-to-Decision-Simulator.git
   cd AI-Evidence-to-Decision-Simulator
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Add your API key as an environment variable or in a `.env` file:
   ```
   API_KEY=your_key_here
   ```
5. Run the app:
   ```bash
   streamlit run app.py
   ```

## How It Works

The app loads the case records, keeps part of them hidden from the user, and passes the relevant context to the LLM when the user asks a question. When the user submits a decision, it is compared against the evidence and scored.

## Author

Ruksar Sayed
