# Работа с тест-кейсами Allure TestOps

Когда пользователь просит написать API тест **по тест-кейсу** из Allure TestOps.

## Важное понимание: Тест-кейс vs Автотест

**Критически важно понимать relationship между тест-кейсом и автотестом:**

- **Тест-кейс** — первичный источник истины (бизнес-требование)
- **Автотест** — техническая реализация проверки этого требования

Если автотест соответствует тест-кейсу — это **не доказательство** того, что тест-кейс правильный. Это лишь означает, что автотест правильно реализует то, что описано в тест-кейсе (даже если в тест-кейсе есть ошибки).

**Пример:**
- Тест-кейс может упускать важные граничные случаи
- Автотест будет проходить, но не покроет все сценарии
- Нужна **ручная проверка** тест-кейса на полноту бизнес-сценариев

**Следствия при написании автотестов:**
- ✅ Автотест должен **точно реализовывать** то, что описано в тест-кейсе
- ✅ Если в тест-кейсе есть пробелы — не добавляй их в автотест без обсуждения
- ✅ Сначала убедись, что тест-кейс **полностью покрывает** бизнес-сценарий
- ❌ Не полагайся на автотесты как на источник бизнес-требований

**Когда пользователь просит "написать автотест по тест-кейсу":**
1. Проанализируй тест-кейс на **полноту** покрытия сценария
2. Если найдёшь пробелы — **укажи на них** пользователю
3. Только после утверждения — реализуй автотест

## ⚠️ КРИТИЧЕСКО: Учёт Precondition

**Большая ошибка:** Пропускать preconditions из тест-кейса → автотест упадёт!

### Алгоритм анализа Precondition

Сопоставь каждый precondition с параметром запроса:

| Precondition | Влияет на | Как реализовать в коде |
|--------------|-----------|------------------------|
| Пользователь авторизован | RequestSpec | Используй `catalogApiWithIntegrationToken()` или `.header("x-integration-token", TOKEN)` |
| **Эксперимент/фича включён** | **ЗАГОЛОВОК запроса** | **`.header("x-vkusvill-ab-tests", "experiment=B")` — ⚠️ ЯВНО!** |
| Номер карты | Path/Query параметр | `.numberQuery(NUMBER)` из BaseTest |
| Товары существуют | Query параметр | `.productIdQuery(39813)` — конкретный ID |
| Пользователь НЕ авторизован | RequestSpec | Используй метод БЕЗ токена |

**КРИТИЧЕСКОЕ ПРАВИЛО:** Эксперименты и фичи из Precondition ДОЛЖНЫ быть переданы в запросе ЯВНО через `.header()`!

### Распространённые ошибки

❌ **Ошибка: Забыл заголовок эксперимента из Precondition**

```java
// ❌ НЕПРАВИЛЬНО
// Precondition: Эксперимент B включён
List<Product> result = catalogApi()
    .method()
    .executeAs(...);  // Эксперимент B НЕ включён! Тест упадёт!

// ✅ ПРАВИЛЬНО
List<Product> result = catalogApi()
    .method()
    .executeAs(response -> response
        .then()
        .header("x-vkusvill-ab-tests", "catalog/exp=B")  // Из precondition!
        .statusCode(200)
        ...
    );
```

❌ **Ошибка: Не все параметры из шага добавлены**

```java
// В тест-кейсе: number, source=4, show_kbju=1, product_id
// ❌ Забыл source=4
api.method()
    .numberQuery(number)
    .showKbjuQuery(1)
    .productIdQuery(id);

// ✅ Все параметры
api.method()
    .numberQuery(number)
    .sourceQuery(4)          // Добавлено!
    .showKbjuQuery(1)
    .productIdQuery(id);
```

## Чек-лист соответствия тест-кейсу

Перед завершением автотеста ПРОВЕРЬ:

**Precondition:**
- [ ] Авторизация: правильный RequestSpec?
- [ ] **Эксперименты/фичи: добавлены как `.header()`?**
- [ ] Номер карты: передаётся явно?
- [ ] Товары: существующий ID?

**Параметры запроса из шага:**
- [ ] **ВСЕ query-параметры добавлены?**
- [ ] **ВСЕ заголовки добавлены?**
- [ ] Типы данных соответствуют Swagger?

**Ожидаемый результат:**
- [ ] HTTP статус проверяется?
- [ ] Структура ответа проверяется?
- [ ] **ВСЕ критичные поля проверяются?**

## Пример полного цикла: Тест-кейс → Автотест

**Тест-кейс:**
```
Precondition:
- Эксперимент catalog/exp = B
- Пользователь авторизован

Шаг:
- Отправить GET /api/product/properties с:
  - number={NUMBER}
  - source=4
  - product_id=123

Expected:
- HTTP 200
- Поле "consist" отсутствует
```

**Автотест:**
```java
@Test
@DisplayName("Проверка отсутствия consist при эксперименте B")
@AllureId("72613")
void getProductPropertiesWithoutConsist() {
    // ✅ Precondition → Авторизация через RequestSpec
    // ✅ Precondition → Эксперимент B через header

    ProductPropertiesResult result = catalogApiWithIntegrationToken()
        .integrationsProductPropertiesForSiteGet()
        .numberQuery(NUMBER)        // ✅ Из шага
        .sourceQuery(4)             // ✅ Из шага
        .productIdQuery(123)        // ✅ Из шага
        .executeAs(response -> response
            .then()
            .header("x-vkusvill-ab-tests", "catalog/exp=B")  // ✅ Из precondition!
            .statusCode(200)        // ✅ Из expected
            .extract()
            .response());

    // ✅ Expected result → Assertions
    step("И я проверяю отсутствие поля consist", () -> {
        assertNotNull(result,
            "Результат не должен быть null");
        result.forEach(property -> {
            assertNull(property.getConsist(),
                "Поле 'consist' должно отсутствовать");
        });
    });
}
```
