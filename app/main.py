import os

import google.generativeai as genai
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

load_dotenv()  # Tự động tìm và load file .env
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.0-flash")
chat = model.start_chat(history=[])

class Question(BaseModel):
    question: str

# Nhận câu hỏi và trả về câu trả lời từ Gemini
@app.post("/ask")
async def ask_question(q: Question):
    try:
        response = model.generate_content(q.question)
        answer = response.text
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
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
