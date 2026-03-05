# Тесты для Langfuse интеграции

## Установка зависимостей

```bash
# Используя uv (рекомендуется)
uv sync

# Или используя pip
pip install -r requirements.txt
```

## Настройка переменных окружения

Скопируйте `.env.example` в `.env` и заполните свои credentials:

```bash
cp .env.example .env
```

```bash
LANGFUSE_PUBLIC_KEY=pk-ваш-ключ
LANGFUSE_SECRET_KEY=sk-ваш-ключ
LANGFUSE_HOST=https://cloud.langfuse.com
```

## Запуск тестов

### Все тесты

```bash
# С использованием uv (рекомендуется)
uv run pytest tests/ -v

# Или напрямую через pytest
pytest tests/ -v
```

### Только локальные тесты (без Langfuse)

```bash
uv run pytest tests/test_pre_node.py::TestPreNode::test_pre_node_with_local_dataset -v
uv run pytest tests/test_pre_node.py::TestPreNode::test_pre_node_output_schema -v
```

### Тесты с удалённым датасетом (требуются credentials)

```bash
uv run pytest tests/test_pre_node.py::TestPreNode::test_pre_node_with_remote_dataset -v
```

## Структура тестов

- `test_pre_node.py` — тесты для pre_node
  - `test_pre_node_with_local_dataset` — локальный тест с mock данными
  - `test_pre_node_with_remote_dataset` — тест с датасетом из Langfuse
  - `test_pre_node_output_schema` — валидация схемы выходных данных

- `test_post_review.py` — тесты для post_review (по методологии Langfuse)
  - `test_post_review_with_local_dataset` — локальный тест с 4 тестовыми случаями
  - `test_post_review_llm_as_judge` — тест с LLM-as-a-Judge evaluator
  - `test_post_review_output_schema` — валидация схемы выходных данных
  - `test_post_review_create_dataset_if_not_exists` — создание датасета в Langfuse

### Тестовые случаи для post_review

| # | Описание | Ожидаемый результат |
|---|----------|---------------------|
| 1 | Ревью с замечаниями | `status_changed: True`, `status_id: 15` |
| 2 | Пустое ревью | `status_changed: False` |
| 3 | Всё исправлено автоматически | `status_changed: False` |
| 4 | Нет замечаний | `status_changed: False` |

## Создание новых тестов

Для создания тестов для других узлов:

1. Скопируйте `test_pre_node.py` или `test_post_review.py` как шаблон
2. Замените функцию задачи на соответствующую
3. Обновите тестовые данные и ожидаемые результаты
4. Обновите схемы в `schemas/`

## Evaluators

Файл: `../utils/evaluators.py`

### post_review_evaluator

Специфический evaluator для post_review с проверкой:

- `comment_published` — комментарий должен быть опубликован
- `testcase_status_changed` — корректность определения смены статуса
- `testcase_status_id` — корректный ID статуса (3 = «Требует актуализации»)

### llm_as_judge_evaluator

Универсальный evaluator с использованием LLM (модель: glm-4.7).

## Ссылки

- [Статья Langfuse о тестировании LLM](https://langfuse.com/guides/llm-app-testing)
- [Документация Langfuse](https://langfuse.com/docs)
