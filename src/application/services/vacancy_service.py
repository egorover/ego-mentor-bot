"""Vacancy service module."""

from typing import Dict, List

from loguru import logger

from src.domain.entities.vacancy import Vacancy


class VacancyService:
    """Service for vacancy analysis."""

    async def analyze_vacancy(self, vacancy_text: str) -> Dict:
        """Analyze vacancy and return structured response."""
        logger.info("Analyzing vacancy")

        # Parse vacancy
        vacancy = self._parse_vacancy(vacancy_text)

        # Analyze
        analysis = vacancy.analyze()

        # Predict questions
        predicted_questions = self._predict_questions(analysis)
        analysis.predicted_questions = predicted_questions

        # Generate recommendations
        recommendations = self._generate_recommendations(analysis)

        return {
            "title": vacancy.title,
            "key_requirements": analysis.key_requirements,
            "risk_areas": analysis.risk_areas,
            "predicted_questions": predicted_questions,
            "recommendations": recommendations,
        }

    def _parse_vacancy(self, text: str) -> Vacancy:
        """Parse vacancy text into structured format."""
        # Extract title (first line or header)
        lines = text.strip().split("\n")
        title = lines[0][:100] if lines else "Unknown Position"

        # Extract skills using pattern matching
        skills = self._extract_skills(text)

        return Vacancy(
            title=title,
            description=text,
            required_skills=skills["required"],
            preferred_skills=skills["preferred"],
        )

    def _extract_skills(self, text: str) -> Dict:
        """Extract skills from vacancy text."""
        tech_keywords = [
            "Python",
            "FastAPI",
            "Django",
            "PostgreSQL",
            "Docker",
            "Kubernetes",
            "AWS",
            "Git",
            "Redis",
            "Celery",
            "AsyncIO",
            "DevOps",
            "CI/CD",
            "Terraform",
            "Prometheus",
            "Grafana",
            "Scrum",
            "Agile",
            "Kanban",
            "Jira",
            "Figma",
            "UI/UX",
        ]

        found_skills = []
        preferred_skills = []

        text_lower = text.lower()

        for skill in tech_keywords:
            if skill.lower() in text_lower:
                # Check if it's mentioned in preferred context
                skill_pos = text_lower.find(skill.lower())
                preceding_text = text_lower[max(0, skill_pos - 100) : skill_pos]
                if "желател" in preceding_text or "будет плюсом" in preceding_text:
                    preferred_skills.append(skill)
                else:
                    found_skills.append(skill)

        return {
            "required": found_skills[:8],
            "preferred": preferred_skills[:4],
        }

    def _predict_questions(self, analysis) -> List[str]:
        """Predict likely interview questions."""
        questions = []

        # Technical questions based on skills
        for skill in analysis.key_requirements[:5]:
            if skill in ["Python", "FastAPI", "Django"]:
                questions.append(f"Расскажите о вашем опыте с {skill}")
            elif skill in ["PostgreSQL", "SQL"]:
                questions.append("Как вы оптимизируете запросы к базе данных?")
            elif skill in ["Docker", "Kubernetes"]:
                questions.append(f"Опишите ваш опыт работы с {skill} в продакшене")

        # Behavioral questions
        questions.extend(
            [
                "Расскажите о самом сложном баге, который вы исправляли",
                "Как вы работаете с дедлайнами?",
                "Приведите пример успешного проекта, которым вы гордитесь",
            ]
        )

        # Risk-based questions
        if analysis.risk_areas:
            questions.append("Как вы работаете в условиях жестких дедлайнов?")

        return questions[:10]

    def _generate_recommendations(self, analysis) -> List[str]:
        """Generate preparation recommendations."""
        recommendations = []

        if analysis.key_requirements:
            recommendations.append(
                f"Подготовьте 2-3 проекта, демонстрирующих: {', '.join(analysis.key_requirements[:3])}"
            )

        recommendations.append("Освежите в памяти 5 STAR-кейсов")
        recommendations.append("Подготовьте 30-секундную самопрезентацию")
        recommendations.append("Сформулируйте 3 вопроса к работодателю")

        return recommendations
