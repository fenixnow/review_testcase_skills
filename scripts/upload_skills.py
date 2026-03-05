#!/usr/bin/env python3
"""
Скрипт для загрузки скиллов на удалённый сервер.

Разбирает YAML frontmatter из SKILL.md и отправляет данные в API.
"""

import os
import re
import yaml
import requests
from pathlib import Path
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")
SERVER = os.getenv("REVIEW_SERVER")
SKILLS_DIR = "skills"


def parse_skill_file(filepath):
    """Разбирает SKILL.md на компоненты для API."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Находим границы YAML frontmatter
    frontmatter_start = -1
    frontmatter_end = -1

    for i, line in enumerate(lines):
        if line.strip() == '---':
            if frontmatter_start == -1:
                frontmatter_start = i + 1  # Строка после первого ---
            else:
                frontmatter_end = i  # Строка второго ---
                break

    # Извлекаем name и description простым grep (без yaml.safe_load)
    name = None
    description = None

    if frontmatter_start >= 0 and frontmatter_end > frontmatter_start:
        for i in range(frontmatter_start, frontmatter_end):
            line = lines[i]
            if line.startswith('name:'):
                name = line.split(':', 1)[1].strip()
            elif line.startswith('description:'):
                description = line.split(':', 1)[1].strip()

        instruction_body = ''.join(lines[frontmatter_end + 1:]).strip()
    else:
        # Если нет frontmatter
        name = filepath.parent.name.replace('-', '_')
        description = ""
        instruction_body = ''.join(lines).strip()

    return {
        "name": name,
        "description": description,
        "instruction": instruction_body
    }


def upload_skill(skill_id, skill_data):
    """Загружает или обновляет скилл на сервере."""
    url = f"{SERVER}/api/skills/{skill_id}"

    response = requests.put(url, json=skill_data)
    response.raise_for_status()
    return response.json()


def upload_all_skills():
    """Загружает все скиллы на сервер."""
    skills_path = Path(SKILLS_DIR)

    # Сначала получим список существующих скиллов
    existing = requests.get(f"{SERVER}/api/skills").json()
    skills_map = {s["name"]: s["id"] for s in existing}

    for skill_dir in skills_path.iterdir():
        if not skill_dir.is_dir():
            continue

        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue

        # Разбираем скилл
        data = parse_skill_file(skill_file)

        if data["name"] in skills_map:
            # Обновляем существующий
            skill_id = skills_map[data["name"]]
            print(f"Обновляем: {data['name']} (ID: {skill_id})")
            result = upload_skill(skill_id, data)
            print(f"  ✅ {result['name']}")
        else:
            # Создаём новый
            print(f"Создаём: {data['name']}")
            response = requests.post(f"{SERVER}/api/skills", json=data)
            response.raise_for_status()
            result = response.json()
            print(f"  ✅ {result['name']} (ID: {result['id']})")


if __name__ == "__main__":
    upload_all_skills()
