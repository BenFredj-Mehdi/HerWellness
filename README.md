# HerWellness — Tunisian Pregnancy Assistant

HerWellness is a hybrid project combining a static informational website and a backend AI assistant focused on supporting pregnant users in Tunisian Arabic (Darja). The repo contains:

- A static month-by-month guidance site (months 1–9).
- A voice/chat backend built with FastAPI providing RAG-enabled conversational responses and WebSocket streaming for low-latency interactions.
- Tools and assets for offline retrieval-augmented generation (RAG) using a local FAISS index.

This README summarizes architecture, models, setup, and how to run the project locally.

**Important disclaimer:** This project provides general guidance only. It is NOT medical advice. Always consult a qualified healthcare professional for medical decisions.

**Contents**

- `index.html`, `month-*.html` — Static site UI for month-by-month pregnancy tips.
- `agent.py` — FastAPI backend implementing chat endpoints, WebSocket streaming, and optional RAG retrieval.
- `voice_client.html` — Demo client for audio/voice flows.
- `RAG/rag_model/` — Local RAG artifacts (FAISS index, chunks, config).
- `README_AGENT.md` — Notes and run instructions specifically for the voice/agent components.
- `requirements.txt` — Python dependencies for the backend.

## Architecture & Models

- Backend: FastAPI (`agent.py`) exposing:
	- `POST /api/chat` — synchronous chat with optional RAG context
	- `POST /api/retrieve` — retrieval endpoint (requires RAG enabled)
	- `GET /health` — health and model info
	- `WebSocket /ws/{session_id}` — real-time audio/text streaming endpoint

- LLM / Inference:
	- Primary LLM (configured in `agent.py`): `llama-3.3-70b-*` (Groq ChatGroq wrapper in the repo expects a Groq API key).
	- System prompt is tailored to produce friendly Tunisian Darja replies (see `SYSTEM_PROMPT` in `agent.py`).

- RAG / Retrieval:
	- Local FAISS vector store and pickle chunks live in `RAG/rag_model/faiss_index` and `RAG/rag_model/chunks.pkl`.
	- Embedding model used: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` (see `RAG/rag_model/config.json`).
	- If the `faiss_index` folder is present, `agent.py` will attempt to load the RAG artifacts at startup and enable retrieval.

- Speech:
	- The project references STT, TTS, and phonetic helpers (see `README_AGENT.md`). Example models mentioned in `README_AGENT.md`:
		- STT: `whisper-large-v3-turbo` (placeholder — wire to your STT provider)
		- TTS: `canopylabs/orpheus-arabic-saudi` (used for Arabic TTS; quality may vary for Tunisian dialect)

## Quick Start (Backend)

1. Copy `.env.example` to `.env` and set keys (do not commit real keys):

```powershell
copy .env.example .env
# edit .env and set GROQ_API_KEY and any other keys
```

2. Create and activate a Python virtual environment and install deps:

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
```

3. Run the API server:

```powershell
uvicorn agent:app --host 0.0.0.0 --port 8082
```

4. Open the static site or demo client in a browser (served from the same directory):

- `index.html` — static site
- `voice_client.html` — voice demo client (for integration with the FastAPI backend)

## RAG Notes

- To enable RAG, place the prepared FAISS index and `chunks.pkl` under `RAG/rag_model/`. The `config.json` there documents the embedding model and chunking used.
- If RAG is not present, the backend gracefully falls back to generating answers without retrieval and sets `rag_enabled=false` in `/health`.

## Config / Environment

- `GROQ_API_KEY` — required to initialize the Groq Chat LLM in `agent.py`. If missing, the server will still run but LLM calls will return fallback messages.
- Other optional keys are used by demo flows (e.g., LiveKit credentials referenced in `README_AGENT.md`).

Keep secrets out of Git using `.env` and `.gitignore`.

## How the Assistant Speaks

- The AI persona is configured in `SYSTEM_PROMPT` inside `agent.py`. It enforces:
	- Tunisian Darja responses
	- Friendly, clear tone
	- Safety guardrails: no medical diagnosis, always suggest seeing a doctor for serious symptoms

## Development Notes

- `agent.py` uses in-memory session histories (`session_histories`) for demo purposes; swap to Redis or a DB for production.
- The repository contains TODOs where you should wire real STT/LLM/TTS providers (Groq SDK, Whisper, or other services).
- Improve TTS pronunciation of Darja using `phoneticize_tunisian` heuristics in `README_AGENT.md` / `agent.py`.

## Troubleshooting

- If the server logs show `RAG not available`, confirm the `RAG/rag_model/faiss_index` folder exists and `chunks.pkl` is present.
- If LLM initialization fails, ensure `GROQ_API_KEY` is set in `.env` and the machine has network access to the model provider.

## Contributing

- Suggest content improvements for the month pages and expand medical sources in the RAG dataset.
- Add tests for endpoints and CI scripts for deployment.

## License

This project currently has no license file. Add a `LICENSE` if you intend to open-source it.

---

If you'd like, I can:

- wire a `.env.example` template for the repo,
- add a short `docker-compose.yml` to run the API locally,
- or update `README_AGENT.md` into the main README as a dedicated section.
Just tell me which next step you prefer.
