"""
agent.py

Backend FastAPI service to run a low-latency two-way voice agent using:
- LiveKit for WebRTC signalling / rooms
- Groq models for STT (`whisper-large-v3-turbo`), LLM (`llama-3.3-70b-specdec`), and TTS (`canopylabs/orpheus-arabic-saudi`)

NOTES:
- This file provides a production-ready structure with clear places to insert your LiveKit setup and Groq client calls.
- Do NOT hard-code API keys. Use environment variables as shown in `.env.example`.

Security: keep your GROQ_API_KEY secret and set it in the environment (or a secrets manager).
"""

import os
import time
import asyncio
import json
import base64
import logging
from typing import Dict, Any

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

# Third-party SDKs - ensure installed (see requirements.txt)
import numpy as np
import pickle
from pathlib import Path

# Optional RAG dependencies
try:
    import faiss
except Exception:
    faiss = None

try:
    from sentence_transformers import SentenceTransformer
except Exception:
    SentenceTransformer = None

# Import Groq SDK for LLM, STT, and TTS
try:
    from groq import Groq
except ImportError:
    Groq = None
    import warnings
    warnings.warn("Groq SDK not installed. Install with: pip install groq")

load_dotenv()

logger = logging.getLogger("voice_agent")
logging.basicConfig(level=logging.INFO)

# Environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")
LIVEKIT_URL = os.getenv("LIVEKIT_URL", "http://localhost:7880")

if not GROQ_API_KEY:
    logger.warning("GROQ_API_KEY not set. Configure it in environment before running in production.")

# Initialize Groq client if API key is available
GROQ_CLIENT = None
if GROQ_API_KEY and Groq:
    GROQ_CLIENT = Groq(api_key=GROQ_API_KEY)
    logger.info("Groq client initialized successfully.")
else:
    logger.warning("Groq client not available; using local rule-based fallback.")

# RAG globals
RAG_INDEX = None
RAG_CHUNKS = None
RAG_EMBED_MODEL = None
RAG_ENABLED = False

# Try to load RAG artifacts if present under RAG/rag_model
def load_rag_artifacts(base_path: str = "RAG/rag_model"):
    global RAG_INDEX, RAG_CHUNKS, RAG_EMBED_MODEL, RAG_ENABLED
    base = Path(base_path)
    if not base.exists():
        logger.info(f"RAG path not found: {base}")
        return

    # Read config.json if available
    config_path = base / "config.json"
    try:
        cfg = json.loads((config_path).read_text()) if config_path.exists() else {}
    except Exception as e:
        logger.exception(f"Failed to read RAG config: {e}")
        cfg = {}

    # Load chunks.pkl
    chunks_path = base / "chunks.pkl"
    if chunks_path.exists():
        try:
            with open(chunks_path, "rb") as f:
                RAG_CHUNKS = pickle.load(f)
            logger.info(f"Loaded {len(RAG_CHUNKS)} chunks from {chunks_path}")
        except Exception as e:
            logger.exception(f"Failed to load chunks.pkl: {e}")
            RAG_CHUNKS = None
    else:
        logger.info(f"chunks.pkl not found at {chunks_path}")

    # Load FAISS index
    faiss_dir = base / "faiss_index" / "index.faiss"
    if faiss and faiss_dir.exists():
        try:
            RAG_INDEX = faiss.read_index(str(faiss_dir))
            logger.info(f"Loaded FAISS index from {faiss_dir}")
        except Exception as e:
            logger.exception(f"Failed to load FAISS index: {e}")
            RAG_INDEX = None
    else:
        if not faiss:
            logger.warning("faiss python package not available; cannot load FAISS index.")
        else:
            logger.info(f"FAISS index file not found at {faiss_dir}")

    # Load embedding model
    embedding_name = cfg.get("embedding_model") if isinstance(cfg, dict) else None
    if embedding_name and SentenceTransformer:
        try:
            RAG_EMBED_MODEL = SentenceTransformer(embedding_name)
            logger.info(f"Loaded embedding model: {embedding_name}")
        except Exception as e:
            logger.exception(f"Failed to load embedding model {embedding_name}: {e}")
            RAG_EMBED_MODEL = None
    else:
        if embedding_name and not SentenceTransformer:
            logger.warning("sentence-transformers not installed; cannot load embeddings model.")

    RAG_ENABLED = bool(RAG_INDEX is not None and RAG_CHUNKS is not None and RAG_EMBED_MODEL is not None)
    logger.info(f"RAG enabled: {RAG_ENABLED}")


