---
name: api-tests-swagger
description: "Напиши API тесты на Java/JUnit 5 используя сгенерированные OpenAPI клиенты. ВСЕГДА используй для: написать API тест, создать автотест REST endpoint, проверить HTTP метод, протестировать API, написать swagger тест, покрыть API тестами, integration тест REST API, добавить автотесты, проверить endpoint через executeAs(), использовать типизированные модели из lk3.model, Builder паттерн, JUnit Assertions вместо RestAssured body(). Если пользователь упоминает REST API, OpenAPI, Swagger, HTTP GET/POST/PUT/DELETE, автотесты API — используй этот навык."
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

assertEquals("success", result.getStatus());
```

**Как работает executeAs():**
- Принимает lambda с параметром `response` (тип `Response`)
- Внутри lambda мы цепочим `.then().statusCode(200).extract().response()`
- **Метод САМ десериализует ответ** в тип `GetUser200Response`
- Не используй `.body().as()` внутри executeAs!

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

```java
assertEquals("success", result.getStatus());
assertNotNull(result.getBody().getData());
assertTrue(result.getBody().getUsers().isEmpty());
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
    assertEquals("success", result.getStatus());
    assertNotNull(result.getBody());
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
        assertEquals("success", result.getStatus());
    });
}
```

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

assertEquals("success", result.getStatus());  // ✅ переменная результата

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

### Примитивы и объекты
```java
assertEquals("success", result.getStatus());
assertNotNull(result.getBody().getData());
assertEquals("John", result.getBody().getUser().getName());
```

### Collections
```java
assertEquals(5, result.getBody().getItems().size());
assertTrue(result.getBody().getTags().isEmpty());

// Поиск элемента
User user = result.getBody().getUsers().stream()
    .filter(u -> "admin".equals(u.getRole()))
    .findFirst()
    .orElseThrow();
```

### Nullable
```java
assertNull(result.getBody().getError());
assertNotNull(result.getBody().getData());
```

## Несоответствие Swagger и API

Проверяй только поля, которые есть в swagger модели. Если реальный API возвращает больше полей — это проблема спецификации, а не тестов.

```java
// Проверяем только поля из swagger
assertEquals("success", result.getStatus());

// TODO: Swagger модель не содержит поле 'metadata'
```

## Дополнительная информация

Подробности о сгенерированном коде и настройке:

- **[generate-resources.md](references/generate-resources.md)** — структура API клиентов и моделей
- **[openapi-generator.md](references/openapi-generator.md)** — настройка Gradle генерации