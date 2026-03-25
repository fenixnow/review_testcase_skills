# Сгенерированные OpenAPI ресурсы

## Структура генерируемых файлов

```
build/generate-resources/src/main/java/lk3/
├── api/                    # API клиенты (по тегам из swagger)
│   ├── AnalyticsApi.java
│   ├── InclusionsApi.java
│   ├── PromoApi.java
│   ├── AuthApi.java
│   └── ...
├── model/                  # Модели запросов/ответов
│   ├── ApiXxxGet200Response.java
│   ├── ApiXxxPostRequest.java
│   └── ...
├── ApiClient.java          # Базовый HTTP клиент
├── JacksonObjectMapper.java # Кастомный ObjectMapper
└── Oper.java               # Интерфейс операции
```

## Пакеты

| Пакет | Содержимое |
|-------|------------|
| `lk3.api` | API клиенты — по одному на тег из swagger |
| `lk3.model` | Все DTO модели — запросы и ответы |

## API Клиент (`lk3.api.*`)

### Структура класса API

Каждый файл соответствует тегу из OpenAPI спецификации:

```java
public class PromoApi {
    // Фабричный метод
    public static PromoApi promoApi(Supplier<RequestSpecBuilder> reqSpecSupplier) { ... }

    // Список всех операций данного API
    public List<Oper> getAllOperations() { ... }

    // Методы для получения операций
    public ApiPromoCreateGetOper apiPromoCreateGet() { ... }

    // Вложенный класс для каждой операции
    public static class ApiPromoCreateGetOper implements Oper { ... }
}
```

#### Метод `getAllOperations()`

Возвращает список всех операций (методов API), доступных в данном API клиенте:

```java
public List<Oper> getAllOperations()
```

**Что возвращает:** `List<Oper>` — список всех операций данного API

**Пример для `ProfileApi`:**
```java
profileApi(UserRole.SUPPLIER).getAllOperations()
// Возвращает:
// - ApiProfileClosingDocumentsExportGetOper
// - ApiProfileClosingDocumentsGetOper
// - ApiProfileEmailsNotificationGetOper
// - ApiProfileEmailsNotificationPatchOper
// - ApiProfileEmailsOrderGetOper
// - ApiProfileEmailsOrderPatchOper
// - ApiProfileGetOper
// - ApiProfileInformationGetOper
// - ApiProfileInformationImageGetOper
// - ApiProfileInformationPatchOper
// - GetProfilePasswordOper
// - UpdateProfilePasswordOper
```

**Методы интерфейса `Oper`:**
- `Method getReqMethod()` — HTTP метод операции
- `String getReqUri()` — URI эндпоинта
- `String getOperationId()` — ID операции (если задан)

### Класс операции (`Oper`)

Каждый метод API представлен вложенным классом `<MethodName>Oper`:

```java
public static class ApiPromoCreateGetOper implements Oper {
    // Константы
    public static final Method REQ_METHOD = GET;
    public static final String REQ_URI = "/api/promo/create";
    public static final String PROMO_ID_PATH = "promo";

    // Выполнение запроса
    @Step("И я выполняю метод GET /api/promo/create")
    public <T> T execute(Function<Response, T> handler) { ... }

    // Выполнение с десериализацией
    @Step("И я выполняю метод GET /api/promo/create")
    public ApiPromoCreateGet200Response executeAs(Function<Response, Response> handler) { ... }

    // Настройка запроса
    public ApiPromoCreateGetOper reqSpec(Consumer<RequestSpecBuilder>) { ... }

    // Настройка ответа
    public ApiPromoCreateGetOper respSpec(Consumer<ResponseSpecBuilder>) { ... }

    // Параметры
    public ApiPromoCreateGetOper promoIdPath(Object value) { ... }
    public ApiPromoCreateGetOper limitQuery(Object... value) { ... }
    public ApiPromoCreateGetOper body(Object value) { ... }
}
```

## Использование в тестах

### Базовый паттерн

```java
import lk3.api.PromoApi;
import lk3.model.ApiPromoCreateGet200Response;
import java.util.function.Function;

// Получение API клиента из BaseTest
ApiPromoCreateGet200Response response = promoApi(UserRole.SUPPLIER)
    .apiPromoCreateGet()
    .respSpec(spec -> spec.expectStatusCode(200))
    .executeAs(Function.identity());
```

### Настройка параметров

| Тип параметра | Метод | Пример |
|---------------|-------|--------|
| Path | `<param>Path(value)` | `.promoIdPath(123L)` |
| Query | `<param>Query(value)` | `.limitQuery(10)` |
| Header | `<param>Header(value)` | `.authorizationHeader("Bearer token")` |
| Form | `<param>Form(value)` | `.usernameForm("john")` |
| Body | `.body(object)` | `.body(requestObject)` |

### Методы выполнения

**`execute()`** — возвращает `Response` для ручной обработки:

```java
Response response = promoApi(UserRole.SUPPLIER)
    .apiPromoCreateGet()
    .execute(r -> r);

String json = response.asString();
```

**`executeAs()`** — десериализует ответ в типизированную модель:

```java
ApiPromoCreateGet200Response response = promoApi(UserRole.SUPPLIER)
    .apiPromoCreateGet()
    .executeAs(Function.identity());
```

### Настройка спецификаций

**RequestSpec** — настройка запроса:

```java
.apiPromoCreateGet()
    .reqSpec(spec -> spec
        .addHeader("X-Custom", "value")
        .setContentType("application/json"))
```

**ResponseSpec (respSpec)** — настройка ожиданий ответа:

```java
.apiPromoCreateGet()
    .respSpec(spec -> spec
        .expectStatusCode(200)
        .expectStatusLine("HTTP/1.1 200 OK"))
```

## Модели (`lk3.model.*`)

### Именование моделей

```
Api<Endpoint><Method><StatusCode>Response    // Ответы
Api<Endpoint><Method>Request                  // Запросы
```

Примеры:
- `ApiPromoCreateGet200Response` — GET /api/promo/create → 200
- `ApiPromoSavePromoPostRequest` — POST /api/promo → тело запроса

### Структура ответа

```java
public class ApiPromoCreateGet200Response {
    private String status;           // "success" / "error"
    private String message;          // Сообщение
    private ApiPromoCreateGet200ResponseBody body;  // Данные

    // Геттеры (и сеттеры если не Builder)
    public String getStatus() { return status; }
    public ApiPromoCreateGet200ResponseBody getBody() { return body; }
}
```

### Создание запросов через Builder

```java
ApiPromoSavePromoPostRequest request = ApiPromoSavePromoPostRequest.builder()
    .action("next")
    .body(ApiPromoSavePromoPostRequestBody.builder()
        .name("Test Promo")
        .startDate("2025-01-01")
        .build())
    .build();
```

## Специальные классы

### `JacksonObjectMapper`

Кастомный ObjectMapper для десериализации ответов. Используется внутри API клиентов.

### `ResponseSpecBuilders`

Утилитный класс для создания `ResponseSpecBuilder` с преднастройками.

### `Oper`

Интерфейс, реализуемый всеми классами операций. Используется для полиморфной работы с разными операциями.