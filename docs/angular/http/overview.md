---
description: "Приложению нужен обмен с сервером по протоколу HTTP, чтобы скачивать и отправлять данные и вызывать серверные сервисы"
---

# Обмен данными с серверными сервисами по HTTP {: #understanding-communication-with-backend-services-using-http}

:date: 30.09.2026

Большинству фронтенд-приложений нужно общаться с сервером по протоколу HTTP: скачивать и отправлять данные и обращаться к другим серверным сервисам. В Angular для этого есть клиентский HTTP API — класс сервиса `HttpClient` из `@angular/common/http`.

## Возможности HTTP-клиента {: #http-client-service-features}

HTTP-клиент даёт следующее:

-   Запрос [типизированных значений ответа](making-requests.md#fetching-json-data)
-   Удобную [обработку ошибок](making-requests.md#handling-request-failure)
-   [Перехват](interceptors.md) запросов и ответов
-   Надёжные [утилиты для тестов](https://angular.dev/guide/http/testing)

## Что дальше {: #whats-next}

-   [Настройка `HttpClient`](setup.md)
-   [HTTP-запросы](making-requests.md)


---

Источник: [https://angular.dev/guide/http](https://angular.dev/guide/http)
