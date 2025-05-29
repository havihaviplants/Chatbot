# gpt_handler.py
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_gpt(message: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # ← 여기만 바꾸면 됨
        messages=[
            {"role": "user", "content": message}
        ],
        temperature=0.7,
        max_tokens=500
    )
    return response.choices[0].message["content"]
