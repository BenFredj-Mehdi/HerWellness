# agent.py - HerWellness Tunisian Pregnancy Voice Assistant
# Complete API with RAG + Chat + Health endpoints

import os
import json
import uuid
import pickle
import logging
from datetime import datetime
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import warnings
warnings.filterwarnings('ignore')

# Load environment
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ========== Pydantic Models ==========
class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    text: str = Field(..., min_length=1, max_length=2000)
    language: str = "ar-TN"
    metadata: Optional[Dict[str, Any]] = None

class Source(BaseModel):
    id: str
    text_snippet: str
    score: float

class ChatResponse(BaseModel):
    reply: str
    reply_html: Optional[str] = None
    normalized: str
    lang: str = "ar-TN"
    sources: Optional[List[Source]] = None
    confidence: Optional[float] = None
    session_id: str
    timestamp: str

class RetrieveRequest(BaseModel):
    query: str
    top_k: int = 5

class RetrieveResult(BaseModel):
    id: str
    text: str
    score: float
    metadata: Optional[Dict[str, Any]] = None

class RetrieveResponse(BaseModel):
    results: List[RetrieveResult]

class HealthResponse(BaseModel):
    status: str
    time: str
    rag_enabled: bool
    model: str

# ========== Global State ==========
app = FastAPI(title="HerWellness - Tunisian Pregnancy Assistant")
rag_enabled = False
vector_store = None
embeddings = None
chunks = None
llm = None
session_histories: Dict[str, List[Dict]] = {}

# ========== Initialize on Startup ==========
@asynccontextmanager
async def lifespan(app: FastAPI):
    global llm, rag_enabled, vector_store, embeddings, chunks
    
    logger.info("🚀 Starting HerWellness API...")
    
    # Initialize Groq
    try:
        from langchain_groq import ChatGroq
        
        GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is not set")
        
        llm = ChatGroq(
            api_key=GROQ_API_KEY,
            model="llama-3.3-70b-versatile",
            temperature=0.5,
            max_tokens=500,
        )
        logger.info("✅ Groq LLM initialized")
    except Exception as e:
        logger.error(f"Failed to initialize LLM: {e}")
        llm = None
    
    # Load RAG model
    try:
        from langchain_community.embeddings import HuggingFaceEmbeddings
        from langchain_community.vectorstores import FAISS
        
        model_path = "./RAG/rag_model"
        if os.path.exists(f"{model_path}/faiss_index"):
            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
                model_kwargs={'device': 'cpu'},
            )
            vector_store = FAISS.load_local(
                f"{model_path}/faiss_index",
                embeddings,
                allow_dangerous_deserialization=True
            )
            
            with open(f"{model_path}/chunks.pkl", "rb") as f:
                chunks = pickle.load(f)
            
            rag_enabled = True
            logger.info("✅ RAG model loaded")
        else:
            logger.warning("RAG model not found")
    except Exception as e:
        logger.warning(f"RAG not available: {e}")
    
    yield
    
    logger.info("👋 Shutting down...")

app = FastAPI(lifespan=lifespan, title="HerWellness API", version="1.0.0")

# Allow browser clients served from other local origins (e.g., Live Server)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== System Prompt ==========
SYSTEM_PROMPT = """أنت 'Maya'، مساعدة صحية ودودة تتكلم التونسي الدارجي. جاوب بلطف، واضح، وبلهجة قريبة من المستخدم.

المهمة:
- دعم الحوامل بنصائح عملية للأكل، الراحة، التمارين
- جاوب بالدارجة التونسية فقط (كلمات مثل: برشا، شنوّة، يلّة، نعشق)
- أعطِ نصائح عامة فقط
- ذكر دائماً بمراجعة الطبيب للحالات الطبية الخطيرة
- إذا ما تعرفش جواب، اعترف و اقترح مصادر أو خطوات عملية

قواعد مهمة:
- ما تنجمش تعطي تشخيص طبي رسمي
- إذا كان أعراض خطيرة (نزيف، ألم حاد)، تقول "لازم تشوفي دكتورة"

السياق من دليل الحمل: {context}

سؤال المستخدم: {question}

جوابك بالدارجة التونسية:"""

FALLBACK_RESPONSE = "سامحني، ما نجمش نجاوب توا. نجربو مرة أخرى؟"

# ========== Helper Functions ==========
def normalize_text(text: str) -> str:
    """Normalize user input (basic cleaning)"""
    # Remove extra spaces
    text = " ".join(text.split())
    return text

