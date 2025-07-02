import os
import re
from dotenv import load_dotenv
from openai import OpenAI


def gpt_answer(question: str, context: str) -> str:
    """
    GPT 응답 생성 (PDF 문서 기반 질문 응답용)
    최신 openai 라이브러리 호환 (openai>=1.3.0)
    """

    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("❌ OPENAI_API_KEY 누락")

    client = OpenAI(api_key=api_key)

    prompt = f"""
당신은 고객 응대를 돕는 AI 어시스턴트입니다.
다음은 내부 PDF 문서에서 추출한 참고 정보입니다. 이 정보를 기반으로 사용자의 질문에 성실히 답변해주세요.

[참고 문서 요약]
{context}

[사용자 질문]
{question}

[답변 형식 가이드]
- 문서 내용 기반으로만 답하세요
- 모호할 경우, 가능한 내용을 추정해 안내하고 '정확하지 않을 수 있다'고 고지하세요
- 답을 모를 경우 '정보가 부족하다'고만 말하세요
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=512,
        )

        return f"📄 PDF 기반 응답입니다:\n\n{response.choices[0].message.content.strip()}"

    except Exception as e:
        return f"❌ GPT 호출 오류: {str(e)}"


def answer_from_pdf(text: str, question: str) -> str:
    """
    질문과 관련된 문맥을 PDF 텍스트에서 추출하여 GPT 입력용으로 반환
    """

    # 1. 문단 분리: 빈 줄 또는 마침표 후 줄바꿈 기준
    raw_paragraphs = re.split(r'(?<=[.?!])\s*\n+|\n{2,}', text.strip())

    # 2. 질문 키워드 추출 (단어 길이 2 이상, 소문자 처리)
    keywords = [kw for kw in question.lower().split() if len(kw) > 1]

    # 3. 관련 문단 추출 (키워드 포함된 문단)
    relevant_paragraphs = [
        para.strip() for para in raw_paragraphs
        if any(kw in para.lower() for kw in keywords)
    ]

    # 4. 관련 문단 합치기 (최대 1500자 제한)
    context = '\n\n'.join(relevant_paragraphs)
    if len(context) > 1500:
        context = context[:1500].rsplit('\n', 1)[0]  # 문단 중간 자르지 않도록 마지막 줄 정리

    # 5. 대체 문맥: 없을 경우 텍스트 앞부분 사용
    if not context.strip():
        context = text[:1000].rsplit('\n', 1)[0]

    return context
