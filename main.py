# main.py

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from models import ChatRequest, ChatResponse
from prompt_engine import build_prompt
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GPT 챗 엔드포인트
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    prompt = build_prompt(request.message)
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}],
        temperature=0.5
    )
    return {"response": response['choices'][0]['message']['content']}

# 정적 파일 서빙 (static 경로로 제공)
app.mount("/static", StaticFiles(directory="frontend", html=True), name="static")

# 루트 요청 시 index.html 직접 반환
@app.get("/")
async def serve_index():
    file_path = os.path.join(os.path.dirname(__file__), "frontend", "index.html")
    return FileResponse(file_path)
