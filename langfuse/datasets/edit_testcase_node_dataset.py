#!/usr/bin/env python3
"""
Синхронизация датасета edit_testcase_node.

Промпт: edit_testcase
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.datasets import create_dataset


def main():
    """Синхронизировать edit_testcase_node."""

    name = "edit_testcase_node"
    description = "Редактирование тест кейса"

    # Загрузить схемы
    schemas_dir = Path(__file__).parent.parent / "schemas"
    with open(schemas_dir / "edit_testcase_node_input_schema.json", 'r', encoding='utf-8') as f:
        input_schema = json.load(f)
    with open(schemas_dir / "edit_testcase_node_expected_output_schema.json", 'r', encoding='utf-8') as f:
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
