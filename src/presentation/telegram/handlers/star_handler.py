"""STAR training handler module."""

from telegram import Update
from telegram.ext import ConversationHandler, ContextTypes
from loguru import logger

from src.application.services.star_service import STARService
from src.infrastructure.repositories.excel_question_repository import (
    ExcelQuestionRepository,
)
from src.presentation.telegram.states import ConversationStates


class StarHandler:
    """Handler for STAR methodology training."""

    def __init__(
        self,
        star_service: STARService,
        question_repository: ExcelQuestionRepository,
    ):
        self.star_service = star_service
        self.question_repository = question_repository

    async def handle_star_start(self, query, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Start STAR training."""
        profession = context.user_data.get("profession")

        if not profession:
            await query.edit_message_text(
                "⚠️ **Сначала выбери профессию**\n\n"
                "Используй /start и выбери свою роль.",
                parse_mode="Markdown",
            )
            return ConversationHandler.END

        # Get behavioral question
        star_question = await self.star_service.get_star_question(profession)

        if not star_question:
            # Fallback to any medium difficulty question
            questions = await self.question_repository.get_by_profession(
                profession, limit=5
            )
            star_question = questions[0] if questions else None

        if not star_question:
            await query.edit_message_text(
                "❌ Не удалось найти подходящий вопрос для STAR-тренировки.\n"
                "Попробуй другую профессию или позже."
            )
            return ConversationHandler.END

        # Store question for this session
        context.user_data["star_question"] = star_question

        star_example = self.question_repository.get_star_example(profession)

        instruction = (
            "⭐ **STAR-тренировка**\n\n"
            "Методика STAR помогает структурировать ответы на поведенческие вопросы:\n\n"
            "• **S**ituation — опиши ситуацию/контекст\n"
            "• **T**ask — сформулируй задачу/проблему\n"
            "• **A**ction — расскажи, что именно ТЫ сделал\n"
            "• **R**esult — покажи результат (лучше с цифрами)\n\n"
            f"**Вопрос:**\n{star_question.text}\n\n"
            "Отправь свой ответ текстом:"
        )

        if star_example:
            instruction += (
                f"\n\n📖 **Пример хорошего ответа:**\n\n"
                f"*Ситуация:* {star_example.get('situation', '—')[:200]}\n"
                f"*Задача:* {star_example.get('task', '—')[:150]}\n"
                f"*Действие:* {star_example.get('action', '—')[:200]}\n"
                f"*Результат:* {star_example.get('result', '—')[:150]}"
            )

        await query.edit_message_text(instruction, parse_mode="Markdown")

        return ConversationStates.WAITING_STAR_ANSWER

    async def handle_star_answer(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> int:
        """Process STAR answer and provide feedback."""
        answer_text = update.message.text or "Нет текста"

        await update.message.reply_text(
            "🔍 **Анализирую ответ по методике STAR**...",
            parse_mode="Markdown",
        )

        try:
            # Analyze answer
            feedback = await self.star_service.analyze_answer(answer_text)

            # Format response
            response = self._format_star_feedback(feedback)

            # Add improvement example if score is low
            if feedback.score < 3.0:
                response += self._get_improvement_example()

            await update.message.reply_text(response, parse_mode="Markdown")

            # Offer to try again
            await update.message.reply_text(
                "🔄 **Хочешь попробовать ещё раз?**\n\n"
                "Отправь /star для нового вопроса\n"
                "Или /interview для полноценного интервью",
                parse_mode="Markdown",
            )

            return ConversationHandler.END

        except Exception as e:
            logger.error(f"Failed to analyze STAR answer: {e}")
            await update.message.reply_text(
                "❌ Произошла ошибка при анализе ответа. Попробуй ещё раз."
            )
            return ConversationStates.WAITING_STAR_ANSWER

    def _format_star_feedback(self, feedback) -> str:
        """Format STAR feedback for display."""
        lines = [
            "⭐ **Результат STAR-анализа**\n",
            f"📊 **Оценка:** {feedback.score:.1f}/5.0\n",
        ]

        if feedback.strengths:
            lines.append("✅ **Что хорошо:**")
            for s in feedback.strengths[:3]:
                lines.append(f"  {s}")
            lines.append("")

        if feedback.weaknesses:
            lines.append("⚠️ **Что можно улучшить:**")
            for w in feedback.weaknesses[:3]:
                lines.append(f"  {w}")
            lines.append("")

        if feedback.recommendations:
            lines.append("💡 **Как улучшить ответ:**")
            for r in feedback.recommendations[:3]:
                lines.append(f"  • {r}")
            lines.append("")

        if feedback.star_feedback:
            lines.append(f"📌 **Детали:** {feedback.star_feedback}")

        return "\n".join(lines)

    def _get_improvement_example(self) -> str:
        """Get example of improved answer."""
        return (
            "\n\n📖 **Пример улучшенного ответа по STAR:**\n\n"
            "**Situation:** В прошлом проекте на пике нагрузки API отвечал за 5-7 секунд\n\n"
            "**Task:** Нужно было снизить время отклика до 500 мс без увеличения серверов\n\n"
            "**Action:** Я провел профилирование, оптимизировал индексы в PostgreSQL и добавил Redis кэширование\n\n"
            "**Result:** Время ответа сократилось до 200 мс, нагрузка на БД упала на 60%\n\n"
            "✨ **Видите разницу?** Конкретные действия и цифры!"
        )
