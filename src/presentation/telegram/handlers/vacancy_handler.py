"""Vacancy analysis handler module."""

from telegram import Update
from telegram.ext import ConversationHandler, ContextTypes
from loguru import logger

from src.application.services.vacancy_service import VacancyService
from src.presentation.telegram.states import ConversationStates


class VacancyHandler:
    """Handler for vacancy analysis."""

    def __init__(self, vacancy_service: VacancyService):
        self.vacancy_service = vacancy_service

    async def handle_vacancy_start(
        self, query, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        """Start vacancy analysis."""
        await query.edit_message_text(
            "📊 **Анализ вакансии**\n\n"
            "Отправь мне текст вакансии (можно скопировать с сайта).\n\n"
            "Я выделю:\n"
            "• Ключевые требования\n"
            "• Вероятные вопросы на собеседовании\n"
            "• Рекомендации по подготовке\n\n"
            "✏️ **Вставь текст вакансии:**",
            parse_mode="Markdown",
        )
        return ConversationStates.WAITING_VACANCY

    async def handle_vacancy_text(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> int:
        """Process vacancy text."""
        vacancy_text = update.message.text

        if not vacancy_text or len(vacancy_text) < 50:
            await update.message.reply_text(
                "⚠️ Текст вакансии слишком короткий.\n"
                "Пожалуйста, вставь полное описание вакансии (минимум 50 символов)."
            )
            return ConversationStates.WAITING_VACANCY

        await update.message.reply_text(
            "🔍 **Анализирую вакансию**...\n" "Это займет несколько секунд.",
            parse_mode="Markdown",
        )

        try:
            # Analyze vacancy
            analysis = await self.vacancy_service.analyze_vacancy(vacancy_text)

            # Format response
            response = self._format_analysis(analysis)

            await update.message.reply_text(response, parse_mode="Markdown")

            # Offer next steps
            await update.message.reply_text(
                "💡 **Что дальше**?\n\n"
                "• /questions — получить вопросы для подготовки\n"
                "• /interview — начать тренировочное интервью\n"
                "• /star — потренировать STAR-ответы\n"
                "• /self — подготовить самопрезентацию",
                parse_mode="Markdown",
            )

            return ConversationHandler.END

        except Exception as e:
            logger.error(f"Failed to analyze vacancy: {e}")
            await update.message.reply_text(
                "❌ Не удалось проанализировать вакансию.\n"
                "Пожалуйста, проверь текст и попробуй снова."
            )
            return ConversationStates.WAITING_VACANCY

    def _format_analysis(self, analysis: dict) -> str:
        """Format analysis results for display."""
        lines = []

        # Title
        lines.append(f"📊 **Анализ вакансии:** {analysis.get('title', 'Unknown')}\n")

        # Key requirements
        lines.append("🔑 **Ключевые требования:**")
        for req in analysis.get("key_requirements", [])[:8]:
            lines.append(f"• {req}")

        # Risk areas
        if analysis.get("risk_areas"):
            lines.append("\n⚠️ **Потенциальные зоны риска:**")
            for risk in analysis["risk_areas"][:3]:
                lines.append(f"• {risk}")

        # Predicted questions
        lines.append("\n❓ **Вероятные вопросы на собеседовании:**")
        for i, q in enumerate(analysis.get("predicted_questions", [])[:8], 1):
            lines.append(f"{i}. {q}")

        # Recommendations
        lines.append("\n💡 **Рекомендации по подготовке:**")
        for rec in analysis.get("recommendations", []):
            lines.append(f"• {rec}")

        return "\n".join(lines)
