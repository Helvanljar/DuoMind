# DuoMind 🧠⚖️  
**Multi-LLM Debate with Evidence-Based Consensus**

DuoMind is a research assistant that runs **multiple large language models in parallel**, compares their answers, and produces a **final, evidence-grounded conclusion**.

Instead of trusting a single model, DuoMind lets LLMs **disagree**, then resolves disagreements using **external research** and an **evidence-gated judge**.

---

## ✨ Key Features

- 🔁 **Dual-LLM reasoning**  
  Uses two public LLMs (e.g. OpenAI + Gemini) to answer the same question independently.

- ⚔️ **Model disagreement & comparison**  
  Clearly surfaces agreements and disagreements between models.

- 📚 **Evidence-based resolution (RAG-style)**  
  Retrieves external evidence from **Wikipedia** and forces the final answer to be based on that evidence.

- 🧑‍⚖️ **Judge step**  
  A dedicated reconciliation step accepts or rejects claims **only if supported by retrieved evidence**.

- 🔌 **MCP integration (Model Context Protocol)**  
  Exposes the debate workflow as MCP tools so external agents (e.g. Claude Desktop, Cursor) can invoke it.

- 🌐 **REST API + UI**  
  Works via standard API endpoints and a web interface.

---

## 🧠 How DuoMind Works

1. User asks a question  
2. **LLM A** produces an answer  
3. **LLM B** produces an independent answer  
4. The system **retrieves external evidence** (Wikipedia)  
5. A **judge step** evaluates both answers against the evidence  
6. DuoMind returns:
   - Final answer
   - Supporting evidence
   - Rejected claims
   - Confidence assessment

Example:  
LLM A says the Earth is flat, LLM B says it is square → evidence retrieval → final answer: *oblate spheroid*.

---

## 🔍 Research & RAG

DuoMind uses a **retrieval-augmented approach** without requiring a private document database.

- Evidence source: **Wikipedia (public, neutral, verifiable)**
- No custom vector database required
- No reliance on model internal knowledge alone

This keeps the system lightweight, reproducible, and easy to extend.

---

## 🔌 MCP (Model Context Protocol)

DuoMind exposes its core capabilities via MCP:

- `duomind_debate_and_converge`
- `duomind_wikipedia_retrieve`

This allows MCP-compatible hosts and agents to integrate DuoMind as a tool.

---

## 🏗️ Project Structure

```
backend/
 └─ duomind_app/
    ├─ llm_orchestrator.py
    ├─ web_retriever.py
    ├─ routes_research.py
    ├─ routes_debate.py
    ├─ mcp_server.py
    ├─ main.py
    └─ templates/
```

---

## 🚀 Getting Started

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run backend
```bash
uvicorn duomind_app.main:app --reload
```

### Open UI
```
http://localhost:8000
```

### MCP endpoint
```
http://localhost:8000/mcp
```

---

## 🛡️ Notes

- Evidence is currently retrieved only from Wikipedia
- Designed for research and educational purposes
- Additional evidence sources can be added later

---

## 📌 Summary

DuoMind demonstrates **multi-model reasoning**, **evidence-based consensus**, and **MCP-based integration** without unnecessary infrastructure.
