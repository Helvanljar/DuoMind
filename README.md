# DuoMind

DuoMind is a **multi-model research and comparison system** that runs the same question through multiple large language models, extracts **agreements and disagreements**, and produces a **reconciled recommendation**.

The project focuses on **model comparison and reasoning transparency**, not just answer generation.

---

## ✨ Core Idea

> *How do different LLMs reason about the same question — and where do they actually agree?*

DuoMind answers this by:
1. Running the same query through **two independent models**
2. Comparing the results
3. Highlighting:
   - Agreements
   - Disagreements
   - A synthesized recommendation

---

## 🧠 Architecture Overview

### MCP-style Multi-Model Orchestration (Current)

DuoMind implements an **MCP-style (Model Coordination Pattern)** architecture:

| Role | Description |
|----|----|
| **Researcher A** | First LLM (e.g. Mistral) answers independently |
| **Researcher B** | Second LLM (e.g. Gemini) answers independently |
| **Judge / Reconciler** | A comparison step analyzes both answers |

Core orchestration logic:
```
backend/duomind_app/llm_orchestrator.py
```

Key functions:
- `run_dual_research()`
- `run_compare_reconcile()`

---

## ❌ RAG Status

**DuoMind does NOT use RAG yet.**

- No document retrieval
- No vector database
- No external knowledge injection

All answers rely on the **internal knowledge of the models**.

RAG is a **planned extension**, not part of the current system.

---

## 📊 Features

- Multi-model research (Mistral + Gemini, optional OpenAI)
- Agreement & disagreement extraction
- Reconciled final recommendation
- MCP-style orchestration
- Daily usage limits (quota pill in UI)
- Guest vs BYOK (Bring Your Own Key)
- Language follows **question language**
- Deterministic, frontend-safe compare output

---

## 🧩 Providers

Supported providers:

- Mistral
- Google Gemini
- OpenAI (BYOK only)

Provider logic:
```
backend/duomind_app/providers/
```

---

## 🔐 Environment Configuration

### `.env.example`

Copy and configure:
```bash
cp .env.example .env
```

Example:
```env
GUEST_MAX_PER_DAY=5
USER_SERVER_MAX_PER_DAY=20

OPENAI_API_KEY=
GEMINI_API_KEY=
MISTRAL_API_KEY=

JWT_SECRET_KEY=dev-secret-change-me
```

⚠️ Never commit `.env`.

---

## 🚦 Quotas & Daily Limits

- Guests and non-BYOK users are IP-limited
- Limits configurable via `.env`
- Current usage shown in the **top bar pill**
- Logic:
```
backend/duomind_app/routes_quota.py
```

---

## 🖥️ Running the Backend

```bash
python -m venv venv
venv\Scripts\activate
pip install -r backend/requirements.txt
uvicorn duomind_app.main:app --reload --env-file .env
```

Server:
```
http://127.0.0.1:8000
```

---

## 🔍 API Endpoints

| Endpoint | Description |
|------|------|
| `/api/research` | Multi-model research |
| `/api/compare` | Compare & reconcile |
| `/api/quota` | Quota status |
| `/api/history` | Research history |

---

## 📁 Project Structure

```
backend/
 ├─ requirements.txt
 └─ duomind_app/
     ├─ main.py
     ├─ llm_orchestrator.py
     ├─ routes_research.py
     ├─ routes_quota.py
     ├─ providers/
     │   ├─ mistral_provider.py
     │   ├─ gemini_provider.py
     │   └─ openai_provider.py
     ├─ templates/
     └─ static/
```

---

## 🎯 Design Goals

- Transparency over raw answers
- Visible consensus & disagreement
- Avoid hallucinated certainty
- Clear separation of research, comparison, synthesis

---

## 🚀 Future Work

- RAG integration
- Source-aware agreements
- Confidence scoring
- Additional agent roles

---

## 📜 License

MIT

---

## 👤 Author

DuoMind by **Helvanljar**
