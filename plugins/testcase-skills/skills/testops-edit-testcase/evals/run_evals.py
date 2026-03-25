#!/usr/bin/env python3
"""
Запуск тестов для скилла testops-edit-testcase.

Использование:
    python3 run_evals.py [--testcase-id ID] [--dry-run]
"""

import sys
import os
import json
from pathlib import Path

# Добавляем корень проекта в path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

try:
    from dotenv import load_dotenv
    import requests
    
    load_dotenv(dotenv_path=Path(__file__).parent.parent.parent.parent.parent / ".env")
    SERVER = os.getenv("REVIEW_SERVER")
except ImportError:
    print("⚠️  Установите зависимости: pip install python-dotenv requests")
    sys.exit(1)


def load_evals():
    """Загружает тесты из evals.json"""
    evals_path = Path(__file__).parent / "evals.json"
    with open(evals_path) as f:
        return json.load(f)


def run_skill_on_testcase(testcase_id, proposed_edit):
    """Запускает скилл на тест-кейсе"""
    url = f"{SERVER}/api/skills/testops-edit-testcase/execute"
    
    payload = {
        "testcase_id": testcase_id,
        "proposed_edit": proposed_edit
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}


def check_attachments_before_delete(testcase_id, step_number):
    """Проверяет, есть ли вложения у шага"""
    # TODO: реализовать проверку через Allure TestOps API
    return False


def run_test(eval_config, dry_run=False):
    """Запускает один тест"""
    print(f"\n🧪 Тест {eval_config['id']}: {eval_config['name']}")
    print(f"   TestCase: #{eval_config['testcase_id']}")
    print(f"   Proposed Edit:\n{eval_config['proposed_edit']}")
    
    if dry_run:
        print("   ⚠️  DRY RUN - пропущен")
        return {"id": eval_config['id'], "skipped": True}
    
    # Запускаем скилл
    result = run_skill_on_testcase(
        eval_config['testcase_id'],
        eval_config['proposed_edit']
    )
    
    if "error" in result:
        print(f"   ❌ Ошибка: {result['error']}")
        return {"id": eval_config['id'], "error": result['error']}
    
    # Проверяем assertions
    passed_assertions = []
    failed_assertions = []
    
    for assertion in eval_config.get('assertions', []):
        # TODO: реализовать проверки assertions
        passed = False  # Заглушка
        if passed:
            passed_assertions.append(assertion['name'])
        else:
            failed_assertions.append(assertion['name'])
    
    print(f"   ✅ Passed: {len(passed_assertions)}")
    print(f"   ❌ Failed: {len(failed_assertions)}")
    
    return {
        "id": eval_config['id'],
        "name": eval_config['name'],
        "passed_assertions": passed_assertions,
        "failed_assertions": failed_assertions,
        "passed": len(failed_assertions) == 0
    }


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Запуск тестов testops-edit-testcase")
    parser.add_argument("--testcase-id", type=int, help="Запустить только для этого testcase")
    parser.add_argument("--dry-run", action="store_true", help="Не выполнять реальные изменения")
    parser.add_argument("--verbose", "-v", action="store_true", help="Подробный вывод")
    
    args = parser.parse_args()
    
    # Загружаем тесты
    evals_config = load_evals()
    
    # Фильтруем тесты
    tests_to_run = evals_config['evals']
    if args.testcase_id:
        tests_to_run = [t for t in tests_to_run if t['testcase_id'] == args.testcase_id]
    
    print(f"🚀 Запуск {len(tests_to_run)} тестов для testops-edit-testcase")
    print(f"   Server: {SERVER}")
    
    if args.dry_run:
        print("   ⚠️  DRY RUN MODE")
    
    # Запускаем тесты
    results = []
    for test in tests_to_run:
        result = run_test(test, dry_run=args.dry_run)
        results.append(result)
    
    # Итоги
    print("\n📊 Результаты:")
    passed = sum(1 for r in results if r.get('passed', False))
    failed = sum(1 for r in results if not r.get('passed', True) and not r.get('skipped', False))
    skipped = sum(1 for r in results if r.get('skipped', False))
    
    print(f"   ✅ Passed: {passed}")
    print(f"   ❌ Failed: {failed}")
    print(f"   ⏭️  Skipped: {skipped}")
    
    # Сохраняем результаты
    results_dir = Path(__file__).parent / "results"
    results_dir.mkdir(exist_ok=True)
    
    results_file = results_dir / "test_results.json"
    with open(results_file, 'w') as f:
        json.dump({
            "skill_name": "testops-edit-testcase",
            "timestamp": Path(__file__).stat().st_mtime,
            "results": results
        }, f, indent=2)
    
    print(f"\n💾 Результаты сохранены: {results_file}")
    
    # Возвращаем код выхода
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
