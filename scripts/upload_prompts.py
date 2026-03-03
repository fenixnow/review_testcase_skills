#!/usr/bin/env python3
"""
Скрипт для загрузки промптов на удалённый сервер.

Считывает .md файлы из директории prompts/ и отправляет в API.
"""

import os
import requests
from pathlib import Path

SERVER = "https://review-test.qa.svc.vkusvill.ru"
PROMPTS_DIR = "prompts"

# Соответствие локальных файлов ID промптов на сервере
PROMPT_MAPPING = {
    "edit_testcase.md": 45,      # Полетаев - Редактирование
    "review.md": 46,              # Полетаев - Ревью 2
    "post_review.md": 51,              # Публикация комментария и изменения статуса
}

# Соответствие имён файлов видам промптов (PromptKind) для новых
PROMPT_KINDS = {
    "edit_testcase.md": "EDIT_TESTCASE",
    "review_simple_1.md": "RUN_REVIEW",
    "review_t.md": "RUN_REVIEW",
    "review_full.md": "RUN_REVIEW",
    "publish_results.md": "PUBLISH_REVIEW_RESULTS",
    "comment_t.md": "PUBLISH_REVIEW_RESULTS",
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


def upload_all_prompts():
    """Загружает все промпты на сервер."""
    prompts_path = Path(PROMPTS_DIR)

    if not prompts_path.exists():
        print(f"❌ Директория {PROMPTS_DIR} не найдена")
        return

    # Получаем список существующих промптов (для информации)
    try:
        existing = requests.get(f"{SERVER}/api/prompts").json()
        print(f"📋 На сервере {len(existing)} промптов")
    except requests.RequestException as e:
        print(f"⚠️  Не удалось получить список промптов: {e}")

    for prompt_file in sorted(prompts_path.glob("*.md")):
        filename = prompt_file.name

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
            # Создаём новый (или пробуем найти по имени)
            print(f"➕ Создаём: {filename}")
            result = create_prompt(data)
            print(f"   ✅ {result['name']} (ID: {result['id']})")


if __name__ == "__main__":
    upload_all_prompts()