def search_knowledge(query: str, k: int = 4) -> tuple[str, List[Dict]]:
    """Search RAG and return context + sources"""
    if not rag_enabled or not vector_store:
        return "", []
    
    try:
        docs = vector_store.similarity_search_with_score(query, k=k)
        context = "\n\n".join([doc[0].page_content for doc in docs])
        
        sources = []
        for i, (doc, score) in enumerate(docs):
            sources.append({
                "id": f"chunk_{i}",
                "text_snippet": doc.page_content[:200],
                "score": float(1 - score / 100)  # Convert distance to similarity
            })
        
        return context, sources
    except Exception as e:
        logger.error(f"Search error: {e}")
        return "", []

def generate_response(question: str, context: str = "") -> str:
    """Generate response using Groq"""
    if not llm:
        return FALLBACK_RESPONSE
    
    try:
        prompt = SYSTEM_PROMPT.format(context=context[:2000], question=question)
        
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        logger.error(f"LLM error: {e}")
        return FALLBACK_RESPONSE

# ========== API Endpoints ==========
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="ok",
        time=datetime.now().isoformat(),
        rag_enabled=rag_enabled,
        model="llama-3.3-70b-versatile"
    )

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Synchronous chat endpoint"""
    try:
        # Normalize input
        normalized = normalize_text(request.text)
        
        # Generate session ID
        session_id = request.session_id or str(uuid.uuid4())
        
        # Search RAG
        context, sources = search_knowledge(normalized)
        
        # Generate response
        reply = generate_response(normalized, context)
        
        # Store history
        if session_id not in session_histories:
            session_histories[session_id] = []
        session_histories[session_id].append({
            "user": normalized,
            "assistant": reply,
            "timestamp": datetime.now().isoformat()
        })
        
        # Limit history to 10 turns
        if len(session_histories[session_id]) > 10:
            session_histories[session_id] = session_histories[session_id][-10:]
        
        # Prepare sources for response
        source_objects = []
        for s in sources:
            source_objects.append(Source(
                id=s["id"],
                text_snippet=s["text_snippet"],
                score=s["score"]
            ))
        
        return ChatResponse(
            reply=reply,
            normalized=normalized,
            lang="ar-TN",
            sources=source_objects if source_objects else None,
            confidence=0.85 if context else 0.70,
            session_id=session_id,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/retrieve", response_model=RetrieveResponse)
async def retrieve_endpoint(request: RetrieveRequest):
    """RAG retrieval endpoint"""
    if not rag_enabled:
        raise HTTPException(status_code=503, detail="RAG not enabled")
    
    try:
        docs = vector_store.similarity_search_with_score(request.query, k=request.top_k)
        
        results = []
        for i, (doc, score) in enumerate(docs):
            results.append(RetrieveResult(
                id=f"chunk_{i}",
                text=doc.page_content,
                score=float(1 - score / 100),
                metadata={"source": doc.metadata.get("source", "unknown")}
            ))
        
        return RetrieveResponse(results=results)
        
    except Exception as e:
        logger.error(f"Retrieve error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sessions/{session_id}/history")
async def get_session_history(session_id: str):
    """Get conversation history for a session"""
    if session_id not in session_histories:
        return {"history": []}
    return {"history": session_histories[session_id]}

@app.delete("/api/sessions/{session_id}")
async def clear_session(session_id: str):
    """Clear session history"""
    if session_id in session_histories:
        del session_histories[session_id]
    return {"status": "cleared", "session_id": session_id}

# ========== WebSocket for Real-time ==========
@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()
    logger.info(f"WebSocket connected: {session_id}")
    
    try:
        while True:
            data = await websocket.receive_text()
            import json
            message = json.loads(data)
            
            msg_type = message.get("type", "")
            
            if msg_type == "message":
                user_text = message.get("text", "")
                normalized = normalize_text(user_text)
                context, sources = search_knowledge(normalized)
                reply = generate_response(normalized, context)
                
                # Stream response in chunks (simulate streaming)
                words = reply.split()
                for i in range(0, len(words), 3):
                    chunk = " ".join(words[i:i+3])
                    await websocket.send_json({
                        "type": "assistant_delta",
                        "delta": chunk
                    })
                    import asyncio
                    await asyncio.sleep(0.1)
                
                await websocket.send_json({
                    "type": "assistant_done",
                    "text": reply,
                    "sources": sources
                })
                
            elif msg_type == "control":
                action = message.get("action", "")
                if action == "interrupt":
                    await websocket.send_json({
                        "type": "info",
                        "msg": "Interrupted by user"
                    })
            elif msg_type == "audio":
                # Placeholder for audio processing
                await websocket.send_json({
                    "type": "partial_transcript",
                    "text": "Audio received, processing..."
                })
                
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected: {session_id}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")

# ========== Frontend ==========
@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    """Redirect root to the website landing page served as static content."""
    return RedirectResponse(url="/index.html")


# Serve website files (index.html, chat.html, assets, css, js) on same host/port.
# Keep this mount after API/WS route declarations.
app.mount("/", StaticFiles(directory=".", html=True), name="site")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8082)