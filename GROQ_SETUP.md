# Groq Integration Setup

This guide walks you through setting up the chatbot with real Groq API calls.

## Prerequisites

1. **Groq API Key**: You have one from earlier. Keep it safe.
2. **Python 3.9+** with pip installed.

## Setup Steps

### 1. Create `.env` file with your Groq API key

Copy `.env.example` to `.env`:

```powershell
Copy-Item .env.example .env
```

Then edit `.env` and set your GROQ_API_KEY (the one you provided):

```dotenv
GROQ_API_KEY=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
LIVEKIT_URL=
LIVEKIT_API_KEY=
LIVEKIT_API_SECRET=
PORT=8082
```

**IMPORTANT**: Never commit `.env` to git. It's in `.gitignore` for a reason.

### 2. Install dependencies (including groq SDK)

From the project folder:

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
```

Verify groq is installed:
```powershell
python -c "import groq; print(groq.__version__)"
```

### 3. Start the FastAPI server

```powershell
uvicorn agent:app --host 0.0.0.0 --port 8082
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8082
INFO:voice_agent:Groq client initialized successfully.
```

### 4. Test the chatbot

Open in your browser:
- **Text chat (supports Arabizi)**: http://localhost:8082/chat.html
- **Simple chat**: http://localhost:8082/chatbot.html
- **Voice demo**: http://localhost:8082/voice_client.html

### Example Test Queries

**Text chat** (try these in http://localhost:8082/chat.html):

1. `Salem, ena 7ebla f chhar lowel kifech naamel` (Arabizi)
   - Groq LLM will recognize and respond in Tunisian Derja

2. `3alech ma jaawebsh?` (Why didn't you reply?)
   - Should get a Derja response

3. `برشا عجبتني الخدمة` (I really like the service)
   - Direct Arabic Derja

## How It Works

### LLM (Text Generation)
- **Model**: `llama-3.3-70b-specdec` (best for Tunisian dialect)
- **System Prompt**: Exactly as you specified (encourages Derja only)
- **Streaming**: Enabled for low latency
- **Temperature**: 0.3 (more consistent output)

The agent will:
1. Normalize arabizi input (e.g., "7ebla" → "حامل")
2. Send to Groq LLM with system prompt + conversation history
3. Return a Tunisian Derja reply

### STT (Speech-to-Text)
- **Model**: `whisper-large-v3-turbo`
- **Language**: Arabic (with Tunisian dialect support)
- **Input**: WAV audio from browser microphone

**Note**: STT in the WebSocket flow is currently a placeholder. For production, integrate:
- [Groq Audio Transcriptions API](https://console.groq.com/docs/speech-text) (if available in your region)
- Or use OpenAI Whisper API directly

### TTS (Text-to-Speech)
- **Status**: Placeholder (Groq doesn't currently provide TTS)
- **Recommendation**: Use one of:
  - **Google Cloud Text-to-Speech** (supports Arabic, free tier available)
  - **Azure Speech Services** (good Arabic quality)
  - **ElevenLabs** (natural sounding, paid)
  - **Local model**: FastPitch + HiFi-GAN (open-source, runs on CPU)

For now, the voice_client.html will receive silent audio. To enable TTS:
1. Choose a TTS provider
2. Update `groq_tts()` in `agent.py` to call that provider
3. Apply `phoneticize_tunisian()` before sending text to improve pronunciation

## Troubleshooting

### "Groq client not available" warning
- Check `.env` file exists and `GROQ_API_KEY` is set
- Restart the server after updating `.env`

### API Rate Limit (429 error)
- Groq free tier has rate limits (~30 calls/min)
- Add exponential backoff retry logic in `groq_llm_reply()` if needed

### No TTS audio playing
- TTS is currently a placeholder. See "TTS" section above for integration options.

### Chat returns "undefined" or empty
- Check server console for error logs
- Ensure GROQ_API_KEY is correct
- Try sending a simple test query

## Production Checklist

- [ ] Move API keys to a secrets manager (AWS Secrets Manager, HashiCorp Vault, etc.)
- [ ] Add rate limiting + exponential backoff for Groq calls
- [ ] Implement persistent session storage (Redis, PostgreSQL)
- [ ] Deploy server behind a load balancer (e.g., Nginx)
- [ ] Integrate LiveKit for WebRTC (sub-500ms latency, echo cancellation)
- [ ] Add a real TTS provider (Google Cloud, Azure, ElevenLabs)
- [ ] Monitor Groq API usage and costs
- [ ] Add comprehensive error handling and logging

## Support

- Groq docs: https://console.groq.com/docs
- FastAPI docs: https://fastapi.tiangolo.com
- LiveKit docs: https://docs.livekit.io

