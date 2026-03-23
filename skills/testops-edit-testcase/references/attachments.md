# 7. Вложения

## Формат входных данных

```
7. Вложения
   - Создать вложение с именем request_body:
     ```json
     {"product_id": 123, "quantity": 1}
     ```
   - Создать вложение для примера ответа (XML)
```

## Алгоритм

1. Извлеки имя вложения (после «с именем» или «для»)
2. Извлеки содержимое (до следующего пункта или конца)
3. Определи тип содержимого:
   - JSON (начинается с `{` или `[`)
   - XML (начинается с `<` или `<?xml`)
   - Текст (по умолчанию)
4. Создай вложение через `testcase_attachment_create`
5. Получи `attachment_id`

## MCP инструменты

```python
mcp__allure_http__testops_testcase_attachment_create(
    testcase_id=80532,
    content='{"example": "value"}',
    content_type="application/json",
    name="example_request"
)

# content_type может быть:
# - "application/json"
# - "application/xml"
# - "text/plain"
# - "text/markdown"
# - "text/csv"
# - "image/png"
# - "video/mp4"
```

## Автоопределение типа

| Признак | content_type | Расширение |
|---------|--------------|------------|
| Начинается с `{` или `[` | `application/json` | .json |
| Начинается с `<` или `<?xml` | `application/xml` | .xml |
| Содержит `---` (YAML) | `application/yaml` | .yaml |
| По умолчанию | `text/plain` | .txt |
