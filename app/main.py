from fastapi import FastAPI
from app.routers import restaurant, complaint, message
from fastapi_mcp import FastApiMCP

app = FastAPI(
    title="MCP-Ticket Forwarding Service",
    description="A microservice to validate and forward tickets to an internal backend.",
    version="0.1.0",  # Version updated to reflect specific endpoint architecture
)

# Include the specific routers
app.include_router(restaurant.router)
app.include_router(complaint.router)
app.include_router(message.router)

@app.get("/")
async def root():
    """
    A simple root endpoint to confirm the service is running.
    """
    return {"status": "ok", "message": "MCP-Ticket Service is running"}

# This is the MCP wrapper around our existing FastAPI app
mcp_app = FastApiMCP(app)

# Add the MCP-specific endpoints (/mcp and /mcp/sse)
mcp_app.mount_http()
mcp_app.mount_sse()
