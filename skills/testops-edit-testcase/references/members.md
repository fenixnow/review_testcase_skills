# 5. Участники

## Формат входных данных

```
5. Участники
   - Добавить участника: username найти по ФИО «Иванов Иван», role_id найти роль «Аналитик»
   - Найти и добавить участника: username для Петров, role_id -1 (Owner)
```

## Роли (role_id)

| Роль | role_id | Описание |
|------|---------|-----------|
| Owner | -1 | Владелец |
| Lead | -2 | Лид |
| Тестировщик | 1 | Тестировщик |
| Разработчик | 2 | Разработчик |
| Аналитик | 3 | Аналитик (SA) |
| tester | 5 | Тестировщик |
| AQA | 6 | AQA |
| QA | 7 | QA |

## Форматы извлечения участников

**Формат 1 — роль нужно найти:**
```
Добавить участника: username найти по ФИО «Иванов», role_id найти роль «Аналитик»
```

**Формат 2 — role_id уже известен:**
```
Найти и добавить участника: username для Петров, role_id -1 (Owner)
```

## Алгоритм

1. Получи список ролей через `testops_roles_read`
2. Для каждого участника:
   - Извлеки ФИО из кавычек
   - Если role_id не указан → найди по названию роли
   - Поиск пользователя через `testops_accounts_read` по фамилии
   - Добавь через `testcase_testcase_member_create`
3. Проверь результат через `testcase_testcase_members_read`

## MCP инструменты

```python
# Получить роли
mcp__allure_http__testops_roles_read()

# Поиск пользователя
mcp__allure_http__testops_accounts_read(query="Иванов")

# Добавить участника
mcp__allure_http__testops_testcase_member_create(
    testcase_id=80532,
    username="i.ivanov",
    role_id=3
)

# Проверить результат
mcp__allure_http__testops_testcase_members_read(testcase_id=80532)
```
