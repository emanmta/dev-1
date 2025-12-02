from pydantic import BaseModel
from typing import Optional, Dict, Any

class WahaWebhook(BaseModel):
    id: str
    timestamp: int
    session: str
    metadata: Any = None
    engine: str
    event: str
    payload: Dict[str, Any]
    me: Dict[str, Any]
    environment: Dict[str, Any]
    version: str
    tier: Any = None
    browser: Any = None