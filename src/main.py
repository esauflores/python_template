"""
Main FastAPI application module.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Python Template API",
    description="A FastAPI application template",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint."""
    return {"message": "Hello World", "status": "OK"}


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint for Docker health checks."""
    return {"status": "healthy", "service": "python-template"}


@app.get("/api/v1/status")
async def api_status() -> dict[str, str]:
    """API status endpoint."""
    return {"api_version": "v1", "status": "running", "message": "API is operational"}
