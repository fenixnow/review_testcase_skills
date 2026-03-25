# OpenAPI Generator Gradle настройка

## Плагин

```groovy
plugins {
    id "org.openapi.generator" version "7.20.0"
}

import org.openapitools.generator.gradle.plugin.tasks.GenerateTask
```

## Структура таски

```groovy
tasks.register("openApiGenerate", GenerateTask) {
    group = "openapi tools"

    // === Основные настройки ===
    apiPackage.set("lk3.api")
    modelPackage.set("lk3.model")
    generatorName = "java"
    library = "rest-assured"

    // === Пути ===
    outputDir.set("$buildDir/generate-resources")
    inputSpec.set("$rootDir/downloads/api-docs.yaml")
    inputSpecRootDirectory.set("$rootDir/downloads")

    // === Генерация ===
    generateApiDocumentation.set(false)
    generateModelDocumentation.set(false)
    generateApiTests.set(false)
    generateModelTests.set(false)

    // === Шаблоны ===
    templateDir.set("$rootDir/src/test/resources/openapi-templates")

    // === Конфигурация ===
    configOptions.set([
        dateLibrary: 'java8',
        serializationLibrary: 'jackson',
        useJakartaEe: 'true',
        generateBuilders: 'true',
        useOneOfInterfaces: 'true',
        openApiNullable: 'false'
    ])
}
```

## Обязательные параметры

| Параметр | Значение | Описание |
|----------|----------|----------|
| `generatorName` | `"java"` | Язык генерации |
| `library` | `"rest-assured"` | HTTP библиотека для тестов |
| `apiPackage` | `"lk3.api"` | Пакет для API клиентов |
| `modelPackage` | `"lk3.model"` | Пакет для моделей |
| `generateBuilders` | `'true'` | Генерировать Builder для моделей |
| `useJakartaEe` | `'true'` | Использовать Jakarta EE (вместо javax) |
| `serializationLibrary` | `'jackson'` | Библиотека сериализации |

## Важные параметры

### Генерация кода vs документации

```groovy
generateApiDocumentation.set(false)   // НЕ генерировать JavaDoc для API
generateModelDocumentation.set(false)  // НЕ генерировать JavaDoc для моделей
generateApiTests.set(false)            // НЕ генерировать тесты
generateModelTests.set(false)          // НЕ генерировать тесты для моделей
```

### Работа с многомодульной спецификацией

```groovy
inputSpec.set("$rootDir/downloads/api-docs.yaml")           // Главный файл
inputSpecRootDirectory.set("$rootDir/downloads")            // Папка с $ref
inputSpecRootDirectorySkipMerge.set(true)                   // НЕ мердить файлы
```

### Шаблоны кастомизации

```groovy
templateDir.set("$rootDir/src/test/resources/openapi-templates")
```

Позволяет переопределить шаблоны генерации. Основные файлы:
- `api.mustache` — шаблон для API клиентов
- `model.mustache` — шаблон для моделей

### Фильтрация генерируемых файлов

```groovy
ignoreFileOverride.set(".openapi-generator-java-sources.ignore")
```

Файл содержит список шаблонов файлов для исключения из генерации:
```
ApiClient.java
StringUtil.java
```

## configOptions — ключевые настройки

| Опция | Значение | Зачем |
|-------|----------|-------|
| `dateLibrary` | `'java8'` | Использовать java.time вместо Date |
| `generateBuilders` | `'true'` | Builder для моделей (обязательно!) |
| `useOneOfInterfaces` | `'true'` | Интерфейсы для oneOf/anyOf |
| `openApiNullable` | `'false'` | НЕ генерировать @Nullable |
| `useJakartaEe` | `'true'` | Jakarta вместо javax |
| `serializationLibrary` | `'jackson'` | Jackson для JSON |

## Автоматическая генерация

```groovy
// Генерация перед компиляцией тестов
compileTestJava.dependsOn("openApiGenerate")

// Добавить сгенерированные исходники в sourceSets
sourceSets {
    test {
        java {
            srcDir('build/generate-resources/src/main/java')
        }
    }
}
```

## Пример полной конфигурации

```groovy
tasks.register("openApiLk3Generate", GenerateTask) {
    group = "openapi tools"

    // Пакеты
    apiPackage.set("lk3.api")
    modelPackage.set("lk3.model")
    apiNameSuffix.set("Api")

    // Генератор
    generatorName = "java"
    library = "rest-assured"

    // Пути
    outputDir.set("$buildDir/generate-resources")
    inputSpec.set("$rootDir/downloads/laravel-app/api-docs/api-docs.yaml")
    inputSpecRootDirectory.set("$rootDir/downloads/laravel-app/api-docs")
    inputSpecRootDirectorySkipMerge.set(true)

    // Что НЕ генерировать
    generateApiDocumentation.set(false)
    generateModelDocumentation.set(false)
    generateApiTests.set(false)
    generateModelTests.set(false)
    logToStderr.set(true)
    validateSpec.set(false)  // Валидация отдельно

    // Игнорируемые файлы
    ignoreFileOverride.set(".openapi-generator-java-sources.ignore")

    // Шаблоны
    templateDir.set("$rootDir/src/test/resources/openapi-templates")

    // Конфигурация генерации
    configOptions.set([
        dateLibrary: 'java8',
        serializationLibrary: 'jackson',
        useJakartaEe: 'true',
        generateBuilders: 'true',
        useOneOfInterfaces: 'true',
        openApiNullable: 'false'
    ])

    // Зависимости
    dependsOn("postProcessingFolder")
}
```

## Зависимости для работы сгенерированного кода

```groovy
dependencies {
    // RestAssured
    testImplementation "io.rest-assured:rest-assured:5.5.0"

    // Jackson
    implementation "com.fasterxml.jackson.core:jackson-databind:2.15.2"
    implementation "com.fasterxml.jackson.datatype:jackson-datatype-jsr310:2.15.2"
    implementation 'org.openapitools:jackson-databind-nullable:0.2.8'

    // Jakarta
    testImplementation "jakarta.annotation:jakarta.annotation-api:2.1.1"
}
```

## Полезные команды

```bash
# Сгенерировать клиенты
./gradlew openApiLk3Generate

# Перегенерировать (чистая генерация)
./gradlew clean openApiLk3Generate

# Посмотреть что сгенерится без генерации
./gradlew openApiLk3Generate --dry-run
```