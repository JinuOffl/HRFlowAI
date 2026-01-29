# backend/main.py
from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from fastapi.middleware.cors import CORSMiddleware

# Imports from your new files
from backend.core.config import settings
from backend.models.db import init_db, get_engine
from backend.models.chat import ChatRequest, ChatResponse
from backend.services.nl2sql import generate_sql
from backend.services.analysis import analyze_and_visualize
from backend.services.summarization import summarize_analysis
from backend.services.context import add_to_history, format_history_for_prompt

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    try:
        session_id = req.session_id
        
        # 1. Get Context (History)
        history_context = format_history_for_prompt(session_id)
        full_prompt = f"{history_context}\nCurrent Question: {req.message}"
        
        # 2. NL2SQL (Pass history context if needed, or just current query)
        # For simple lookup, current query often suffices, but context helps disambiguation
        sql_query = generate_sql(full_prompt)
        
        # 3. DB Execution
        engine = get_engine()
        with engine.connect() as conn:
            # Safety: Ensure it's a SELECT statement
            if not sql_query.strip().upper().startswith("SELECT"):
                raise HTTPException(status_code=400, detail="Invalid query type generated.")
                
            result = conn.execute(text(sql_query))
            rows = result.fetchall()
            keys = result.keys()
            data = [dict(zip(keys, row)) for row in rows]
            
        # 4. Save User Query to History
        add_to_history(session_id, "user", req.message)

        if not data:
            resp_text = "I couldn't find any data matching your criteria."
            add_to_history(session_id, "assistant", resp_text)
            return {"response": resp_text, "charts": [], "sql_debug": sql_query}

        # 5. Analyze & Visualize
        df, charts = analyze_and_visualize(data)
        
        # 6. Summarize
        summary = summarize_analysis(df, req.message)
        
        # 7. Save AI Response to History
        add_to_history(session_id, "assistant", summary)
        
        return {
            "response": summary,
            "charts": charts,
            "sql_debug": sql_query
        }
        
    except Exception as e:
        print(f"Error: {e}")
        return {"response": "I encountered an error processing your request.", "charts": [], "sql_debug": str(e)}

@app.get("/suggest_names")
async def suggest_names(prefix: str):
    engine = get_engine()
    with engine.connect() as conn:
        # Secure parameterized query
        query = text("SELECT first_name, last_name FROM employees WHERE first_name LIKE :p OR last_name LIKE :p LIMIT 5")
        result = conn.execute(query, {"p": f"{prefix}%"}).fetchall()
        
    suggestions = [f"@{row[0]}{row[1]}" for row in result] # Format as @Name
    return suggestions