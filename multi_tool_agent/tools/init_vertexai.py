import os
import vertexai
from dotenv import load_dotenv

_vertexai_initialized = False

def init_vertexai():
    """
    Guardrail method to ensure vertexai is only
    initiated once per server spin up, NOT per
    user session.
    """
    global _vertexai_initialized
    if _vertexai_initialized:
        return
    
    load_dotenv()

    project_id = os.environ.get("VECTOR_DB_PROJECT")
    location = os.environ.get("VECTOR_DB_LOCATION")

    if project_id and location:
        vertexai.init(project=project_id, location=location)
    else:
        raise RuntimeError("Vertexxai missing project_id and location env vars.")

    _vertexai_initialized = True
    
