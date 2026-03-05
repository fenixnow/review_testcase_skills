#!/usr/bin/env python3
"""
Скрипт для скачивания промптов с удалённого сервера.

Получает список промптов из API и сохраняет в директорию prompts/.
"""

import os
import requests
from pathlib import Path
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")
SERVER = os.getenv("REVIEW_SERVER")
PROMPTS_DIR = "prompts"


def download_all_prompts():
    """Скачивает все промпты с сервера."""
    prompts_path = Path(PROMPTS_DIR)

    # Создаём директорию если нет
    prompts_path.mkdir(exist_ok=True)

    # Получаем список промптов
    response = requests.get(f"{SERVER}/api/prompts")
    response.raise_for_status()
    prompts = response.json()

    print(f"📥 Найдено {len(prompts)} промптов на сервере")

    for prompt in prompts:
        name = prompt["name"]
        content = prompt.get("content", "")

        filename = prompts_path / f"{name}.md"

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"   ✅ {name}.md (kind: {prompt.get('kind')}, enabled: {prompt.get('is_enabled')})")


if __name__ == "__main__":
    download_all_prompts()