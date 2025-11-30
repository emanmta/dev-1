from pydantic import BaseModel
from uuid import UUID

class SendMessage(BaseModel):
    x_session_token: str
    message: str