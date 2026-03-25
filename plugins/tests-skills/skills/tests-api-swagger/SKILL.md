---
name: api-tests-swagger
description: "Напиши API тесты на Java/JUnit 5 используя сгенерированные OpenAPI клиенты. Используй для: написать API тест, создать автотест REST endpoint, проверить HTTP метод, протестировать API, написать swagger тест, покрыть API тестами, integration тест REST API, добавить автотесты, написать тест по тест-кейсу из Allure TestOps. Если пользователь упоминает REST API, OpenAPI, Swagger, HTTP GET/POST/PUT/DELETE, автотесты API — используй этот навык."
---

# API Тесты на Java с OpenAPI

Этот навык помогает писать API автотесты используя сгенерированные по OpenAPI спецификации клиенты и модели.

## Когда использовать

Используй когда:
- Пишешь новый API тест или autotest
- Создаёшь тест для REST endpoint
- Покрываешь существующий API тестами
- Проверяешь работу HTTP метода
- Работаешь со сгенерированными по OpenAPI клиентам

## Структура класса API тестов

**Обязательное правило:** Класс с API тестами должен быть аннотирован `@Api`.

```java
@Api                              // Обязательная мета-аннотация для API тестов
@DisplayName("Название функционала")  // Короткое название, без пути endpoint
public class SomeTests extends BaseTest {

    @Test
    @DisplayName("Получение списка пользователей")  // Без GET /api/users
    void testGetUsers() {
        // ...
    }
}
```

**Важно:** `@DisplayName` теста описывает **что делает тест**, а не какой endpoint вызывается. Не включай HTTP метод и путь в название.

**Что делает `@Api`:**
- Добавляет `@Layer(LayerType.API)` — слой тестирования
- Добавляет `@ExtendWith(AllureJunit5.class)` — интеграция с Allure

## Импорты

```java
// Статические импорты для шагов Allure и утверждений
import static io.qameta.allure.Allure.step;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

// Импорты аннотаций
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import io.qameta.allure.junit5.AllureJunit5;
import io.qameta.allure.AllureId;  // Для связки с тест-кейсами TestOps

// Импорты API клиентов и моделей
import lk3.api.UserApi;
import lk3.model.GetUser200Response;
```

**ВАЖНО:** `step()` — это **статический импорт** от `io.qameta.allure.Allure`, не `Allure.step()`.

```java
// ПРАВИЛЬНО
step("Дано ID пользователя: %s".formatted(userId));

// НЕПРАВИЛЬНО
Allure.step("Дано ID пользователя: %s".formatted(userId));  // ❌
```

## Quick Start

```java
// Для успешного ответа (статус 200) используем executeAs()
GetUser200Response result = userApi()
    .apiUsersUserIdGet()
    .userIdPath(1L)
    .executeAs(response -> response
        .then()
        .statusCode(200)
        .extract().response());

assertEquals("success", result.getStatus(),
    "Статус ответа должен быть 'success'");
```

**Как работает executeAs():**
- Принимает lambda с параметром `response` (тип `Response`)
- Внутри lambda мы цепочим `.then().statusCode(200).extract().response()`
- **Метод САМ десериализует ответ** в тип `GetUser200Response`
- Не используй `.body().as()` внутри executeAs!

### Quick Start: Написание автотеста по тест-кейсу

Когда пользователь просит написать API тест **по тест-кейсу** из Allure TestOps:

1. Скопируй ID → добавь `@AllureId("ID")`
2. Проанализируй **preconditions** → определи RequestSpec и заголовки
3. Выпиши ВСЕ параметры из шага → сопоставь с методами API
4. Напиши код → используй executeAs() для успешных ответов

**⚠️ Критично:** Не пропускай preconditions! Подробно → [references/testcases.md](references/testcases.md)

## Паттерны

### Используй типизированные модели

Swagger модели имеют явные типы из спецификации API. Указывай тип явно — это улучшает читаемость и помогает IDE с автодополнением.

```java
GetUser200Response result = api()
    .method()
    .executeAs(response -> response
            .then()
            .statusCode(200)
            .extract().response());
```

Не используй `var` — он скрывает тип и делает код менее читаемым.

### Создавай запросы через Builder

OpenAPI генератор создаёт Builder для всех моделей. Используй его — чище и читабельнее, чем цепочки `setXxx()`.

```java
CreateUserRequest request = CreateUserRequest.builder()
    .name("John")
    .email("john@example.com")
    .build();
```

**Правило упрощения:** В тестовых примерах используй только **необходимые** поля. Не копируй все технические поля из реальных тестов — это делает пример сложным для понимания.

