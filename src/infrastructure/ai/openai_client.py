"""OpenAI client wrapper."""

from typing import Dict, List

from loguru import logger
from openai import AsyncOpenAI


class OpenAIClient:
    """Wrapper for OpenAI API."""

    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)
        logger.info("OpenAI client initialized")

    async def generate_questions(
        self, profession: str, category: str, count: int = 5
    ) -> List[str]:
        """Generate interview questions using AI."""
        try:
            prompt = f"""
            Generate {count} interview questions for a {profession} position.
            Category: {category}

            Make questions specific, practical, and at a professional level.
            Return only the questions, one per line.
            """

            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=500,
            )

            content = response.choices[0].message.content
            questions = [q.strip() for q in content.split("\n") if q.strip()]

            return questions[:count]

        except Exception as e:
            logger.error(f"Failed to generate questions: {e}")
            return []

    async def analyze_answer(self, question: str, answer: str, profession: str) -> Dict:
        """Analyze answer using AI."""
        try:
            prompt = f"""
            Analyze this interview answer.

            Question: {question}
            Answer: {answer}
            Profession: {profession}

            Provide analysis in JSON format:
            {{
                "score": float (0-5),
                "strengths": ["strength1", "strength2"],
                "weaknesses": ["weakness1", "weakness2"],
                "recommendations": ["rec1", "rec2"]
            }}
            """

            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=300,
            )

            import json

            result = json.loads(response.choices[0].message.content)
            return result

        except Exception as e:
            logger.error(f"Failed to analyze answer: {e}")
            return {
                "score": 3.0,
                "strengths": ["Ответ получен"],
                "weaknesses": ["Не удалось выполнить глубокий анализ"],
                "recommendations": ["Попробуйте использовать структуру STAR"],
            }

    async def is_available(self) -> bool:
        """Check if OpenAI API is available."""
        try:
            await self.client.models.list()
            return True
        except Exception:
            return False
