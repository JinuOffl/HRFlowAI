# backend/models/chat.py
from pydantic import BaseModel
from typing import Optional, List

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default_user" # Added for context tracking

class ChatResponse(BaseModel):
    response: str
    charts: List[str] = []
    sql_debug: Optional[str] = None