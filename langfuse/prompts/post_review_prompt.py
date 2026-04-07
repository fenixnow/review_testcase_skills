#!/usr/bin/env python3
"""
Синхронизация промпта post_review.

1. Имя промпта: post_review
2. Тип: text
3. Содержимое: post_review.md
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.prompts import create_prompt, get_prompt, update_prompt, load_prompt_file


def main():
    """Синхронизировать post_review."""

    # 1. Имя промпта
    name = "post_review"

    # 2. Тип: text
    # 3. Загружаем промпт
    prompt_content = load_prompt_file("post_review.md")

    labels = ["user"]

    # 4. Проверяю по имени, что промпт есть в Langfuse
    try:
        existing = get_prompt(name, label=labels[0])

        # 5. Если есть — обновляю
        result = update_prompt(
            name=name,
            version=existing.version,
            prompt=prompt_content,
            labels=labels
        )

    except Exception:
        # 6. Если нет — создаю
        result = create_prompt(
            name=name,
            prompt=prompt_content,
            labels=labels
        )


if __name__ == "__main__":
    main()
