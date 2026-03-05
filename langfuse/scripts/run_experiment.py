#!/usr/bin/env python3
"""
Скрипт запуска эксперимента для post_review.

Использование:
    python3 scripts/run_experiment.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.experiments import run_experiment
from utils.post_review import post_review_task
from utils.datasets import get_dataset
from utils.config import get_langfuse_config


def main():
    """Запустить эксперимент."""

    print("🧪 Запуск эксперимента для post_review")
    print("=" * 50)

    config = get_langfuse_config()
    print(f"✅ Langfuse: {config['host']}")
    print()

    dataset = get_dataset("post_node")
    print(f"📊 Датасет: {dataset.name}")
    print(f"   Элементов: {len(dataset.items)}")
    print()

    # Запускаем эксперимент
    result = run_experiment(
        dataset_name="post_node",
        task=post_review_task,
        name="post_review_experiment_v1",
        description="Тестирование логики публикации ревью",
        metadata={
            "prompt_name": "post_review",
            "model": "claude-sonnet-4-6",
        }
    )

    print("✅ Эксперимент завершён")
    print(f"   ID: {result.id}")
    print(f"   Статус: {result.status}")
    print()
    print("📊 Результаты:")
    print("-" * 50)
    print(result.format())
    print()
    print("🔗 https://cloud.langfuse.com/experiments")


if __name__ == "__main__":
    main()
