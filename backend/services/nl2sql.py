import os
from groq import Groq
from backend.utils.helpers import get_schema_string

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def generate_sql(user_query: str) -> str:
    schema = get_schema_string()
    prompt = f"""
    You are an expert SQL generator for a SQLite database.
    Schema:
    {schema}
    
    Question: {user_query}
    
    Rules:
    1. Return ONLY the raw SQL query. No markdown, no explanations.
    2. Use 'LIKE' for name matching (case insensitive).
    3. Join tables where necessary (employees.uuid = attendance_records.employee_id).
    
    SQL:
    """
    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        stop=None
    )
    
    sql = completion.choices[0].message.content.strip()
    # Cleanup if LLM wraps in markdown
    sql = sql.replace("```sql", "").replace("```", "")
    return sql