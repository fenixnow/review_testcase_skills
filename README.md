# Review Testcase Skills

Набор скиллов Claude Code для автоматизированного ревью и редактирования тест-кейсов в Allure TestOps.

## Структура проекта

```
review_testcase_skills/
├── skills/                          # Исполняемые скиллы
│   ├── edit-name/SKILL.md           # Редактирование имени тест-кейса
│   ├── edit-description/SKILL.md    # Редактирование описания
│   ├── edit-precondition/SKILL.md   # Редактирование предусловия
│   ├── edit-steps/SKILL.md          # Редактирование шагов
│   ├── edit-links/SKILL.md          # Перемещение ссылок (вспомогательный)
│   ├── edit-members/SKILL.md        # Добавление участников (вспомогательный)
│   └── edit-attachments/SKILL.md    # Работа с вложениями (вспомогательный)
│
├── prompts/                         # Промпты для LLM
│   ├── review.md                    # Полный промпт ревью тест-кейсов
│   ├── review_simple.md             # Упрощённый промпт ревью
│   ├── comment.md                   # Промпт для формирования комментариев
│   └── edit_testcase.md             # Орркестратор применения правок
│
└── docs/                            # Справочная документация
    └── review_checklist.md          # Чек-лист проверки формулировок ревью
```

## Структура скилла

Каждый скилл — это папка с файлом `SKILL.md`:

```
skill-name/
└── SKILL.md
    ├── YAML frontmatter (name, description)
    └── Markdown инструкции
```

## Использование

### 1. Ревью тест-кейса

Используйте промпт `prompts/review.md` для проведения полного ревью тест-кейса.

### 2. Применение правок

Используйте орркестратор `prompts/edit_testcase.md` для автоматического применения правок из ревью.

**Входные параметры:**
- `testcase_id` — ID тест-кейса
- `review_result` — полный текст ревью с секцией «Предлагаемые правки»

### 3. Прямое редактирование

Каждый основной скилл может быть вызван напрямую для изменения конкретной секции тест-кейса.

## Зависимости скиллов

```
prompts/edit_testcase (оркестратор)
    ├─→ skills/edit-name
    ├─→ skills/edit-description
    │    ├─→ skills/edit-links (автоматически)
    │    └─→ skills/edit-members (автоматически)
    ├─→ skills/edit-precondition
    │    └─→ skills/edit-attachments (автоматически)
    └─→ skills/edit-steps
         └─→ skills/edit-attachments (автоматически)
```

## MCP инструменты

Для работы скиллов требуются MCP инструменты Allure TestOps:
- `testops_testcase_get` — получение данных тест-кейса
- `testops_testcase_patch` — обновление тест-кейса
- `testops_testcase_link_create` — добавление ссылок
- `testops_integration_list` — получение интеграций проекта

## Версия

v1.0.0
