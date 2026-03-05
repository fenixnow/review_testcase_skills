"""Работа с промптами в Langfuse Prompt Management."""

from pathlib import Path
from typing import Optional, Dict, Any, List
from .client import get_langfuse_client


PROMPTS_DIR = Path(__file__).parent.parent.parent / "prompts"


def load_prompt_file(filename: str) -> str:
    """Загрузить файл промпта из папки prompts/."""
    return (PROMPTS_DIR / filename).read_text(encoding='utf-8')


def load_prompt_from_file(prompt_path: Path) -> str:
    """
    Загрузить промпт из файла.

    Args:
        prompt_path: Путь к файлу промпта

    Returns:
        str: Содержимое промпта

    Raises:
        FileNotFoundError: Если файл не найден
    """
    if not prompt_path.exists():
        raise FileNotFoundError(f"Файл промпта не найден: {prompt_path}")

    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read()


def create_prompt(
    name: str,
    prompt: str,
    labels: Optional[List[str]] = None,
    config: Optional[Dict[str, Any]] = None,
) -> object:
    """
    Создать текстовый промпт в Langfuse Prompt Management.

    Args:
        name: Имя промпта
        prompt: Текст промпта (может содержать {{variable}})
        labels: Список лейблов (например, ['production', 'user'])
        config: Конфигурация (model, temperature, etc.)

    Returns:
        Созданный объект промпта
    """
    langfuse = get_langfuse_client()

    return langfuse.create_prompt(
        name=name,
        type="text",
        prompt=prompt,
        labels=labels or [],
        config=config or {}
    )


def create_chat_prompt(
    name: str,
    prompt: List[Dict[str, str]],
    labels: Optional[List[str]] = None,
    config: Optional[Dict[str, Any]] = None,
) -> object:
    """
    Создать chat промпт в Langfuse Prompt Management.

    Args:
        name: Имя промпта
        prompt: Список сообщений [{"role": "system", "content": "..."}, ...]
        labels: Список лейблов
        config: Конфигурация

    Returns:
        Созданный объект промпта
    """
    langfuse = get_langfuse_client()

    return langfuse.create_prompt(
        name=name,
        type="chat",
        prompt=prompt,
        labels=labels or [],
        config=config or {}
    )


def update_prompt(
    name: str,
    version: int,
    prompt: Optional[str] = None,
    labels: Optional[List[str]] = None,
    config: Optional[Dict[str, Any]] = None,
) -> object:
    """
    Обновить промпт (создать новую версию).

    Args:
        name: Имя промпта
        version: Номер версии для обновления
        prompt: Новый текст промпта (опционально)
        labels: Новые лейблы (опционально)
        config: Новая конфигурация (опционально)

    Returns:
        Обновлённый объект промпта

    Пример:
        prompt = update_prompt(
            name="translator",
            version=1,
            labels=["production", "v2"]
        )
    """
    langfuse = get_langfuse_client()

    return langfuse.update_prompt(
        name=name,
        version=version,
        prompt=prompt,
        labels=labels,
        config=config
    )


def update_prompt_labels(
    name: str,
    version: int,
    new_labels: List[str],
) -> object:
    """
    Обновить лейблы промпта.

    Args:
        name: Имя промпта
        version: Номер версии
        new_labels: Новые лейблы

    Returns:
        Обновлённый объект промпта

    Пример:
        # Продвинуть версию в production
        update_prompt_labels("my-prompt", version=2, new_labels=["production"])
    """
    langfuse = get_langfuse_client()

    return langfuse.update_prompt(
        name=name,
        version=version,
        new_labels=new_labels
    )


def get_prompt(name: str, label: Optional[str] = None, version: Optional[int] = None) -> object:
    """
    Получить промпт из Langfuse.

    Args:
        name: Имя промпта
        label: Лейбл версии (например, 'production')
        version: Номер версии (если не указан label)

    Returns:
        Объект промпта с методом compile()

    Пример:
        # Получить по label
        prompt = get_prompt("my-prompt", label="production")
        compiled = prompt.compile(variable="value")

        # Получить по версии
        prompt = get_prompt("my-prompt", version=1)
    """
    langfuse = get_langfuse_client()

    if label:
        return langfuse.get_prompt(name, label=label)
    if version:
        return langfuse.get_prompt(name, version=version)
    return langfuse.get_prompt(name)


def create_prompt_from_file(
    name: str,
    prompt_path: Path,
    labels: Optional[List[str]] = None,
    config: Optional[Dict[str, Any]] = None,
) -> object:
    """
    Создать промпт из файла.

    Args:
        name: Имя промпта
        prompt_path: Путь к файлу промпта
        labels: Список лейблов
        config: Конфигурация

    Returns:
        Созданный объект промпта
    """
    prompt_content = load_prompt_from_file(prompt_path)

    return create_prompt(
        name=name,
        prompt=prompt_content,
        labels=labels,
        config=config
    )
