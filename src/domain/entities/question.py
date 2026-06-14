"""Question entity module."""

from dataclasses import dataclass
from typing import Optional

from src.domain.value_objects.difficulty import Difficulty


@dataclass
class Question:
    """Domain entity representing an interview question."""

    text: str
    category: str
    profession: str
    difficulty: Difficulty
    question_id: Optional[str] = None

    def __post_init__(self) -> None:
        """Validate question data."""
        if not self.text or not self.text.strip():
            raise ValueError("Question text cannot be empty")
        if not self.category:
            raise ValueError("Category cannot be empty")
        if not self.profession:
            raise ValueError("Profession cannot be empty")

    def is_behavioral(self) -> bool:
        """Check if question is behavioral (STAR format expected)."""
        behavioral_keywords = ["расскаж", "ситуац", "пример", "опис", "сложн"]
        text_lower = self.text.lower()
        return any(keyword in text_lower for keyword in behavioral_keywords)

    def get_difficulty_level(self) -> int:
        """Get numeric difficulty level."""
        return self.difficulty.value
