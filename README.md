# ⭐ DuoMind

**DuoMind** is a dual-LLM research platform that runs multiple AI models
in parallel, compares their outputs, and provides structured synthesis
for better decision-making.

It lets users:

-   Run two AI models side-by-side
-   Compare answers and reconcile differences
-   Bring their own API keys (BYOK)
-   View research history
-   Use a multilingual interface

Built for research, analysis, and high-confidence AI workflows.

------------------------------------------------------------------------

## 🚀 Features

### 🧠 Dual Model Research

-   Run two LLMs simultaneously
-   Independent outputs
-   Side-by-side comparison

Supported providers: - OpenAI - Google Gemini - Anthropic - OpenRouter -
Mistral

------------------------------------------------------------------------

### 🔍 Compare & Reconcile

-   Detect agreements between models
-   Highlight disagreements
-   Provide synthesis/recommendation
-   Identify open questions
-   Structured comparison output

------------------------------------------------------------------------

### 🔑 Bring Your Own Keys (BYOK)

-   Encrypted key storage
-   Automatic key validation
-   Per-provider configuration
-   Full usage when using own keys

------------------------------------------------------------------------

### ⚡ Tiered Rate Limits

  User Type              Limits
  ---------------------- ---------------
  Guest                  Low daily cap
  Registered (no keys)   Medium cap
  Registered + BYOK      Uncapped

------------------------------------------------------------------------

### 📜 Research History

-   View past research runs
-   Reopen previous queries
-   See model pairs used
-   Pagination support

------------------------------------------------------------------------

### 🌍 Multilingual Interface

-   Multiple language support
-   Automatic language switching
-   Full translation coverage

------------------------------------------------------------------------

## 🛠 Installation

### Requirements

-   Python 3.10+
-   API keys (optional but recommended)

### Setup

``` bash
git clone https://github.com/Helvanljar/DuoMind.git
cd DuoMind
pip install -r requirements.txt
```

Create a `.env` file:

    OPENAI_API_KEY=your_key
    GEMINI_API_KEY=your_key
    ANTHROPIC_API_KEY=your_key
    OPENROUTER_API_KEY=your_key
    MISTRAL_API_KEY=your_key

Run:

``` bash
python backend/app.py
```

------------------------------------------------------------------------

## 🧩 Architecture

-   **Backend:** Python (Flask)
-   **Database:** SQLite
-   **Frontend:** HTML / JS
-   **Key Storage:** Encrypted
-   **Rate Limiting:** Tiered middleware

------------------------------------------------------------------------

## 🔒 Security

-   API keys encrypted at rest
-   No keys stored in plaintext
-   BYOK validation before save
-   Rate limiting protection

------------------------------------------------------------------------

## 📄 License

MIT License
