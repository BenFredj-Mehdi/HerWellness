# Tunisian Derja Voice Agent

This README covers the voice AI agent backend and frontend for real-time phone-like conversations in Tunisian Arabic (Derja).

Important: Do not commit your real API keys. Put secrets in a `.env` file as described in `.env.example`.

Quick start

1. Copy `.env.example` to `.env` and fill your keys:

```powershell
copy .env.example .env
# edit .env and set GROQ_API_KEY, LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET
```

2. Create a virtual environment and install deps:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

3. Run the backend:

```powershell
uvicorn agent:app --host 0.0.0.0 --port 8082
```

4. Open the test client in a browser:

Open `voice_client.html` in the same folder (or serve the directory and open `http://localhost:8082/voice_client.html`).

Architecture notes

- `agent.py` implements a FastAPI server with a WebSocket endpoint `/ws/{session_id}` used for streaming audio and receiving TTS back.
- The server maintains lightweight in-memory session state in `SESSIONS` (swap for Redis or DB for production).
- STT, LLM, and TTS calls are marked as TODOs where you should plug in the Groq SDK calls using models:
  - STT: `whisper-large-v3-turbo`
  - LLM: `llama-3.3-70b-specdec` (the system prompt is included in `SYSTEM_PROMPT`)
  - TTS: `canopylabs/orpheus-arabic-saudi`

Tunisian dialect notes

- The system prompt in `agent.py` must be sent exactly to the LLM.
- We perform a small phonetic pre-processing step (`phoneticize_tunisian`) before sending text to TTS to improve pronunciation of Tunisian words.
- The TTS model may still speak with a MSA accent; adjust and expand `phoneticize_tunisian` for better results.

Testing phrases (for validating Tunisian Derja behavior)

- "شنوّة تحبّ نعمل اليوم؟"
- "برشا عجبتني الخدمة"
- "ما فهمتش، عاودلي بالشويّة"
- "يلّة نبداو"
- "على حساب ما تجي الدنيا"

Text (Arabizi) support

- You can write Tunisian Arabic using Latin letters (Arabizi). The backend applies a heuristic transliteration (`arabizi_to_arabic`) before sending text to the LLM.
- Examples to try in the chat UI:
  - `kifeh 3lik` → system will normalize to دارجة
  - `ma fhemtsh, a3awedli belchwiya` → asks for repetition


LiveKit configuration

- This project uses a simple WebSocket audio streaming flow for demos. For a real phone-like experience with TURN traversal and low-latency media, integrate LiveKit rooms and issue ephemeral tokens to browser clients.
- See LiveKit docs to create tokens on the server and use LiveKit JS on the client.

Troubleshooting

- Latency: ensure your Groq/TTS calls use streaming endpoints and place your server close to the model region.
- VAD and turn detection: currently implemented as a simple timeout. For robust production use, integrate `webrtcvad` or an audio energy/VAD model.
- Echo cancellation: the browser provides some AEC; for best results, use full WebRTC with proper AEC/AGC/ANS.

Security

- Do not upload your API keys to source control.
- Rate limits and errors from Groq should be handled by retry/backoff — see TODO sections in `agent.py` for guidance.
