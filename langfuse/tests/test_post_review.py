import sys
import pytest
import json
from pathlib import Path
from typing import Dict, Any

from langfuse.utils.post_review import post_review_task

# Добавляем parent в path для импортов
sys.path.insert(0, str(Path(__file__).parent.parent))

from langfuse import Langfuse, get_client

POST_REVIEW_TEST_DATA = [
    # Case 1: Ревью с замечаниями → статус должен измениться
    {
        "input": {
            "testcase_id": 80719,
            "project_id": 133,
            "review_result": """1. Имя тест-кейса
   - Название слишком длинное

Предлагаемые правки:
1. Имя тест-кейса
   - Изменить имя на: «Создание достижения»""",
            "post_processing_enabled": True,
        },
        "expected_output": {
            "testcase_status_changed": True,
            "testcase_status_id": 3,  # ID статуса «Требует актуализации»
            "comment_published": True
        },
        "metadata": {
            "category": "with_issues",
            "description": "Ревью с замечаниями - статус должен измениться"
        }
    },

    # Case 2: Пустое ревью → статус НЕ меняется
    {
        "input": {
            "testcase_id": 80720,
            "project_id": 133,
            "review_result": "",
            "post_processing_enabled": True,
        },
        "expected_output": {
            "testcase_status_changed": False,
            "comment_published": True
        },
        "metadata": {
            "category": "empty_review",
            "description": "Пустое ревью - статус не меняется"
        }
    },

    # Case 3: Всё исправлено автоматически → статус НЕ меняется
    {
        "input": {
            "testcase_id": 80721,
            "project_id": 133,
            "review_result": """## Исправлено автоматически
- 1. Имя тест-кейса → изменено""",
            "post_processing_enabled": True,
        },
        "expected_output": {
            "testcase_status_changed": False,
            "comment_published": True
        },
        "metadata": {
            "category": "auto_fixed",
            "description": "Всё исправлено автоматически - статус не меняется"
        }
    },

    # Case 4: Нет замечаний → статус НЕ меняется
    {
        "input": {
            "testcase_id": 80722,
            "project_id": 133,
            "review_result": "Тест-кейс проверен, замечаний нет.",
            "post_processing_enabled": True,
        },
        "expected_output": {
            "testcase_status_changed": False,
            "comment_published": True
        },
        "metadata": {
            "category": "without_issues",
            "description": "Нет замечаний - статус не меняется"
        }
    },
]

def post_review_task():
    la

@pytest.fixture
def langfuse_client() -> Langfuse:
    return get_client()

def test_post_review_with_local_dataset(langfuse_client: Langfuse):


    passed = 0
    failed = 0

    for i, test_case in enumerate(POST_REVIEW_TEST_DATA, 1):
        print(f"\nТест-кейс #{i}: {test_case['metadata']['description']}")

        # Создаём mock item
        item = MockDatasetItem(
            input_data=test_case["input"],
            expected_output=test_case["expected_output"],
            metadata=test_case["metadata"]
        )

        # Выполняем задачу
        try:
            result_str = post_review_task(item=item)

            # Парсим результат (если вернулся JSON string)
            if isinstance(result_str, str):
                try:
                    result = json.loads(result_str)
                except json.JSONDecodeError:
                    # Если не JSON, создаём dict из строки
                    result = {"raw_output": result_str}
            else:
                result = result_str

            # Проверяем ожидаемые значения
            expected = test_case["expected_output"]
            test_passed = True
            errors = []

            # Проверка comment_published
            if "comment_published" in expected:
                if not result.get("comment_published", True):
                    test_passed = False
                    errors.append(f"comment_published должно быть {expected['comment_published']}")

            # Проверка testcase_status_changed
            if "testcase_status_changed" in expected:
                actual_status_changed = result.get("status_changed", result.get("testcase_status_changed"))
                if actual_status_changed != expected["testcase_status_changed"]:
                    test_passed = False
                    errors.append(
                        f"testcase_status_changed: ожидалось {expected['testcase_status_changed']}, "
                        f"получено {actual_status_changed}"
                    )

            # Проверка testcase_status_id
            if "testcase_status_id" in expected and expected["testcase_status_changed"]:
                actual_status_id = result.get("testcase_status_id")
                if actual_status_id != expected["testcase_status_id"]:
                    test_passed = False
                    errors.append(
                        f"testcase_status_id: ожидалось {expected['testcase_status_id']}, "
                        f"получено {actual_status_id}"
                    )

            if test_passed:
                print(f"  ✅ PASSED")
                passed += 1
            else:
                print(f"  ❌ FAILED:")
                for error in errors:
                    print(f"     - {error}")
                print(f"     Результат: {result}")
                failed += 1

        except Exception as e:
            print(f"  ❌ ERROR: {e}")
            failed += 1

    print(f"\n=== Итого: {passed} passed, {failed} failed ===")

    # Провальный тест если есть ошибки
    assert failed == 0, f"{failed} тест(ов) не прошли"

