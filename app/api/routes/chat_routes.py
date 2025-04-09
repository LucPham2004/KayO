from typing import AsyncGenerator

import google.generativeai as genai
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.config import Config
from app.schemas.message_schema import CreateMessageSchema
from app.services.message_service import MessageService

chat_bp = APIRouter()

GEMINI_API_KEY = Config.GEMINI_API_KEY
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.0-flash")
chat = model.start_chat(history=[])

class Question(BaseModel):
    conv_id: str
    question: str

async def generate_response_stream(prompt: str) -> AsyncGenerator[str, None]:
    response_stream = model.generate_content(prompt, stream=True)
    for chunk in response_stream:
        yield chunk.text


@chat_bp.post("/chat")
def chat_with_gemini(q: Question):
    try:
        # Lấy lịch sử 10 tin nhắn gần nhất của cuộc hội thoại
        history = MessageService.get_history(q.conv_id)

        # Chuyển lịch sử tin nhắn thành một chuỗi hội thoại
        history_str = "\n".join([f"{msg['question']} → {msg['answer']}" for msg in history])

        # Gửi lịch sử + câu hỏi mới
        prompt = f"{history_str}\nUser: {q.question}\nAI:"
        response = chat.send_message(prompt)
        answer = response.text

        # Lưu tin nhắn vào db
        MessageService.create_message(
            CreateMessageSchema(conversation_id=q.conv_id, question=q.question, answer=answer)
        )

        return {
            "question": q,
            "answer": answer
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@chat_bp.post("/chat/stream")
async def stream_chat_with_gemini(q: Question):
    try:
        # Lấy lịch sử 10 tin nhắn gần nhất của cuộc hội thoại
        history = MessageService.get_history(q.conv_id)

        # Chuyển lịch sử tin nhắn thành một chuỗi hội thoại
        history_str = "\n".join([f"{msg['question']} → {msg['answer']}" for msg in history])

        # Gửi lịch sử + câu hỏi mới
        prompt = f"{history_str}\nUser: {q.question}\nAI:"
        async def generate():
            full_answer = ""
            async for chunk in generate_response_stream(prompt):
                full_answer += chunk
                yield chunk.encode("utf-8")

            MessageService.create_message(
                CreateMessageSchema(conversation_id=q.conv_id, question=q.question, answer=full_answer)
            )

        return StreamingResponse(generate(), media_type="text/event-stream")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
