"""Question repository interface (Port)."""

from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.entities.question import Question
from src.domain.value_objects.difficulty import DifficultyLevel


class QuestionRepository(ABC):
    """Abstract interface for question storage."""

    @abstractmethod
    async def get_by_profession(
        self,
        profession: str,
        difficulty: Optional[DifficultyLevel] = None,
        limit: int = 10,
    ) -> List[Question]:
        """Get questions by profession."""
        pass

    @abstractmethod
    async def get_by_id(self, question_id: str) -> Optional[Question]:
        """Get single question by ID."""
        pass

    @abstractmethod
    async def get_random_star_question(self, profession: str) -> Optional[Question]:
        """Get random behavioral question for STAR practice."""
        pass