def test_post_review_llm_as_judge(langfuse_client: Langfuse):

    # Создаём датасет в Langfuse (если его ещё нет)
    dataset_name = "post_review_test_dataset"

    try:
        # Пытаемся получить существующий датасет
        dataset = langfuse_client.get_dataset(dataset_name)
        print(f"📊 Используем существующий датасет: {dataset_name}")
    except Exception:
        # Создаём новый датасет
        dataset = langfuse_client.create_dataset(
            name=dataset_name,
            description="Тестовый датасет для post_review",
        )
        print(f"📊 Создан новый датасет: {dataset_name}")

        # Загружаем тестовые данные в датасет
        for test_case in POST_REVIEW_TEST_DATA:
            langfuse_client.create_dataset_item(
                dataset_name=dataset_name,
                input=test_case["input"],
                expected_output=test_case["expected_output"],
                metadata=test_case["metadata"]
            )

        print(f"  ✅ Загружено {len(POST_REVIEW_TEST_DATA)} тестовых случаев")


    langfuse_client.run_experiment(
        name="post_review_test",
        description="Тестирование post_review с LLM-as-a-Judge evaluator",
        task=post_review_task,
        evaluators=[post_review_evaluator],  # Отключено для отладки
        metadata={
            "evaluator": "llm_as_judge",
            "model": "glm-4.7",
            "test_type": "automated"
        }
    )

def test_post_review_output_schema(self):
    """Тест схемы выходных данных post_review."""
    print("\n=== Тест схемы выходных данных ===")

    test_input = {
        "testcase_id": 12345,
        "project_id": 133,
        "review_result": """1. Имя тест-кейса
- Замечание о названии""",
        "post_processing_enabled": True
    }

    expected_output = {
        "comment_published": True
    }

    item = MockDatasetItem(
        input_data=test_input,
        expected_output=expected_output
    )

    # Выполняем задачу
    result_str = post_review_task(item=item)

    # Парсим результат
    if isinstance(result_str, str):
        try:
            result = json.loads(result_str)
        except json.JSONDecodeError:
            result = {"raw_output": result_str}
    else:
        result = result_str

    # Проверяем обязательные поля
    required_fields = ["testcase_id", "comment_published", "status_changed"]

    for field in required_fields:
        assert field in result, f"Результат должен содержать поле '{field}'"

    # Проверяем типы данных
    assert isinstance(result["testcase_id"], int), "testcase_id должен быть integer"
    assert isinstance(result["comment_published"], bool), "comment_published должен быть boolean"
    assert isinstance(result["status_changed"], bool), "status_changed должен быть boolean"

    print("✅ Схема выходных данных корректна")
    print(f"   Поля: {list(result.keys())}")

def test_post_review_create_dataset_if_not_exists(self):
    """Тест создания датасета в Langfuse если он не существует."""

    dataset_name = "post_review_test_dataset"

    # Проверяем что датасет можно получить
    try:
        dataset = self.langfuse.get_dataset(dataset_name)
        print(f"✅ Датасет существует: {dataset_name}")
        print(f"   Элементов: {len(dataset.items) if dataset.items else 0}")
    except Exception:
        # Создаём датасет
        dataset = self.langfuse.create_dataset(
            name=dataset_name,
            description="Тестовый датасет для post_review",
        )
        print(f"✅ Датасет создан: {dataset_name}")

        # Загружаем данные
        for test_case in POST_REVIEW_TEST_DATA:
            self.langfuse.create_dataset_item(
                dataset_name=dataset_name,
                input=test_case["input"],
                expected_output=test_case["expected_output"],
                metadata=test_case["metadata"]
            )

        print(f"   Загружено {len(POST_REVIEW_TEST_DATA)} элементов")

    assert dataset is not None, "Датасет должен быть создан или получен"

