# backend/utils/helpers.py
import hashlib

# In-memory store for de-anonymization (Use Redis in production)
_hash_map = {}

def hash_sensitive_data(text: str) -> str:
    """Hashes a string (SHA-256) and stores the mapping."""
    if not text:
        return ""
    
    text_str = str(text)
    # Generate SHA-256 hash
    hashed_val = hashlib.sha256(text_str.encode()).hexdigest()
    
    # Create a token that looks like an ID but is opaque
    # We use first 10 chars to keep it readable for the LLM
    token = f"EMP_{hashed_val[:10]}"
    
    # Store reverse mapping
    _hash_map[token] = text_str
    
    return token

def de_anonymize(text: str) -> str:
    """Replaces hash tokens with original values."""
    if not text:
        return ""
    
    # Simple replace for MVP
    # Ideally, extract tokens via regex and look up
    result = text
    for token, original in _hash_map.items():
        result = result.replace(token, original)
        
    return result

def get_schema_string():
    # Return your DDL statements here for the LLM context
    return """
    CREATE TABLE employees (uuid text, first_name text, last_name text, official_email text, job_role text);
    CREATE TABLE attendance_records (uuid text, employee_id text, date text, check_in_time text, check_out_time text, status text);
    """