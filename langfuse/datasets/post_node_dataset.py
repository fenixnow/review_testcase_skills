#!/usr/bin/env python3
"""
Синхронизация датасета post_node.

Промпт: post_review
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.datasets import create_dataset


def main():
    """Синхронизировать post_node."""

    name = "post_review_dataset"
    description = "Тестовые кейсы для проверки публикации ревью тест-кейса"

    # Загрузить схемы
    schemas_dir = Path(__file__).parent.parent / "schemas"

    with open(schemas_dir / "post_node_input_schema.json", 'r', encoding='utf-8') as f:
        input_schema = json.load(f)
    with open(schemas_dir / "post_review_dataset_output_schema.json", 'r', encoding='utf-8') as f:
        expected_output_schema = json.load(f)

    # Создать датасет со схемами
    create_dataset(
        name=name,
        description=description,
        input_schema=input_schema,
        expected_output_schema=expected_output_schema
    )


if __name__ == "__main__":
    main()
