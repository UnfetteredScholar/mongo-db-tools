from api.v1.routers import database
from core.config import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_mcp import FastApiMCP

# Create main FastAPI app
app = FastAPI(title=settings.APP_TITLE)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS.split(","),
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
)


# Include all app routers
app.include_router(database.router, prefix=settings.API_V1_STR, tags=["database"])

# Mount MCP
mcp = FastApiMCP(app)
mcp.mount_http(mount_path="/streamable-http/mcp")
