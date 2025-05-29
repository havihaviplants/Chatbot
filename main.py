# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import ChatRequest, ChatResponse
from prompt_engine import build_prompt
import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# CORS 설정 (필요 시 수정)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    prompt = build_prompt(request.message)
    
    response = openai.ChatCompletion.create(
        model="gpt-4",  # 필요 시 gpt-3.5-turbo로 변경
        messages=[{"role": "system", "content": prompt}],
        temperature=0.5
    )
    return {"response": response['choices'][0]['message']['content']}

from fastapi.staticfiles import StaticFiles

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

from fastapi.responses import FileResponse
from fastapi import Request

@app.get("/")
async def serve_index(request: Request):
    return FileResponse("frontend/index.html")

