"""STAR checker interface (Port)."""

from abc import ABC, abstractmethod

from src.domain.value_objects.star_result import STARResult


class STARChecker(ABC):
    """Abstract interface for STAR structure validation."""

    @abstractmethod
    async def check(self, answer_text: str) -> STARResult:
        """Analyze answer and return STAR result."""
        pass