```java
// ПРАВИЛЬНО: Только нужные для примера поля
SaveInclusionAnswerRequest request = SaveInclusionAnswerRequest.builder()
    .action(SaveInclusionAnswerRequest.ActionEnum.SAVE)
    .body(SaveInclusionAnswerRequestBody.builder()
        .manufactureDate(SaveInclusionAnswerRequestBodyManufactureDate.builder()
            .label("2025-10-13")
            .value("2025-10-13")
            .build())
        .build())
    .build();

// НЕПРАВИЛЬНО: Слишком много технических полей
SaveInclusionAnswerRequest request = SaveInclusionAnswerRequest.builder()
    .action(...)
    .body(SaveInclusionAnswerRequestBody.builder()
        .manufactureDate(...)
        .isDateUnknown(...)
        .inclusionDescription(...)
        .inclusionCause(...)
        .processDescription(...)
        .controlMethod(...)
        .plannedCorrectiveActions(...)
        .deadlineForCorrectiveActions(...)
        .videoRecording(...)
        .filledOut(...)
        .comment(...)
        .answerFiles(...)
        .build())
    .build();
```

### Проверяй через JUnit Assertions

Используй JUnit Assertions вместо RestAssured `.body()` — типизированная модель уже десериализована, работай с ней напрямую.

