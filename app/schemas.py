from pydantic import BaseModel
from typing import Optional

class GenerateRequest(BaseModel):
    prompt: str
    top_text: Optional[str] = None
    bottom_text: Optional[str] = None
