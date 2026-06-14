"""Self presentation handler module."""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from src.application.services.self_presentation_service import SelfPresentationService


class SelfPresentationHandler:
    """Handler for self presentation templates."""

    def __init__(self, presentation_service: SelfPresentationService):
        self.presentation_service = presentation_service

    async def handle_self_presentation(
        self, query, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Handle self presentation request."""
        profession = context.user_data.get("profession")

        if not profession:
            await query.edit_message_text(
                "⚠️ **Сначала выбери профессию**\n\n"
                "Используй /start и выбери свою роль.",
                parse_mode="Markdown",
            )
            return

        keyboard = [
            [InlineKeyboardButton("🎤 Короткая (30 сек)", callback_data="pres_short")],
            [InlineKeyboardButton("📖 Полная (90 сек)", callback_data="pres_full")],
            [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")],
        ]

        await query.edit_message_text(
            f"🗣 **Самопрезентация для {profession}**\n\n"
            f"Выбери формат:\n\n"
            f"• **Короткая (30 сек)** — для быстрого знакомства\n"
            f"• **Полная (90 сек)** — для основного интервью\n\n"
            f"💡 **Совет:** Замени примеры на свои реальные достижения и отрепетируй перед зеркалом!",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )

        # Store selection
        context.user_data["presentation_profession"] = profession

    async def handle_presentation_version(
        self,
        query,
        version: str,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> None:
        """Handle presentation version selection."""
        profession = context.user_data.get("presentation_profession")

        if not profession:
            await query.edit_message_text(
                "⚠️ Ошибка: профессия не выбрана. Используй /start"
            )
            return

        version_map = {
            "pres_short": "Short (30 sec)",
            "pres_full": "Full (90 sec)",
        }

        version_name = version_map.get(version, "Short (30 sec)")

        # Generate presentation
        presentation = await self.presentation_service.generate_presentation(
            profession=profession,
            version="short" if "short" in version else "full",
        )

        if not presentation:
            presentation = await self._get_fallback_presentation(
                profession, version_name
            )

        response = (
            f"🗣 **Самопрезентация ({version_name})**\n\n"
            f"```\n{presentation}\n```\n\n"
            f"📝 **Как использовать:**\n\n"
            f"1. Замени `[Ваше имя]` и другие скобки на свои данные\n"
            f"2. Добавь реальные цифры достижений\n"
            f"3. Отрепетируй 3-5 раз перед зеркалом\n"
            f"4. Засеки время — оно должно точно соответствовать формату\n\n"
            f"💡 **Важно:** Не читай с листа! Рассказывай естественно."
        )

        await query.edit_message_text(response, parse_mode="Markdown")

    async def _get_fallback_presentation(self, profession: str, version: str) -> str:
        """Get fallback presentation if generation fails."""
        if "коротк" in version.lower() or "short" in version.lower():
            return f"Я {profession}. Имею опыт работы в этой сфере. Стремлюсь развиваться и приносить пользу компании."
        return f"Я {profession} с опытом работы в IT-сфере. Владею необходимыми компетенциями. Готов к новым вызовам и профессиональному росту."
