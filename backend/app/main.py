"""
Main FastAPI application for the CV Enhancement API.

Responsibilities:
- Configure application lifecycle (startup/shutdown) and directory housekeeping
- Register API routes for upload, enhance, download, and models
- Provide simple health endpoints for uptime monitoring
"""

import atexit
import uvicorn
import warnings
from fastapi import FastAPI, Depends
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
from app.application.contracts.cleanup_service import CleanupService
from app.interface.di import get_cleanup_service
from app.utils.logger import get_logger

logger = get_logger(__name__)


# Lifespan event handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown."""
    # Startup
    logger.info("=== CV ENHANCEMENT API STARTING UP ===")

    # Get cleanup service via DI
    cleanup_service = get_cleanup_service()

    # Clean up any existing files from previous runs
    cleanup_service.cleanup_all_directories()

    # Clean up old session log files if configured
    if settings.CLEANUP_SESSION_LOGS_ON_STARTUP:
        logger.info("Cleaning up old session log files on startup...")
        cleanup_service.cleanup_old_session_logs(settings.SESSION_LOG_RETENTION_DAYS)

    # Clean up old session output files if configured
    if settings.CLEANUP_SESSION_OUTPUTS_ON_STARTUP:
        logger.info("Cleaning up old session output files on startup...")
        cleanup_service.cleanup_old_session_outputs(
            settings.SESSION_OUTPUT_RETENTION_DAYS
        )

    # Ensure directories exist
    cleanup_service.ensure_directories_exist()

    logger.info("=== CV ENHANCEMENT API STARTUP COMPLETED ===")

    yield

    # Shutdown
    logger.info("=== CV ENHANCEMENT API SHUTTING DOWN ===")

    # Clean up temporary files
    cleanup_service.cleanup_all_directories()

    # Clean up session log files if configured
    if settings.CLEANUP_SESSION_LOGS_ON_SHUTDOWN:
        logger.info("Cleaning up session log files on shutdown...")
        cleanup_service.cleanup_session_logs_directory()

    # Clean up session output files if configured
    if settings.CLEANUP_SESSION_OUTPUTS_ON_SHUTDOWN:
        logger.info("Cleaning up session output files on shutdown...")
        cleanup_service.cleanup_session_outputs_directory()

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
    """Cleanup function for unexpected shutdowns."""
    logger.info("=== CLEANUP ON EXIT TRIGGERED ===")
    cleanup_service = get_cleanup_service()
    cleanup_service.cleanup_all_directories()

    # Clean up session log files if configured
    if settings.CLEANUP_SESSION_LOGS_ON_SHUTDOWN:
        logger.info("Cleaning up session log files on unexpected exit...")
        cleanup_service.cleanup_session_logs_directory()

    # Clean up session output files if configured
    if settings.CLEANUP_SESSION_OUTPUTS_ON_SHUTDOWN:
        logger.info("Cleaning up session output files on unexpected exit...")
        cleanup_service.cleanup_session_outputs_directory()


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

# Mount static files for session outputs
# Note: Directory creation is handled by startup event; avoid requiring it at import time
app.mount(
    "/session-outputs",
    StaticFiles(directory=settings.SESSION_OUTPUT_DIR, check_dir=False),
    name="session-outputs",
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
async def manual_cleanup(
    cleanup_service: CleanupService = Depends(get_cleanup_service),
):
    """Trigger cleanup of temporary files (primarily for testing).

    Returns:
        Dict with a success message upon completion.
    """
    logger.info("=== MANUAL CLEANUP REQUESTED ===")
    cleanup_service.cleanup_all_directories()
    return {"message": "Cleanup completed successfully"}


@app.post("/cleanup/session-logs")
async def manual_session_log_cleanup(
    cleanup_service: CleanupService = Depends(get_cleanup_service),
):
    """
    Manual session log cleanup endpoint for development and maintenance.

    Returns:
        Dict with a success message.
    """
    logger.info("=== MANUAL SESSION LOG CLEANUP TRIGGERED ===")
    cleanup_service.cleanup_session_logs_directory()

    return {"message": "Session log cleanup completed successfully"}


@app.post("/cleanup/session-outputs")
async def manual_session_output_cleanup(
    cleanup_service: CleanupService = Depends(get_cleanup_service),
):
    """
    Manual session output cleanup endpoint for development and maintenance.

    Returns:
        Dict with a success message.
    """
    logger.info("=== MANUAL SESSION OUTPUT CLEANUP TRIGGERED ===")
    cleanup_service.cleanup_session_outputs_directory()

    return {"message": "Session output cleanup completed successfully"}


@app.post("/cleanup/session-outputs/old")
async def manual_old_session_output_cleanup(
    days_to_keep: int = 7,
    cleanup_service: CleanupService = Depends(get_cleanup_service),
):
    """
    Manual old session output cleanup endpoint for development and maintenance.

    Args:
        days_to_keep: Number of days to keep session output files (default: 7)

    Returns:
        Dict with a success message.
    """
    logger.info(
        f"=== MANUAL OLD SESSION OUTPUT CLEANUP TRIGGERED (keeping {days_to_keep} days) ==="
    )
    cleanup_service.cleanup_old_session_outputs(days_to_keep)

    return {
        "message": f"Old session output cleanup completed successfully (kept {days_to_keep} days)"
    }


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app", host="0.0.0.0", port=8000, reload=True, log_level="info"
    )
