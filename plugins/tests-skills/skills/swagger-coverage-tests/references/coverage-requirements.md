# Структура отчёта swagger-coverage-results

## Общая структура

```json
{
  "api": "Название API",
  "generated_at": "2026-05-07 13:55:41",
  "summary": {
    "total_operations": 89,
    "fully_covered": 5,
    "partially_covered": 20,
    "not_covered": 128,
    "deprecated": 0,
    "total_conditions": 1022,
    "covered_conditions": 133,
    "coverage_percent": 13.0
  },
  "paths": {
    "/endpoint/path": {
      "GET": {
        "state": "EMPTY | PARTY | FULL",
        "coverage": "0/16",
        "deprecated": false,
        "requirements": {
          "status_codes": [...],
          "parameters": [...],
          "body": [...],
          "properties": [...]
        }
      }
    }
  }
}
```

## Состояния операций (state)

| State | Значение |
|-------|---------|
| `EMPTY` | Нет ни одного вызова — все требования не покрыты |
| `PARTY` | Есть вызовы, но часть требований не покрыта |
| `FULL` | Все требования покрыты |

## Требования (requirements)

Каждая операция содержит требования в поле `requirements`. Каждое требование имеет поле `covered` (true/false).
Требование считается выполненным когда `covered: true`.

### status_codes

Требование: эндпоинт должен вернуть указанный HTTP статус код.

```json
{ "code": "200", "covered": false, "description": "OK" }
```

### parameters

Требование: параметр должен быть передан в запросе.

```json
{ "in": "query", "covered": false, "name": "product_id", "description": "ID товара" }
```

### body

Требование: запрос должен содержать тело.

```json
{ "covered": false, "description": "Параметры метода" }
```

### properties

Требование: в тесте должно быть обращение к указанному полю ответа (через getter в assert).

```json
{ "covered": false, "name": "product_id", "description": "" }
```