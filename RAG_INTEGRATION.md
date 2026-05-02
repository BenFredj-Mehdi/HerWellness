# RAG Integration Guide

The FastAPI backend (`agent.py`) now integrates the RAG model from the `RAG/rag_model/` folder to power chat responses.

## How It Works

1. **Startup**: When `agent.py` starts, it loads:
   - FAISS index from `RAG/rag_model/faiss_index/index.faiss`
   - Chunks from `RAG/rag_model/chunks.pkl`
   - Embedding model specified in `RAG/rag_model/config.json` (default: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`)

2. **Chat Flow**: When a user submits a question via `/api/chat`:
   - The question is normalized (Arabizi → Arabic if needed)
   - RAG retrieval computes embeddings and retrieves top-4 relevant chunks
   - Retrieved chunks are prepended to the user prompt
   - The combined prompt is sent to Groq LLM
   - The LLM replies in Tunisian Derja

3. **Fallbacks**:
   - If `faiss` or `sentence-transformers` are not installed, RAG is disabled but chat still works (using Groq LLM or local rule-based responses)
   - If Groq is unavailable, a simple rule-based responder handles common pregnancy questions

## Setup & Run

### Install Dependencies

```bash
cd "c:\Users\mbfga\Desktop\New Project"
pip install -r requirements.txt
```

Note: `faiss-cpu` is included. If you have a GPU, replace with `faiss-gpu` for faster retrieval (optional).

### Environment Configuration

Create a `.env` file (do NOT commit to git):

```env
GROQ_API_KEY=your-groq-api-key-here
```

### Start the Server

```bash
python agent.py
```

Or with auto-reload during development:

```bash
uvicorn agent:app --host 0.0.0.0 --port 8000 --reload
```

## Testing

### Chat Endpoint

Open http://localhost:8000/chat.html and type a question (e.g., "شنوّة الغثيان في الشهر الأول؟").

The response will include relevant information retrieved from the pregnancy PDF.

### Curl Example (Text Chat)

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test_user",
    "text": "شنوّة الغثيان في الشهر الأول؟"
  }'
```

Expected output:
```json
{
  "reply": "...[response in Tunisian Derja with info from RAG]...",
  "normalized": "شنوّة الغثيان في الشهر الأول؟"
}
```

### Health Check

```bash
curl http://localhost:8000/health
```

## Logging

On startup, you'll see logs like:
- `Loaded 123 chunks from RAG/rag_model/chunks.pkl`
- `Loaded FAISS index from RAG/rag_model/faiss_index/index.faiss`
- `Loaded embedding model: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`
- `RAG enabled: True`

If RAG fails to load, the app continues but uses Groq LLM without context retrieval.

## Customization

### Adjust Retrieval Count

In `agent.py`, the `retrieve_rag_context()` call uses `k=4` (top-4 chunks). To change:

```python
retrieved = retrieve_rag_context(prompt, k=6)  # Change k to 6, 8, etc.
```

### Adjust LLM Parameters

In `groq_llm_reply()`, you can tune:
- `max_tokens` (default 512) — controls response length
- `temperature` (default 0.3) — lower = more consistent, higher = more creative
- `model` — currently `llama-3.3-70b-specdec`; can swap for other Groq models

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `RAG path not found` | Ensure `RAG/rag_model/` exists with `chunks.pkl`, `config.json`, and `faiss_index/` |
| `faiss not installed` | Run `pip install faiss-cpu` (or `faiss-gpu` for GPU) |
| `sentence-transformers not installed` | Run `pip install sentence-transformers` |
| `No RAG context retrieved` | Check that chunks.pkl is valid and FAISS index matches the embedding model |
| `Groq API errors` | Verify `GROQ_API_KEY` is set in `.env` |

## Architecture

```
┌─────────────────────┐
│  chat.html (UI)     │
└──────────┬──────────┘
           │ POST /api/chat
           ▼
┌──────────────────────────────┐
│  FastAPI /api/chat endpoint  │
│  1. Normalize text (Arabizi) │
│  2. Retrieve RAG context     │
│  3. Call Groq LLM            │
│  4. Return reply             │
└──────────────────────────────┘
           │
           ├─► RAG/rag_model/
           │   ├── chunks.pkl
           │   ├── config.json
           │   └── faiss_index/
           │
           └─► Groq API
               (whisper, llama-3.3-70b-specdec, TTS)
```

## Next Steps

- Replace TTS placeholder with a real provider (Google Cloud, Azure, ElevenLabs)
- Add persistent session storage (Redis) for long-term memory
- Implement rate-limiting and backoff for Groq API calls
- Add semantic search UI for browsing RAG chunks
- Build a re-indexing pipeline for PDF updates
