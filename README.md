# 📊 Prompt2SQL

A Streamlit app that lets you upload Excel files and get summaries, answers, and insights using either:
- **Local Ollama models** (e.g., `llama3.1:8b`, `qwen2.5:7b`, `mistral:7b`), or
- **OpenAI-compatible APIs** (provide your base URL and API key).

## ✨ Features
- Multiple Excel uploads (reads all sheets).
- Three modes: **Summarize sheets**, **Ask a question**, **Free-form prompt**.
- Provider switch: **Ollama** or **API** (OpenAI-compatible).
- **Size guard** with technical error message when data is too large (limits can be adjusted in `utils.py`).

## 🚀 Quickstart

### 1) Create a virtual environment and install deps
```bash
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt