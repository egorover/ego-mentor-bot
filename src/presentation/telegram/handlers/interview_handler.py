"""Interview handler module."""

from telegram import Update
from telegram.ext import ConversationHandler, ContextTypes
from loguru import logger

from src.application.services.interview_service import InterviewService
from src.presentation.telegram.states import ConversationStates


class InterviewHandler:
    """Handler for interview functionality."""

    def __init__(self, interview_service: InterviewService):
        self.interview_service = interview_service
        self.user_professions = {}

    async def handle_interview_start(
        self, query, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        """Start interview session."""
        user_id = query.from_user.id
        profession = context.user_data.get("profession")

        if not profession:
            await query.edit_message_text(
                "⚠️ **Сначала выбери профессию**\n\n"
                "Используй /start и выбери свою роль.",
                parse_mode="Markdown",
            )
            return ConversationHandler.END

        await query.edit_message_text(
            f"🎤 **Тренировочное интервью**\n\n"
            f"Профессия: {profession}\n"
            f"Количество вопросов: 10\n\n"
            f"**Правила:**\n"
            f"• Отвечай на вопросы по одному\n"
            f"• Я не буду комментировать до конца\n"
            f"• В конце получишь оценку и рекомендации\n\n"
            f"Готов? Начинаем! 🚀",
            parse_mode="Markdown",
        )

        try:
            session = await self.interview_service.start_interview(
                user_id=str(user_id),
                profession=profession,
                question_count=10,
            )

            context.user_data["interview_session"] = session
            context.user_data["interview_active"] = True

            first_question = await self.interview_service.get_next_question(
                str(user_id)
            )

            if first_question:
                await query.message.reply_text(
                    f"**Вопрос 1/10**\n\n"
                    f"📌 *{first_question.category}:*\n"
                    f"{first_question.text}\n\n"
                    f"Отправь свой ответ текстом или голосовым сообщением:",
                    parse_mode="Markdown",
                )
                return ConversationStates.WAITING_INTERVIEW_ANSWER

        except Exception as e:
            logger.error(f"Failed to start interview: {e}")
            await query.message.reply_text(
                "❌ Не удалось начать интервью. Попробуй позже."
            )
            return ConversationHandler.END

        return ConversationStates.WAITING_INTERVIEW_ANSWER

    async def handle_interview_answer(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> int:
        """Handle answer during interview."""
        user_id = str(update.effective_user.id)

        # Handle voice message
        if update.message.voice:
            answer_text = "🎤 Голосовое сообщение (текст не распознан)"
        else:
            answer_text = update.message.text or "Нет текста"

        logger.debug(f"Received answer from user {user_id}")

        try:
            # Process answer
            await self.interview_service.submit_answer(user_id, answer_text)

            # Get next question
            next_question = await self.interview_service.get_next_question(user_id)

            if next_question:
                # Get current question number
                session = context.user_data.get("interview_session")
                current_idx = session.current_index if session else 0
                total = len(session.question_ids) if session else 10

                await update.message.reply_text(
                    f"✅ **Ответ принят!**\n\n"
                    f"**Вопрос {current_idx + 1}/{total}**\n\n"
                    f"📌 *{next_question.category}:*\n"
                    f"{next_question.text}\n\n"
                    f"Отправь свой ответ:",
                    parse_mode="Markdown",
                )
                return ConversationStates.WAITING_INTERVIEW_ANSWER
            else:
                # Interview completed
                session = context.user_data.get("interview_session")
                avg_score = session.get_average_score() if session else 0
                completion_rate = session.get_completion_rate() if session else 100

                result_text = (
                    f"🏆 **Интервью завершено!**\n\n"
                    f"📊 **Итоговая оценка:** {avg_score:.1f}/5.0\n"
                    f"📈 **Полнота ответов:** {completion_rate:.0f}%\n\n"
                    f"💪 **Сильные стороны:**\n"
                    f"• Вы прошли все вопросы\n"
                    f"• Показали свои знания\n\n"
                    f"📈 **Зоны развития:**\n"
                    f"• Добавляйте цифры в результаты\n"
                    f"• Используйте STAR структуру\n\n"
                    f"💡 **Рекомендации:**\n"
                    f"• Повтори интервью через 2 дня\n"
                    f"• Сравни результаты\n"
                    f"• Тренируйся с /star для сложных вопросов\n\n"
                    f"Хочешь попробовать ещё раз? Нажми /interview"
                )

                await update.message.reply_text(result_text, parse_mode="Markdown")

                # Cleanup
                context.user_data.pop("interview_session", None)
                context.user_data.pop("interview_active", None)

                return ConversationHandler.END

        except ValueError as e:
            logger.warning(f"Interview error for user {user_id}: {e}")
            await update.message.reply_text(
                "⚠️ Нет активной сессии интервью.\n" "Начни новое с помощью /interview"
            )
            return ConversationHandler.END
        except Exception as e:
            logger.error(f"Failed to process answer: {e}")
            await update.message.reply_text(
                "❌ Произошла ошибка при обработке ответа. Попробуй ещё раз."
            )
            return ConversationStates.WAITING_INTERVIEW_ANSWER
