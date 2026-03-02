# API руководство: Обновление скиллов и промптов

**Базовый URL:** `https://review-test.qa.svc.vkusvill.ru`

## Синхронизация скиллов

Локальная структура скилла (с YAML frontmatter) → Поля API

```
Локальный файл (SKILL.md):
---
name: edit-name
description: Редактирование имени...
---

# Роль
Ты — специалист...

↓ Разбор при загрузке

API запрос:
{
  "name": "edit-name",
  "description": "Редактирование имени...",
  "instruction": "# Роль\n\nТы — специалист..."
}
```

**Правило:**
- `instruction` = содержимое SKILL.md **после** YAML frontmatter
- `name` и `description` = из YAML frontmatter

---

### Модель данных

```json
{
  "id": 1,
  "name": "edit-name",
  "description": "Описание скилла",
  "instruction": "Содержимое SKILL.md (включая YAML frontmatter или без него)",
  "tags": "tag1, tag2"
}
```

**Важно:** Наши SKILL.md имеют YAML frontmatter. При работе с API учитывай:

- `name` и `description` в API должны соответствовать YAML frontmatter
- `instruction` — это всё содержимое SKILL.md **после** YAML frontmatter
- При обновлении через API — синхронизируй YAML frontmatter с полями `name`/`description`

### API методы

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| `GET` | `/api/skills` | Получить список скиллов |
| `GET` | `/api/skills/{id}` | Получить скилл по ID |
| `POST` | `/api/skills` | Создать новый скилл |
| `PUT` | `/api/skills/{id}` | Обновить скилл |
| `DELETE` | `/api/skills/{id}` | Удалить скилл |

### Получение списка скиллов

```bash
curl -X GET "https://review-test.qa.svc.vkusvill.ru/api/skills" \
  -H "accept: application/json"
```

**Фильтрация:**
```bash
curl -X GET "https://review-test.qa.svc.vkusvill.ru/api/skills?name=edit&limit=10" \
  -H "accept: application/json"
```

### Создание скилла

```bash
curl -X POST "https://review-test.qa.svc.vkusvill.ru/api/skills" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "edit-name",
    "description": "Редактирование имени тест-кейса",
    "instruction": "---\nname: edit-name\ndescription: ...\n---\n\n# Роль\n...",
    "tags": "allure, testops, edit"
  }'
```

### Обновление скилла

```bash
curl -X PUT "https://review-test.qa.svc.vkusvill.ru/api/skills/{id}" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "edit-name",
    "description": "Новое описание",
    "instruction": "Новое содержимое",
    "tags": "allure, testops"
  }'
```

### Удаление скилла

```bash
curl -X DELETE "https://review-test.qa.svc.vkusvill.ru/api/skills/{id}" \
  -H "accept: application/json"
```

---

## Промпты (Prompts)

### Модель данных

```json
{
  "id": 1,
  "name": "review_full",
  "content": "Содержимое промпта",
  "is_enabled": true,
  "is_global": false,
  "kind": "RUN_REVIEW"
}
```

### Виды промптов (PromptKind)

| Значение | Описание |
|----------|----------|
| `EDIT_TESTCASE` | Промпт для редактирования тест-кейса |
| `RUN_REVIEW` | Промпт для запуска ревью |
| `PUBLISH_REVIEW_RESULTS` | Промпт для публикации результатов ревью |

### API методы

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| `GET` | `/api/prompts` | Получить список промптов |
| `GET` | `/api/prompts/{id}` | Получить промпт по ID |
| `POST` | `/api/prompts` | Создать новый промпт |
| `PUT` | `/api/prompts/{id}` | Обновить промпт |
| `DELETE` | `/api/prompts/{id}` | Удалить промпт |

### Получение списка промптов

```bash
curl -X GET "https://review-test.qa.svc.vkusvill.ru/api/prompts" \
  -H "accept: application/json"
```

**Фильтрация:**
```bash
curl -X GET "https://review-test.qa.svc.vkusvill.ru/api/prompts?is_enabled=true&kind=RUN_REVIEW" \
  -H "accept: application/json"
```

### Создание промпта

```bash
curl -X POST "https://review-test.qa.svc.vkusvill.ru/api/prompts" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "review_full",
    "content": "Содержимое промпта...",
    "is_enabled": true,
    "is_global": false,
    "kind": "RUN_REVIEW"
  }'
```

### Обновление промпта

```bash
curl -X PUT "https://review-test.qa.svc.vkusvill.ru/api/prompts/{id}" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "review_full",
    "content": "Обновлённое содержимое",
    "is_enabled": true,
    "is_global": false,
    "kind": "RUN_REVIEW"
  }'
```

### Удаление промпта

```bash
curl -X DELETE "https://review-test.qa.svc.vkusvill.ru/api/prompts/{id}" \
  -H "accept: application/json"
```

---

## Скрипты для синхронизации

### Установка зависимостей

```bash
pip install requests pyyaml
```

### Загрузка скиллов на сервер

```bash
python scripts/upload_skills.py
```

Скрипт:
1. Находит все `skills/*/SKILL.md`
2. Разбирает YAML frontmatter
3. Отправляет данные в API (обновляет существующие, создаёт новые)

### Скачивание скиллов с сервера

```bash
python scripts/download_skills.py
```

Скрипт:
1. Получает список скиллов из API
2. Собирает SKILL.md из полей API (с YAML frontmatter)
3. Сохраняет в `skills/{name}/SKILL.md`

### Ручное обновление одного скилла

```bash
#!/bin/bash

SKILL_ID=1
SKILL_FILE="skills/edit-name/SKILL.md"
SERVER="https://review-test.qa.svc.vkusvill.ru"

# Разбираем YAML frontmatter (через Python)
python3 << EOF
import re, yaml, sys, json

with open('$SKILL_FILE') as f:
    content = f.read()

match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
if match:
    frontmatter = yaml.safe_load(match.group(1))
    instruction = match.group(2).strip()
else:
    frontmatter = {"name": "unknown", "description": ""}
    instruction = content

print(json.dumps({
    "name": frontmatter.get("name"),
    "description": frontmatter.get("description"),
    "instruction": instruction
}))
EOF
```

### Обновление промпта из файла

```bash
#!/bin/bash

PROMPT_ID=1
PROMPT_FILE="prompts/review.md"
SERVER="https://review-test.qa.svc.vkusvill.ru"

# Читаем содержимое файла
CONTENT=$(cat "$PROMPT_FILE")

# Обновляем промпт
curl -X PUT "$SERVER/api/prompts/$PROMPT_ID" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"$(basename "$PROMPT_FILE" .md)\",
    \"content\": $(echo "$CONTENT" | jq -Rs .),
    \"is_enabled\": true,
    \"is_global\": false,
    \"kind\": \"RUN_REVIEW\"
  }"
```

---

## HTTP Client (IntelliJ IDEA)

Файл запросов можно создать в проекте:

```
### Получить все скиллы
GET https://review-test.qa.svc.vkusvill.ru/api/skills
accept: application/json

### Обновить скилл
PUT https://review-test.qa.svc.vkusvill.ru/api/skills/{{skill_id}}
accept: application/json
Content-Type: application/json

{
  "name": "edit-name",
  "description": "Описание",
  "instruction": "Содержимое SKILL.md",
  "tags": "allure, testops"
}

### Обновить промпт
PUT https://review-test.qa.svc.vkusvill.ru/api/prompts/{{prompt_id}}
accept: application/json
Content-Type: application/json

{
  "name": "review_full",
  "content": "Содержимое промпта",
  "is_enabled": true,
  "is_global": false,
  "kind": "RUN_REVIEW"
}
```
