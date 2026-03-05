# Langfuse интеграция для системы AI-ревью тест-кейсов

## Установка и настройка

### Требования

- Python >= 3.10
- [uv](https://github.com/astral-sh/uv) — быстрый Python пакетный менеджер

### Установка зависимостей проекта

```bash
# Создание виртуального окружения и установка зависимостей
uv sync

# Или только установка зависимостей (если .venv уже создан)
uv pip install -r requirements.txt

# Установка dev-зависимостей (для тестов)
uv sync --dev
```

### Настройка переменных окружения

Скопируйте `.env.example` в `.env` и заполните свои credentials:

```bash
cp .env.example .env
```

Отредактируйте `.env`:

```bash
LANGFUSE_PUBLIC_KEY=pk-ваш-ключ
LANGFUSE_SECRET_KEY=sk-ваш-ключ
LANGFUSE_HOST=https://cloud.langfuse.com
```

## Логика работы

```
1. Промпты в prompts/
   ↓
2. Синхронизация в Langfuse Prompt Management
   ↓
3. Создание датасета с тестовыми кейсами
   ↓
4. Запуск эксперимента
   ↓
5. Результаты в UI
```

## Структура

```
langfuse/
├── .env                      # Credentials
├── .env.example              # Шаблон
├── utils/                    # Утилиты
│   ├── config.py             # Загрузка .env
│   ├── client.py             # Langfuse клиент
│   ├── prompts.py            # Создание/обновление промптов
│   ├── sync.py               # Синхронизация промптов
│   ├── datasets.py           # Датасеты
│   ├── experiments.py        # Эксперименты
│   └── post_review.py        # Логика post_review
├── scripts/                  # Скрипты
│   ├── sync_post_review.py   # Синхронизация post_review
│   ├── sync_review.py        # Синхронизация review
│   ├── sync_edit_testcase.py # Синхронизация edit_testcase
│   ├── create_dataset.py     # Создание датасета
│   ├── run_experiment.py     # Запуск эксперимента
│   └── run_all.py            # Все стадии
└── README.md
```

## Использование

### Запуск тестов

```bash
# Все тесты
uv run pytest tests/ -v

# Только локальные тесты (без Langfuse credentials)
uv run pytest tests/test_pre_node.py::TestPreNode::test_pre_node_with_local_dataset -v

# Тест валидации схемы
uv run pytest tests/test_pre_node.py::TestPreNode::test_pre_node_output_schema -v

# С отладочным выводом
uv run pytest tests/test_pre_node.py -v -s
```

### Синхронизация промптов

```bash
# Синхронизировать post_review (chat: system.md + post_review.md)
uv run python prompts/post_review_prompt.py

# Синхронизировать review (text: review.md)
uv run python prompts/review_prompt.py

# Синхронизировать edit_testcase (text: edit_testcase.md)
uv run python prompts/edit_testcase_prompt.py
```

### Создание датасетов

```bash
# Создать датасет для post_node
uv run python datasets/post_node_dataset.py

# Создать датасет для review_node
uv run python datasets/review_node_dataset.py

# Создать датасет для edit_testcase_node
uv run python datasets/edit_testcase_node_dataset.py

# Создать датасет для pre_node
uv run python datasets/pre_node_dataset.py
```

### Запуск эксперимента

```bash
# Запустить эксперимент с датасетом
uv run python experiments/run_pre_node_experiment.py
```

## Промпты

| Промпт | Тип | Файлы | Лейблы |
|--------|-----|-------|--------|
| post_review | Chat | system.md + post_review.md | production, user |
| review | Text | review.md | production, user |
| edit_testcase | Text | edit_testcase.md | production, user |

## Разработка

### Добавление зависимостей

```bash
# Добавить зависимость основного проекта
uv add package-name

# Добавить dev-зависимость
uv add --dev package-name

# Добавить с версией
uv add 'package-name==1.0.0'

# Добавить из requirements.txt
uv add -r requirements.txt
```

### Запуск Python скриптов в проектном окружении

```bash
# Вместо python3 script.py используйте:
uv run python script.py

# Или активируйте виртуальное окружение:
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# Затем запускайте как обычно:
python script.py
```

### Управление виртуальным окружением

```bash
# Создать виртуальное окружение (автоматически при uv sync)
uv venv

# Удалить виртуальное окружение
rm -rf .venv

# Переустановить все зависимости
uv sync --reinstall
```

## Структура проекта

```
langfuse/
├── .env                      # Credentials (не в git)
├── .env.example              # Шаблон credentials
├── .venv/                    # Виртуальное окружение (создаётся uv)
├── pyproject.toml            # Метаданные проекта и зависимости
├── uv.lock                   # Lock файл (автоматически генерируется uv)
├── utils/                    # Утилиты
│   ├── config.py             # Загрузка .env
│   ├── client.py             # Langfuse клиент
│   ├── prompts.py            # Создание/обновление промптов
│   ├── datasets.py           # Датасеты
│   └── experiments.py        # Эксперименты
├── prompts/                  # Скрипты синхронизации промптов
│   ├── post_review_prompt.py
│   ├── review_prompt.py
│   └── edit_testcase_prompt.py
├── datasets/                 # Скрипты создания датасетов
│   ├── post_node_dataset.py
│   ├── review_node_dataset.py
│   ├── edit_testcase_node_dataset.py
│   └── pre_node_dataset.py
├── schemas/                  # JSON схемы для датасетов
│   ├── post_node_input_schema.json
│   ├── post_node_expected_output_schema.json
│   ├── review_node_input_schema.json
│   └── ...
├── tests/                    # Тесты
│   ├── test_pre_node.py
│   └── README.md
└── README.md
```

## Документация

- [Datasets](https://langfuse.com/docs/evaluation/datasets)
- [Experiments via SDK](https://langfuse.com/docs/evaluation/experiments/experiments-via-sdk)
- [Prompt Management](https://langfuse.com/docs/prompts/get-started)
- [uv Documentation](https://github.com/astral-sh/uv)
