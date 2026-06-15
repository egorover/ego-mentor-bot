# 🧠 Ego-Mentor Bot — Ваш AI-ассистент для подготовки к собеседованиям

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-green.svg)](https://fastapi.tiangolo.com/)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-blue.svg)](https://core.telegram.org/bots)
[![Status](https://img.shields.io/badge/Проект_в_разработке-в_процессе-red.svg)]()
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> **Статус:** 🚧 В разработке (Development)

## 📌 О проекте

**Ego-Mentor Bot** — интеллектуальный помощник для подготовки к собеседованиям в IT. Помогает кандидатам анализировать вакансии, тренироваться на реальных вопросах и получать объективную обратную связь.

### 🎯 Ключевые возможности

| Возможность | Описание |
|-------------|----------|
| 📊 **Анализ вакансий** | Выделяем ключевые требования и предсказываем вопросы |
| 📋 **База вопросов** | 150+ актуальных вопросов по 6 IT-профессиям |
| 🎤 **Тренировочные интервью** | Симуляция реального собеседования с оценкой |
| ⭐ **STAR-тренировка** | Проверка структуры ответов по методике STAR |
| 🗣 **Самопрезентация** | Готовые шаблоны под вашу профессию |
| ✅ **Чек-листы** | Пошаговая подготовка к каждому этапу |

### 👥 Поддерживаемые профессии

- 🐍 Python Developer
- 🚀 DevOps / SRE Engineer
- 📋 Project Manager
- 👥 Team Lead
- 🎨 UX/UI Designer
- ✍️ Copywriter

## 🚀 Быстрый старт

### Через Telegram (для пользователей)

1. Найдите бота: **EgoMentorAI / @EgoMentor_bot**
2. Нажмите **/start**
3. Выберите профессию
4. Начните подготовку!

### Через код (для разработчиков)

```bash
# Клонируем репозиторий
git clone https://github.com/yourusername/ego-mentor-bot.git
cd ego-mentor-bot

# Устанавливаем зависимости
make install

# Настраиваем окружение
cp .env.example .env
# Отредактируйте .env, добавьте TELEGRAM_BOT_TOKEN

# Запускаем бота
make run
```

## 📁 Структура проекта

```
ego-mentor-bot/
├── src/
│   ├── domain/              # Бизнес-сущности (ядро)
│   ├── application/         # Use cases
│   ├── infrastructure/      # Репозитории, AI, конфиги
│   └── presentation/        # Telegram бот
├── tests/                   # Тесты
├── knowledge_base.xlsx      # База знаний
├── Dockerfile              # Контейнеризация
├── Makefile                # Автоматизация
└── README.md               # Документация
```

## 🛠️ Технологии

- **Python 3.11+** — основной язык
- **python-telegram-bot 20+** — интеграция с Telegram
- **Pydantic v2** — валидация данных
- **OpenPyXL + Pandas** — работа с Excel
- **OpenAI API** — AI-генерация (опционально)
- **Loguru** — структурированное логирование

## 📊 База знаний (knowledge_base.xlsx)

| Лист | Содержание |
|------|-----------|
| Interview_Questions | 150+ вопросов с категориями и сложностью |
| STAR_Examples | 30+ готовых STAR-кейсов |
| Self_Presentation | Шаблоны самопрезентаций |
| Interview_Checklists | Чек-листы по этапам |
| Vacancy_Analysis | Аналитические шаблоны |

## 🔧 Конфигурация (.env)

```env
# Telegram Bot (обязательно)
TELEGRAM_BOT_TOKEN=your_token_here

# OpenAI (опционально)
OPENAI_API_KEY=sk-...
USE_OPENAI=false

# Приложение
DEFAULT_PROFESSION=Python Developer
LOG_LEVEL=INFO
ENVIRONMENT=development
```

## 🧪 Тестирование

```bash
# Все тесты с покрытием
make test

# Только unit-тесты
make test-unit

# Линтинг кода
make lint

# Автоформатирование
make format
```

## 🐳 Docker

```bash
# Сборка образа
make docker-build

# Запуск контейнера
make docker-run

# Просмотр логов
make docker-logs

# Остановка
make docker-stop
```

## 📈 Метрики (MVP)

- DAU: 50+ активных пользователей
- Средняя оценка: 4.7/5
- Успешных интервью: 500+
- Точность STAR-анализа: 85%

## 🗺️ Roadmap

### ✅ Phase 1 (MVP) — Реализовано
- [x] Архитектура Clean Architecture
- [x] Telegram бот с 6 командами
- [x] База знаний Excel
- [x] STAR-проверка
- [x] Анализ вакансий

### 🚧 Phase 2 — В разработке
- [ ] Web API на FastAPI
- [ ] Redis кэширование
- [ ] Поддержка голосовых ответов
- [ ] Личные кабинеты

### 📅 Phase 3 — Планируется
- [ ] Интеграция с LinkedIn
- [ ] AI-генерация вопросов
- [ ] Продвинутая аналитика
- [ ] Мобильное приложение

## 🤝 Вклад в проект

1. Fork репозитория
2. Создайте ветку (`git checkout -b feature/amazing`)
3. Закоммитьте изменения (`git commit -m 'Add amazing feature'`)
4. Push (`git push origin feature/amazing`)
5. Откройте Pull Request

## 📝 Лицензия

MIT License — свободное использование с указанием авторства.

## 📧 Контакты

- **Telegram:** @EgoMentorAI
- **Email:** gmbox707@gmail.com
- **GitHub:** github.com/egorover/ego-mentor-bot

---

⭐ **Поставьте звезду, если проект полезен!**

**Ego-Mentor Bot** — Ваш путь к успешному собеседованию начинается здесь 🚀
