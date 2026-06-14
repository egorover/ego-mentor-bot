"""STAR result value object module."""

from dataclasses import dataclass


@dataclass
class STARResult:
    """Value object representing STAR analysis result."""

    has_situation: bool
    has_task: bool
    has_action: bool
    has_result: bool
    has_numbers: bool = False

    def is_complete(self) -> bool:
        """Check if all STAR elements are present."""
        return all(
            [
                self.has_situation,
                self.has_task,
                self.has_action,
                self.has_result,
            ]
        )

    def get_missing_elements(self) -> list:
        """Get list of missing STAR elements."""
        missing = []
        if not self.has_situation:
            missing.append("Situation (ситуация)")
        if not self.has_task:
            missing.append("Task (задача)")
        if not self.has_action:
            missing.append("Action (действие)")
        if not self.has_result:
            missing.append("Result (результат)")
        return missing

    def get_score(self) -> float:
        """Calculate STAR score (0-5)."""
        present_count = sum(
            [
                self.has_situation,
                self.has_task,
                self.has_action,
                self.has_result,
            ]
        )

        # Bonus for numbers in result
        bonus = 0.5 if self.has_result and self.has_numbers else 0

        return min(5.0, (present_count * 1.25) + bonus)

    def get_feedback(self) -> str:
        """Generate human-readable feedback."""
        if self.is_complete():
            if self.has_numbers:
                return "✅ Отлично! Полный STAR-ответ с измеримыми результатами!"
            return "✅ Хорошо! Есть все элементы STAR, добавьте цифры для усиления."

        missing = self.get_missing_elements()
        return (
            f"⚠️ В ответе не хватает: {', '.join(missing)}. Используйте структуру STAR."
        )
