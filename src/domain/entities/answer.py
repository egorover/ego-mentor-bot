"""Answer entity module."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.domain.value_objects.star_result import STARResult
from src.domain.value_objects.score import Score


@dataclass
class Answer:
    """Domain entity representing a user's answer."""

    text: str
    question_id: str
    user_id: str
    timestamp: datetime
    star_result: Optional[STARResult] = None
    score: Optional[Score] = None

    def __post_init__(self) -> None:
        """Validate answer data."""
        if not self.text:
            raise ValueError("Answer text cannot be empty")
        if not self.user_id:
            raise ValueError("User ID cannot be empty")

    def has_star_structure(self) -> bool:
        """Check if answer contains all STAR elements."""
        if not self.star_result:
            return False
        return self.star_result.is_complete()

    def get_final_score(self) -> float:
        """Get final score as float."""
        if self.score:
            return self.score.value
        return 0.0
