# backend/services/context.py
from datetime import datetime

# Simple in-memory store for MVP. 
# Key = user_id (or session_id), Value = List of messages
session_store = {}

MAX_HISTORY = 5

def get_session_history(session_id: str) -> list:
    """Retrieve chat history for context."""
    return session_store.get(session_id, [])

def add_to_history(session_id: str, role: str, message: str):
    """Add a message to the session history."""
    if session_id not in session_store:
        session_store[session_id] = []
    
    session_store[session_id].append({
        "role": role,
        "content": message,
        "timestamp": datetime.now()
    })
    
    # Keep only last N messages to save tokens
    if len(session_store[session_id]) > MAX_HISTORY:
        session_store[session_id] = session_store[session_id][-MAX_HISTORY:]

def format_history_for_prompt(session_id: str) -> str:
    """Formats history into a string for the LLM prompt."""
    history = get_session_history(session_id)
    if not history:
        return ""
    
    formatted = "Previous conversation:\n"
    for msg in history:
        formatted += f"{msg['role'].capitalize()}: {msg['content']}\n"
    return formatted