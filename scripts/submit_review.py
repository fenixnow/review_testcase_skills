#!/usr/bin/env python3
"""
Скрипт для отправки тест-кейса на ревью.

Использование:
    python3 scripts/submit_review.py <testcase_id>

Пример:
    python3 scripts/submit_review.py 80040
"""

import sys
import os
import requests
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")
SERVER = os.getenv("REVIEW_SERVER")


def submit_review(testcase_id, project_id=None, edit_testcase_enabled=True, post_processing_enabled=True, review_id=None):
    """Отправляет тест-кейс на ревью."""
    url = f"{SERVER}/api/reviews/submit"

    payload = {
        "testcase_filter": str(testcase_id),
        "review_postprocessing_required": post_processing_enabled,
        "review_edit_testcase_required": edit_testcase_enabled,
    }

    if project_id is not None:
        payload["project_id"] = project_id
    if review_id is not None:
        payload["review_id"] = review_id

    print(f"📤 Отправляем тест-кейс #{testcase_id} на ревью...")
    print(f"   review_edit_testcase_required: {edit_testcase_enabled}")
    print(f"   review_postprocessing_required: {post_processing_enabled}")

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()

        print(f"✅ Тест-кейс отправлен на ревью!")
        print(f"   Review ID: {result.get('id')}")
        print(f"   Статус: {result.get('status')}")

        return result

    except requests.RequestException as e:
        print(f"❌ Ошибка отправки: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"   Ответ сервера: {e.response.text}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Отправить тест-кейс на ревью")
    parser.add_argument("testcase_id", type=int, help="ID тест-кейса для отправки на ревью")
    parser.add_argument("-p", "--project", type=int, help="ID проекта (опционально)")
    parser.add_argument("--no-edit", action="store_false", dest="edit_enabled", help="Отключить редактирование тест-кейса")
    parser.add_argument("--no-post", action="store_false", dest="post_enabled", help="Отключить пост-обработку")
    parser.add_argument("-r", "--review", type=int, help="ID существующего ревью (для перепроверки)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Подробный вывод")

    args = parser.parse_args()

    submit_review(
        testcase_id=args.testcase_id,
        project_id=args.project,
        edit_testcase_enabled=args.edit_enabled,
        post_processing_enabled=args.post_enabled,
        review_id=args.review
    )


if __name__ == "__main__":
    main()