"""Специфическая логика для тестирования промпта post_review."""

import os
import json
from typing import Dict, Any
from .prompts import get_prompt

# Проверяем наличие Langfuse credentials
HAS_LANGFUSE_CREDS = bool(os.environ.get("LANGFUSE_PUBLIC_KEY"))

if HAS_LANGFUSE_CREDS:
    from langfuse import observe
else:
    # Создаём no-op decorator для локальных тестов
    def observe(*decorator_args, **decorator_kwargs):
        def decorator(func):
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator


@observe()
def post_review_task(*, item, **kwargs) -> str:
    """
    Задача для эксперимента post_review.

    Анализирует ревью и определяет, нужно ли менять статус тест-кейса.

    Args:
        item: Элемент датасета с полями input и expected_output
        **kwargs: Дополнительные параметры

    Returns:
        str: Результат в виде JSON строки
    """
    testcase_id = item.input.get("testcase_id")
    review_result = item.input.get("review_result", "")

    # Логика анализа ревью
    review_text = review_result.strip()

    # Признаки того, что статус НЕ нужно менять:
    is_empty = not bool(review_text)
    has_auto_fixed = "Исправлено автоматически" in review_text
    has_no_issues = any(
        phrase in review_text
        for phrase in ["замечаний нет", "нет замечаний", "без замечаний"]
    )

    # Признаки наличия замечаний:
    # Ищем нумерованные секции (1., 2., и т.д.)
    numbered_prefixes = tuple(f"{i}." for i in range(1, 10))
    has_numbered_sections = any(
        line.strip().startswith(numbered_prefixes)
        for line in review_text.split('\n')
    )

    # Проверяем наличие секции "Предлагаемые правки"
    has_proposed_edits = "Предлагаемые правки" in review_text

    # Определяем нужно ли менять статус
    # Статус меняется если:
    # 1. Ревью не пустое
    # 2. Не всё исправлено автоматически
    # 3. Есть нумерованные секции с замечаниями или предложенные правки
    should_change_status = (
        not (is_empty or has_auto_fixed or has_no_issues)
        and (has_numbered_sections or has_proposed_edits)
    )

    # Формируем результат
    result = {
        "testcase_id": int(testcase_id) if testcase_id else 0,
        "comment_published": True,
        "status_changed": should_change_status,
        "testcase_status_changed": should_change_status,  # Для совместимости
        "new_status": "Требует актуализации" if should_change_status else None,
        "testcase_status_id": 3 if should_change_status else None,
        "analysis": {
            "is_empty": is_empty,
            "has_auto_fixed": has_auto_fixed,
            "has_no_issues": has_no_issues,
            "has_numbered_sections": has_numbered_sections,
            "has_proposed_edits": has_proposed_edits
        }
    }

    return json.dumps(result, ensure_ascii=False)


def get_post_review_test_cases() -> list[Dict[str, Any]]:
    """
    Получить тестовые кейсы для post_review.

    Returns:
        Список тестовых кейсов
    """
    return [
        {
            "input": {
                "testcase_id": "80719",
                "review_result": """1. Имя тест-кейса
   - Название слишком длинное и содержит технические детали

Предлагаемые правки:
1. Имя тест-кейса
   - Изменить имя на: «Создание достижения»"""
            },
            "expected_output": {
                "status_changed": True,
                "new_status": "Требует актуализации",
                "comment_published": True,
                "testcase_status_id": 3
            },
            "metadata": {
                "category": "with_issues",
                "expected_status_change": True,
                "description": "Ревью с замечаниями - статус должен измениться"
            }
        },
        {
            "input": {
                "testcase_id": "80720",
                "review_result": "Тест-кейс проверен, замечаний нет."
            },
            "expected_output": {
                "status_changed": False,
                "comment_published": True
            },
            "metadata": {
                "category": "without_issues",
                "expected_status_change": False,
                "description": "Нет замечаний - статус не меняется"
            }
        },
        {
            "input": {
                "testcase_id": "80721",
                "review_result": ""
            },
            "expected_output": {
                "status_changed": False,
                "comment_published": True
            },
            "metadata": {
                "category": "empty_review",
                "expected_status_change": False,
                "description": "Пустое ревью - статус не меняется"
            }
        },
        {
            "input": {
                "testcase_id": "80722",
                "review_result": """## Исправлено автоматически
- 1. Имя тест-кейса → изменено на «Создание достижения»"""
            },
            "expected_output": {
                "status_changed": False,
                "comment_published": True,
                "all_fixed": True
            },
            "metadata": {
                "category": "auto_fixed",
                "expected_status_change": False,
                "description": "Всё исправлено автоматически - статус не меняется"
            }
        },
    ]


def analyze_review_content(review_result: str) -> Dict[str, Any]:
    """
    Анализирует содержимое ревью для определения необходимости смены статуса.

    Args:
        review_result: Текст ревью

    Returns:
        dict: Результат анализа с полями:
            - should_change_status: bool
            - reasons: list[str]
            - analysis: dict с деталями
    """
    review_text = review_result.strip()

    # Признаки
    is_empty = not bool(review_text)
    has_auto_fixed = "Исправлено автоматически" in review_text
    has_no_issues = any(
        phrase in review_text
        for phrase in ["замечаний нет", "нет замечаний", "без замечаний"]
    )
    has_numbered_sections = any(
        line.strip().startswith((f"{i}." for i in range(1, 10)))
        for line in review_text.split('\n')
    )
    has_proposed_edits = "Предлагаемые правки" in review_text

    # Определяем необходимость смены статуса
    should_change = (
        not (is_empty or has_auto_fixed or has_no_issues)
        and (has_numbered_sections or has_proposed_edits)
    )

    # Формируем причины
    reasons = []
    if is_empty:
        reasons.append("Пустое ревью")
    if has_auto_fixed:
        reasons.append("Всё исправлено автоматически")
    if has_no_issues:
        reasons.append("Нет замечаний")
    if has_numbered_sections:
        reasons.append("Есть нумерованные секции с замечаниями")
    if has_proposed_edits:
        reasons.append("Есть предложенные правки")

    return {
        "should_change_status": should_change,
        "reasons": reasons,
        "analysis": {
            "is_empty": is_empty,
            "has_auto_fixed": has_auto_fixed,
            "has_no_issues": has_no_issues,
            "has_numbered_sections": has_numbered_sections,
            "has_proposed_edits": has_proposed_edits
        }
    }
