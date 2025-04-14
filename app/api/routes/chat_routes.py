import asyncio
import json
import re
from typing import AsyncGenerator

import google.generativeai as genai
import requests
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.config import Config
from app.schemas.message_schema import CreateMessageSchema
from app.services.message_service import MessageService

chat_bp = APIRouter()

GEMINI_API_KEY = Config.GEMINI_API_KEY
OPENROUTER_API_KEY = Config.OPENROUTER_API_KEY

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


@chat_bp.post("/gemini/chat")
def chat_with_gemini(q: Question):
    try:
        # Lấy lịch sử 10 tin nhắn gần nhất của cuộc hội thoại
        history = MessageService.get_history(q.conv_id)
        history.reverse()

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


@chat_bp.post("/gemini/stream")
async def stream_chat_with_gemini(q: Question):
    try:
        # Lấy lịch sử 10 tin nhắn gần nhất của cuộc hội thoại
        history = MessageService.get_history(q.conv_id)
        history.reverse()

        # Chuyển lịch sử tin nhắn thành một chuỗi hội thoại
        gemini_history = []
        for msg in history:
            gemini_history.append({"role": "user", "parts": [msg["question"]]})
            gemini_history.append({"role": "model", "parts": [msg["answer"]]})

        chat = model.start_chat(history=gemini_history)
        response = chat.send_message(q.question)
        full_answer = response.text

        words = re.findall(r'\S+|\n', full_answer)  # Giữ dấu xuống dòng riêng

        async def generate():
            buffer = []
            for word in words:
                buffer.append(word)
                if len(buffer) >= 1:
                    chunk = ' '.join(buffer) + ' '
                    yield chunk.encode("utf-8")
                    buffer.clear()
                    await asyncio.sleep(0.04)  # 25 từ mỗi giây

            if buffer:
                yield (' '.join(buffer)).encode("utf-8")

            # Lưu lại câu hỏi và câu trả lời
            MessageService.create_message(
                CreateMessageSchema(conversation_id=q.conv_id, question=q.question, answer=full_answer)
            )

        return StreamingResponse(generate(), media_type="text/event-stream")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@chat_bp.post("/llama/stream")
async def stream_chat_with_llama(request: Question):
    try:
        history = MessageService.get_history(request.conv_id)
        history.reverse()

        messages = []
        for msg in history:
            messages.append({
                "role": "user",
                "content": msg["question"]
            })
            messages.append({
                "role": "assistant",
                "content": msg["answer"]
            })

        # Thêm câu hỏi mới nhất
        messages.append({
            "role": "user",
            "content": request.question
        })

        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": "Bearer " + OPENROUTER_API_KEY,
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "model": "meta-llama/llama-4-maverick:free",
                "messages": messages,
            })
        )

        parsed = response.json()
        full_answer = parsed["choices"][0]["message"]["content"]

        words = re.findall(r'\S+|\n', full_answer)

        async def generate():
            buffer = []
            for word in words:
                buffer.append(word)
                if len(buffer) >= 1:
                    chunk = ' '.join(buffer) + ' '
                    yield chunk.encode("utf-8")
                    buffer.clear()
                    await asyncio.sleep(0.04)  # 25 từ mỗi giây

            if buffer:
                yield (' '.join(buffer)).encode("utf-8")

            MessageService.create_message(
                CreateMessageSchema(conversation_id=request.conv_id, question=request.question, answer=full_answer)
            )

        return StreamingResponse(generate(), media_type="text/event-stream")

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with the AIML API: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


@chat_bp.post("/deepseek/stream")
async def stream_chat_with_deepseek(request: Question):
    try:

        history = MessageService.get_history(request.conv_id)
        history.reverse()

        messages = []
        for msg in history:
            messages.append({
                "role": "user",
                "content": msg["question"]
            })
            messages.append({
                "role": "assistant",
                "content": msg["answer"]
            })

        # Thêm câu hỏi mới nhất
        messages.append({
            "role": "user",
            "content": request.question
        })

        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": "Bearer " + OPENROUTER_API_KEY,
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "model": "deepseek/deepseek-r1:free",
                "messages": messages,
            })
        )

        parsed = response.json()
        full_answer = parsed["choices"][0]["message"]["content"]

        words = re.findall(r'\S+|\n', full_answer)  # Giữ dấu xuống dòng riêng

        async def generate():
            buffer = []
            for word in words:
                buffer.append(word)
                if len(buffer) >= 1:
                    chunk = ' '.join(buffer) + ' '
                    yield chunk.encode("utf-8")
                    buffer.clear()
                    await asyncio.sleep(0.04)  # 25 từ mỗi giây

            if buffer:
                yield (' '.join(buffer)).encode("utf-8")

            MessageService.create_message(
                CreateMessageSchema(conversation_id=request.conv_id, question=request.question, answer=full_answer)
            )

        return StreamingResponse(generate(), media_type="text/event-stream")


    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

