"""Unit tests for domain entities."""

import pytest
from datetime import datetime

from src.domain.entities.answer import Answer
from src.domain.entities.question import Question
from src.domain.entities.user_session import UserSession
from src.domain.value_objects.difficulty import Difficulty, DifficultyLevel
from src.domain.value_objects.score import Score
from src.domain.value_objects.star_result import STARResult


def test_question_creation():
    """Test question entity creation."""
    diff = Difficulty(DifficultyLevel.MEDIUM)
    question = Question(
        text="What is Python?",
        category="Python Basics",
        profession="Python Developer",
        difficulty=diff,
    )

    assert question.text == "What is Python?"
    assert question.is_behavioral() is False
    assert question.get_difficulty_level() == 2


def test_behavioral_question_detection():
    """Test behavioral question detection."""
    diff = Difficulty(DifficultyLevel.MEDIUM)
    question = Question(
        text="Расскажите о сложной ситуации в проекте",
        category="Behavioral",
        profession="Python Developer",
        difficulty=diff,
    )

    assert question.is_behavioral() is True


def test_answer_creation():
    """Test answer entity creation."""
    answer = Answer(
        text="My answer text",
        question_id="q123",
        user_id="user456",
        timestamp=datetime.now(),
    )

    assert answer.text == "My answer text"
    assert answer.has_star_structure() is False


def test_answer_with_star():
    """Test answer with STAR result."""
    star_result = STARResult(True, True, True, True, True)
    score = Score(4.5)

    answer = Answer(
        text="STAR answer",
        question_id="q123",
        user_id="user456",
        timestamp=datetime.now(),
        star_result=star_result,
        score=score,
    )

    assert answer.has_star_structure() is True
    assert answer.get_final_score() == 4.5


def test_user_session():
    """Test user session management."""
    session = UserSession(
        user_id="user123",
        profession="Python Developer",
        question_ids=["q1", "q2", "q3"],
    )

    assert session.current_index == 0
    assert session.get_current_question_id() == "q1"
    assert session.completed is False

    # Move to q2
    assert session.move_to_next() is True
    assert session.current_index == 1
    assert session.get_current_question_id() == "q2"
    assert session.completed is False

    # Move to q3 (last question)
    assert session.move_to_next() is True
    assert session.current_index == 2
    assert session.get_current_question_id() == "q3"
    assert session.completed is False

    # Move past last question - interview completed
    assert session.move_to_next() is False
    assert session.completed is True
    assert session.get_current_question_id() is None


def test_session_score_calculation():
    """Test session average score calculation."""
    session = UserSession(
        user_id="user123",
        profession="Developer",
        question_ids=["q1", "q2"],
    )

    answer1 = Answer(
        text="Answer 1",
        question_id="q1",
        user_id="user123",
        timestamp=datetime.now(),
        score=Score(4.0),
    )

    answer2 = Answer(
        text="Answer 2",
        question_id="q2",
        user_id="user123",
        timestamp=datetime.now(),
        score=Score(5.0),
    )

    session.add_answer(answer1)
    session.add_answer(answer2)

    assert session.get_average_score() == 4.5
    assert session.get_completion_rate() == 100


def test_score_validation():
    """Test score value validation."""
    with pytest.raises(ValueError):
        Score(6.0)  # Exceeds max

    with pytest.raises(ValueError):
        Score(-1.0)  # Negative

    score = Score(3.5)
    assert score.percentage == 70.0
    assert score.get_grade() == "B (Хорошо)"


def test_difficulty_creation():
    """Test difficulty value object."""
    easy = Difficulty.easy()
    medium = Difficulty.medium()
    hard = Difficulty.hard()

    assert easy.value == 1
    assert medium.value == 2
    assert hard.value == 3

    assert "🟢" in easy.label
    assert "🟡" in medium.label
    assert "🔴" in hard.label
