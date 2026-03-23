# 4. Ссылки

## Формат входных данных

```
4. Ссылки
   - переместить ссылку https://tracker.yandex.ru/... в поле «Связанные задачи»
   - вынести ссылку https://docs... в поле «Ссылки»
```

## Алгоритм

1. Проверь интеграции проекта через `testops_integration_list`
2. Для каждой ссылки:
   - Определи тип (tracker/wiki/etc)
   - Если интеграция с трекером есть → добавь в `issues`
   - Иначе → добавь в `links`
   - Удали markdown-ссылку из описания
3. Вызови `testcase_patch` один раз со всеми изменениями

## Типы ссылок

| Тип | Поле | Пример |
|-----|------|--------|
| Yandex Tracker | `issues` | `https://tracker.yandex.ru/PROJECT-123` |
| Jira | `issues` | `https://jira.company.com/browse/PROJ-123` |
| Конfluence/Bookstack | `links` | `https://bookstack.int...` |
| Swagger/OpenAPI | `links` | `https://swagger...` |

## MCP инструменты

```python
# Проверить интеграции
mcp__allure_http__testops_integration_list(project_id=90)

# Поиск задачи в трекере
mcp__allure_http__testops_integration_search_issue(
    project_id=90,
    integration_id=43,
    key="PROJ-123"
)

# Добавить связанные задачи
mcp__allure_http__testops_testcase_issues_set(
    testcase_id=80532,
    issues=[
        {"integration_id": 43, "name": "PROJ-123"},
        {"integration_id": 43, "name": "PROJ-456"}
    ]
)

# Добавить внешнюю ссылку
mcp__allure_http__testops_testcase_link_create(
    testcase_id=80532,
    link_url="https://docs...",
    link_name="Документация"
)
```
