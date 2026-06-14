"""STAR service module."""

from typing import Optional

from loguru import logger

from src.application.dto.feedback_dto import FeedbackDTO
from src.domain.entities.question import Question
from src.domain.interfaces.question_repository import QuestionRepository
from src.domain.interfaces.star_checker import STARChecker
from src.domain.value_objects.star_result import STARResult


class STARService:
    """Service for STAR methodology training."""

    def __init__(
        self,
        question_repository: QuestionRepository,
        star_checker: STARChecker,
    ):
        self.question_repository = question_repository
        self.star_checker = star_checker

    async def get_star_question(self, profession: str) -> Optional[Question]:
        """Get a behavioral question for STAR practice."""
        return await self.question_repository.get_random_star_question(profession)

    async def analyze_answer(self, answer_text: str) -> FeedbackDTO:
        """Analyze answer for STAR structure."""
        logger.debug("Analyzing answer for STAR structure")

        star_result = await self.star_checker.check(answer_text)

        feedback = self._generate_star_feedback(star_result, answer_text)

        return feedback

    def _generate_star_feedback(
        self,
        star_result: STARResult,
        answer_text: str,
    ) -> FeedbackDTO:
        """Generate STAR-specific feedback."""
        strengths = []
        weaknesses = []
        recommendations = []

        if star_result.has_situation:
            strengths.append("✅ Описана ситуация (Situation)")
        else:
            weaknesses.append("❌ Не описана ситуация")
            recommendations.append("Начните с контекста: где и когда это произошло")

        if star_result.has_task:
            strengths.append("✅ Сформулирована задача (Task)")
        else:
            weaknesses.append("❌ Не указана задача")
            recommendations.append("Четко скажите, что нужно было сделать")

        if star_result.has_action:
            strengths.append("✅ Описаны конкретные действия (Action)")
        else:
            weaknesses.append("❌ Нет описания действий")
            recommendations.append(
                "Расскажите, что именно ВЫ сделали, используйте глаголы"
            )

        if star_result.has_result:
            strengths.append("✅ Есть результат (Result)")
            if star_result.has_numbers:
                strengths.append("🎯 Результат подкреплен цифрами!")
            else:
                recommendations.append(
                    "Добавьте измеримые результаты: 'ускорил на X%', 'сократил время на Y часов'"
                )
        else:
            weaknesses.append("❌ Нет результата")
            recommendations.append(
                "Обязательно завершайте ответ результатом. Что изменилось?"
            )

        return FeedbackDTO(
            score=star_result.get_score(),
            strengths=strengths,
            weaknesses=weaknesses,
            recommendations=recommendations,
            star_feedback=star_result.get_feedback(),
        )

    async def get_star_example(self, profession: str) -> Optional[dict]:
        """Get a STAR example from knowledge base."""
        # This will be implemented in infrastructure layer
        pass
