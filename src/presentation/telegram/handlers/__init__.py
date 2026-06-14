"""Handlers module for Telegram bot."""

from .start_handler import StartHandler
from .interview_handler import InterviewHandler
from .vacancy_handler import VacancyHandler
from .star_handler import StarHandler
from .self_presentation_handler import SelfPresentationHandler
from .checklist_handler import ChecklistHandler

__all__ = [
    "StartHandler",
    "InterviewHandler",
    "VacancyHandler",
    "StarHandler",
    "SelfPresentationHandler",
    "ChecklistHandler",
]
