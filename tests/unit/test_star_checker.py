"""Unit tests for STAR checker."""

import pytest

from src.domain.value_objects.star_result import STARResult
from src.infrastructure.ai.star_checker_impl import RuleBasedSTARChecker


@pytest.mark.asyncio
async def test_star_checker_perfect_answer():
    """Test perfect STAR answer detection."""
    checker = RuleBasedSTARChecker()

    answer = """
    В прошлом проекте (Situation) у нас была проблема с производительностью API.
    Нужно было (Task) сократить время ответа с 5 секунд до 500 мс.
    Я сделал (Action): провел профилирование, оптимизировал индексы и добавил кэш.
    В результате (Result) время ответа сократилось на 80% до 200 мс.
    """

    result = await checker.check(answer)

    assert result.has_situation is True
    assert result.has_task is True
    assert result.has_action is True
    assert result.has_result is True
    assert result.has_numbers is True
    assert result.is_complete() is True
    assert result.get_score() >= 4.5


@pytest.mark.asyncio
async def test_star_checker_missing_elements():
    """Test STAR checker with missing elements."""
    checker = RuleBasedSTARChecker()

    answer = "Я сделал оптимизацию базы данных и улучшил производительность."

    result = await checker.check(answer)

    # Short answer will fail all checks due to < 30 words rule
    assert result.is_complete() is False


@pytest.mark.asyncio
async def test_star_checker_short_answer():
    """Test very short answer."""
    checker = RuleBasedSTARChecker()

    answer = "Да, было такое"

    result = await checker.check(answer)

    assert result.has_situation is False
    assert result.has_task is False
    assert result.has_action is False
    assert result.has_result is False
    assert result.get_score() <= 1.0


@pytest.mark.asyncio
async def test_star_checker_numbers_detection():
    """Test numbers detection in result."""
    checker = RuleBasedSTARChecker()

    answer = """
    В проекте заказчика была ситуация с медленной базой данных.
    Задача состояла в оптимизации запросов для улучшения производительности.
    Я сделал анализ и переписал код, добавил индексы.
    В результате ускорил систему на 45% и сэкономил 100 часов работы.
    """

    result = await checker.check(answer)

    # Should detect numbers
    assert result.has_numbers is True


def test_star_result_feedback():
    """Test STAR result feedback generation."""
    # Complete result
    complete = STARResult(True, True, True, True, True)
    feedback = complete.get_feedback()
    assert "Отлично" in feedback or "хорошо" in feedback.lower()

    # Incomplete result
    incomplete = STARResult(True, False, True, False, False)
    feedback = incomplete.get_feedback()
    assert "не хватает" in feedback or "missing" in feedback.lower()


def test_star_result_score():
    """Test STAR result scoring."""
    # Perfect score
    perfect = STARResult(True, True, True, True, True)
    assert perfect.get_score() >= 4.5

    # Half score
    half = STARResult(True, True, False, False, False)
    assert 2.0 <= half.get_score() <= 3.0

    # Zero score
    zero = STARResult(False, False, False, False, False)
    assert zero.get_score() == 0
