"""User session entity module."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional

from src.domain.entities.answer import Answer


@dataclass
class UserSession:
    """Domain aggregate for user interview session."""

    user_id: str
    profession: str
    started_at: datetime = field(default_factory=datetime.now)
    question_ids: List[str] = field(default_factory=list)
    answers: Dict[str, Answer] = field(default_factory=dict)
    current_index: int = 0
    completed: bool = False

    def add_answer(self, answer: Answer) -> None:
        """Add answer to session."""
        self.answers[answer.question_id] = answer

    def get_current_question_id(self) -> Optional[str]:
        """Get current question ID."""
        if self.current_index < len(self.question_ids):
            return self.question_ids[self.current_index]
        return None

    def move_to_next(self) -> bool:
        """Move to next question. Returns True if more questions exist."""
        if self.current_index < len(self.question_ids) - 1:
            self.current_index += 1
            return True
        # At the last question, mark as completed
        self.current_index += 1
        self.completed = True
        return False

    def get_average_score(self) -> float:
        """Calculate average score of all answers."""
        if not self.answers:
            return 0.0

        total = sum(
            a.get_final_score() for a in self.answers.values() if a.score is not None
        )
        return total / len(self.answers) if self.answers else 0.0

    def get_completion_rate(self) -> float:
        """Get completion rate as percentage."""
        if not self.question_ids:
            return 0.0
        return (len(self.answers) / len(self.question_ids)) * 100
