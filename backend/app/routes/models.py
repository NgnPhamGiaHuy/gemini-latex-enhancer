"""
Models API routes for fetching available AI models dynamically from the Google Gemini API.
"""

from fastapi import APIRouter, Depends

from app.application.contracts.model_service import ModelService
from app.interface.di import get_model_service
from app.utils.response_builder import ResponseBuilder
from app.utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get("/models")
async def get_available_models(
    model_service: ModelService = Depends(get_model_service),
):
    """List available AI models and indicate the default choice."""
    logger.info("=== FETCHING AVAILABLE MODELS ===")

    try:
        # Retrieve models from the model service
        models_data = model_service.get_available_models()
        default_model_id = model_service.get_default_model()

        logger.info(f"✅ Found {len(models_data)} available models")
        logger.info(f"✅ Default model: {default_model_id}")

        # Log a subset of models for debugging (first five)
        for i, model in enumerate(models_data[:5]):
            logger.debug(
                f"Model {i+1}: {model['id']} - {model['name']} ({'default' if model['default'] else 'optional'})"
            )

        if len(models_data) > 5:
            logger.debug(f"... and {len(models_data) - 5} more models")

        logger.info("=== MODELS FETCHED SUCCESSFULLY ===")

        return ResponseBuilder.success_response(
            message="Available models fetched successfully",
            data={
                "models": models_data,
                "default_model": default_model_id,
                "total_count": len(models_data),
            },
        )

    except Exception as e:
        logger.error(f"❌ Failed to fetch models: {str(e)}", exc_info=True)
        return ResponseBuilder.error_response(
            message="Failed to fetch available models",
            status_code=500,
            details={"error": str(e)},
        )


@router.get("/models/default")
async def get_default_model(
    model_service: ModelService = Depends(get_model_service),
):
    """Return the default AI model as configured/derived by the service."""
    logger.info("=== FETCHING DEFAULT MODEL ===")

    try:
        default_model_id = model_service.get_default_model()
        default_model = model_service.get_model_by_id(default_model_id)

        if not default_model:
            logger.warning("No default model found, using fallback")
            default_model = {
                "id": "gemini-2.5-flash",
                "name": "Gemini 2.5 Flash",
                "description": "Fast and efficient model for quick processing",
                "provider": "Google",
                "default": True,
                "supported_methods": ["generateContent", "countTokens"],
                "version": "2.5",
            }

        logger.info(f"✅ Default model: {default_model['id']}")
        logger.info("=== DEFAULT MODEL FETCHED SUCCESSFULLY ===")

        return ResponseBuilder.success_response(
            data=default_model, message="Default model fetched successfully"
        )

    except Exception as e:
        logger.error(f"❌ Failed to fetch default model: {str(e)}", exc_info=True)
        return ResponseBuilder.error_response(
            message="Failed to fetch default model",
            status_code=500,
            details={"error": str(e)},
        )


@router.post("/models/refresh")
async def refresh_models_cache(
    model_service: ModelService = Depends(get_model_service),
):
    """Refresh the models cache by fetching fresh data from the provider API."""
    logger.info("=== REFRESHING MODELS CACHE ===")

    try:
        # Clear the cache and fetch fresh models
        model_service.clear_cache()
        models_data = model_service.get_available_models()
        default_model_id = model_service.get_default_model()

        logger.info(f"✅ Cache refreshed with {len(models_data)} models")
        logger.info("=== MODELS CACHE REFRESHED SUCCESSFULLY ===")

        return ResponseBuilder.success_response(
            message="Models cache refreshed successfully",
            data={
                "models": models_data,
                "default_model": default_model_id,
                "total_count": len(models_data),
            },
        )

    except Exception as e:
        logger.error(f"❌ Failed to refresh models cache: {str(e)}", exc_info=True)
        return ResponseBuilder.error_response(
            message="Failed to refresh models cache", error=str(e), status_code=500
        )


@router.get("/models/{model_id}")
async def get_model_by_id(
    model_id: str, model_service: ModelService = Depends(get_model_service)
):
    """Fetch detailed information for a specific model by id."""
    logger.info(f"=== FETCHING MODEL: {model_id} ===")

    try:
        model = model_service.get_model_by_id(model_id)

        if not model:
            logger.warning(f"Model {model_id} not found")
            return ResponseBuilder.error_response(
                message=f"Model '{model_id}' not found", status_code=404
            )

        logger.info(f"✅ Found model: {model['name']}")
        logger.info("=== MODEL FETCHED SUCCESSFULLY ===")

        return ResponseBuilder.success_response(
            data=model, message=f"Model '{model_id}' fetched successfully"
        )

    except Exception as e:
        logger.error(f"❌ Failed to fetch model {model_id}: {str(e)}", exc_info=True)
        return ResponseBuilder.error_response(
            message=f"Failed to fetch model '{model_id}'",
            status_code=500,
            details={"error": str(e)},
        )
