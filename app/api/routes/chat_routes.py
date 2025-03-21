from fastapi import APIRouter, HTTPException

from app.config import Config
import google.generativeai as genai
from pydantic import BaseModel

chat_bp = APIRouter()

GEMINI_API_KEY = Config.GEMINI_API_KEY
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.0-flash")
chat = model.start_chat(history=[])


class Question(BaseModel):
    question: str

@chat_bp.post("/ask")
async def ask_question(q: Question):
    try:
        response = model.generate_content(q.question)
        answer = response.text
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@chat_bp.post("/chat")
async def chat_with_gemini(q: Question):
    try:
        response = chat.send_message(q.question)
        answer = response.text

        history = [
            {"role": msg.role, "text": msg.parts[0].text}
            for msg in chat.history
        ]

        return {
            "answer": answer,
            "history": history
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))