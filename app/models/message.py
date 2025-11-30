from pydantic import BaseModel
from uuid import UUID

class SendMessage(BaseModel):
    message: str