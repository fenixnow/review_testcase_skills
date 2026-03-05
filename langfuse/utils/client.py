"""Инициализация клиента Langfuse."""

from langfuse import Langfuse
from .config import get_langfuse_config


_client = None


def get_langfuse_client():
    """
    Получить инициализированный клиент Langfuse (синглтон).

    Returns:
        Langfuse: Клиент Langfuse
    """
    global _client

    if _client is None:
        config = get_langfuse_config()
        _client = Langfuse(
            public_key=config["public_key"],
            secret_key=config["secret_key"],
            host=config["host"],
        )

    return _client

