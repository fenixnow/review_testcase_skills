# Claude Code Instructions

## Проект

Система AI-ревью тест-кейсов для Allure TestOps.

**Сервер:** `https://review-test.qa.svc.vkusvill.ru`

## Структура

```
├── prompts/           # Промпты для системы
├── skills/            # Скиллы (по одному на директорию)
├── scripts/           # Скрипты для работы с сервером
└── CLAUDE.md          # Этот файл
```

## Команды

```bash
# Обновить промпты на сервере
python3 scripts/upload_prompts.py

# Обновить скиллы на сервере
python3 scripts/upload_skills.py

# Отправить тест-кейс на ревью
python3 scripts/submit_review.py <testcase_id>
```

## Маппинг промптов (scripts/upload_prompts.py)

- `edit_testcase.md` → ID 45
- `review.md` → ID 46
- `post_review.md` → ID 51

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
  "testcase_id": 80719,
  "proposed_edit": "1. Имя тест-кейса\n- Изменить имя на: «Новое название»"
}
```

## Скиллы

| Скилл | Описание |
|-------|----------|
| edit-name | Изменение имени тест-кейса |
| edit-description | Изменение описания, вызывает edit_members/edit_links |
| edit-precondition | Изменение предусловия, выносит JSON/XML во вложения |
| edit-steps | Изменение шагов |
| edit-links | Вынос ссылок в поле «Ссылки» |
| edit-members | Добавление участников |
| edit-attachments | Создание вложений |

## Важные правила

1. **Параметры скиллов** — всегда JSON с полями `testcase_id` и `proposed_edit`
2. **Участники** — извлекаются в форматах:
   - `Роль: ФИО`
   - `Роль - ФИО @telegram` (SA→Аналитик, QA→Тестировщик)
   - `[ФИО](ссылка)`
3. **Предлагаемые правки** — только конкретные действия, без абстрактных фраз
4. **Вложенные скиллы** — edit_description автоматически вызывает edit_members/edit_links

## После изменений

После изменения промптов или скиллов — загружай на сервер:
```bash
python3 scripts/upload_prompts.py
python3 scripts/upload_skills.py
```
