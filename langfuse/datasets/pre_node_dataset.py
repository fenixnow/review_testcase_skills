#!/usr/bin/env python3
"""
Синхронизация датасета pre_node.

Промпт: (пока нет)
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.datasets import create_dataset


def main():
    """Синхронизировать pre_node."""

    name = "pre_node"
    description = "Тестовые кейсы для пре-обработки"

    # Загрузить схемы
    schemas_dir = Path(__file__).parent.parent / "schemas"
    with open(schemas_dir / "pre_node_input_schema.json", 'r', encoding='utf-8') as f:
        input_schema = json.load(f)
    with open(schemas_dir / "pre_node_expected_output_schema.json", 'r', encoding='utf-8') as f:
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
