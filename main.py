from fastapi import FastAPI, Body
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv

# 🔹 .env에서 API 키 로드
load_dotenv()

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest = Body(...)):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": req.message}]
        )
        answer = completion['choices'][0]['message']['content']
        return ChatResponse(response=answer)

    except Exception as e:
        return ChatResponse(response=f"오류 발생: {str(e)}")
