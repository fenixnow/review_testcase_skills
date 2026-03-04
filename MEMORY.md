# Проект: Review Testcase Skills

Система AI-ревью тест-кейсов для Allure TestOps.

## Технологический стек

**LangGraph** — для построения агента со скиллами. Скиллы = узлы/функции в графе агента.

## Важно: Правила работы

**НЕ строить догадки!** Уточнять у пользователя, если не уверен. Говорить "нужно больше информации" вместо предположений. Не делать выводов без явных данных.

## Сервер

**URL:** `https://review-test.qa.svc.vkusvill.ru`

## Скрипты

```bash
# Обновление промптов на сервере
python3 scripts/upload_prompts.py

# Обновление скиллов на сервере
python3 scripts/upload_skills.py

# Отправка тест-кейса на ревью
python3 scripts/submit_review.py <testcase_id>
```

## API форматы

**Submit review:**
```json
{
  "testcase_filter": "80719",
  "review_postprocessing_required": true,
  "review_edit_testcase_required": true
}
```

**Вызов скилла:**
```json
{
  "text": "{\"testcase_id\": 80719, \"proposed_edit\": \"...\"}"
}
```

## Маппинг промптов

- `edit_testcase.md` → ID 45
- `review.md` → ID 46
- `post_review.md` → ID 51

## Скиллы

- `edit-name` — изменение имени
- `edit-description` — описание, вызывает edit_members/edit_links
- `edit-precondition` — предусловие, выносит JSON/XML
- `edit-steps` — шаги
- `edit-links` — ссылки
- `edit-members` — участники
- `edit-attachments` — вложения

## Ключевые нюансы

1. Параметры скиллов — JSON с полями `testcase_id` и `proposed_edit` внутри `text`
2. Участники — форматы: `Роль: ФИО`, `Роль - ФИО @telegram` (SA→Аналитик, QA→Тестировщик)
3. Предлагаемые правки — только конкретные действия
4. Вложенные скиллы — edit_description вызывает edit_members/edit_links

## Формат документации скиллов

В SKILL.md используется формат Args (как в MCP инструментах):

```
Args:
    testcase_id (int, required): Уникальный числовой идентификатор тест-кейса.
    proposed_edit (str, required): Готовый текст секции из ревью.

Returns:
    str: Отчёт о выполнении изменений.
```
