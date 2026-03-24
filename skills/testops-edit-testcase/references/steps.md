# 6. Шаги сценария

## Формат входных данных

```
6. Шаги сценария
   - Изменить шаг 1: «Новый текст шага»
   - Удалить шаг 2
   - Добавить шаг после 3: «Новый шаг» → «Ожидаемый результат»
   - Переместить шаг 4 после шага 2
```

## Алгоритм

1. Получи текущие шаги через `testops_scenario_steps_read`
2. Построй карту шагов (id, number, текст)
3. **ПРОВЕРЬ ВЛОЖЕНИЯ ПЕРЕД УДАЛЕНИЕМ:**
   - Если команда «Удалить шаг N» → сначала проверь вложения этого шага
   - Получи список вложений через `testcase_attachment_list`
   - Если вложения есть → **НЕ УДАЛЯЙ шаг**, вместо этого:
     - Предупреди пользователя о вложениях
     - Предложи альтернативы: перенести вложение в другой шаг или сохранить шаг
4. Примени изменения:
   - **Изменить** → `scenario_step_patch`
   - **Удалить** → `scenario_step_delete` (только если нет вложений!)
   - **Добавить** → `scenario_step_create` или `scenario_step_create_with_expected_result`
   - **Переместить** → `scenario_step_move`
5. Проверь результат

## Структура шага

```yaml
id: 123456
number: "1"
step: "Текст шага"
expected_result:
  id: 123457
  steps:
    - id: 123458
      number: "2.1"
      step: "Ожидаемый результат"
```

## MCP инструменты

```python
# Получить шаги
mcp__allure_http__testops_scenario_steps_read(testcase_id=80532)

# Изменить шаг
mcp__allure_http__testops_scenario_step_patch(
    step_id=123456,
    body="Новый текст",
    with_expected_result=false
)

# Удалить шаг
mcp__allure_http__testops_scenario_step_delete(step_id=123456)

# Создать шаг
mcp__allure_http__testops_scenario_step_create(
    testcase_id=80532,
    body="Новый шаг",
    after_id=123456
)

# Создать шаг с ожидаемым результатом
mcp__allure_http__testops_scenario_step_create_with_expected_result(
    testcase_id=80532,
    body="Действие",
    expected_result_body="Результат",
    after_id=123456
)

# Переместить шаг
mcp__allure_http__testops_scenario_step_move(
    step_id=123456,
    after_id=123450
)
```
