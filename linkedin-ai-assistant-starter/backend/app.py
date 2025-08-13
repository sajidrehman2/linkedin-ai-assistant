import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
from dotenv import load_dotenv

from llm_client import complete
from prompts import SYSTEM_PROMPT

load_dotenv()
PORT = int(os.getenv("PORT", "8000"))

app = FastAPI(title="LinkedIn AI Assistant (Local)")

# CORS for Streamlit and Chrome extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501", "chrome-extension://*","http://localhost:3000","http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SuggestRequest(BaseModel):
    conversation: str = Field(..., description="Conversation text or last message")
    tone: str = Field("neutral", description="e.g., friendly, formal, concise")
    language: str = Field("English", description="Language to write the reply in")
    max_words: int = Field(120, ge=30, le=400)

class SuggestResponse(BaseModel):
    reply_text: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/suggest_reply", response_model=SuggestResponse)
def suggest_reply(req: SuggestRequest):
    if not req.conversation.strip():
        raise HTTPException(status_code=400, detail="Conversation is empty")

    system = {"role": "system", "content": SYSTEM_PROMPT}
    user_prompt = f"""Conversation:
---
{req.conversation.strip()}
---
Write a single reply in {req.language}. Tone: {req.tone}.
Aim for under {req.max_words} words unless brevity harms clarity.
"""

    msgs = [system, {"role": "user", "content": user_prompt}]
    try:
        text = complete(msgs, temperature=0.5, max_tokens=500)
        return {"reply_text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class SummarizeRequest(BaseModel):
    text: str
    language: str = "English"
    bullets: int = 5

class SummarizeResponse(BaseModel):
    summary: str

@app.post("/summarize", response_model=SummarizeResponse)
def summarize(req: SummarizeRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Text is empty")

    system = {"role": "system", "content": "You summarize LinkedIn conversations crisply in bullets."}
    user = {"role": "user", "content": f"Summarize in {req.language} as {req.bullets} bullets:\n{req.text.strip()}"}
    try:
        text = complete([system, user], temperature=0.4, max_tokens=400)
        return {"summary": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Run via: uvicorn main:app --reload --port 8000