from pydantic import BaseModel
from uuid import UUID

class SendMessage(BaseModel):
    session_id: UUID
    message: str