"""Score value object module."""

from dataclasses import dataclass
from typing import Dict


@dataclass
class Score:
    """Value object representing answer score."""

    value: float
    max_value: float = 5.0

    def __post_init__(self) -> None:
        """Validate score value."""
        if not 0 <= self.value <= self.max_value:
            raise ValueError(f"Score must be between 0 and {self.max_value}")

    @property
    def percentage(self) -> float:
        """Get score as percentage."""
        return (self.value / self.max_value) * 100

    def get_grade(self) -> str:
        """Get letter grade."""
        if self.value >= 4.5:
            return "A (Отлично)"
        elif self.value >= 3.5:
            return "B (Хорошо)"
        elif self.value >= 2.5:
            return "C (Удовлетворительно)"
        elif self.value >= 1.5:
            return "D (Нужно улучшить)"
        return "F (Слабый ответ)"


@dataclass
class DetailedScore(Score):
    """Score with detailed criteria breakdown."""

    criteria_scores: Dict[str, float] = None

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.criteria_scores is None:
            self.criteria_scores = {}

    @classmethod
    def from_criteria(
        cls,
        structure: float = 0.0,
        action_quality: float = 0.0,
        result_quality: float = 0.0,
        communication: float = 0.0,
        relevance: float = 0.0,
    ) -> "DetailedScore":
        """Create DetailedScore from individual criteria."""
        total = (
            structure * 0.20
            + action_quality * 0.25
            + result_quality * 0.25
            + communication * 0.15
            + relevance * 0.15
        )

        return cls(
            value=total,
            criteria_scores={
                "structure": structure,
                "action_quality": action_quality,
                "result_quality": result_quality,
                "communication": communication,
                "relevance": relevance,
            },
        )
