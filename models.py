# models.py
from pydantic import BaseModel

class QuestionRequest(BaseModel):
    message: str
