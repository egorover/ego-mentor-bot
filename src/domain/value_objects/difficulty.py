"""Difficulty value object module."""

from enum import Enum
from typing import Optional


class DifficultyLevel(str, Enum):
    """Difficulty levels for questions."""

    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"

    @classmethod
    def from_string(cls, value: str) -> Optional["DifficultyLevel"]:
        """Parse difficulty from string."""
        try:
            return cls(value)
        except ValueError:
            return None


class Difficulty:
    """Value object representing question difficulty."""

    def __init__(self, level: DifficultyLevel):
        self._level = level

    @property
    def level(self) -> DifficultyLevel:
        return self._level

    @property
    def value(self) -> int:
        """Get numeric value for scoring."""
        mapping = {
            DifficultyLevel.EASY: 1,
            DifficultyLevel.MEDIUM: 2,
            DifficultyLevel.HARD: 3,
        }
        return mapping.get(self._level, 2)

    @property
    def label(self) -> str:
        """Get human-readable label."""
        labels = {
            DifficultyLevel.EASY: "🟢 Начальный",
            DifficultyLevel.MEDIUM: "🟡 Средний",
            DifficultyLevel.HARD: "🔴 Продвинутый",
        }
        return labels.get(self._level, self._level.value)

    @classmethod
    def easy(cls) -> "Difficulty":
        return cls(DifficultyLevel.EASY)

    @classmethod
    def medium(cls) -> "Difficulty":
        return cls(DifficultyLevel.MEDIUM)

    @classmethod
    def hard(cls) -> "Difficulty":
        return cls(DifficultyLevel.HARD)
