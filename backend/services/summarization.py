import os
from groq import Groq
from backend.utils.helpers import hash_sensitive_data, de_anonymize
import pandas as pd

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def summarize_analysis(df: pd.DataFrame, query_context: str) -> str:
    if df.empty:
        return "No data found to analyze."

    # 1. Create a copy to anonymize
    safe_df = df.copy()
    
    # 2. Hash sensitive columns if they exist
    sensitive_cols = ['first_name', 'last_name', 'official_email', 'phone']
    for col in sensitive_cols:
        if col in safe_df.columns:
            safe_df[col] = safe_df[col].apply(hash_sensitive_data)

    # 3. Convert to CSV/String for LLM
    data_str = safe_df.to_string(index=False)
    
    prompt = f"""
    Analyze the following attendance data based on the query: "{query_context}".
    Data:
    {data_str}
    
    Task:
    1. Identify trends (late arrivals, average hours, leave frequency).
    2. Calculate an 'Engagement Score' if work hours are available.
    3. Do NOT mention specific hash tokens (e.g., EMP_...) in the final output, refer to them as "Employee".
    4. Provide a professional HR summary.
    """
    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )
    
    raw_summary = completion.choices[0].message.content
    
    # 4. De-anonymize the result before returning to UI
    final_summary = de_anonymize(raw_summary)
    
    return final_summary