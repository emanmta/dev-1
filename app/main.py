from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.routers import customer_service, restaurant, message, order
from fastapi_mcp import FastApiMCP
from app.core.middleware import SessionMiddleware

app = FastAPI(
    title="MCP-Ticket Forwarding Service",
    description="A microservice to validate and forward tickets to an internal backend.",
    version="0.1.0",
)

# Add the session middleware to handle global authentication
app.add_middleware(SessionMiddleware)

# Include the specific routers
app.include_router(restaurant.router)
app.include_router(customer_service.router)
app.include_router(message.router)
app.include_router(order.router)

@app.get("/")
async def root():
    """
    A simple root endpoint to confirm the service is running.
    """
    return {"status": "ok", "message": "MCP-Ticket Service is running"}

# This is the MCP wrapper around our existing FastAPI app
mcp_app = FastApiMCP(
    app,
    headers=["X-Session-Token"],
    include_tags=["Actions"]
)

# Add the MCP-specific endpoints (/mcp and /mcp/sse)
mcp_app.mount_http()
mcp_app.mount_sse()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    # Define the security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "XSessionToken": {
            "type": "apiKey",
            "in": "header",
            "name": "X-Session-Token",
            "description": "Enter your session token in the format: `X-Session-Token: <token>`"
        }
    }
    
    # Apply the security scheme globally to all paths
    openapi_schema["security"] = [{"XSessionToken": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
