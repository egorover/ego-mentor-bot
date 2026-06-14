"""Main Telegram bot module."""

import asyncio
from typing import Optional

from loguru import logger
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from src.infrastructure.ai.openai_client import OpenAIClient
from src.infrastructure.ai.star_checker_impl import RuleBasedSTARChecker
from src.infrastructure.config.logger import setup_logging
from src.infrastructure.config.settings import settings
from src.infrastructure.repositories.excel_question_repository import (
    ExcelQuestionRepository,
)
from src.presentation.telegram.handlers import (
    ChecklistHandler,
    InterviewHandler,
    SelfPresentationHandler,
    StartHandler,
    STARHandler,
    VacancyHandler,
)
from src.presentation.telegram.keyboards import get_main_keyboard
from src.presentation.telegram.states import ConversationStates
from src.application.services.interview_service import InterviewService
from src.application.services.star_service import STARService
from src.application.services.vacancy_service import VacancyService
from src.application.services.self_presentation_service import SelfPresentationService


class EgoMentorBot:
    """Main bot class."""

    def __init__(self):
        """Initialize bot and dependencies."""
        logger.info("Initializing EgoMentor Bot...")

        # Infrastructure
        self.question_repository = ExcelQuestionRepository(settings.knowledge_base_path)

        # OpenAI client (optional)
        self.openai_client: Optional[OpenAIClient] = None
        if settings.use_openai and settings.openai_api_key:
            self.openai_client = OpenAIClient(settings.openai_api_key)

        # STAR checker
        self.star_checker = RuleBasedSTARChecker(
            use_openai=settings.use_openai,
            openai_client=self.openai_client,
        )

        # Services
        self.interview_service = InterviewService(
            question_repository=self.question_repository,
            star_checker=self.star_checker,
        )
        self.star_service = STARService(
            question_repository=self.question_repository,
            star_checker=self.star_checker,
        )
        self.vacancy_service = VacancyService()
        self.presentation_service = SelfPresentationService()

        # Handlers
        self.start_handler = StartHandler(
            professions=settings.professions,
            default_profession=settings.default_profession,
        )
        self.interview_handler = InterviewHandler(self.interview_service)
        self.vacancy_handler = VacancyHandler(self.vacancy_service)
        self.star_handler = STARHandler(self.star_service, self.question_repository)
        self.presentation_handler = SelfPresentationHandler(self.presentation_service)
        self.checklist_handler = ChecklistHandler(self.question_repository)

        # Application
        self.application = None

    async def start(self) -> None:
        """Start the bot."""
        logger.info("Starting EgoMentor Bot...")

        # Create application
        self.application = (
            Application.builder().token(settings.telegram_bot_token).build()
        )

        # Register handlers
        self._register_handlers()

        # Start polling
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling()

        logger.info("Bot is running!")

        # Keep running
        try:
            while True:
                await asyncio.sleep(3600)
        except KeyboardInterrupt:
            logger.info("Shutting down...")
            await self.shutdown()

    def _register_handlers(self) -> None:
        """Register all handlers."""
        # Command handlers
        self.application.add_handler(
            CommandHandler("start", self.start_handler.handle_start)
        )
        self.application.add_handler(
            CommandHandler("help", self.start_handler.handle_help)
        )

        # Conversation handlers
        vacancy_conv = ConversationHandler(
            entry_points=[
                CallbackQueryHandler(
                    self.vacancy_handler.handle_vacancy_start,
                    pattern="^analyze_vacancy$",
                )
            ],
            states={
                ConversationStates.WAITING_VACANCY: [
                    MessageHandler(
                        filters.TEXT & ~filters.COMMAND,
                        self.vacancy_handler.handle_vacancy_text,
                    )
                ]
            },
            fallbacks=[CommandHandler("start", self.start_handler.handle_start)],
        )

        star_conv = ConversationHandler(
            entry_points=[
                CallbackQueryHandler(
                    self.star_handler.handle_star_start,
                    pattern="^star_training$",
                )
            ],
            states={
                ConversationStates.WAITING_STAR_ANSWER: [
                    MessageHandler(
                        filters.TEXT | filters.VOICE,
                        self.star_handler.handle_star_answer,
                    )
                ]
            },
            fallbacks=[CommandHandler("start", self.start_handler.handle_start)],
        )

        interview_conv = ConversationHandler(
            entry_points=[
                CallbackQueryHandler(
                    self.interview_handler.handle_interview_start,
                    pattern="^start_interview$",
                )
            ],
            states={
                ConversationStates.WAITING_INTERVIEW_ANSWER: [
                    MessageHandler(
                        filters.TEXT | filters.VOICE,
                        self.interview_handler.handle_interview_answer,
                    )
                ]
            },
            fallbacks=[CommandHandler("start", self.start_handler.handle_start)],
        )

        self.application.add_handler(vacancy_conv)
        self.application.add_handler(star_conv)
        self.application.add_handler(interview_conv)

        # Callback query handler (for all other buttons)
        self.application.add_handler(CallbackQueryHandler(self._handle_callback))

        # Fallback
        self.application.add_handler(MessageHandler(filters.ALL, self._handle_unknown))

    async def _handle_callback(self, update, context) -> None:
        """Handle callback queries."""
        query = update.callback_query
        await query.answer()

        data = query.data

        if data == "select_profession":
            await self.start_handler.handle_select_profession(query)
        elif data.startswith("prof_"):
            await self.start_handler.handle_profession_selected(query, data)
        elif data == "get_questions":
            await self.start_handler.handle_get_questions(query, context)
        elif data.startswith("questions_"):
            await self.start_handler.handle_questions_difficulty(query, data, context)
        elif data == "self_presentation":
            await self.presentation_handler.handle_self_presentation(query, context)
        elif data == "checklist":
            await self.checklist_handler.handle_checklist_menu(query)
        elif data.startswith("checklist_"):
            await self.checklist_handler.handle_checklist_stage(query, data)
        elif data == "help":
            await self.start_handler.handle_help_callback(query)
        elif data.startswith("pres_"):
            await self.presentation_handler.handle_presentation_version(
                query, data, context
            )
        elif data == "back_to_menu":
            profession = context.user_data.get("profession")
            await query.edit_message_text(
                "🏠 **Главное меню**\n\n" "Что хочешь сделать?",
                reply_markup=get_main_keyboard(profession),
                parse_mode="Markdown",
            )

    async def _handle_unknown(self, update, context) -> None:
        """Handle unknown messages."""
        await update.message.reply_text(
            "❓ Я не понял эту команду.\n"
            "Используй /start для начала работы или /help для списка команд."
        )

    async def shutdown(self) -> None:
        """Shutdown the bot gracefully."""
        if self.application:
            await self.application.updater.stop()
            await self.application.stop()
            await self.application.shutdown()
        logger.info("Bot stopped.")


def main():
    """Entry point."""
    setup_logging()

    bot = EgoMentorBot()

    try:
        asyncio.run(bot.start())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise


if __name__ == "__main__":
    main()
