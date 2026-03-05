"""Конфигурация и загрузка переменных окружения."""

import os
from pathlib import Path


def load_env_file(env_path: Path = None):
    """
    Загрузить переменные из .env файла в environment.

    Args:
        env_path: Путь к .env файлу. Если None, ищет в langfuse/.env
    """
    if env_path is None:
        env_path = Path(__file__).parent.parent / ".env"

    if not env_path.exists():
        return

    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Пропускаем пустые строки и комментарии
            if not line or line.startswith('#'):
                continue
            # Разбираем KEY=VALUE
            if '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()


def get_langfuse_config():
    """
    Получить конфигурацию Langfuse.

    Сначала загружает из .env, затем берёт из environment.

    Returns:
        Словарь с public_key, secret_key, host
    """
    load_env_file()

    return {
        "public_key": os.getenv("LANGFUSE_PUBLIC_KEY"),
        "secret_key": os.getenv("LANGFUSE_SECRET_KEY"),
        "host": os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com"),
    }

