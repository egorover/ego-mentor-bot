"""Interview service - core use case."""

from datetime import datetime
from typing import Dict, Optional

from loguru import logger

from src.application.dto.feedback_dto import FeedbackDTO
from src.domain.entities.answer import Answer
from src.domain.entities.question import Question
from src.domain.entities.user_session import UserSession
from src.domain.interfaces.question_repository import QuestionRepository
from src.domain.interfaces.star_checker import STARChecker
from src.domain.value_objects.score import Score
from src.domain.value_objects.star_result import STARResult


class InterviewService:
    """Service for conducting interview sessions."""

    def __init__(
        self,
        question_repository: QuestionRepository,
        star_checker: STARChecker,
    ):
        self.question_repository = question_repository
        self.star_checker = star_checker
        self._sessions: Dict[str, UserSession] = {}
        self._session_questions: Dict[str, Dict[str, Question]] = {}

    async def start_interview(
        self,
        user_id: str,
        profession: str,
        question_count: int = 10,
        difficulty: Optional[str] = None,
    ) -> UserSession:
        """Start a new interview session."""
        logger.info(f"Starting interview for user {user_id}, profession {profession}")

        # Get questions
        questions = await self.question_repository.get_by_profession(
            profession=profession, limit=question_count
        )

        if not questions:
            raise ValueError(f"No questions found for profession: {profession}")

        # Create session
        session = UserSession(
            user_id=user_id,
            profession=profession,
            question_ids=[q.question_id for q in questions],
        )

        self._sessions[user_id] = session
        self._session_questions[user_id] = {q.question_id: q for q in questions}

        return session

    async def submit_answer(
        self,
        user_id: str,
        answer_text: str,
    ) -> FeedbackDTO:
        """Submit and evaluate an answer."""
        session = self._sessions.get(user_id)
        if not session:
            raise ValueError("No active interview session found")

        current_q_id = session.get_current_question_id()
        if not current_q_id:
            raise ValueError("Interview completed")

        # Get question
        question = await self._get_question(user_id, current_q_id)

        # Analyze STAR structure
        star_result = await self.star_checker.check(answer_text)

        # Calculate score
        score = self._calculate_score(answer_text, star_result, question)

        # Create answer entity
        answer = Answer(
            text=answer_text,
            question_id=current_q_id,
            user_id=user_id,
            timestamp=datetime.now(),
            star_result=star_result,
            score=score,
        )

        session.add_answer(answer)
        has_more = session.move_to_next()

        # Generate feedback
        feedback = self._generate_feedback(answer, has_more)

        # Clean up if interview completed
        if not has_more:
            self._cleanup_session(user_id)

        return feedback

    async def get_next_question(self, user_id: str) -> Optional[Question]:
        """Get the next question in the interview."""
        session = self._sessions.get(user_id)
        if not session:
            return None

        q_id = session.get_current_question_id()
        if not q_id:
            return None

        return await self._get_question(user_id, q_id)

    def _calculate_score(
        self,
        answer_text: str,
        star_result: STARResult,
        question: Question,
    ) -> Score:
        """Calculate score based on multiple factors."""
        # Base score from STAR
        star_score = star_result.get_score()

        # Bonus for answer length (not too short, not too long)
        words = len(answer_text.split())
        if 50 <= words <= 300:
            length_bonus = 0.5
        elif words > 300:
            length_bonus = 0.2  # Too long
        else:
            length_bonus = 0.0  # Too short

        # Penalize very short answers
        if words < 20:
            length_bonus = -0.5

        # Calculate final score
        final_score = min(5.0, max(0.0, star_score + length_bonus))

        return Score(final_score)

    def _generate_feedback(
        self,
        answer: Answer,
        has_more: bool,
    ) -> FeedbackDTO:
        """Generate detailed feedback for answer."""
        star_result = answer.star_result

        strengths = []
        weaknesses = []
        recommendations = []

        # STAR-based feedback
        if star_result and star_result.is_complete():
            strengths.append("Хорошая структура STAR")
            if star_result.has_numbers:
                strengths.append("Есть измеримые результаты")
            else:
                recommendations.append(
                    "Добавьте цифры в результат (на сколько % улучшили?)"
                )
        else:
            if star_result:
                missing = star_result.get_missing_elements()
                weaknesses.append(f"Не хватает элементов STAR: {', '.join(missing)}")
                recommendations.append(
                    "Используйте структуру: Ситуация → Задача → Действие → Результат"
                )

        # Length-based feedback
        words = len(answer.text.split())
        if words < 30:
            weaknesses.append("Ответ слишком короткий")
            recommendations.append("Раскройте ответ подробнее, добавьте детали")
        elif words > 400:
            weaknesses.append("Ответ слишком длинный")
            recommendations.append("Старайтесь укладываться в 2-3 минуты")
        else:
            strengths.append("Оптимальная длина ответа")

        # Progress feedback
        if not has_more:
            strengths.append("Интервью завершено! Вы молодец!")

        return FeedbackDTO(
            score=answer.get_final_score(),
            strengths=strengths,
            weaknesses=weaknesses,
            recommendations=recommendations,
            star_feedback=star_result.get_feedback() if star_result else None,
        )

    async def _get_question(self, user_id: str, question_id: str) -> Question:
        """Get question by ID."""
        questions = self._session_questions.get(user_id, {})
        if question_id in questions:
            return questions[question_id]

        return await self.question_repository.get_by_id(question_id)

    def _cleanup_session(self, user_id: str) -> None:
        """Clean up session data."""
        if user_id in self._sessions:
            del self._sessions[user_id]
        if user_id in self._session_questions:
            del self._session_questions[user_id]
