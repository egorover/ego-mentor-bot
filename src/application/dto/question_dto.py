"""Question DTO module."""

from dataclasses import dataclass
from typing import Optional

from src.domain.entities.question import Question
from src.domain.value_objects.difficulty import Difficulty, DifficultyLevel


@dataclass
class QuestionDTO:
    """Data Transfer Object for Question."""

    text: str
    category: str
    difficulty: str
    question_id: Optional[str] = None

    @classmethod
    def from_entity(cls, question: Question) -> "QuestionDTO":
        """Create DTO from domain entity."""
        return cls(
            text=question.text,
            category=question.category,
            difficulty=question.difficulty.level.value,
            question_id=question.question_id,
        )

    def to_entity(self, profession: str) -> Question:
        """Convert DTO to domain entity."""
        difficulty_level = DifficultyLevel.from_string(self.difficulty)
        if not difficulty_level:
            difficulty_level = DifficultyLevel.MEDIUM

        return Question(
            text=self.text,
            category=self.category,
            profession=profession,
            difficulty=Difficulty(difficulty_level),
            question_id=self.question_id,
        )
