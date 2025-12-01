from pydantic import BaseModel

class MCPBase(BaseModel):
    """
    A base model for MCP proxy requests that only require a session token.
    """
    session_token: str