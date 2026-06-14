"""Feedback DTO module."""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class FeedbackDTO:
    """Data Transfer Object for answer feedback."""

    score: float
    max_score: float = 5.0
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    star_feedback: Optional[str] = None

    @property
    def percentage(self) -> float:
        """Get score as percentage."""
        return (self.score / self.max_score) * 100

    def get_rating_emoji(self) -> str:
        """Get emoji based on score."""
        if self.score >= 4.5:
            return "🌟🌟🌟"
        elif self.score >= 3.5:
            return "🌟🌟"
        elif self.score >= 2.5:
            return "🌟"
        return "📈"

    def format_for_user(self) -> str:
        """Format feedback for user display."""
        lines = [
            f"{self.get_rating_emoji()} **Результат:** {self.score:.1f}/{self.max_score:.0f}",
            f"📊 **Процент:** {self.percentage:.0f}%\n",
        ]

        if self.strengths:
            lines.append("💪 **Сильные стороны:**")
            for s in self.strengths[:3]:
                lines.append(f"• {s}")
            lines.append("")

        if self.weaknesses:
            lines.append("📈 **Зоны развития:**")
            for w in self.weaknesses[:3]:
                lines.append(f"• {w}")
            lines.append("")

        if self.recommendations:
            lines.append("💡 **Рекомендации:**")
            for r in self.recommendations[:3]:
                lines.append(f"• {r}")

        if self.star_feedback:
            lines.append(f"\n⭐ **STAR-анализ:**\n{self.star_feedback}")

        return "\n".join(lines)
