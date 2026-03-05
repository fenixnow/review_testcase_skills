#!/usr/bin/env python3
"""
Синхронизация промпта post_review.

1. Имя промпта: post_review
2. Тип: chat
3. Системный промпт: system.md
4. Пользовательский промпт: post_review.md
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.prompts import create_chat_prompt, get_prompt, update_prompt, load_prompt_file


def main():
    """Синхронизировать post_review."""

    # 1. Имя промпта
    name = "post_review"

    # 2. Тип: chat
    # 3. Загружаем системный промпт
    system_content = load_prompt_file("system.md")

    # 4. Загружаем пользовательский промпт
    user_content = load_prompt_file("post_review.md")

    # Формируем chat промпт
    chat_prompt = [
        {"role": "system", "content": system_content},
        {"role": "user", "content": user_content},
    ]

    labels = ["user"]

    # 5. Проверяю по имени, что промпт есть в Langfuse
    try:
        existing = get_prompt(name, label=labels[0])

        # 6. Если есть — обновляю
        result = update_prompt(
            name=name,
            version=existing.version,
            prompt=chat_prompt,
            labels=labels
        )

    except Exception:
        # 7. Если нет — создаю
        result = create_chat_prompt(
            name=name,
            prompt=chat_prompt,
            labels=labels
        )


if __name__ == "__main__":
    main()
