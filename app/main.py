from fastapi import FastAPI, Depends
from app.routers import customer_service, restaurant, message, order
from fastapi_mcp import FastApiMCP
from app.core.dependencies import validate_bearer_token

app = FastAPI(
    title="MCP-Ticket Forwarding Service",
    description="A microservice to validate and forward tickets to an internal backend.",
    version="0.1.0",  # Version updated to reflect specific endpoint architecture
)

# Include the specific routers
app.include_router(restaurant.router, dependencies=[Depends(validate_bearer_token)])
app.include_router(customer_service.router, dependencies=[Depends(validate_bearer_token)])
app.include_router(message.router, dependencies=[Depends(validate_bearer_token)])
app.include_router(order.router, dependencies=[Depends(validate_bearer_token)])

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
