"""Start command handler."""

from typing import List

from loguru import logger
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from src.infrastructure.config.settings import settings
from src.infrastructure.repositories.excel_question_repository import (
    ExcelQuestionRepository,
)
from src.presentation.telegram.keyboards import (
    get_profession_keyboard,
    get_main_keyboard,
)


class StartHandler:
    """Handler for /start command and profession selection."""

    def __init__(self, professions: List[str], default_profession: str):
        self.professions = professions
        self.default_profession = default_profession
        self.user_professions = {}

    async def handle_start(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Handle /start command."""
        user = update.effective_user
        logger.info(f"User {user.id} started the bot")

        welcome_text = (
            f"👋 Привет, {user.first_name}!\n\n"
            "Я **Ego-Mentor AI** — интеллектуальный ассистент для подготовки к собеседованиям.\n\n"
            "Я помогу тебе:\n"
            "• 📊 Анализировать вакансии\n"
            "• 📋 Готовить ответы на вопросы\n"
            "• 🎤 Тренироваться в реальных интервью\n"
            "• ⭐ Проверять ответы по методике STAR\n"
            "• 🗣 Составлять самопрезентацию\n\n"
            "**Выбери свою профессию для начала:**"
        )

        await update.message.reply_text(
            welcome_text,
            reply_markup=get_profession_keyboard(self.professions),
            parse_mode="Markdown",
        )

    async def handle_select_profession(self, query) -> None:
        """Handle profession selection button."""
        await query.edit_message_text(
            "🎯 **Выбери свою профессию:**",
            reply_markup=get_profession_keyboard(self.professions),
            parse_mode="Markdown",
        )

    async def handle_profession_selected(self, query, data: str) -> None:
        """Handle profession selection."""
        profession = data.replace("prof_", "")
        user_id = query.from_user.id

        self.user_professions[user_id] = profession
        logger.info(f"User {user_id} selected profession: {profession}")

        await query.edit_message_text(
            f"✅ **Профессия выбрана:** {profession}\n\n"
            f"Теперь я буду задавать вопросы под твою роль.\n\n"
            f"**Что хочешь сделать?**",
            reply_markup=get_main_keyboard(profession),
            parse_mode="Markdown",
        )

    async def handle_get_questions(
        self, query, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Handle get questions button."""
        profession = context.user_data.get("profession")

        if not profession:
            await query.edit_message_text(
                "⚠️ **Сначала выбери профессию**\n\n"
                "Нажми кнопку «Выбрать профессию» в главном меню.",
                parse_mode="Markdown",
            )
            return

        keyboard = [
            [InlineKeyboardButton("🟢 Easy (базовые)", callback_data="questions_Easy")],
            [
                InlineKeyboardButton(
                    "🟡 Medium (средние)", callback_data="questions_Medium"
                )
            ],
            [InlineKeyboardButton("🔴 Hard (сложные)", callback_data="questions_Hard")],
            [InlineKeyboardButton("🎲 Все уровни", callback_data="questions_All")],
            [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")],
        ]

        await query.edit_message_text(
            f"📋 **Вопросы для {profession}**\n\n" f"Выбери уровень сложности:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )

    async def handle_questions_difficulty(
        self, query, data: str, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Handle questions difficulty selection and show questions."""
        profession = context.user_data.get("profession")

        if not profession:
            await query.edit_message_text(
                "⚠️ **Сначала выбери профессию**\n\n" "Используй /start",
                parse_mode="Markdown",
            )
            return

        difficulty = data.replace("questions_", "")
        if difficulty == "All":
            difficulty = None

        # Get questions from repository
        from src.domain.value_objects.difficulty import DifficultyLevel

        repo = ExcelQuestionRepository(settings.knowledge_base_path)

        diff_enum = None
        if difficulty and difficulty != "All":
            diff_enum = DifficultyLevel.from_string(difficulty)

        questions = await repo.get_by_profession(profession, diff_enum, limit=15)

        if not questions:
            await query.edit_message_text(
                f"❌ Нет вопросов для {profession} уровнем {difficulty or 'все'}\n\n"
                f"Попробуй другой уровень сложности.",
                parse_mode="Markdown",
            )
            return

        # Format questions
        lines = [f"📋 **Вопросы для {profession}**"]
        if difficulty:
            lines.append(f"Уровень: {difficulty}")
        lines.append("")

        current_category = None
        for i, q in enumerate(questions, 1):
            if q.category != current_category:
                current_category = q.category
                lines.append(f"\n*{current_category}:*")
            lines.append(f"{i}. {q.text}")

        lines.append("\n---")
        lines.append("💡 **Как тренироваться:**")
        lines.append("• /interview - пройти полноценное интервью")
        lines.append("• /star - отработать STAR-ответы")
        lines.append("• Отвечай вслух перед зеркалом")

        # Split if too long (Telegram limit 4096)
        response = "\n".join(lines)
        if len(response) > 4000:
            # Send first part
            await query.edit_message_text(response[:4000], parse_mode="Markdown")
            # Send second part
            await query.message.reply_text(response[4000:8000], parse_mode="Markdown")
        else:
            await query.edit_message_text(response, parse_mode="Markdown")

    async def handle_help(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Handle /help command."""
        help_text = (
            "❓ **Помощь по Ego-Mentor AI**\n\n"
            "**Доступные команды:**\n"
            "/start — начать работу\n"
            "/help — эта справка\n\n"
            "**Что я умею:**\n\n"
            "📊 **Анализ вакансий** — пришли текст вакансии, я выделю ключевые требования и вероятные вопросы\n\n"
            "📋 **Вопросы по профессии** — получу список вопросов для твоей роли с разным уровнем сложности\n\n"
            "🎤 **Тренировочное интервью** — проведу полноценное интервью с обратной связью в конце\n\n"
            "⭐ **STAR-тренировка** — проверю, насколько хорошо твои ответы соответствуют методике STAR\n\n"
            "🗣 **Самопрезентация** — дам шаблоны для рассказа о себе (30 сек и 90 сек)\n\n"
            "✅ **Чек-лист** — покажу, к чему готовиться перед интервью\n\n"
            "**Совет:** Всегда используй структуру STAR для поведенческих вопросов!"
        )

        await update.message.reply_text(help_text, parse_mode="Markdown")

    async def handle_help_callback(self, query) -> None:
        """Handle help button callback."""
        help_text = (
            "❓ **Помощь по Ego-Mentor AI**\n\n"
            "**Что я умею:**\n\n"
            "📊 **Анализ вакансий** — пришли текст вакансии\n\n"
            "📋 **Вопросы по профессии** — выбери уровень сложности\n\n"
            "🎤 **Тренировочное интервью** — отвечай на вопросы по одному\n\n"
            "⭐ **STAR-тренировка** — расскажи о своем опыте\n\n"
            "🗣 **Самопрезентация** — получи готовый шаблон\n\n"
            "✅ **Чек-лист** — подготовься ко всем этапам\n\n"
            "💡 **Важно:** Для поведенческих вопросов используй STAR: Ситуация → Задача → Действие → Результат"
        )

        await query.edit_message_text(help_text, parse_mode="Markdown")
