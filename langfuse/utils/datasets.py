"""Работа с датасетами в Langfuse."""

from typing import Dict, Any, Optional
from .client import get_langfuse_client


def create_dataset(
    name: str,
    description: Optional[str] = None,
    input_schema: Optional[Dict[str, Any]] = None,
    expected_output_schema: Optional[Dict[str, Any]] = None,
) -> object:
    """
    Создать датасет в Langfuse.

    Args:
        name: Имя датасета
        description: Описание датасета
        input_schema: JSON Schema для валидации входных данных
        expected_output_schema: JSON Schema для валидации ожидаемых результатов

    Returns:
        Созданный объект датасета
    """
    langfuse = get_langfuse_client()

    return langfuse.create_dataset(
        name=name,
        description=description or f"Датасет {name}",
        input_schema=input_schema,
        expected_output_schema=expected_output_schema
    )


def create_dataset_item(
    dataset_name: str,
    input: Dict[str, Any],
    expected_output: Optional[Dict[str, Any]] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> object:
    """
    Создать элемент датасета.

    Args:
        dataset_name: Имя датасета
        input: Входные данные
        expected_output: Ожидаемый результат
        metadata: Метаданные

    Returns:
        Созданный объект элемента датасета
    """
    langfuse = get_langfuse_client()

    return langfuse.create_dataset_item(
        dataset_name=dataset_name,
        input=input,
        expected_output=expected_output or {},
        metadata=metadata or {}
    )


def get_dataset(name: str) -> object:
    """
    Получить датасет из Langfuse.

    Args:
        name: Имя датасета

    Returns:
        Объект датасета
    """
    langfuse = get_langfuse_client()

    return langfuse.get_dataset(name)