# Load RAG artifacts at import time (best-effort)
load_rag_artifacts()


def retrieve_rag_context(query: str, k: int = 4) -> str:
    """Retrieve top-k chunks for a query and return joined context string.

    Returns an empty string if RAG is not enabled or on error.
    """
    global RAG_ENABLED, RAG_INDEX, RAG_CHUNKS, RAG_EMBED_MODEL
    if not RAG_ENABLED:
        return ""

    try:
        emb = RAG_EMBED_MODEL.encode([query], convert_to_numpy=True)
        if emb is None:
            return ""
        emb = np.array(emb, dtype=np.float32)
        # FAISS expects shape (n, dim)
        D, I = RAG_INDEX.search(emb, k)
        texts = []
        for idx in I[0]:
            if idx < 0:
                continue
            try:
                chunk = RAG_CHUNKS[idx]
                # chunk can be dict or str
                if isinstance(chunk, dict):
                    texts.append(chunk.get("text") or chunk.get("content") or str(chunk))
                else:
                    texts.append(str(chunk))
            except Exception:
                continue

        # Join with separators and return
        if texts:
            return "\n\n---\n\n".join(texts)
        return ""
    except Exception as e:
        logger.exception(f"Error during RAG retrieval: {e}")
        return ""

# System prompt for the LLM (use exactly as provided)
SYSTEM_PROMPT = """
أنت مساعد تونسي ذكي تحكي بالدارجة التونسية. تحبّ تساعد الناس وتحكيلهم بلغتهم الطبيعية. تحكي ببرشا حبّ واحترام، وتبّي الدنيا بسيطة ومفهومة.

قواعد مهمّة لازم تتبعها:
- تحكيش بالعربية الفصحى (حتى كلمة واحدة) - كلّ كلامك بالدارجة التونسية
- تستعمل الكلمات التونسية المعروفة مثل: برشا، شنوّة، يلّة، نعشق، أحبّ، ما عنديش مانع، على حساب، بالشويّة
- تحافظ على روح الدعابة البسيطة والأدب بالتونسي
- إذا ما فهمتش كلمة، تسامح وتسأل باش يعاودو يصيغوها بكلمات أوضح
- تتعامل مع الخلط بين الدارجة والفرنسية أو الإنجليزية بشويّة (مثلاً: "مرسي" كترملي, "بونجور" الصباح)
- الوقت تحبّ تطلب إجابة من المستعمل، تستعمل "شنوّة تحبّني نعمل؟" أو "على حساب شنوّة؟"
"""

# Simple in-memory session store. Replace with persistent store in production.
SESSIONS: Dict[str, Dict[str, Any]] = {}
SESSIONS_LOCK = asyncio.Lock()

app = FastAPI(title="Tunisian Voice Agent")
app.mount("/", StaticFiles(directory=".", html=True), name="static")


