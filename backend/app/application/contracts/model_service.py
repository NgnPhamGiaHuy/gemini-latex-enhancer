from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, List, Optional


class ModelService(ABC):
    """Abstract contract for AI model discovery and management."""

    @abstractmethod
    def get_available_models(self) -> List[Dict]:
        """Return available models, using cache when valid."""
        ...

    @abstractmethod
    def get_default_model(self) -> str:
        """Return the id of the default model."""
        ...

    @abstractmethod
    def get_model_by_id(self, model_id: str) -> Optional[Dict]:
        """Return a specific model dict by id, or None if not found."""
        ...

    @abstractmethod
    def clear_cache(self) -> None:
        """Clear the in-memory models cache."""
        ...
