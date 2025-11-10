from __future__ import annotations

from dataclasses import dataclass

from app.domain.services.latex_validator import LatexValidator


@dataclass(frozen=True)
class LatexDocument:
    """Immutable representation of a LaTeX document."""

    content: str

    def assert_valid(self) -> "LatexDocument":
        LatexValidator.validate(self.content)
        return self
