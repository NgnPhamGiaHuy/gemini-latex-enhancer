"""
Main FastAPI application for the CV Enhancement API.

Responsibilities:
- Configure app lifecycle (startup/shutdown) and directory housekeeping
- Register API routes for upload, enhance, download, and models
- Provide simple health endpoints for uptime monitoring
"""

import atexit
import uvicorn
import warnings
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# Suppress specific warnings
warnings.filterwarnings(
    "ignore", message='Field "model_id" has conflict with protected namespace "model_"'
)
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

from app.routes import upload, enhance, download, models
from app.config import settings
from app.services.cleanup_service import FileCleanupService
from app.utils.logger import get_logger

logger = get_logger(__name__)


# Lifespan event handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown"""
    # Startup
    logger.info("=== CV ENHANCEMENT API STARTING UP ===")

    # Clean up any existing files from previous runs
    FileCleanupService.cleanup_all_directories()

    # Ensure directories exist
    FileCleanupService.ensure_directories_exist()

    logger.info("=== CV ENHANCEMENT API STARTUP COMPLETED ===")

    yield

    # Shutdown
    logger.info("=== CV ENHANCEMENT API SHUTTING DOWN ===")

    # Clean up temporary files
    FileCleanupService.cleanup_all_directories()

    logger.info("=== CV ENHANCEMENT API SHUTDOWN COMPLETED ===")


# Create FastAPI app with lifespan
app = FastAPI(
    title="CV Enhancement API",
    description="AI-powered LaTeX CV enhancement tool",
    version="1.0.0",
    lifespan=lifespan,
)


# Register cleanup function for unexpected shutdowns
def cleanup_on_exit():
    """Cleanup function for unexpected shutdowns"""
    logger.info("=== CLEANUP ON EXIT TRIGGERED ===")
    FileCleanupService.cleanup_all_directories()


atexit.register(cleanup_on_exit)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router, prefix="/api", tags=["upload"])
app.include_router(enhance.router, prefix="/api", tags=["enhance"])
app.include_router(download.router, prefix="/api", tags=["download"])
app.include_router(models.router, prefix="/api", tags=["models"])

# Mount static files for outputs
# Note: Directory creation is handled by startup event; avoid requiring it at import time
app.mount(
    "/outputs",
    StaticFiles(directory=settings.OUTPUT_DIR, check_dir=False),
    name="outputs",
)


@app.get("/")
async def root():
    """Root health endpoint.

    Returns:
        Dict with a status message and semantic version string.
    """
    return {"message": "CV Enhancement API is running", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    """Simple health endpoint for liveness checks.

    Returns:
        Dict with `status` set to "healthy".
    """
    return {"status": "healthy"}


@app.post("/cleanup")
async def manual_cleanup():
    """Trigger cleanup of temporary files (primarily for testing).

    Returns:
        Dict with a success message upon completion.
    """
    logger.info("=== MANUAL CLEANUP REQUESTED ===")
    FileCleanupService.cleanup_all_directories()
    return {"message": "Cleanup completed successfully"}


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app", host="0.0.0.0", port=8000, reload=True, log_level="info"
    )
