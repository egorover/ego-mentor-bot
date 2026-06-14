"""Vacancy entity module."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Vacancy:
    """Domain entity representing a job vacancy."""

    title: str
    description: str
    required_skills: List[str] = field(default_factory=list)
    preferred_skills: List[str] = field(default_factory=list)
    key_responsibilities: List[str] = field(default_factory=list)

    def analyze(self) -> "VacancyAnalysis":
        """Perform domain analysis of vacancy."""
        return VacancyAnalysis(
            vacancy=self,
            key_requirements=self._extract_key_requirements(),
            risk_areas=self._identify_risk_areas(),
        )

    def _extract_key_requirements(self) -> List[str]:
        """Extract key requirements from description."""
        requirements = []
        keywords = ["требовани", "необходим", "должен уметь", "опыт работы"]
        desc_lower = self.description.lower()

        for keyword in keywords:
            if keyword in desc_lower:
                requirements.append(keyword)

        return requirements + self.required_skills

    def _identify_risk_areas(self) -> List[str]:
        """Identify potential risk areas for this vacancy."""
        risks = []
        risk_indicators = ["строгий", "жёстк", "дедлайн", "высоконагруз"]

        for indicator in risk_indicators:
            if indicator in self.description.lower():
                risks.append(f"Возможны {indicator} условия")

        return risks


@dataclass
class VacancyAnalysis:
    """Value object for vacancy analysis result."""

    vacancy: Vacancy
    key_requirements: List[str]
    risk_areas: List[str]
    predicted_questions: List[str] = field(default_factory=list)
