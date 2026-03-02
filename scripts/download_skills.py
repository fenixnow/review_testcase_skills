#!/usr/bin/env python3
"""
Скрипт для скачивания скиллов с удалённого сервера.

Собирает данные из API в формат SKILL.md с YAML frontmatter.
"""

import os
import requests
from pathlib import Path

SERVER = "https://review-test.qa.svc.vkusvill.ru"
SKILLS_DIR = "skills"


def assemble_skill_markdown(name, description, instruction, tags=None):
    """Собирает SKILL.md из компонентов API."""
    frontmatter = f"""---
name: {name}
description: {description}
"""

    if tags:
        frontmatter += f'tags: "{tags}"\n'

    frontmatter += "---\n"

    return f"{frontmatter}\n\n{instruction}"


def download_skill(skill_id, skill_dir):
    """Скачивает скилл и сохраняет в SKILL.md."""
    url = f"{SERVER}/api/skills/{skill_id}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    # Создаём папку скилла
    skill_path = Path(skill_dir) / data["name"]
    skill_path.mkdir(exist_ok=True)

    # Собираем SKILL.md
    content = assemble_skill_markdown(
        name=data["name"],
        description=data.get("description", ""),
        instruction=data.get("instruction", ""),
        tags=data.get("tags")
    )

    # Сохраняем
    skill_file = skill_path / "SKILL.md"
    with open(skill_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  ✅ {data['name']} → {skill_file}")


def download_all_skills():
    """Скачивает все скиллы с сервера."""
    # Получаем список скиллов
    response = requests.get(f"{SERVER}/api/skills")
    response.raise_for_status()
    skills = response.json()

    print(f"Найдено {len(skills)} скиллов:")

    for skill in skills:
        download_skill(skill["id"], SKILLS_DIR)


if __name__ == "__main__":
    download_all_skills()
