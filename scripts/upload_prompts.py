#!/usr/bin/env python3
"""
Скрипт для загрузки промптов на удалённый сервер.

Использование:
    python3 scripts/upload_prompts.py <filename>

Пример:
    python3 scripts/upload_prompts.py review.md
"""

import os
import sys
import requests
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")
SERVER = os.getenv("REVIEW_SERVER")
PROMPTS_DIR = "prompts"

# Соответствие локальных файлов ID промптов на сервере (из .env)
PROMPT_MAPPING = {
    "edit_testcase.md": os.getenv("PROMPT_EDIT_TESTCASE_ID"),
    "review.md": os.getenv("PROMPT_REVIEW_ID"),
    "post_review.md": os.getenv("PROMPT_POST_REVIEW_ID")
}
# Удаляем None значения (если переменная не задана в .env)
PROMPT_MAPPING = {k: v for k, v in PROMPT_MAPPING.items() if v is not None}

# Соответствие имён файлов видам промптов (PromptKind) для новых
PROMPT_KINDS = {
    "edit_testcase.md": "EDIT_TESTCASE",
    "review.md": "RUN_REVIEW",
    "post_review.md": "PUBLISH_REVIEW_RESULTS"
}


def parse_prompt_file(filepath):
    """Разбирает .md файл на компоненты для API."""
    filename = filepath.name

    # Читаем содержимое файла
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    # Определяем имя промпта (без расширения)
    name = filepath.stem

    # Определяем вид промпта
    kind = PROMPT_KINDS.get(filename, "RUN_REVIEW")

    return {
        "name": name,
        "content": content,
        "is_enabled": True,
        "is_global": False,
        "kind": kind
    }


def upload_prompt(prompt_id, prompt_data):
    """Обновляет промпт на сервере."""
    url = f"{SERVER}/api/prompts/{prompt_id}"

    response = requests.put(url, json=prompt_data)
    response.raise_for_status()
    return response.json()


def create_prompt(prompt_data):
    """Создаёт новый промпт на сервере."""
    url = f"{SERVER}/api/prompts"

    response = requests.post(url, json=prompt_data)
    response.raise_for_status()
    return response.json()


def upload_prompt_file(filename):
    """Загружает конкретный промпт на сервер."""
    prompts_path = Path(PROMPTS_DIR)
    prompt_file = prompts_path / filename

    if not prompt_file.exists():
        print(f"❌ Файл {filename} не найден")
        sys.exit(1)

    # Пропускаем system.md - не публикуем
    if filename == "system.md":
        print("⚠️  system.md не публикуется")
        sys.exit(1)

    # Разбираем промпт
    data = parse_prompt_file(prompt_file)

    # Проверяем маппинг
    if filename in PROMPT_MAPPING:
        # Обновляем существующий по ID
        prompt_id = PROMPT_MAPPING[filename]
        print(f"🔄 Обновляем: {filename} → ID {prompt_id}")
        result = upload_prompt(prompt_id, data)
        print(f"   ✅ {result['name']} (ID: {result['id']})")
    else:
        # Создаём новый
        print(f"➕ Создаём: {filename}")
        result = create_prompt(data)
        print(f"   ✅ {result['name']} (ID: {result['id']})")


def main():
    parser = argparse.ArgumentParser(description="Загрузить промпт на сервер")
    parser.add_argument("filename", help="Имя файла промпта (например: review.md)")
    args = parser.parse_args()

    upload_prompt_file(args.filename)


if __name__ == "__main__":
    main()