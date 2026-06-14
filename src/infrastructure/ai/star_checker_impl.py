"""STAR checker implementation."""

import re
from typing import Optional

from loguru import logger

from src.domain.value_objects.star_result import STARResult
from src.domain.interfaces.star_checker import STARChecker


class RuleBasedSTARChecker(STARChecker):
    """Rule-based STAR checker without AI."""

    # Keywords for each STAR component
    SITUATION_KEYWORDS = [
        "ситуац",
        "проект",
        "задач",
        "работал",
        "команда",
        "разработк",
        "было",
        "столкнул",
        "возникл",
        "клиент",
    ]

    TASK_KEYWORDS = [
        "задач",
        "нужно",
        "требовал",
        "необходимо",
        "цель",
        "должен",
        "надо было",
        "стояла",
        "поручен",
    ]

    ACTION_KEYWORDS = [
        "сделал",
        "написал",
        "внедрил",
        "реализовал",
        "оптимизировал",
        "настроил",
        "создал",
        "разработал",
        "предложил",
        "организовал",
        "провел",
        "улучшил",
        "изменил",
        "применил",
    ]

    RESULT_KEYWORDS = [
        "результат",
        "удалось",
        "достиг",
        "сократил",
        "увеличил",
        "улучшил",
        "выросло",
        "упало",
        "сэкономил",
        "повысил",
        "%,",
        "% ",
        "процент",
        "секунд",
        "миллисекунд",
        "раз",
        "ускорил",
        "снизил",
    ]

    def __init__(self, use_openai: bool = False, openai_client: Optional = None):
        self.use_openai = use_openai
        self.openai_client = openai_client

    async def check(self, answer_text: str) -> STARResult:
        """Check answer for STAR structure."""
        if self.use_openai and self.openai_client:
            return await self._check_with_openai(answer_text)
        return self._check_with_rules(answer_text)

    def _check_with_rules(self, answer_text: str) -> STARResult:
        """Check using rule-based approach."""
        text_lower = answer_text.lower()

        has_situation = any(
            keyword in text_lower for keyword in self.SITUATION_KEYWORDS
        )
        has_task = any(keyword in text_lower for keyword in self.TASK_KEYWORDS)
        has_action = any(keyword in text_lower for keyword in self.ACTION_KEYWORDS)
        has_result = any(keyword in text_lower for keyword in self.RESULT_KEYWORDS)

        # Check for numbers (good indicator of measurable results)
        has_numbers = bool(re.search(r"\d+", answer_text))

        # If result is present, check for numbers bonus
        if has_result and has_numbers:
            has_result = True

        # If answer is very short, it's likely incomplete
        if len(answer_text.split()) < 30:
            has_situation = has_situation and False
            has_task = has_task and False
            has_action = has_action and False
            has_result = has_result and False

        logger.debug(
            f"STAR result: S={has_situation}, T={has_task}, A={has_action}, R={has_result}, N={has_numbers}"
        )

        return STARResult(
            has_situation=has_situation,
            has_task=has_task,
            has_action=has_action,
            has_result=has_result,
            has_numbers=has_numbers,
        )

    async def _check_with_openai(self, answer_text: str) -> STARResult:
        """Check using OpenAI API for more accurate analysis."""
        try:
            from openai import AsyncOpenAI

            client = self.openai_client or AsyncOpenAI()

            prompt = f"""
            Analyze the following answer for STAR structure (Situation, Task, Action, Result).
            Return JSON with boolean values for each component and whether numbers are present.

            Answer: {answer_text}

            Return format: {{"situation": true/false, "task": true/false, "action": true/false, "result": true/false, "has_numbers": true/false}}
            """

            response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=150,
            )

            import json

            result = json.loads(response.choices[0].message.content)

            return STARResult(
                has_situation=result.get("situation", False),
                has_task=result.get("task", False),
                has_action=result.get("action", False),
                has_result=result.get("result", False),
                has_numbers=result.get("has_numbers", False),
            )

        except Exception as e:
            logger.error(f"OpenAI check failed: {e}, falling back to rules")
            return self._check_with_rules(answer_text)
