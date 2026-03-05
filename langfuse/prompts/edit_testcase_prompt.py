#!/usr/bin/env python3
"""
Синхронизация промпта edit_testcase.

Тип: text
Файл: edit_testcase.md
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.prompts import create_prompt, get_prompt, update_prompt, load_prompt_file


def main():
    """Синхронизировать edit_testcase."""

    name = "edit_testcase"
    prompt_content = load_prompt_file("edit_testcase.md")
    labels = ["user"]

    try:
        existing = get_prompt(name, label=labels[0])
        result = update_prompt(
            name=name,
            version=existing.version,
            prompt=prompt_content,
            labels=labels
        )
    except Exception:
        result = create_prompt(
            name=name,
            prompt=prompt_content,
            labels=labels
        )


if __name__ == "__main__":
    main()
