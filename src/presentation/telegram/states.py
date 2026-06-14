"""Conversation states for Telegram bot."""

from enum import IntEnum


class ConversationStates(IntEnum):
    """States for conversation handlers."""

    # Vacancy analysis
    WAITING_VACANCY = 1

    # STAR training
    WAITING_STAR_ANSWER = 2

    # Interview
    WAITING_INTERVIEW_ANSWER = 3

    # Question selection
    WAITING_DIFFICULTY = 4

    # Self presentation
    WAITING_PRESENTATION_VERSION = 5
