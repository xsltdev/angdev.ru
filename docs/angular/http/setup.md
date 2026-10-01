---
description: "Начиная с версии 21 клиент HTTP доступен для инъекции по умолчанию"
---

# Настройка `HttpClient` {: #setting-up-httpclient}

:date: 30.09.2026

Начиная с Angular v21 сервис `HttpClient` доступен для инъекции по умолчанию.

## Провайдер `HttpClient` через инъекцию зависимостей {: #providing-httpclient-through-dependency-injection}

Функция `provideHttpClient` задаёт набор возможностей HTTP по умолчанию или добавляет возможности в `providers` приложения в `app.config.ts`.

```ts
export const appConfig: ApplicationConfig = {
  providers: [provideHttpClient(/* add features here, such as withInterceptors(...) */)],
};
```

Если приложение стартует через NgModule, `provideHttpClient` добавляют в `providers` корневого NgModule — так же настраивается набор возможностей по умолчанию или дополнительные возможности:

```ts
@NgModule({
  providers: [provideHttpClient(/* add features here, such as withInterceptors(...) */)],
  // ... other application configuration
})
export class AppModule {}
```

Дальше `HttpClient` внедряется в компоненты, сервисы и другие классы:

```ts
@Service()
export class ConfigService {
  private http = inject(HttpClient);
  // This service can now make HTTP requests via `this.http`.
}
```

## Настройка возможностей `HttpClient` {: #configuring-features-of-httpclient}

`provideHttpClient` принимает список необязательных настроек: ими включают или меняют отдельные стороны клиента. Ниже — эти возможности и как ими пользоваться.

### `withXhr` {: #withxhr}

```ts
export const appConfig: ApplicationConfig = {
  providers: [provideHttpClient(withXhr())],
};
```

По умолчанию `HttpClient` ходит в сеть через API [`fetch`](https://developer.mozilla.org/docs/Web/API/Fetch_API). `withXhr` переключает клиент на [`XMLHttpRequest`](https://developer.mozilla.org/docs/Web/API/XMLHttpRequest).

`fetch` — более современный API, и он есть в средах, где `XMLHttpRequest` не поддерживается. У него есть ограничения: например, он не отдаёт события прогресса выгрузки.

!!! danger "Не используйте `withXhr` при серверном рендеринге (SSR)"

    Поддержка XHR на сервере **устарела** и её уберут в Angular 23. Библиотека `xhr2` небезопасно обрабатывает перенаправления: она может переслать заголовки `Authorization` при кросс-доменном редиректе и уязвима к отказу в обслуживании (DoS) через циклы перенаправлений. В SSR-приложениях оставляйте серверную часть `fetch` по умолчанию.

### `withInterceptors(...)` {: #withinterceptors}

`withInterceptors` задаёт набор функций-перехватчиков, через которые проходят запросы `HttpClient`. Подробнее — в [руководстве по перехватчикам](interceptors.md).

### `withInterceptorsFromDi()` {: #withinterceptorsfromdi}

`withInterceptorsFromDi` подключает прежний вид перехватчиков — классы из инъекции зависимостей. Подробнее — в [руководстве по перехватчикам](interceptors.md).

!!! tip ""

    У функциональных перехватчиков (через `withInterceptors`) порядок предсказуемее. Берите их вместо перехватчиков на DI.

### `withRequestsMadeViaParent()` {: #withrequestsmadeviaparent}

По умолчанию `provideHttpClient` в данном инжекторе перекрывает настройку `HttpClient` родительского инжектора.

С `withRequestsMadeViaParent()` запрос после локальных перехватчиков уходит в экземпляр `HttpClient` родительского инжектора. Так в дочернем инжекторе добавляют свои перехватчики и при этом сохраняют перехватчики родителя.

!!! danger ""

    Выше текущего инжектора уже должен быть настроен экземпляр `HttpClient`. Иначе параметр недопустим, и при обращении к нему будет ошибка во время выполнения.

### `withJsonpSupport()` {: #withjsonpsupport}

`withJsonpSupport` включает метод `.jsonp()` у `HttpClient`: GET-запрос по [соглашению JSONP](https://en.wikipedia.org/wiki/JSONP) для загрузки данных с другого домена.

!!! tip ""

    Для кросс-доменных запросов по возможности берите [CORS](https://developer.mozilla.org/docs/Web/HTTP/CORS), а не JSONP.

### `withXsrfConfiguration(...)` {: #withxsrfconfiguration}

Этот параметр настраивает встроенную защиту `HttpClient` от XSRF. Подробнее — в [руководстве по безопасности](../security.md).

### `withNoXsrfProtection()` {: #withnoxsrfprotection}

Этот параметр отключает встроенную защиту `HttpClient` от XSRF. Подробнее — в [руководстве по безопасности](../security.md).

## Настройка через `HttpClientModule` {: #httpclientmodule-based-configuration}

Часть приложений настраивает `HttpClient` старым API на NgModule.

В таблице — NgModule из `@angular/common/http` и соответствующие им функции провайдеров.

| **NgModule**                            | Эквивалент `provideHttpClient()`                     |
| --------------------------------------- | ---------------------------------------------------- |
| `HttpClientModule`                      | `provideHttpClient(withInterceptorsFromDi(), withXhr())` |
| `HttpClientJsonpModule`                 | `withJsonpSupport()`                                 |
| `HttpClientXsrfModule.withOptions(...)` | `withXsrfConfiguration(...)`                         |
| `HttpClientXsrfModule.disable()`        | `withNoXsrfProtection()`                             |

!!! warning "Осторожно с `HttpClientModule` в нескольких инжекторах"

    Если `HttpClientModule` есть в нескольких инжекторах, поведение перехватчиков определено плохо и зависит от точных параметров и порядка провайдеров и импортов.

    Для конфигурации с несколькими инжекторами берите `provideHttpClient`: поведение стабильнее. Смотрите возможность `withRequestsMadeViaParent` выше.


---

Источник: [https://angular.dev/guide/http/setup](https://angular.dev/guide/http/setup)
