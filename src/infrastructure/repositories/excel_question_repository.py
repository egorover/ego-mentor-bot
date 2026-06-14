"""Excel-based question repository implementation."""

from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd
from loguru import logger

from src.domain.entities.question import Question
from src.domain.interfaces.question_repository import QuestionRepository
from src.domain.value_objects.difficulty import Difficulty, DifficultyLevel


class ExcelQuestionRepository(QuestionRepository):
    """Question repository using Excel file as storage."""

    def __init__(self, excel_path: Path):
        self.excel_path = excel_path
        self._questions_df = None
        self._star_df = None
        self._presentation_df = None
        self._checklist_df = None
        self._vacancy_df = None
        self._load_data()

    def _load_data(self) -> None:
        """Load all data from Excel file."""
        try:
            logger.info(f"Loading knowledge base from {self.excel_path}")

            self._questions_df = pd.read_excel(
                self.excel_path, sheet_name="Interview_Questions"
            )
            self._star_df = pd.read_excel(self.excel_path, sheet_name="STAR_Examples")
            self._presentation_df = pd.read_excel(
                self.excel_path, sheet_name="Self_Presentation"
            )
            self._checklist_df = pd.read_excel(
                self.excel_path, sheet_name="Interview_Checklists"
            )
            self._vacancy_df = pd.read_excel(
                self.excel_path, sheet_name="Vacancy_Analysis"
            )

            logger.info(f"Loaded {len(self._questions_df)} questions")

        except Exception as e:
            logger.error(f"Failed to load knowledge base: {e}")
            raise

    async def get_by_profession(
        self,
        profession: str,
        difficulty: Optional[DifficultyLevel] = None,
        limit: int = 10,
    ) -> List[Question]:
        """Get questions by profession and optional difficulty."""
        df = self._questions_df[self._questions_df["Profession"] == profession]

        if difficulty:
            df = df[df["Difficulty"] == difficulty.value]

        # Shuffle for variety
        df = df.sample(frac=1).head(limit)

        questions = []
        for _, row in df.iterrows():
            diff_level = DifficultyLevel.from_string(row["Difficulty"])
            if diff_level:
                question = Question(
                    text=row["Question"],
                    category=row["Category"],
                    profession=profession,
                    difficulty=Difficulty(diff_level),
                    question_id=f"{profession}_{row.name}",
                )
                questions.append(question)

        logger.debug(f"Retrieved {len(questions)} questions for {profession}")
        return questions

    async def get_by_id(self, question_id: str) -> Optional[Question]:
        """Get single question by ID."""
        # Parse question_id to find row
        for _, row in self._questions_df.iterrows():
            qid = f"{row['Profession']}_{row.name}"
            if qid == question_id:
                diff_level = DifficultyLevel.from_string(row["Difficulty"])
                if diff_level:
                    return Question(
                        text=row["Question"],
                        category=row["Category"],
                        profession=row["Profession"],
                        difficulty=Difficulty(diff_level),
                        question_id=qid,
                    )
        return None

    async def get_random_star_question(self, profession: str) -> Optional[Question]:
        """Get random behavioral question for STAR practice."""
        df = self._questions_df[
            (self._questions_df["Profession"] == profession)
            & (self._questions_df["Difficulty"].isin(["Medium", "Hard"]))
        ]

        # Filter behavioral questions
        behavioral_df = df[
            df["Question"]
            .str.lower()
            .str.contains(
                "расскаж|ситуац|пример|опис|сложн|сталкивал",
                na=False,
            )
        ]

        if behavioral_df.empty:
            behavioral_df = df

        if behavioral_df.empty:
            return None

        row = behavioral_df.sample(1).iloc[0]
        diff_level = DifficultyLevel.from_string(row["Difficulty"])

        if diff_level:
            return Question(
                text=row["Question"],
                category=row["Category"],
                profession=profession,
                difficulty=Difficulty(diff_level),
                question_id=f"{profession}_star_{row.name}",
            )

        return None

    def get_star_example(self, profession: str) -> Optional[Dict]:
        """Get STAR example from knowledge base."""
        df = self._star_df[self._star_df["Profession"] == profession]

        if df.empty:
            logger.warning(f"No STAR examples found for {profession}")
            return None

        row = df.sample(1).iloc[0]
        return {
            "competency": row.get("Competency", "Общий кейс"),
            "situation": row.get("Situation", ""),
            "task": row.get("Task", ""),
            "action": row.get("Action", ""),
            "result": row.get("Result", ""),
        }

    def get_self_presentation(
        self, profession: str, version: str = "Short (30 sec)"
    ) -> Optional[str]:
        """Get self presentation template."""
        df = self._presentation_df[
            (self._presentation_df["Profession"] == profession)
            & (self._presentation_df["Version"] == version)
        ]

        if df.empty:
            logger.warning(f"No presentation template for {profession}/{version}")
            return None

        return df.iloc[0]["Presentation"]

    def get_checklist(self, stage: str) -> List[str]:
        """Get checklist items by stage."""
        df = self._checklist_df[self._checklist_df["Stage"] == stage]
        return df["Checklist Item"].tolist()

    def get_vacancy_analysis(
        self, profession: str, level: str = "Middle"
    ) -> Optional[Dict]:
        """Get vacancy analysis template."""
        df = self._vacancy_df[
            (self._vacancy_df["Vacancy Type"] == profession)
            & (self._vacancy_df["Level"] == level)
        ]

        if df.empty:
            return None

        row = df.iloc[0]
        return {
            "key_skills": row.get("Key Skills", ""),
            "common_questions": row.get("Common Questions", ""),
            "preparation_tips": row.get("Preparation Tips", ""),
        }
