# 3. Предусловие

## Формат входных данных

```
3. Предусловие
   - Заменить предусловие на: «Новый текст предусловия»

Или:

3. Предусловие
   - Вынести JSON в отдельное вложение
   - Удалить устаревшие шаги из предусловия
```

## Алгоритм

1. Извлечь новый текст предусловия
2. Проверь наличие JSON/XML блоков
3. Если есть `Вынести JSON в отдельное вложение`:
   - Найди JSON/XML в тексте
   - Создай вложение через `testcase_attachment_create`
   - Замени в тексте на ссылку на вложение
4. Вызови `testcase_patch` с обновлённым `precondition`

## Вынос JSON/XML во вложения

**Обнаружение блоков:**
- JSON: ищи `{...}` или `[...]`
- XML: ищи `<?xml...>`, `<root>...</root>`

**Создание вложения:**
```python
mcp__allure_http__testops_testcase_attachment_create(
    testcase_id=80532,
    content='{"example": "value"}',
    content_type="application/json",
    name="example_request"
)
```

## MCP инструменты

```python
mcp__allure_http__testops_testcase_patch(
    testcase_id=80532,
    precondition="Новый текст предусловия"
)

# Создание вложения
mcp__allure_http__testops_testcase_attachment_create(
    testcase_id=80532,
    content='...',
    name='request_body'
)
```
