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

SERVER = "https://review-test.qa.svc.vkusvill.ru"
SKILLS_DIR = "skills"


def parse_skill_file(filepath):
    """Разбирает SKILL.md на компоненты для API."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Извлекаем YAML frontmatter
    match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)

    if match:
        frontmatter_text = match.group(1)
        instruction_body = match.group(2).strip()
        frontmatter = yaml.safe_load(frontmatter_text)
    else:
        # Если нет frontmatter — используем имя папки
        frontmatter = {
            "name": filepath.parent.name,
            "description": ""
        }
        instruction_body = content.strip()

    return {
        "name": frontmatter.get("name"),
        "description": frontmatter.get("description"),
        "instruction": instruction_body,
        "tags": frontmatter.get("tags")
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
