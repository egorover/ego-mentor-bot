"""Checklist handler module."""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from src.infrastructure.repositories.excel_question_repository import (
    ExcelQuestionRepository,
)


class ChecklistHandler:
    """Handler for interview checklists."""

    def __init__(self, question_repository: ExcelQuestionRepository):
        self.question_repository = question_repository

    async def handle_checklist_menu(self, query) -> None:
        """Show checklist menu."""
        keyboard = [
            [InlineKeyboardButton("📅 До интервью", callback_data="checklist_before")],
            [
                InlineKeyboardButton(
                    "⚡ Во время интервью", callback_data="checklist_during"
                )
            ],
            [
                InlineKeyboardButton(
                    "🏁 После интервью", callback_data="checklist_after"
                )
            ],
            [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")],
        ]

        await query.edit_message_text(
            "✅ **Чек-лист подготовки к интервью**\n\n"
            "Выбери этап, чтобы увидеть подробный список:\n\n"
            "📅 **До интервью** — что сделать за день до собеседования\n"
            "⚡ **Во время** — как правильно себя вести\n"
            "🏁 **После** — как закрепить успех",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )

    async def handle_checklist_stage(self, query, data: str) -> None:
        """Handle checklist stage selection."""
        stage_map = {
            "checklist_before": "Этап 1: До интервью (Подготовка)",
            "checklist_during": "Этап 2: Во время интервью (Тактика)",
            "checklist_after": "Этап 3: После интервью (Закрепление)",
        }

        stage = stage_map.get(data, "Этап 1: До интервью (Подготовка)")

        items = self.question_repository.get_checklist(stage)

        if not items:
            await query.edit_message_text(
                f"📋 **{stage}**\n\n"
                f"Чек-лист временно недоступен.\n\n"
                f"🔙 Нажми назад для возврата в меню.",
                parse_mode="Markdown",
            )
            return

        # Format checklist
        lines = [f"📋 **{stage}**\n"]

        for item in items:
            lines.append(f"☐ {item}")

        lines.append("\n💡 **Совет:** Распечатай этот чек-лист и отмечай галочки!")
        lines.append("\n🔙 Нажми /checklist для возврата в меню")

        await query.edit_message_text(
            "\n".join(lines),
            parse_mode="Markdown",
        )
