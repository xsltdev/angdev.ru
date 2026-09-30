---
description: "Клиент HTTP поддерживает промежуточный слой перехватчиков для повторов, кэша, журнала и аутентификации"
---

# Перехватчики {: #interceptors}

:date: 30.09.2026

`HttpClient` поддерживает разновидность промежуточного слоя — _перехватчики_.

Коротко: перехватчики выносят из отдельных запросов общие приёмы — повтор, кэш, журнал и аутентификацию.

У `HttpClient` два вида перехватчиков: функциональные и на инъекции зависимостей. Лучше функциональные: их поведение предсказуемее, особенно в сложной конфигурации. Примеры в этом руководстве — функциональные. [Перехватчики на DI](#di-based-interceptors) разобраны в конце.

## Перехватчики {: #interceptors-1}

Перехватчик — это обычно функция, которая выполняется для каждого запроса и может менять содержимое и ход запроса и ответа. Несколько перехватчиков образуют цепочку: каждый обрабатывает запрос или ответ и передаёт его следующему.

На перехватчиках собирают типичные сценарии:

-   Заголовок аутентификации у исходящих запросов к конкретному API.
-   Повтор неудачных запросов с экспоненциальной задержкой.
-   Кэш ответов на время или до сброса мутациями.
-   Свой разбор ответов.
-   Замер и запись времени ответа сервера.
-   Элементы интерфейса вроде индикатора загрузки, пока идёт сеть.
-   Сбор и пакетирование запросов за заданный промежуток времени.
-   Автоматический срыв запроса по настраиваемому сроку или таймауту.
-   Регулярный опрос сервера и обновление результатов.

## Объявление перехватчика {: #defining-an-interceptor}

Базовая форма — функция, которая получает исходящий `HttpRequest` и функцию `next`, следующий шаг цепочки.

Например, `loggingInterceptor` пишет URL исходящего запроса в `console.log` и передаёт запрос дальше:

```ts
export function loggingInterceptor(
  req: HttpRequest<unknown>,
  next: HttpHandlerFn,
): Observable<HttpEvent<unknown>> {
  console.log(req.url);
  return next(req);
}
```

Чтобы перехватчик реально видел запросы, его нужно подключить к `HttpClient`.

## Подключение перехватчиков {: #configuring-interceptors}

Набор перехватчиков задаётся при настройке `HttpClient` через инъекцию зависимостей, функцией `withInterceptors`:

```ts
bootstrapApplication(App, {
  providers: [provideHttpClient(withInterceptors([loggingInterceptor, cachingInterceptor]))],
});
```

Перехватчики сцепляются в том порядке, в каком они перечислены в провайдерах. В примере выше `loggingInterceptor` обрабатывает запрос и передаёт его в `cachingInterceptor`.

### События ответа {: #intercepting-response-events}

Перехватчик может преобразовать поток `Observable` из `HttpEvent`, который вернул `next`, чтобы прочитать или изменить ответ. В потоке все события ответа, поэтому итоговый объект ответа часто отличают по `.type`.

```ts
export function loggingInterceptor(
  req: HttpRequest<unknown>,
  next: HttpHandlerFn,
): Observable<HttpEvent<unknown>> {
  return next(req).pipe(
    tap((event) => {
      if (event.type === HttpEventType.Response) {
        console.log(req.url, 'returned a response with status', event.status);
      }
    }),
  );
}
```

!!! tip ""

    Ответ естественно связан с исходящим запросом: перехватчик преобразует поток ответа в замыкании, которое захватило объект запроса.

## Изменение запросов {: #modifying-requests}

Большинство свойств экземпляров `HttpRequest` и `HttpResponse` _неизменяемы_, и перехватчик не может поменять их на месте. Мутации делают через клон `.clone()`, указывая, какие свойства должны отличаться в новом экземпляре. Само значение при этом тоже обновляют неизменяемо (как `HttpHeaders` или `HttpParams`).

Например, чтобы добавить заголовок:

```ts
const reqWithHeader = req.clone({
  headers: req.headers.set('X-New-Header', 'new header value'),
});
```

Из-за неизменяемости большинство перехватчиков идемпотентны, если один и тот же `HttpRequest` проходит цепочку несколько раз. Так бывает, в частности, при повторе запроса после ошибки.

!!! danger ""

    Тело запроса или ответа **не** защищено от глубокой мутации. Если перехватчику нужно менять тело, учитывайте, что он может выполниться на одном запросе несколько раз.

## Инъекция зависимостей в перехватчиках {: #dependency-injection-in-interceptors}

Перехватчики выполняются в _контексте инъекции_ того инжектора, который их зарегистрировал, и могут получать зависимости через [`inject`](https://angular.dev/api/core/inject).

Допустим, в приложении есть сервис `AuthService`, который выдаёт токены для исходящих запросов. Перехватчик внедряет его и пользуется им:

```ts
export function authInterceptor(req: HttpRequest<unknown>, next: HttpHandlerFn) {
  // Inject the current `AuthService` and use it to get an authentication token:
  const authToken = inject(AuthService).getAuthToken();

  // Clone the request to add the authentication header.
  const newReq = req.clone({
    headers: req.headers.append('X-Authentication-Token', authToken),
  });
  return next(newReq);
}
```

## Метаданные запроса и ответа {: #request-and-response-metadata}

Часто в запрос нужно вложить сведения, которые не уходят на сервер, а предназначены перехватчикам. У `HttpRequest` есть объект `.context`: он хранит такие метаданные как экземпляр `HttpContext`. Это типизированная карта с ключами типа `HttpContextToken`.

Ниже метаданные решают, включён ли перехватчик кэша для конкретного запроса.

### Токены контекста {: #defining-context-tokens}

Чтобы в карте `.context` запроса хранить, должен ли перехватчик кэша сохранять этот запрос, заводят ключ `HttpContextToken`:

```ts
export const CACHING_ENABLED = new HttpContextToken<boolean>(() => true);
```

Переданная функция создаёт значение токена по умолчанию для запросов, которые его явно не задали. Функция нужна, чтобы при значении-объекте или массиве у каждого запроса был свой экземпляр.

### Чтение токена в перехватчике {: #reading-the-token-in-an-interceptor}

Перехватчик читает токен и по значению решает, применять ли логику кэша:

```ts
export function cachingInterceptor(req: HttpRequest<unknown>, next: HttpHandlerFn): Observable<HttpEvent<unknown>> {
  if (req.context.get(CACHING_ENABLED)) {
    // apply caching logic
    return ...;
  } else {
    // caching has been disabled for this request
    return next(req);
  }
}
```

### Токены контекста при запросе {: #setting-context-tokens-when-making-a-request}

В запросе через API `HttpClient` можно передать значения `HttpContextToken`:

```ts
const data$ = http.get('/sensitive/data', {
  context: new HttpContext().set(CACHING_ENABLED, false),
});
```

Перехватчики читают эти значения из `HttpContext` запроса.

### Контекст запроса изменяем {: #the-request-context-is-mutable}

В отличие от остальных свойств `HttpRequest`, связанный `HttpContext` _изменяем_. Если перехватчик меняет контекст запроса, который потом повторяют, тот же перехватчик увидит изменение при следующем запуске. Так между повторами передают состояние, если оно нужно.

## Синтетические ответы {: #synthetic-responses}

Большинство перехватчиков просто вызывает обработчик `next`, преобразуя запрос или ответ, но это не обязательное требование. Ниже — способы, которыми перехватчик добавляет более сложное поведение.

Вызывать `next` не обязательно. Ответ можно собрать иначе: из кэша или отправив запрос другим механизмом.

Ответ собирают конструктором `HttpResponse`:

```ts
const resp = new HttpResponse({
  body: 'response body',
});
```

## Сведения о перенаправлении {: #working-with-redirect-information}

Когда `HttpClient` работает через серверную часть fetch, у ответа есть свойство `redirected`: ответ получен в результате перенаправления. Свойство совпадает со спецификацией Fetch API и пригождается в перехватчиках, которые обрабатывают редиректы.

Перехватчик читает сведения о перенаправлении и действует по ним:

```ts
export function redirectTrackingInterceptor(
  req: HttpRequest<unknown>,
  next: HttpHandlerFn,
): Observable<HttpEvent<unknown>> {
  return next(req).pipe(
    tap((event) => {
      if (event.type === HttpEventType.Response && event.redirected) {
        console.log('Request to', req.url, 'was redirected to', event.url);
        // Handle redirect logic - maybe update analytics, security checks, etc.
      }
    }),
  );
}
```

По тем же сведениям в перехватчике строят условную логику:

```ts
export function authRedirectInterceptor(
  req: HttpRequest<unknown>,
  next: HttpHandlerFn,
): Observable<HttpEvent<unknown>> {
  return next(req).pipe(
    tap((event) => {
      if (event.type === HttpEventType.Response && event.redirected) {
        // Check if we were redirected to a login page
        if (event.url?.includes('/login')) {
          // Handle authentication redirect
          handleAuthRedirect();
        }
      }
    }),
  );
}
```

## Типы ответа {: #working-with-response-types}

Когда `HttpClient` работает через серверную часть fetch, у ответа есть свойство `type`: как браузер обработал ответ с учётом политики CORS и режима запроса. Свойство совпадает со спецификацией Fetch API и помогает разбирать проблемы CORS и доступность ответа.

У свойства `type` ответа бывают такие значения:

-   `'basic'` — ответ того же источника, все заголовки доступны
-   `'cors'` — кросс-доменный ответ с корректно настроенными заголовками CORS
-   `'opaque'` — кросс-доменный ответ без CORS, заголовки и тело могут быть ограничены
-   `'opaqueredirect'` — ответ перенаправленного запроса в режиме no-cors
-   `'error'` — произошла сетевая ошибка

Перехватчик использует тип ответа, чтобы разбирать CORS и обрабатывать ошибки:

```ts
export function responseTypeInterceptor(
  req: HttpRequest<unknown>,
  next: HttpHandlerFn,
): Observable<HttpEvent<unknown>> {
  return next(req).pipe(
    map((event) => {
      if (event.type === HttpEventType.Response) {
        // Handle different response types appropriately
        switch (event.responseType) {
          case 'opaque':
            // Limited access to response data
            console.warn('Limited response data due to CORS policy');
            break;
          case 'cors':
          case 'basic':
            // Full access to response data
            break;
          case 'error':
            // Handle network errors
            console.error('Network error in response');
            break;
        }
      }
    }),
  );
}
```

## Перехватчики на DI {: #di-based-interceptors}

`HttpClient` также поддерживает перехватчики в виде внедряемых классов, которые настраиваются через DI. Возможности те же, что у функциональных перехватчиков, отличается механизм настройки.

Перехватчик на DI — внедряемый класс с интерфейсом `HttpInterceptor`:

```ts
@Injectable()
export class LoggingInterceptor implements HttpInterceptor {
  intercept(req: HttpRequest<any>, handler: HttpHandler): Observable<HttpEvent<any>> {
    console.log('Request URL: ' + req.url);
    return handler.handle(req);
  }
}
```

Такие перехватчики подключают мультипровайдером инъекции зависимостей:

```ts
bootstrapApplication(App, {
  providers: [
    provideHttpClient(
      // DI-based interceptors must be explicitly enabled.
      withInterceptorsFromDi(),
    ),

    {provide: HTTP_INTERCEPTORS, useClass: LoggingInterceptor, multi: true},
  ],
});
```

Перехватчики на DI выполняются в порядке регистрации провайдеров. В приложении с обширной иерархической конфигурацией DI этот порядок трудно предсказать.


---

Источник: [https://angular.dev/guide/http/interceptors](https://angular.dev/guide/http/interceptors)