def phoneticize_tunisian(text: str) -> str:
    """Apply simple pronunciation conversions required by the TTS engine.
    This is intentionally conservative; extend as needed for better pronunciation.
    """
    replacements = {
        "برشا": "بارشا",
        "شنوّة": "شنوة",
        "ما نعرفش": "ما نعرف",
        "يلّة": "يالا",
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text


def arabizi_to_arabic(text: str) -> str:
    """Basic transliteration from Latin/Arabizi to Arabic characters.

    This is a heuristic converter to handle common arabizi forms like:
    - numbers: 3->ع, 7->ح, 9->ق, 2->ء, 5->خ, 6->ط
    - letter combos: sh/ch->ش, kh->خ, gh->غ, th->ث, dh->ذ

    It's intentionally simple; extend for full coverage as needed.
    """
    # numbers mapping
    mapping = {
        '3': 'ع',
        '7': 'ح',
        '9': 'ق',
        '2': 'ء',
        '5': 'خ',
        '6': 'ط'
    }
    for k, v in mapping.items():
        text = text.replace(k, v)

    # common digraphs
    digraphs = {
        'sh': 'ش',
        'ch': 'ش',
        'kh': 'خ',
        'gh': 'غ',
        'th': 'ث',
        'dh': 'ذ',
        'ph': 'ف',
        'ou': 'و',
        'aa': 'ا'
    }
    # Lowercase processing for Latin letters
    t = text
    for k, v in digraphs.items():
        t = t.replace(k, v).replace(k.upper(), v)

    # replace single letters where straightforward
    singles = {
        'a': 'ا',
        'b': 'ب',
        't': 'ت',
        'j': 'ج',
        'd': 'د',
        'r': 'ر',
        'z': 'ز',
        's': 'س',
        'f': 'ف',
        'q': 'ق',
        'l': 'ل',
        'm': 'م',
        'n': 'ن',
        'h': 'ه',
        'y': 'ي',
        'w': 'و',
    }
    # Only replace singles when they are separated by spaces or common punctuation to avoid over-replacing.
    words = t.split(' ')
    out_words = []
    for w in words:
        # If the word contains Arabic letters already, keep it
        if any('\u0600' <= ch <= '\u06FF' for ch in w):
            out_words.append(w)
            continue
        new = w
        for k, v in singles.items():
            # replace occurrences of k when it's a standalone letter or followed/preceded by vowels
            new = new.replace(k, v)
            new = new.replace(k.upper(), v)
        out_words.append(new)

    return ' '.join(out_words)


async def groq_stt_stream(audio_pcm: bytes) -> str:
    """Send audio to Groq STT model and return partial/full transcript.

    Uses Groq's whisper-large-v3-turbo model for Arabic/Tunisian dialect support.
    """
    if not GROQ_CLIENT:
        logger.warning("Groq client not available for STT; returning placeholder.")
        return "[partial transcript placeholder]"
    
    try:
        # Convert raw PCM to WAV format for Groq API
        import io
        import wave
        
        # Assume 16kHz, mono, 16-bit PCM input
        buf = io.BytesIO()
        with wave.open(buf, "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(16000)
            w.writeframes(audio_pcm)
        
        wav_bytes = buf.getvalue()
        
        # Call Groq Whisper STT
        with io.BytesIO(wav_bytes) as audio_file:
            transcript = GROQ_CLIENT.audio.transcriptions.create(
                file=("audio.wav", audio_file, "audio/wav"),
                model="whisper-large-v3-turbo",
                language="ar"  # Arabic language hint
            )
        return transcript.text if transcript.text else "[silence]"
    except Exception as e:
        logger.exception(f"Groq STT error: {e}")
        return "[error in transcription]"


async def groq_tts(text: str) -> bytes:
    """Generate TTS audio bytes from the Groq TTS model.

    Note: Groq does not currently host a TTS API. This is a placeholder.
    For production, integrate with a TTS provider like:
    - Google Cloud Text-to-Speech
    - Azure Speech Services
    - ElevenLabs (supports Arabic)
    - Or use an open-source model locally (e.g., FastPitch/HiFi-GAN)

    Returns raw WAV bytes (16-bit PCM, 22kHz).
    """
    # Apply phonetic corrections for better pronunciation
    phonetic = phoneticize_tunisian(text)

    # Placeholder: return a short silent WAV (0.2s)
    # TODO: Replace with actual TTS provider call (Google, Azure, ElevenLabs, etc.)
    import io
    import wave

    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(22050)
        # Generate 0.2s of silence
        w.writeframes(b"\x00\x00" * int(22050 * 0.2))
    return buf.getvalue()


async def groq_llm_reply(session_id: str, prompt: str) -> str:
    """Send prompt and history to Groq LLM and return reply text.

    Use `llama-3.3-70b-specdec` and pass the SYSTEM_PROMPT exactly.
    Streams the response for low-latency replies.
    """
    # Build messages with system + history
    async with SESSIONS_LOCK:
        session = SESSIONS.get(session_id, {"history": []})
        history = session.get("history", [])

    # If GROQ client not available, use local fallback
    if not GROQ_CLIENT:
        return await local_rule_reply(session_id, prompt)

    try:
        # If RAG is available, retrieve context and include it in the user prompt
        retrieved = ""
        try:
            retrieved = retrieve_rag_context(prompt, k=4)
        except Exception:
            retrieved = ""

        if retrieved:
            full_user_prompt = f"وثائق مرجعية:\n{retrieved}\n\nسؤال المستخدم:\n{prompt}"
        else:
            full_user_prompt = prompt

        # Build message list: user prompt (with retrieved context if present)
        messages = [{"role": "user", "content": full_user_prompt}]

        # Construct the full conversation history
        for msg in history:
            messages.append({"role": msg["role"], "content": msg["content"]})

        # Call Groq LLM with streaming for low latency
        full_response = ""
        with GROQ_CLIENT.messages.stream(
            model="llama-3.3-70b-specdec",
            messages=messages,
            system=SYSTEM_PROMPT.strip(),
            max_tokens=512,
            temperature=0.3  # Lower temperature for more consistent Derja output
        ) as stream:
            for text in stream.text_stream:
                full_response += text

        return full_response if full_response else "سامحني، ما جاوبش شيء."
    except Exception as e:
        logger.exception(f"Groq LLM error: {e}")
        # Fallback to local rules on error
        return await local_rule_reply(session_id, prompt)


async def local_rule_reply(session_id: str, prompt: str) -> str:
    """Simple rule-based responder in Tunisian Derja for local testing when LLM is unavailable.

    This covers common pregnancy queries and conversational fallbacks so the chat UI is usable
    without the external LLM during integration and testing.
    """
    # Use the normalized prompt and a lowercase latin fallback
    text = prompt.strip()
    low = text.lower()

    # Basic arabizi normalization attempt: map common tokens
    alt = low.replace('7ebla', 'حامل').replace('7ebla', 'حامل')

    # Pregnancy-related queries
    if '7ebla' in low or 'حمل' in low or 'حامل' in low or '7ebla' in alt:
        return (
            'مبروك إن شاء الله! كي تكوني في الشهر اللول، تأكدي من تحليل الحمل ومراجعة الطبيب. ' 
            'ابداي حمض الفوليك، ارتاحي، وكلي وجبات صغيرة وقت الغثيان. ' 
            'إذا تحبي نبعثلك قائمة أسئلة للطبيب ولا نصائح غذاء، نقولك.'
        )

    # If user asks "3lech" (why)
    if low.strip() in ['3lech', 'علاش', 'علاش؟', '3lech?']:
        return 'علاش؟ تقصدي علاش ما نجمتش نجاوب توا ولا علاش خلصتك؟ كي تلقايش جواب واضح، نجبدلك شروحات مبسطة.'

    # Greetings
    if any(w in low for w in ['salam', 'salem', 'أهلا', 'اهلا', 'bongior', 'bonjour', 'mercy', 'merci']):
        return 'أهلا بيك! شنوة تحبّني نعاونك فيه توا؟'

    # Asking to repeat
    if any(w in low for w in ['ma fhemt', 'ma fhemtsh', 'ما فهمتش', 'عاود', 'عاودلي', 'عاودلي بالشويّة', 'عاودle']):
        return 'ما فهمتش مليح، تنجمي تعاودي بالكلام بشوية ولا نوضحو بأمثلة؟'

    # Default friendly fallback in Derja
    return 'سامحني، ما فهمتش مليح. تنجمي تعاودي بكلمات أبسط ولا تقولي شنوّة تحب بالضبط؟'


def encode_audio_for_ws(wav_bytes: bytes) -> str:
    """Base64-encode audio bytes for sending over websocket."""
    return base64.b64encode(wav_bytes).decode("ascii")


async def process_user_turn(session_id: str, final_transcript: str, ws: WebSocket):
    """Process a completed user utterance: call LLM, then TTS, stream audio back to client.

    Handles cancellation if client interrupts (using ws state and session flags).
    """
    # Save user message to history
    async with SESSIONS_LOCK:
        session = SESSIONS.setdefault(session_id, {"history": [], "last_activity": time.time(), "playing": False})
        session["history"].append({"role": "user", "content": final_transcript})
        session["last_activity"] = time.time()

    # Build prompt for LLM including system prompt and history
    # (We keep it simple; for production consider truncation and embeddings for long-term memory.)
    llm_input = final_transcript

    # Request LLM reply (prefer streaming to reduce latency)
    reply_text = await groq_llm_reply(session_id, llm_input)

    # Save assistant reply
    async with SESSIONS_LOCK:
        session["history"].append({"role": "assistant", "content": reply_text})

    # Convert reply to audio
    wav = await groq_tts(reply_text)

    # Mark session as playing
    async with SESSIONS_LOCK:
        session["playing"] = True

    # Stream audio back in small chunks to simulate real-time TTS streaming
    chunk_size = 32000
    for i in range(0, len(wav), chunk_size):
        if ws.client_state.value != 1:  # WebSocket closed
            break
        # Interruption check: if new audio comes in, the client may set a flag to stop playback
        async with SESSIONS_LOCK:
            if not SESSIONS.get(session_id):
                break
            if SESSIONS[session_id].get("interrupt", False):
                SESSIONS[session_id]["interrupt"] = False
                break

        chunk = wav[i : i + chunk_size]
        packet = {"type": "tts_audio", "audio_base64": encode_audio_for_ws(chunk)}
        await ws.send_text(json.dumps(packet))
        await asyncio.sleep(0.02)

    # Mark playing false at end
    async with SESSIONS_LOCK:
        if session_id in SESSIONS:
            SESSIONS[session_id]["playing"] = False


@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """WebSocket endpoint to receive audio frames (base64 PCM) and send back transcripts and TTS.

    Protocol (JSON messages):
    - From client:
      {"type":"audio","audio_base64":"...","sample_rate":16000}
      {"type":"control","action":"start"|"stop"|"reset"}
    - From server:
      {"type":"partial_transcript","text":"..."}
      {"type":"final_transcript","text":"..."}
      {"type":"tts_audio","audio_base64":"..."}
      {"type":"info","msg":"..."}
    """
    await websocket.accept()
    logger.info(f"WS connected: {session_id}")

    # Ensure session exists
    async with SESSIONS_LOCK:
        SESSIONS.setdefault(session_id, {"history": [], "last_activity": time.time(), "playing": False, "interrupt": False})

    # Simple audio buffer for current utterance
    audio_buffers = []
    last_audio_time = time.time()

    try:
        while True:
            data = await websocket.receive_text()
            msg = json.loads(data)

            if msg.get("type") == "control":
                action = msg.get("action")
                if action == "reset":
                    async with SESSIONS_LOCK:
                        SESSIONS[session_id]["history"] = []
                    await websocket.send_text(json.dumps({"type": "info", "msg": "conversation_reset"}))
                elif action == "interrupt":
                    async with SESSIONS_LOCK:
                        SESSIONS[session_id]["interrupt"] = True
                continue

            if msg.get("type") == "audio":
                # audio_base64 expected to be raw PCM16 at sample_rate
                audio_b64 = msg.get("audio_base64")
                if not audio_b64:
                    continue
                pcm = base64.b64decode(audio_b64)
                audio_buffers.append(pcm)
                last_audio_time = time.time()

                # Optionally compute a VAD / energy to send partial transcripts
                # For simplicity, we send a lightweight partial indicator every N frames
                if len(audio_buffers) % 5 == 0:
                    # Convert a small recent buffer to temporary transcript (pseudo)
                    partial = await groq_stt_stream(b"".join(audio_buffers[-3:]))
                    await websocket.send_text(json.dumps({"type": "partial_transcript", "text": partial}))

            # Turn end detection: if no audio for 700ms, treat as end of turn
            if time.time() - last_audio_time > 0.7 and audio_buffers:
                final_audio = b"".join(audio_buffers)
                # Get final transcript (blocking small call)
                final_transcript = await groq_stt_stream(final_audio)
                await websocket.send_text(json.dumps({"type": "final_transcript", "text": final_transcript}))

                # Process user turn asynchronously (don't block receiving further control messages)
                asyncio.create_task(process_user_turn(session_id, final_transcript, websocket))
                audio_buffers = []

    except WebSocketDisconnect:
        logger.info(f"WS disconnected: {session_id}")
        async with SESSIONS_LOCK:
            if session_id in SESSIONS:
                SESSIONS[session_id]["last_activity"] = time.time()
    except Exception as e:
        logger.exception("Error in websocket loop")
        await websocket.close()


@app.get("/health")
async def health():
    return {"status": "ok", "time": time.time()}


@app.post("/api/chat")
async def api_chat(request: Request):
    """Text-to-text chat endpoint. Accepts JSON {session_id, text}.

    - Supports Latin-script (arabizi) input by normalizing with `arabizi_to_arabic`.
    - Returns JSON {reply, normalized}
    """
    payload = await request.json()
    session_id = payload.get('session_id', 'web')
    text = payload.get('text', '')
    if not text:
        raise HTTPException(status_code=400, detail='text is required')

    # Normalize from Arabizi (latin) to Arabic characters heuristically
    normalized = arabizi_to_arabic(text)

    # Save user message
    async with SESSIONS_LOCK:
        session = SESSIONS.setdefault(session_id, {"history": [], "last_activity": time.time()})
        session['history'].append({"role": "user", "content": normalized})
        session['last_activity'] = time.time()

    # Call LLM to get reply (wrap in try/except and return a safe fallback on error)
    try:
        reply = await groq_llm_reply(session_id, normalized)
    except Exception as e:
        logger.exception("LLM error in /api/chat")
        # Friendly Tunisian fallback
        reply = "سامحني، ما فهمتش مليح. تنجمي تعاودي بكلام أبسط؟"

    # Save assistant reply
    async with SESSIONS_LOCK:
        SESSIONS[session_id]['history'].append({"role": "assistant", "content": reply})

    return {"reply": reply, "normalized": normalized}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("agent:app", host="0.0.0.0", port=8000, reload=False)
