from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Callable

from app.application.contracts import CleanupService, ModelService
from app.application.use_cases.batch_enhance import BatchEnhanceUseCase
from app.application.use_cases.enhance_cv import EnhanceCvUseCase
from app.application.use_cases.parse_job_file import ParseJobFileUseCase
from app.application.use_cases.save_and_compile import SaveAndCompileUseCase
from app.application.use_cases.upload_cv import UploadCvUseCase
from app.config import settings
from app.infrastructure.ai.gemini_cv_enhancer import GeminiCvEnhancer, GeminiClient
from app.infrastructure.ai.model_service_adapter import GeminiModelService
from app.infrastructure.file_system.local_file_storage import LocalFileStorage
from app.infrastructure.latex.lualatex_compiler import LualatexCompiler
from app.infrastructure.maintenance.cleanup_service_adapter import LocalCleanupService
from app.infrastructure.output.local_output_packager import LocalOutputPackager
from app.infrastructure.parsers.job_file_parser import CsvJsonJobParser
from app.infrastructure.persistence.in_memory_progress_tracker import (
    InMemoryProgressTracker,
)


@lru_cache(maxsize=1)
def get_cv_enhancer() -> GeminiCvEnhancer:
    return create_cv_enhancer(settings.AI_MODEL)


def create_cv_enhancer(model_id: str) -> GeminiCvEnhancer:
    """Create a CV enhancer for a specific model, validating the model exists."""
    # Validate that the model exists via the model service
    model_service = get_model_service()
    available_model = model_service.get_model_by_id(model_id)
    if not available_model:
        # Fallback to default if specified model is not available
        model_id = model_service.get_default_model()

    client = GeminiClient(
        model_id=model_id,
        api_key=settings.GEMINI_API_KEY,
    )
    return GeminiCvEnhancer(client)


@lru_cache(maxsize=1)
def get_file_storage() -> LocalFileStorage:
    return LocalFileStorage(
        Path(settings.UPLOAD_DIR), Path(settings.SESSION_OUTPUT_DIR)
    )


@lru_cache(maxsize=1)
def get_packager() -> LocalOutputPackager:
    return LocalOutputPackager()


@lru_cache(maxsize=1)
def get_compiler() -> LualatexCompiler:
    return LualatexCompiler()


@lru_cache(maxsize=1)
def get_progress_tracker() -> InMemoryProgressTracker:
    return InMemoryProgressTracker()


def enhance_cv_use_case() -> EnhanceCvUseCase:
    return EnhanceCvUseCase(
        enhancer=get_cv_enhancer(),
        enhancer_factory=create_cv_enhancer,
    )


def parse_job_use_case() -> ParseJobFileUseCase:
    return ParseJobFileUseCase(parser=CsvJsonJobParser())


@lru_cache(maxsize=1)
def save_and_compile_use_case() -> SaveAndCompileUseCase:
    return SaveAndCompileUseCase(
        compiler=get_compiler(),
        packager=get_packager(),
    )


@lru_cache(maxsize=1)
def upload_cv_use_case() -> UploadCvUseCase:
    return UploadCvUseCase(
        storage=get_file_storage(),
        max_file_size=settings.MAX_FILE_SIZE,
    )


@lru_cache(maxsize=1)
def batch_enhance_use_case() -> BatchEnhanceUseCase:
    return BatchEnhanceUseCase(
        enhance_use_case=enhance_cv_use_case(),
        save_use_case=save_and_compile_use_case(),
        packager=get_packager(),
        progress_tracker=get_progress_tracker(),
    )


@lru_cache(maxsize=1)
def get_model_service() -> ModelService:
    """Get the model service adapter."""
    return GeminiModelService()


@lru_cache(maxsize=1)
def get_cleanup_service() -> CleanupService:
    """Get the cleanup service adapter."""
    return LocalCleanupService()
