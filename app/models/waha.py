from pydantic import BaseModel
from typing import Optional, Dict, Any

class WahaWebhook(BaseModel):
    id: str
    timestamp: int
    session: str
    metadata: Optional[Dict[str, Any]] = None
    engine: str
    event: str
    payload: Dict[str, Any]
    me: Dict[str, Any]
    environment: Dict[str, Any]
    version: str
    tier: Optional[str] = None
    browser: Optional[str] = None