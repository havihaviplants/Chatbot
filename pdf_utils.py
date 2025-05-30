import fitz  # PyMuPDF
import re

def extract_pdf_text(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def answer_from_pdf(text, question):
    question = question.lower()

    # 키워드 매핑 예시
    if "납기" in question or "언제 받을 수 있나요" in question:
        match = re.search(r'납기.*?(?=\n|$)', text, re.IGNORECASE)
        return match.group() if match else "납기 관련 내용이 명확하지 않습니다."

    elif "할인" in question:
        match = re.search(r'(할인.*?)\n', text, re.IGNORECASE)
        return match.group() if match else "할인 관련 정보를 찾을 수 없습니다."

    elif "포장" in question or "opp" in question or "박스" in question:
        match = re.search(r'(박스.*?포장.*?)\n', text, re.IGNORECASE)
        return match.group() if match else "포장 관련 설명이 없습니다."

    else:
        return "질문을 이해하지 못했습니다. 다시 말씀해 주세요."

from PyPDF2 import PdfReader
import re

def extract_pdf_text(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def answer_from_pdf(text: str, question: str) -> str:
    raw_paragraphs = re.split(r'(?<=[.?!])\s*\n+|\n{2,}', text.strip())
    keywords = [kw for kw in question.lower().split() if len(kw) > 1]
    relevant_paragraphs = [
        para.strip() for para in raw_paragraphs
        if any(kw in para.lower() for kw in keywords)
    ]
    context = '\n\n'.join(relevant_paragraphs)
    if len(context) > 1500:
        context = context[:1500].rsplit('\n', 1)[0]
    if not context.strip():
        context = text[:1000].rsplit('\n', 1)[0]
    return context
