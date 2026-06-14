"""Pytest configuration and fixtures."""

from pathlib import Path

import pytest

from src.application.services.star_service import STARService
from src.infrastructure.ai.star_checker_impl import RuleBasedSTARChecker
from src.infrastructure.repositories.excel_question_repository import (
    ExcelQuestionRepository,
)


@pytest.fixture
def test_knowledge_base_path():
    """Path to test knowledge base."""
    return Path(__file__).parent / "fixtures" / "test_knowledge_base.xlsx"


@pytest.fixture
def question_repository(test_knowledge_base_path):
    """Question repository fixture."""
    return ExcelQuestionRepository(test_knowledge_base_path)


@pytest.fixture
def star_checker():
    """STAR checker fixture."""
    return RuleBasedSTARChecker(use_openai=False)


@pytest.fixture
def star_service(question_repository, star_checker):
    """STAR service fixture."""
    return STARService(question_repository, star_checker)
