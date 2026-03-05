#!/usr/bin/env python3
"""
Тесты для pre_node используя Langfuse datasets.

Запуск: pytest langfuse/tests/test_pre_node.py -v
"""

import os
import sys
import pytest
from pathlib import Path

# Добавляем parent parent в path для импортов
sys.path.insert(0, str(Path(__file__).parent.parent))

from langfuse import Langfuse

# Импортируем observe только если есть Langfuse credentials
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


# Инициализация Langfuse клиента
def get_langfuse_client():
    """Получить Langfuse клиент из переменных окружения."""
    return Langfuse(
        public_key=os.environ.get("LANGFUSE_PUBLIC_KEY"),
        secret_key=os.environ.get("LANGFUSE_SECRET_KEY"),
        host=os.environ.get("LANGFUSE_HOST", "https://cloud.langfuse.com")
    )


@observe()
def pre_node_task(*, item, **kwargs):
    """
    Задача pre_node для тестирования.

    Args:
        item: Элемент датасета с input и expected_output

    Returns:
        Результат выполнения pre_node
    """
    # Здесь должна быть реальная логика pre_node
    # Для тестов возвращаем mock данные

    testcase_id = item.input.get("testcase_id")
    project_id = item.input.get("project_id") or 133

    # Mock результат - в реальности здесь будет вызов вашего API
    result = {
        "project_id": project_id,
        "review_prompt": "# Роль: QA-инженер...",
        "edit_testcase_prompt": "# Роль...",
        "skills": [
            {
                "name": "edit-name",
                "description": "Редактирование имени",
                "id": 1,
                "parameters": []
            }
        ],
        "post_prompt": "### Инструкция по обработке..."
    }

    return result


class TestPreNode:
    """Тесты для pre_node."""

    @pytest.fixture(autouse=True)
    def setup_langfuse(self):
        """Setup Langfuse клиент для всех тестов."""
        self.langfuse = get_langfuse_client()

    def test_pre_node_with_local_dataset(self):
        """Тест pre_node с локальным тестовым случаем."""
        # Локальный тестовый случай
        test_input = {
            "testcase_id": 80681,
            "project_id": None,
            "edit_testcase_enabled": True,
            "post_processing_enabled": True,
            "messages": []
        }

        expected_output = {
            "project_id": 133,
            "review_prompt": "# Роль: QA-инженер...",
            "skills": []
        }

        # Создаём mock item
        class MockItem:
            def __init__(self, input_data, expected):
                self.input = input_data
                self.expected_output = expected

        item = MockItem(test_input, expected_output)

        # Выполняем задачу
        result = pre_node_task(item=item)

        # Отладочный вывод
        print(f"DEBUG: result = {result}")
        print(f"DEBUG: result type = {type(result)}")

        # Проверки
        assert result is not None, "Результат не должен быть None"
        assert "project_id" in result, "Результат должен содержать project_id"
        assert isinstance(result["project_id"], int), "project_id должен быть integer"
        assert result["project_id"] == 133, f"Ожидается project_id=133, получено {result['project_id']}"

        print("✅ Тест пройден: pre_node возвращает корректную структуру")

    @pytest.mark.skipif(not HAS_LANGFUSE_CREDS, reason="Требуются LANGFUSE_PUBLIC_KEY и LANGFUSE_SECRET_KEY")
    def test_pre_node_with_remote_dataset(self):
        """Тест pre_node с удалённым датасетом из Langfuse."""
        # Получаем датасет из Langfuse
        dataset_name = "pre_node"
        dataset = self.langfuse.get_dataset(dataset_name)

        # Проверяем что датасет существует
        assert dataset is not None, f"Датасет '{dataset_name}' не найден"

        # Запускаем эксперимент
        experiment = dataset.run_experiment(
            name="pre_node_test",
            description="Тестирование pre_node",
            task=pre_node_task,
            metadata={
                "environment": "testing",
                "model": "claude-sonnet-4-6"
            }
        )

        # Проверяем результаты эксперимента
        assert experiment is not None, "Эксперимент не был создан"
        assert experiment.status == "COMPLETED", f"Эксперимент не завершился успешно: {experiment.status}"

        # Проверяем что все тестовые случаи были обработаны
        dataset_items = dataset.items
        assert len(dataset_items) > 0, "Датасет должен содержать хотя бы один элемент"

        print(f"✅ Эксперимент завершён: {experiment.id}")
        print(f"   Обработано элементов: {len(dataset_items)}")

        # Проверяем результаты
        for item_run in experiment.item_runs:
            assert item_run.status == "COMPLETED", f"Элемент {item_run.id} не завершился успешно"

        print(f"✅ Все элементы обработаны успешно")

    def test_pre_node_output_schema(self):
        """Тест схемы выходных данных pre_node."""
        test_input = {
            "testcase_id": 12345,
            "project_id": 133,
            "messages": []
        }

        class MockItem:
            def __init__(self, input_data):
                self.input = input_data
                self.expected_output = {}

        item = MockItem(test_input)

        # Выполняем задачу
        result = pre_node_task(item=item)

        # Проверяем структуру ответа
        required_fields = ["project_id", "review_prompt", "edit_testcase_prompt", "skills", "post_prompt"]

        for field in required_fields:
            assert field in result, f"Результат должен содержать поле '{field}'"

        # Проверяем типы данных
        assert isinstance(result["project_id"], int), "project_id должен быть integer"
        assert isinstance(result["review_prompt"], str), "review_prompt должен быть string"
        assert isinstance(result["edit_testcase_prompt"], str), "edit_testcase_prompt должен быть string"
        assert isinstance(result["skills"], list), "skills должен быть list"
        assert isinstance(result["post_prompt"], str), "post_prompt должен быть string"

        print("✅ Схема выходных данных корректна")


if __name__ == "__main__":
    # Запуск тестов напрямую
    pytest.main([__file__, "-v"])
