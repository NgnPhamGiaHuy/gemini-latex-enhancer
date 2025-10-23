"""
Model Service for fetching available AI models from Google Gemini API.

This service centralizes model discovery, default selection, and basic caching
to avoid frequent API calls. It returns processed, frontend-friendly model
metadata and provides helpers to retrieve specific models or the default one.
"""

import google.generativeai as genai
from typing import List, Dict, Optional
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ModelService:
    """Service for managing AI model information and caching."""

    def __init__(self):
        """Initialize cache structures and durations."""
        self._models_cache: Optional[List[Dict]] = None
        self._cache_timestamp: Optional[float] = None
        self._cache_duration = 300  # 5 minutes cache

    def _is_cache_valid(self) -> bool:
        """Return True if the in-memory cache is still fresh."""
        if not self._models_cache or not self._cache_timestamp:
            return False

        import time

        return (time.time() - self._cache_timestamp) < self._cache_duration

    def _fetch_models_from_api(self) -> List[Dict]:
        """Fetch and normalize models directly from the Gemini API.

        Returns:
            A list of processed model dictionaries suitable for the UI.
        """
        logger.info("=== FETCHING MODELS FROM GEMINI API ===")

        try:
            if not settings.GEMINI_API_KEY:
                logger.error("❌ GEMINI_API_KEY not configured")
                return self._get_fallback_models()

            # Configure Gemini
            genai.configure(api_key=settings.GEMINI_API_KEY)

            # Fetch models from API
            models = list(genai.list_models())  # Convert generator to list
            logger.info(f"✅ Fetched {len(models)} models from API")

            # Process and filter models
            processed_models = []
            for model in models:
                # Only include models that support generateContent (text generation)
                if "generateContent" in model.supported_generation_methods:
                    model_info = {
                        "id": model.name.replace("models/", ""),
                        "name": model.display_name,
                        "description": model.description or "No description available",
                        "provider": "Google",
                        "default": self._is_default_model(model.name),
                        "supported_methods": list(model.supported_generation_methods),
                        "version": self._extract_version(model.name),
                    }
                    processed_models.append(model_info)

            logger.info(f"✅ Processed {len(processed_models)} text generation models")
            return processed_models

        except Exception as e:
            logger.error(f"❌ Failed to fetch models from API: {str(e)}")
            return self._get_fallback_models()

    def _is_default_model(self, model_name: str) -> bool:
        """Return True if a model (by name) is considered default by policy."""
        default_models = ["gemini-2.0-flash", "gemini-2.5-flash", "gemini-flash-latest"]

        model_id = model_name.replace("models/", "")
        return model_id in default_models

    def _extract_version(self, model_name: str) -> str:
        """Extract a simple semantic version from a model name/id string."""
        model_id = model_name.replace("models/", "")

        # Configurable version patterns
        version_patterns = [
            ("2.5", "2.5"),
            ("2.0", "2.0"),
            ("1.5", "1.5"),
            ("1.0", "1.0"),
            ("pro", "Pro"),
            ("flash", "Flash"),
            ("latest", "Latest"),
        ]

        for pattern, version in version_patterns:
            if pattern in model_id.lower():
                return version

        return "Unknown"

    def _get_fallback_models(self) -> List[Dict]:
        """Return a hardcoded fallback list when the API is unavailable."""
        logger.warning("⚠️ Using fallback models due to API unavailability")
        return [
            {
                "id": "gemini-2.0-flash",
                "name": "Gemini 2.0 Flash",
                "description": "Fast and efficient model for quick processing",
                "provider": "Google",
                "default": True,
                "supported_methods": ["generateContent", "countTokens"],
                "version": "2.0",
            },
            {
                "id": "gemini-2.5-flash",
                "name": "Gemini 2.5 Flash",
                "description": "Latest stable version with enhanced capabilities",
                "provider": "Google",
                "default": False,
                "supported_methods": ["generateContent", "countTokens"],
                "version": "2.5",
            },
            {
                "id": "gemini-2.5-pro",
                "name": "Gemini 2.5 Pro",
                "description": "Advanced model with enhanced capabilities",
                "provider": "Google",
                "default": False,
                "supported_methods": ["generateContent", "countTokens"],
                "version": "2.5",
            },
        ]

    def get_available_models(self) -> List[Dict]:
        """Return available models, using cache when valid."""
        if self._is_cache_valid():
            logger.info("✅ Using cached models")
            return self._models_cache

        logger.info("🔄 Cache expired or empty, fetching fresh models")
        models = self._fetch_models_from_api()

        # Update cache
        import time

        self._models_cache = models
        self._cache_timestamp = time.time()

        return models

    def get_default_model(self) -> str:
        """Return the id of the default model, using fallbacks as needed."""
        models = self.get_available_models()

        # Find the first default model
        for model in models:
            if model.get("default", False):
                return model["id"]

        # Fallback to first model if no default found
        if models:
            return models[0]["id"]

        # Ultimate fallback
        return "gemini-2.5-flash"

    def get_model_by_id(self, model_id: str) -> Optional[Dict]:
        """Return a specific model dict by id, or None if not found."""
        models = self.get_available_models()

        for model in models:
            if model["id"] == model_id:
                return model

        return None

    def clear_cache(self):
        """Clear the in-memory models cache and timestamp."""
        logger.info("🗑️ Clearing models cache")
        self._models_cache = None
        self._cache_timestamp = None


# Global instance
model_service = ModelService()
