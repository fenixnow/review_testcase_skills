"""Запуск экспериментов в Langfuse."""

from typing import Callable, Dict, Any, Optional, List
from langfuse import get_client


def run_experiment(
    dataset_name: str,
    task: Callable,
    name: str,
    description: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> object:
    """
    Запустить эксперимент на датасете.

    Args:
        dataset_name: Имя датасета
        task: Функция задачи для выполнения
        name: Имя эксперимента
        description: Описание эксперимента
        metadata: Метаданные эксперимента

    Returns:
        Результат эксперимента
    """
    langfuse = get_client()

    dataset = langfuse.get_dataset(dataset_name)

    return dataset.run_experiment(
        name=name,
        description=description,
        task=task,
        metadata=metadata or {}
    )


def run_experiment_on_local_data(
    data: List[Dict[str, Any]],
    task: Callable,
    name: str,
    description: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> object:
    """
    Запустить эксперимент на локальных данных.

    Args:
        data: Список элементов с input и expected_output
        task: Функция задачи для выполнения
        name: Имя эксперимента
        description: Описание эксперимента
        metadata: Метаданные эксперимента

    Returns:
        Результат эксперимента
    """
    langfuse = get_client()

    return langfuse.run_experiment(
        name=name,
        description=description,
        data=data,
        task=task,
        metadata=metadata or {}
    )
