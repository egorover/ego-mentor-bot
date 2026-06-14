"""Telegram keyboard builders."""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_profession_keyboard(professions: list) -> InlineKeyboardMarkup:
    """Build profession selection keyboard."""
    keyboard = []

    for prof in professions:
        keyboard.append([InlineKeyboardButton(prof, callback_data=f"prof_{prof}")])

    return InlineKeyboardMarkup(keyboard)


def get_main_keyboard(profession: str = None) -> InlineKeyboardMarkup:
    """Build main menu keyboard."""
    prof_text = f"🎯 {profession}" if profession else "🎯 Выбрать профессию"

    keyboard = [
        [InlineKeyboardButton(prof_text, callback_data="select_profession")],
        [InlineKeyboardButton("📊 Анализ вакансии", callback_data="analyze_vacancy")],
        [
            InlineKeyboardButton(
                "📋 Вопросы по профессии", callback_data="get_questions"
            )
        ],
        [
            InlineKeyboardButton(
                "🎤 Тренировочное интервью", callback_data="start_interview"
            )
        ],
        [InlineKeyboardButton("⭐ STAR-тренировка", callback_data="star_training")],
        [InlineKeyboardButton("🗣 Самопрезентация", callback_data="self_presentation")],
        [InlineKeyboardButton("✅ Чек-лист подготовки", callback_data="checklist")],
        [InlineKeyboardButton("❓ Помощь", callback_data="help")],
    ]

    return InlineKeyboardMarkup(keyboard)


def get_difficulty_keyboard() -> InlineKeyboardMarkup:
    """Build difficulty selection keyboard."""
    keyboard = [
        [InlineKeyboardButton("🟢 Easy (Базовый)", callback_data="difficulty_easy")],
        [
            InlineKeyboardButton(
                "🟡 Medium (Средний)", callback_data="difficulty_medium"
            )
        ],
        [
            InlineKeyboardButton(
                "🔴 Hard (Продвинутый)", callback_data="difficulty_hard"
            )
        ],
        [InlineKeyboardButton("🎲 Все уровни", callback_data="difficulty_all")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_interview_settings_keyboard() -> InlineKeyboardMarkup:
    """Build interview settings keyboard."""
    keyboard = [
        [InlineKeyboardButton("5 вопросов", callback_data="interview_5")],
        [InlineKeyboardButton("10 вопросов", callback_data="interview_10")],
        [InlineKeyboardButton("15 вопросов", callback_data="interview_15")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)
