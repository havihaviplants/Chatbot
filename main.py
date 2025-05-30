from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Dict
import shutil
import os

from pdf_utils import extract_pdf_text, answer_from_pdf
from gpt_utils import gpt_answer

app = FastAPI(
    title="PDF Q&A API",
    docs_url=None,         # Swagger UI 제거
    redoc_url=None,        # ReDoc 제거
    openapi_url=None       # OpenAPI spec 제거
)

templates = Jinja2Templates(directory="frontend")
pdf_path = "static/uploaded.pdf"
cached_text = ""

class QuestionRequest(BaseModel):
    question: str

@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload_pdf", response_model=Dict[str, str])
async def upload_pdf(file: UploadFile = File(...)):
    global cached_text
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

    try:
        with open(pdf_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        cached_text = extract_pdf_text(pdf_path)
        return {"status": "PDF 업로드 및 텍스트 추출 완료"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF 업로드 중 오류 발생: {e}")

@app.post("/ask", response_model=Dict[str, str])
async def ask_question(payload: QuestionRequest):
    global cached_text
    if not cached_text:
        raise HTTPException(status_code=400, detail="먼저 PDF를 업로드해야 합니다.")

    try:
        question = payload.question
        print(f"\n📥 질문 입력: {question}")
        print(f"📄 텍스트 길이: {len(cached_text)}자")

        context = answer_from_pdf(cached_text, question)

        if not context.strip():
            context = "이 문서는 업무 관련 문서입니다. 납기일은 일반적으로 마감 기한을 의미합니다."

        print(f"🧠 문맥 (300자 이내): {context[:300]}")
        gpt_response = gpt_answer(question, context)
        print(f"✅ GPT 응답: {gpt_response}")

        return {"answer": gpt_response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"GPT 응답 처리 중 오류 발생: {e}")
