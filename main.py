from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PyPDF2 import PdfReader
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv

load_dotenv()  # .env 파일에서 OPENAI_API_KEY 로드

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = os.getenv("OPENAI_API_KEY")
pdf_context = ""

class Question(BaseModel):
    question: str

@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    global pdf_context
    try:
        reader = PdfReader(file.file)
        pdf_context = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                pdf_context += text
        if not pdf_context.strip():
            raise HTTPException(status_code=400, detail="PDF에서 텍스트를 추출할 수 없습니다.")
        return {"message": "PDF 업로드 및 파싱 완료"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF 처리 중 오류: {str(e)}")

@app.post("/ask")
async def ask_question(data: Question):
    global pdf_context
    if not pdf_context.strip():
        raise HTTPException(status_code=400, detail="먼저 PDF 파일을 업로드해주세요.")
    prompt = f"다음 문맥을 기반으로 질문에 대답해줘.\n\n문맥:\n{pdf_context}\n\n질문: {data.question}"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "다음 문맥을 기반으로 질문에 대답해줘."},
                {"role": "user", "content": prompt}
            ]
        )
        answer = response.choices[0].message["content"].strip()
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"GPT 오류: {str(e)}")
