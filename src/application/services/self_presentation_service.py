"""Self presentation service module."""

from typing import Optional

from loguru import logger


class SelfPresentationService:
    """Service for self presentation preparation."""

    # Templates for each profession
    TEMPLATES = {
        "Python Developer": {
            "short": "Я Python-разработчик с {experience}+ годами опыта. Мой стек: {stack}. Специализируюсь на {specialization}. В последнем проекте {achievement}. Ищу {motivation}.",
            "full": "Я {name}, Python-разработчик с {experience} годами опыта. Прошел путь от Junior до {level} в {company}. Моя экспертиза — {expertise}. В своей работе я всегда отталкиваюсь от бизнес-метрик. Например, на последнем месте работы я столкнулся с проблемой {problem}. Я {action}. В результате {result}. Мне интересна ваша вакансия, потому что {motivation}.",
        },
        "DevOps / SRE": {
            "short": "Я DevOps/SRE инженер с {experience}+ годами опыта. Работаю с {stack}. Моя главная гордость — {achievement}. Ищу проект для {motivation}.",
            "full": "Я {name}, DevOps инженер с {experience} годами опыта. Специализируюсь на {specialization}. На предыдущем проекте я {achievement_full}. Ваша вакансия привлекла меня возможностью {motivation}.",
        },
        "Project Manager": {
            "short": "Я IT Project Manager с {experience} годами опыта. Работаю по {methodology}. Моя сильная сторона — {strength}. Успешно {achievement}. Хочу {motivation}.",
            "full": "Я {name}, Project Manager с {experience} годами опыта. Управлял командами до {team_size} человек. Моя ключевая компетенция — {competency}. В проекте {project_name} мы {achievement}. Ваша вакансия мне интересна, так как {motivation}.",
        },
        "Team Lead": {
            "short": "Я Team Lead команды разработки. Сочетаю техническую экспертизу с управлением людьми. За последний год {achievement}. Ищу позицию лидера в {motivation}.",
            "full": "Я {name}, в IT {total_exp} лет, из них {lead_exp} лет руководил командой из {team_size} инженеров. Моя философия — {philosophy}. Я {achievement_full}. Ищу проект, где смогу {motivation}.",
        },
        "UX/UI Designer": {
            "short": "Я UX/UI Designer с {experience} годами опыта. Специализируюсь на {specialization}. Разработал {achievement}. Ищу команду, ориентированную на {motivation}.",
            "full": "Я {name}, занимаюсь дизайном цифровых продуктов {experience} лет. Моя экспертиза включает {expertise}. В проекте {project} я {achievement_full}. Ваша вакансия интересна мне {motivation}.",
        },
        "Copywriter": {
            "short": "Я коммерческий писатель с {experience} годами опыта. Пишу {type}. Мое портфолио включает {achievement}. Ищу задачи по {motivation}.",
            "full": "Я {name}, создаю коммерческий контент {experience} лет. Моя экспертиза — {expertise}. Запустил {achievement_full}. Ваша вакансия мне интересна, так как {motivation}.",
        },
    }

    async def generate_presentation(
        self,
        profession: str,
        version: str = "short",
        user_context: Optional[dict] = None,
    ) -> str:
        """Generate self presentation based on profession."""
        logger.info(f"Generating {version} presentation for {profession}")

        template = self.TEMPLATES.get(
            profession, self.TEMPLATES.get("Python Developer")
        )

        if not template:
            return self._get_default_presentation(profession, version)

        context = user_context or {}
        template_str = template.get(version.lower(), template.get("short", ""))

        return self._fill_template(template_str, context, profession)

    def _fill_template(self, template: str, context: dict, profession: str) -> str:
        """Fill template with user context."""
        defaults = self._get_default_context(profession)
        defaults.update(context)

        try:
            return template.format(**defaults)
        except KeyError as e:
            logger.warning(f"Missing context key: {e}")
            return template

    def _get_default_context(self, profession: str) -> dict:
        """Get default context values."""
        if profession == "Python Developer":
            return {
                "name": "[Ваше имя]",
                "experience": "5",
                "stack": "FastAPI, Django, AsyncIO, PostgreSQL",
                "specialization": "проектировании микросервисной архитектуры",
                "achievement": "сократил время ответа API в 10 раз",
                "achievement_full": "переписал legacy-монолит на асинхронные сервисы, сократив время отклика API в 10 раз",
                "level": "Senior",
                "company": "[компания]",
                "expertise": "построение отказоустойчивых бэкенд-систем",
                "problem": "деградацией БД в пиковые распродажи",
                "action": "провел аудит и оптимизировал запросы",
                "result": "выдержали нагрузку без увеличения бюджета",
                "motivation": "сложные Highload-задачи",
            }

        # Default for any profession
        return {
            "name": "[Ваше имя]",
            "experience": "X",
            "stack": "[ваши технологии]",
            "specialization": "[ваша специализация]",
            "achievement": "[ваше достижение]",
            "motivation": "[ваша мотивация]",
        }

    def _get_default_presentation(self, profession: str, version: str) -> str:
        """Get default presentation if template not found."""
        if version == "short":
            return f"Я {profession}. Имею опыт работы в этой сфере. Стремлюсь развиваться и приносить пользу компании."

        return f"Я {profession} с опытом работы в IT-сфере. Владею необходимыми компетенциями. Готов к новым вызовам и профессиональному росту."