**⚠️ Важно:** Всегда добавляй message параметр для понятных ошибок (см. раздел [Проверки](#проверки)).

```java
assertEquals("success", result.getStatus(),
    "Статус ответа должен быть 'success'");
assertNotNull(result.getBody().getData(),
    "Поле 'data' не должно быть null");
assertTrue(result.getBody().getUsers().isEmpty(),
    "Список пользователей должен быть пустым");
```

### Логируй шаги через step()

Используй Gherkin стиль: **Дано → Действие → Проверка**.

```java
String userId = "123";
step("Дано ID пользователя: %s".formatted(userId));

GetUser200Response result = userApi()
    .apiUsersUserIdGet()
    .userIdPath(userId)
    .executeAs(response -> response
        .then()
        .statusCode(200)
        .extract().response());

step("И я проверяю тело ответа", () -> {
    assertEquals("success", result.getStatus(),
        "Статус ответа должен быть 'success'");
    assertNotNull(result.getBody(),
        "Тело ответа не должно быть null");
});
```

**Правила:**
- **Дано:** Входные данные — `step("Дано ID пользователя: %s", value)`
- **Создание объектов:** НЕ оборачивай в step() — это просто код
- **Проверки:** `step("И я проверяю ...", () -> { ... })`

## Структура теста

```java
@Test
@DisplayName("Получение пользователя по ID")  // Описание действия, без HTTP метода
@Tag("api")
@AllureId("12345")  // ОБЯЗАТЕЛЬНО при генерации по тест-кейсу TestOps
void getUserById() {
    // Подготовка
    Long userId = 1L;

    // Действие
    GetUser200Response result = userApi()
        .apiUsersUserIdGet()
        .userIdPath(userId)
        .executeAs(response -> response
            .then()
            .statusCode(200)
            .extract().response());

    // Проверки
    step("И я проверяю тело ответа", () -> {
        assertEquals("success", result.getStatus(),
            "Статус ответа должен быть 'success'");
    });
}
```

**⚠️ ПРАВИЛО @AllureId:**

При генерации теста **по тест-кейсу из Allure TestOps** — ОБЯЗАТЕЛЬНО добавь `@AllureId` с ID тест-кейса:

```java
import io.qameta.allure.AllureId;

@Test
@DisplayName("Название из тест-кейса")
@AllureId("72456")  // ID тест-кейса из TestOps
void testFromTestcase() {
    // ...
}
```

**Зачем нужно:**
- Связывает автотест с тест-кейсом в Allure TestOps
- Позволяет видеть результаты автотестов в тест-кейсе
- Обеспечивает трассировку от тест-кейса до автотеста

**Когда НЕ добавлять:**
- Если пишешь тест не по конкретному тест-кейсу
- Если это пример/демо код
- Если тест не связан с TestOps


## Работа с тест-кейсами Allure TestOps

**⚠️ КРИТИЧЕСКО:** При написании теста по тест-кейсу НЕ пропускай preconditions!

**Основные ошибки:**
- ❌ Эксперименты/фичи из precondition → забыл добавить `.header()`
- ❌ Параметры из шага → не все добавлены
- ❌ Неправильный RequestSpec (без токена, когда нужен)

**Подробный алгоритм, чек-лист и примеры:** → см. **[references/testcases.md](references/testcases.md)**

**Краткая справка:**
| Precondition | Реализация |
|--------------|------------|
| Эксперимент включён | `.header("x-vkusvill-ab-tests", "exp=B")` |
| Пользователь авторизован | `catalogApiWithIntegrationToken()` |

---

## Именование переменных---

## Именование переменных

| Тип ответа | Рекомендуемое название |
|------------|------------------------|
| `GetUser200Response` | `result`, `userResponse`, `userData` |
| `CreateUser201Response` | `result`, `createdUser` |
| `GetUsersList200Response` | `result`, `usersList`, `usersResponse` |
| Параметр lambda в `executeAs()` | **всегда** `response` |

**Важно:** Переменная результата обычно называется `result`. Параметр lambda в `executeAs()` **всегда** называется `response`.

## Работа с API клиентом

### Именование в executeAs()

**Правило:** В `executeAs()` используй `response` как имя параметра lambda, а `result` — для переменной результата.

```java
// ПРАВИЛЬНО: Параметр lambda = response, переменная = result
GetUser200Response result = userApi()
    .apiUsersUserIdGet()
    .executeAs(response -> response      // ✅ параметр lambda
        .then()
        .statusCode(200)
        .extract().response());

assertEquals("success", result.getStatus(),
    "Статус ответа должен быть 'success'");  // ✅ переменная результата

// НЕПРАВИЛЬНО: Одинаковое имя — затенение переменной
GetUser200Response response = userApi()
    .apiUsersUserIdGet()
    .executeAs(response -> response          // ❌ конфликт имён!
        .then()
        .statusCode(200)
        .extract().response());
```

### Форматирование цепочки вызовов

**Правило:** Вызов метода API (например, `.apiMethod()`, `.apiFilesStarterDocsGet()`) **всегда** должен начинаться с новой строки.

```java
// ПРАВИЛЬНО: Метод API с новой строки
ResponseType result = api()
    .apiMethod()           // ✅ новая строка
    .paramPath(value)
    .executeAs(response -> response
        .then()
        .statusCode(200)
        .extract().response());

// НЕПРАВИЛЬНО: Метод API на той же строке, что и api()
var result = api().apiMethod()    // ❌
    .paramPath(value)
    .executeAs(...);
```

Это улучшает читаемость — глаз легко считывает структуру: `api()` → метод → параметры → выполнение.

### 🚫 ЗАПРЕЩЕННЫЕ ПАТТЕРНЫ

### Никогда не используй .extract().body().as() для статус 200

```java
// ❌ НЕПРАВИЛЬНО - вариант 1
GetUser200Response result = userApi()
    .apiUsersUserIdGet()
    .userIdPath(1L)
    .execute(Validatable::then)
    .statusCode(200)
    .extract().body().as(GetUser200Response.class);

// ❌ НЕПРАВИЛЬНО - вариант 2 (внутри executeAs!)
GetUser200Response result = userApi()
    .apiUsersUserIdGet()
    .userIdPath(1L)
    .executeAs(response -> response.body().as(GetUser200Response.class));

// ✅ ПРАВИЛЬНО - используем executeAs() правильно
GetUser200Response result = userApi()
    .apiUsersUserIdGet()
    .userIdPath(1L)
    .executeAs(response -> response
        .then()
        .statusCode(200)
        .extract().response());
```

**Почему:** `executeAs()` автоматически десериализует ответ в правильный тип. Использование `.extract().body().as()` для успешных ответов — это антипаттерн.

### Путь endpoint не должен быть в @DisplayName

```java
// ❌ НЕПРАВИЛЬНО
@DisplayName("GET /api/users/{id} - получение пользователя")

// ❌ НЕПРАВИЛЬНО
@DisplayName("POST /api/inclusions/{inclusionId}/answer - сохранение ответа")

// ✅ ПРАВИЛЬНО
@DisplayName("Получение пользователя по ID")
@DisplayName("Сохранение ответа на включение")
```

---

## Выбор между executeAs() и execute()

**Критически важное правило:** Выбор метода зависит от ожидаемого HTTP статуса ответа.

| Ожидаемый статус | Метод | Паттерн |
|-----------------|-------|---------|
| **200 (успех)** | `executeAs()` | Типизированный возврат, автоматически десериализует в модель |
| **400, 404, 422, 429 (ошибки)** | `execute()` | Явное указание statusCode и десериализация |

```java
// ✅ Статус 200 — используем executeAs() для типизированного ответа
Success result = authApi()
    .authLk3ResetPasswordPost()
    .body(request)
    .executeAs(response -> response
        .then()
        .statusCode(200)
        .extract().response());

// ✅ Статус 422 — используем execute() с явной десериализацией
Error422 result = authApi()
    .authLk3ResetPasswordPost()
    .body(request)
    .execute(Validatable::then)
    .statusCode(422)
    .extract().body().as(Error422.class);
```

**Правило:** Если у метода есть типизированный `executeAs()` и ожидается статус 200 — **всегда** используй его. Он сразу возвращает нужный тип. Для ошибок используй `execute()` с явным `.statusCode(XXX).extract().body().as(Model.class)`.

**Важно при работе с тест-кейсами:** При выборе метода ориентируйся на **Ожидаемый результат** тест-кейса:
- Если expected result: "HTTP 200" → используй `executeAs()`
- Если expected result: "HTTP 422" или другой код ошибки → используй `execute()`

**Precondition тоже влияют на выбор RequestSpec:**
- Если precondition: "Пользователь НЕ авторизован" → нужен RequestSpec без токена
- Если precondition: "Пользователь авторизован" → нужен RequestSpec с токеном (`catalogApiWithIntegrationToken()`)
- Если precondition: "Эксперимент B включён" → нужно добавить `.header("x-vkusvill-ab-tests", "exp=B")`

### Базовый паттерн (для успешных ответов)

```java
ResponseType result = api()
    .apiMethod()           // метод
    .paramPath(value)      // path параметр
    .paramQuery(value)     // query параметр
    .body(request)         // тело запроса
    .executeAs(response -> response
        .then()
        .statusCode(200)
        .extract().response());
```

### Паттерн для ответов с ошибками

```java
ErrorResponse result = api()
    .apiMethod()           // метод
    .paramPath(value)      // path параметр
    .body(request)         // тело запроса
    .execute(Validatable::then)
    .statusCode(422)       // код ошибки
    .extract().body().as(ErrorResponse.class);
```

### Параметры

| Тип | Суффикс | Пример |
|-----|---------|--------|
| Path | `Path` | `.userIdPath(123L)` |
| Query | `Query` | `.limitQuery(10)` |
| Header | `Header` | `.authHeader("token")` |
| Body | `body()` | `.body(request)` |

## Проверки

### ⚠️ ОБЯЗАТЕЛЬНО: Добавляй message в ассерты

**Критическое правило:** Все ассерты должны иметь **параметр message** для понятных сообщений об ошибках.

**Зачем нужно:**
- При падении теста сразу понятно, **что именно** проверялось
- Не нужно копаться в коде для понимания причины ошибки
- Ускоряет отладку и анализ падений

**Примеры:**

```java
// ❌ НЕПРАВИЛЬНО: Нет message
assertEquals("success", result.getStatus());
assertNotNull(result.getBody().getData());
assertEquals(5, result.getBody().getItems().size());
assertTrue(result.getBody().getTags().isEmpty());

// ✅ ПРАВИЛЬНО: Есть понятный message
assertEquals("success", result.getStatus(),
    "Статус ответа должен быть 'success'");
assertNotNull(result.getBody().getData(),
    "Поле 'data' не должно быть null");
assertEquals(5, result.getBody().getItems().size(),
    "Должно быть 5 элементов в списке items");
assertTrue(result.getBody().getTags().isEmpty(),
    "Список тегов должен быть пустым");
```

**Формат message:**
- Описывай **что проверяется**, а не какой ожидается результат
- Используй формат: `"Поле X должно быть Y"` или `"Список X должен содержать Y элементов"`
- Включай имя проверяемого поля/сущности для контекста

### Примитивы и объекты
```java
assertEquals("success", result.getStatus(),
    "Статус ответа должен быть 'success'");
assertNotNull(result.getBody().getData(),
    "Поле 'data' не должно быть null");
assertEquals("John", result.getBody().getUser().getName(),
    "Имя пользователя должно быть 'John'");
```

### Collections
```java
assertEquals(5, result.getBody().getItems().size(),
    "Должно быть 5 элементов в списке items");
assertTrue(result.getBody().getTags().isEmpty(),
    "Список тегов должен быть пустым");

// Поиск элемента
User user = result.getBody().getUsers().stream()
    .filter(u -> "admin".equals(u.getRole()))
    .findFirst()
    .orElseThrow();
```

### Nullable
```java
assertNull(result.getBody().getError(),
    "Поле 'error' должно быть null");
assertNotNull(result.getBody().getData(),
    "Поле 'data' не должно быть null");
```

## Несоответствие Swagger и API

Проверяй только поля, которые есть в swagger модели. Если реальный API возвращает больше полей — это проблема спецификации, а не тестов.

```java
// Проверяем только поля из swagger
assertEquals("success", result.getStatus(),
    "Статус ответа должен быть 'success'");

// TODO: Swagger модель не содержит поле 'metadata'
```

## Дополнительная информация

Подробности о сгенерированном коде и настройке:

- **[generate-resources.md](references/generate-resources.md)** — структура API клиентов и моделей
- **[openapi-generator.md](references/openapi-generator.md)** — настройка Gradle генерации