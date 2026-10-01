---
description: "Методы клиента HTTP соответствуют глаголам протокола и возвращают поток, который отправляет запрос при подписке"
---

# HTTP-запросы {: #making-http-requests}

:date: 30.09.2026

У `HttpClient` есть методы под разные HTTP-глаголы: ими и загружают данные, и меняют состояние на сервере. Каждый метод возвращает [RxJS `Observable`](https://rxjs.dev/guide/observable). Подписка отправляет запрос, а когда сервер отвечает, `Observable` отдаёт результат.

!!! info ""

    На `Observable`, который создал `HttpClient`, можно подписаться сколько угодно раз. Каждая подписка делает новый запрос к серверу.

Объект параметров, который передают методу запроса, меняет свойства запроса и тип возвращаемого ответа.

## Загрузка JSON {: #fetching-json-data}

Данные с сервера чаще всего забирают GET-запросом через [`HttpClient.get()`](https://angular.dev/api/common/http/HttpClient#get). У метода два аргумента: строка URL, откуда читать, и _необязательный объект параметров_ запроса.

Например, конфигурация с условного API через `HttpClient.get()`:

```ts
http.get<Config>('/api/config').subscribe((config) => {
  // process the configuration.
});
```

Обобщённый аргумент типа говорит, что сервер вернёт данные типа `Config`. Аргумент необязателен: без него тип данных — `Object`.

!!! tip ""

    Если структура данных неясна и в ней бывают `undefined` или `null`, в качестве типа ответа берите `unknown`, а не `Object`.

!!! danger ""

    Обобщённый тип методов запроса — это **утверждение** о данных, которые вернул сервер. `HttpClient` не проверяет, что фактические данные совпадают с этим типом.

## Другие типы данных {: #fetching-other-types-of-data}

По умолчанию `HttpClient` считает, что сервер вернёт JSON. Для API не на JSON при запросе указывают ожидаемый тип ответа параметром `responseType`.

| **Значение `responseType`** | **Тип ответа**                                                                                                                |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `'json'` (по умолчанию)       | JSON-данные указанного обобщённого типа                                                                                                       |
| `'text'`                 | строка                                                                                                                               |
| `'arraybuffer'`          | [`ArrayBuffer`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/ArrayBuffer) с сырыми байтами ответа |
| `'blob'`                 | экземпляр [`Blob`](https://developer.mozilla.org/docs/Web/API/Blob)                                                                        |

Например, сырые байты изображения `.jpeg` можно скачать в `ArrayBuffer`:

```ts
http.get('/images/dog.jpg', {responseType: 'arraybuffer'}).subscribe((buffer) => {
  console.log('The image is ' + buffer.byteLength + ' bytes large');
});
```

!!! warning "Литерал для `responseType`"

    Значение `responseType` влияет на тип, который возвращает `HttpClient`, поэтому это должен быть литеральный тип, а не `string`.

    Так получается само, если объект параметров — литерал. Если параметры вынесены в переменную или вспомогательный метод, литерал задают явно, например `responseType: 'text' as const`.

## Изменение состояния на сервере {: #mutating-server-state}

API, которые меняют состояние, часто ждут POST с телом: новое состояние или описание изменения.

Метод [`HttpClient.post()`](https://angular.dev/api/common/http/HttpClient#post) устроен как `get()`, но перед параметрами принимает дополнительный аргумент `body`:

```ts
http.post<Config>('/api/config', newConfig).subscribe((config) => {
  console.log('Updated config:', config);
});
```

В `body` можно передать значения разных типов, и `HttpClient` сериализует их соответственно:

| **Тип `body`**                                                                                                               | **Сериализация**                                    |
| ----------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| string                                                                                                                        | обычный текст                                           |
| number, boolean, array или обычный объект                                                                                       | JSON                                                 |
| [`ArrayBuffer`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/ArrayBuffer)                       | сырые данные из буфера                             |
| [`Blob`](https://developer.mozilla.org/docs/Web/API/Blob)                                                                     | сырые данные с типом содержимого `Blob`              |
| [`FormData`](https://developer.mozilla.org/docs/Web/API/FormData)                                                             | данные в кодировке `multipart/form-data`                   |
| [`HttpParams`](https://angular.dev/api/common/http/HttpParams) или [`URLSearchParams`](https://developer.mozilla.org/docs/Web/API/URLSearchParams) | строка в формате `application/x-www-form-urlencoded` |

!!! warning ""

    Чтобы мутирующий запрос реально ушёл, на его `Observable` нужно вызвать `.subscribe()`.

## Параметры URL {: #setting-url-parameters}

Параметры, которые должны попасть в URL запроса, задают опцией `params`.

Проще всего передать объект-литерал:

```ts
http
  .get('/api/config', {
    params: {filter: 'all'},
  })
  .subscribe((config) => {
    // ...
  });
```

Если над сборкой или сериализацией параметров нужен больший контроль, передают экземпляр `HttpParams`.

!!! warning ""

    Экземпляры `HttpParams` _неизменяемы_, их нельзя поменять на месте. Методы вроде `append()` возвращают новый экземпляр `HttpParams` с применённым изменением.

```ts
const baseParams = new HttpParams().set('filter', 'all');

http
  .get('/api/config', {
    params: baseParams.set('details', 'enabled'),
  })
  .subscribe((config) => {
    // ...
  });
```

`HttpParams` можно создать со своим `HttpParameterCodec`: он определяет, как `HttpClient` закодирует параметры в URL.

### Своё кодирование параметров {: #custom-parameter-encoding}

По умолчанию `HttpParams` кодирует и декодирует ключи и значения встроенным [`HttpUrlEncodingCodec`](https://angular.dev/api/common/http/HttpUrlEncodingCodec).

Свою реализацию [`HttpParameterCodec`](https://angular.dev/api/common/http/HttpParameterCodec) передают, чтобы задать кодирование и декодирование самостоятельно.

```ts
import {HttpClient, HttpParams, HttpParameterCodec} from '@angular/common/http';
import {inject} from '@angular/core';

export class CustomHttpParamEncoder implements HttpParameterCodec {
  encodeKey(key: string): string {
    return encodeURIComponent(key);
  }

  encodeValue(value: string): string {
    return encodeURIComponent(value);
  }

  decodeKey(key: string): string {
    return decodeURIComponent(key);
  }

  decodeValue(value: string): string {
    return decodeURIComponent(value);
  }
}

export class ApiService {
  private http = inject(HttpClient);

  search() {
    const params = new HttpParams({
      encoder: new CustomHttpParamEncoder(),
    })
      .set('email', 'dev+alerts@example.com')
      .set('q', 'a & b? c/d = e');

    return this.http.get('/api/items', {params});
  }
}
```

## Заголовки запроса {: #setting-request-headers}

Заголовки запроса задают опцией `headers`.

Проще всего передать объект-литерал:

```ts
http
  .get('/api/config', {
    headers: {
      'X-Debug-Level': 'verbose',
    },
  })
  .subscribe((config) => {
    // ...
  });
```

Если над сборкой заголовков нужен больший контроль, передают экземпляр `HttpHeaders`.

!!! warning ""

    Экземпляры `HttpHeaders` _неизменяемы_, их нельзя поменять на месте. Методы вроде `append()` возвращают новый экземпляр `HttpHeaders` с применённым изменением.

```ts
const baseHeaders = new HttpHeaders().set('X-Debug-Level', 'minimal');

http
  .get<Config>('/api/config', {
    headers: baseHeaders.set('X-Debug-Level', 'verbose'),
  })
  .subscribe((config) => {
    // ...
  });
```

## События ответа сервера {: #interacting-with-the-server-response-events}

Для удобства `HttpClient` по умолчанию возвращает `Observable` данных, которые отдал сервер (тело ответа). Иногда нужно посмотреть сам ответ, например прочитать конкретные заголовки.

Чтобы получить ответ целиком, ставят `observe: 'response'`:

```ts
http.get<Config>('/api/config', {observe: 'response'}).subscribe((res) => {
  console.log('Response status:', res.status);
  console.log('Body:', res.body);
});
```

!!! warning "Литерал для `observe`"

    Значение `observe` влияет на тип, который возвращает `HttpClient`, поэтому это должен быть литеральный тип, а не `string`.

    Так получается само, если объект параметров — литерал. Если параметры вынесены в переменную или вспомогательный метод, литерал задают явно, например `observe: 'response' as const`.

## Сырые события прогресса {: #receiving-raw-progress-events}

Помимо тела или объекта ответа `HttpClient` может отдать поток сырых _событий_ — моментов жизненного цикла запроса. События отмечают отправку запроса, приход заголовка ответа и завершение тела. Среди них бывают _события прогресса_: статус выгрузки и загрузки больших тел запроса или ответа.

События прогресса по умолчанию выключены (у них есть цена по производительности). Их включают параметрами `reportUploadProgress` и `reportDownloadProgress`.

!!! info ""

    Серверная часть fetch у `HttpClient` по умолчанию не поддерживает события прогресса _выгрузки_ и бросает ошибку, если задать `reportUploadProgress`. Если приложению нужны события прогресса выгрузки, настройте `HttpClient` через `withXhr()` в `provideHttpClient(...)`.

Чтобы наблюдать поток событий, ставят `observe: 'events'`:

```ts
http
  .get('/api/download', {
    reportDownloadProgress: true,
    observe: 'events',
  })
  .subscribe((event) => {
    switch (event.type) {
      case HttpEventType.DownloadProgress:
        console.log('Downloaded ' + event.loaded + ' out of ' + event.total + ' bytes');
        break;
      case HttpEventType.Response:
        console.log('Finished downloading!');
        break;
    }
  });
```

!!! warning "Литерал для `observe`"

    Значение `observe` влияет на тип, который возвращает `HttpClient`, поэтому это должен быть литеральный тип, а не `string`.

    Так получается само, если объект параметров — литерал. Если параметры вынесены в переменную или вспомогательный метод, литерал задают явно, например `observe: 'events' as const`.

У каждого `HttpEvent` в потоке есть `type`, который отличает смысл события:

| **Значение `type`**                 | **Смысл события**                                                                  |
| -------------------------------- | ---------------------------------------------------------------------------------- |
| `HttpEventType.Sent`             | Запрос отправлен на сервер                                      |
| `HttpEventType.UploadProgress`   | `HttpUploadProgressEvent` — прогресс выгрузки тела запроса      |
| `HttpEventType.ResponseHeader`   | Получено начало ответа, включая статус и заголовки           |
| `HttpEventType.DownloadProgress` | `HttpDownloadProgressEvent` — прогресс загрузки тела ответа |
| `HttpEventType.Response`         | Ответ получен целиком, включая тело                 |
| `HttpEventType.User`             | Своё событие от HTTP-перехватчика.                                           |

## Ошибка запроса {: #handling-request-failure}

HTTP-запрос может сорваться тремя способами:

-   Сеть или соединение не дали запросу дойти до сервера.
-   Запрос не успел ответить, когда был задан таймаут.
-   Сервер получил запрос, но не смог его обработать и вернул ответ с ошибкой.

`HttpClient` собирает все такие ошибки в `HttpErrorResponse` и отдаёт их через канал ошибок `Observable`. У сетевых ошибок и таймаута код `status` равен `0`, а `error` — экземпляр [`ProgressEvent`](https://developer.mozilla.org/docs/Web/API/ProgressEvent). У ошибок сервера `status` — код, который вернул сервер, а `error` — тело ошибочного ответа. По ответу определяют причину и то, как её обработать.

В [библиотеке RxJS](https://rxjs.dev/) есть операторы, которые удобны для обработки ошибок.

Оператор `catchError` превращает ошибочный ответ в значение для интерфейса. По нему интерфейс показывает страницу или значение ошибки и при необходимости сохраняет причину.

Иногда кратковременный сбой, например обрыв сети, роняет запрос неожиданно, и простой повтор его спасает. В RxJS есть операторы _retry_: они автоматически переподписываются на упавший `Observable` при определённых условиях. Например, `retry()` повторяет подписку заданное число раз.

### Таймауты {: #timeouts}

Таймаут запроса задают параметром `timeout` — число миллисекунд рядом с остальными параметрами. Если запрос к серверу не завершился за это время, он прерывается, и приходит ошибка.

!!! info ""

    Таймаут относится только к самому HTTP-запросу к серверу. Это не таймаут всей цепочки обработки. Задержка, которую внесли перехватчики, на этот параметр не влияет.

```ts
http
  .get('/api/config', {
    timeout: 3000,
  })
  .subscribe({
    next: (config) => {
      console.log('Config fetched successfully:', config);
    },
    error: (err) => {
      // If the request times out, an error will have been emitted.
    },
  });
```

## Расширенные параметры fetch {: #advanced-fetch-options}

`HttpClient` в Angular поддерживает расширенные параметры Fetch API: они улучшают производительность и опыт пользователя. Параметры доступны на серверной части fetch, а она используется по умолчанию.

### Параметры fetch {: #fetch-options}

Следующие параметры тонко управляют поведением запроса на серверной части fetch.

#### Соединения keep-alive {: #keep-alive-connections}

Параметр `keepalive` позволяет запросу пережить страницу, которая его начала. Это особенно полезно для аналитики и журнала: запрос должен завершиться, даже если пользователь ушёл со страницы.

```ts
http
  .post('/api/analytics', analyticsData, {
    keepalive: true,
  })
  .subscribe();
```

#### Управление HTTP-кэшем {: #http-caching-control}

Параметр `cache` задаёт, как запрос взаимодействует с HTTP-кэшем браузера. Для повторяющихся запросов это заметно ускоряет работу.

```ts
//  Use cached response regardless of freshness
http
  .get('/api/config', {
    cache: 'force-cache',
  })
  .subscribe((config) => {
    // ...
  });

// Always fetch from network, bypass cache
http
  .get('/api/live-data', {
    cache: 'no-cache',
  })
  .subscribe((data) => {
    // ...
  });

// Use cached response only, fail if not in cache
http
  .get('/api/static-data', {
    cache: 'only-if-cached',
  })
  .subscribe((data) => {
    // ...
  });
```

#### Приоритет запроса и Core Web Vitals {: #request-priority-for-core-web-vitals}

Параметр `priority` указывает относительную важность запроса. Браузер лучше планирует загрузку ресурсов, и оценки Core Web Vitals растут.

```ts
// High priority for critical resources
http
  .get('/api/user-profile', {
    priority: 'high',
  })
  .subscribe((profile) => {
    // ...
  });

// Low priority for non-critical resources
http
  .get('/api/recommendations', {
    priority: 'low',
  })
  .subscribe((recommendations) => {
    // ...
  });

// Auto priority (default) lets the browser decide
http
  .get('/api/settings', {
    priority: 'auto',
  })
  .subscribe((settings) => {
    // ...
  });
```

Допустимые значения `priority`:

-   `'high'` — высокий приоритет, загрузка раньше (например, критичные данные пользователя и содержимое первого экрана)
-   `'low'` — низкий приоритет, загрузка когда ресурсы свободны (например, аналитика и предзагрузка)
-   `'auto'` — приоритет выбирает браузер по контексту запроса (по умолчанию)

!!! tip ""

    Ставьте `priority: 'high'` запросам, которые влияют на отрисовку самого крупного содержимого (LCP), и `priority: 'low'` тем, что не затрагивают первый опыт пользователя.

#### Режим запроса {: #request-mode}

Параметр `mode` задаёт, как запрос ведёт себя с чужим источником, и определяет тип ответа.

```ts
// Same-origin requests only
http
  .get('/api/local-data', {
    mode: 'same-origin',
  })
  .subscribe((data) => {
    // ...
  });

// CORS-enabled cross-origin requests
http
  .get('https://api.external.com/data', {
    mode: 'cors',
  })
  .subscribe((data) => {
    // ...
  });

// No-CORS mode for simple cross-origin requests
http
  .get('https://external-api.com/public-data', {
    mode: 'no-cors',
  })
  .subscribe((data) => {
    // ...
  });
```

Допустимые значения `mode`:

-   `'same-origin'` — только запросы того же источника, кросс-доменные падают
-   `'cors'` — кросс-доменные запросы с CORS (по умолчанию)
-   `'no-cors'` — простые кросс-доменные запросы без CORS, ответ непрозрачный

!!! tip ""

    В браузере для чувствительных запросов, которые не должны уходить на другой источник, ставьте `mode: 'same-origin'`.

!!! warning ""

    При SSR на Node.js `HttpClient` использует [реализацию Fetch на Undici](https://nodejs.org/api/globals.html#fetch). [Undici не применяет браузерные проверки CORS](https://undici.nodejs.org/#cors), поэтому `mode: 'same-origin'` не ограничивает серверные запросы. URL, на которые влияет пользователь, сверяйте с белым списком.

#### Обработка перенаправлений {: #redirect-handling}

Параметр `redirect` задаёт, что делать с ответами-перенаправлениями сервера.

```ts
// Follow redirects automatically (default behavior)
http
  .get('/api/resource', {
    redirect: 'follow',
  })
  .subscribe((data) => {
    // ...
  });

// Prevent automatic redirects
http
  .get('/api/resource', {
    redirect: 'manual',
  })
  .subscribe((response) => {
    // Handle redirect manually
  });

// Treat redirects as errors
http
  .get('/api/resource', {
    redirect: 'error',
  })
  .subscribe({
    next: (data) => {
      // Success response
    },
    error: (err) => {
      // Redirect responses will trigger this error handler
    },
  });
```

Допустимые значения `redirect`:

-   `'follow'` — следовать перенаправлениям автоматически (по умолчанию)
-   `'error'` — считать перенаправления ошибками
-   `'manual'` — не следовать автоматически, вернуть ответ-перенаправление

!!! tip ""

    Ставьте `redirect: 'manual'`, когда перенаправления нужно обрабатывать своей логикой.

#### Учётные данные {: #credentials-handling}

Параметр `credentials` решает, уходят ли куки, заголовки авторизации и другие учётные данные с кросс-доменным запросом. Это особенно важно для аутентификации.

```ts
// Include credentials for cross-origin requests
http
  .get('https://api.example.com/protected-data', {
    credentials: 'include',
  })
  .subscribe((data) => {
    // ...
  });

// Never send credentials (default for cross-origin)
http
  .get('https://api.example.com/public-data', {
    credentials: 'omit',
  })
  .subscribe((data) => {
    // ...
  });

// Send credentials only for same-origin requests
http
  .get('/api/user-data', {
    credentials: 'same-origin',
  })
  .subscribe((data) => {
    // ...
  });

// withCredentials overrides credentials setting
http
  .get('https://api.example.com/data', {
    credentials: 'omit', // This will be ignored
    withCredentials: true, // This forces credentials: 'include'
  })
  .subscribe((data) => {
    // Request will include credentials despite credentials: 'omit'
  });

// Legacy approach (still supported)
http
  .get('https://api.example.com/data', {
    withCredentials: true,
  })
  .subscribe((data) => {
    // Equivalent to credentials: 'include'
  });
```

!!! warning ""

    Параметр `withCredentials` важнее `credentials`. Если заданы оба, `withCredentials: true` всегда даёт `credentials: 'include'`, каким бы ни было явное значение `credentials`.

Допустимые значения `credentials`:

-   `'omit'` — никогда не отправлять учётные данные
-   `'same-origin'` — отправлять учётные данные только для запросов того же источника (по умолчанию)
-   `'include'` — всегда отправлять учётные данные, в том числе на другой источник

!!! tip ""

    Ставьте `credentials: 'include'`, когда куки или заголовки аутентификации нужно отправить на другой домен с поддержкой CORS. Не смешивайте `credentials` и `withCredentials`, чтобы не запутаться.

!!! warning ""

    При SSR на Node.js `credentials: 'include'` сам не пересылает куки входящего запроса браузера. Параметр `credentials` не убирает заголовки `Cookie` и `Authorization`, которые добавлены явно. [Undici пропускает часть заголовков, которые браузер запрещает](https://undici.nodejs.org/#forbidden-and-safelisted-header-names), поэтому заголовки с учётными данными пересылайте только на доверенные источники.

#### Referrer {: #referrer}

Параметр `referrer` задаёт, какие сведения об источнике перехода уходят с запросом. Это важно для приватности и безопасности.

```ts
// Send a specific referrer URL
http
  .get('/api/data', {
    referrer: 'https://example.com/page',
  })
  .subscribe((data) => {
    // ...
  });

// Use the current page as referrer (default behavior)
http
  .get('/api/analytics', {
    referrer: 'about:client',
  })
  .subscribe((data) => {
    // ...
  });
```

Параметр `referrer` принимает:

-   Строку с корректным URL — конкретный URL источника перехода
-   Пустую строку `''` — сведения об источнике перехода не отправляются
-   `'about:client'` — источник перехода по умолчанию (URL текущей страницы)

!!! tip ""

    Для чувствительных запросов, где URL страницы-источника не должен утечь, ставьте `referrer: ''`.

#### Политика referrer {: #referrer-policy}

Параметр `referrerPolicy` задаёт, какая часть сведений об источнике перехода — URL страницы, которая делает запрос, — уходит вместе с HTTP-запросом. От этого зависят и приватность, и аналитика: видно, сколько данных открыто и насколько это безопасно.

```ts
// Send no referrer information regardless of the current page
http
  .get('/api/data', {
    referrerPolicy: 'no-referrer',
  })
  .subscribe();

// Send origin only (e.g. https://example.com)
http
  .get('/api/analytics', {
    referrerPolicy: 'origin',
  })
  .subscribe();
```

Параметр `referrerPolicy` принимает:

-   `'no-referrer'` — никогда не отправлять заголовок `Referer`.
-   `'no-referrer-when-downgrade'` — отправлять источник перехода для того же источника и для безопасных запросов (HTTPS→HTTPS) и опускать его при переходе с безопасного источника на менее безопасный (HTTPS→HTTP).
-   `'origin'` — отправлять только источник (схема, хост, порт), без пути и строки запроса.
-   `'origin-when-cross-origin'` — полный URL для запросов того же источника и только источник для кросс-доменных.
-   `'same-origin'` — полный URL для запросов того же источника и ничего для кросс-доменных.
-   `'strict-origin'` — только источник, и только если уровень безопасности протокола не понижается (например, HTTPS→HTTPS). При понижении источник перехода опускается.
-   `'strict-origin-when-cross-origin'` — поведение браузера по умолчанию. Полный URL для того же источника, источник для кросс-доменных запросов без понижения протокола, и ничего при понижении.
-   `'unsafe-url'` — всегда полный URL, включая путь и строку запроса. Так можно раскрыть чувствительные данные, пользуйтесь осторожно.

!!! tip ""

    Для запросов, где важна приватность, берите сдержанные значения: `'no-referrer'`, `'origin'` или `'strict-origin-when-cross-origin'`.

#### Целостность {: #integrity}

Параметр `integrity` проверяет, что ответ не подменили: передаётся криптографический хеш ожидаемого содержимого. Это особенно полезно, когда скрипты и другие ресурсы грузятся с CDN.

```ts
// Verify response integrity with SHA-256 hash
http
  .get('/api/script.js', {
    integrity: 'sha256-ABC123...',
    responseType: 'text',
  })
  .subscribe((script) => {
    // Script content is verified against the hash
  });
```

!!! warning ""

    `integrity` требует точного совпадения содержимого ответа и переданного хеша. Если содержимое не совпало, запрос упадёт с сетевой ошибкой.

!!! danger ""

    При SSR реализация Fetch читает всё тело ответа, чтобы проверить `integrity`, и только потом возвращает ответ — так требует [стандарт Fetch](https://fetch.spec.whatwg.org/#concept-main-fetch). Angular применяет [`maxResponseBodySize`](https://angular.dev/guide/ssr#configuring-the-response-body-size-limit) только после того, как Fetch вернул ответ, поэтому этот предел не ограничивает данные, накопленные во время проверки целостности.

!!! tip ""

    Целостность подресурса стоит включать, когда критичные ресурсы грузятся из внешних источников: так видно, что их не изменили. Хеши считают инструментами вроде `openssl`.

## HTTP-`Observable` {: #http-observables}

Каждый метод запроса `HttpClient` создаёт и возвращает `Observable` запрошенного типа ответа. Чтобы пользоваться `HttpClient`, важно понимать, как устроены эти `Observable`.

`HttpClient` создаёт то, что в RxJS называют «холодными» `Observable`: реального запроса нет, пока на `Observable` не подпишутся. Только тогда запрос уходит на сервер. Несколько подписок на один и тот же `Observable` дают несколько запросов к серверу. Подписки независимы.

!!! tip ""

    `Observable` от `HttpClient` можно считать _заготовками_ реальных запросов к серверу.

После подписки отписка прерывает запрос, который ещё идёт. Это удобно, если подписка идёт через пайп `async`: запрос отменится сам, когда пользователь уйдёт со страницы. То же самое с комбинаторами RxJS вроде `switchMap`: отмена убирает устаревшие запросы.

Когда ответ приходит, `Observable` от `HttpClient` обычно завершаются (на это могут влиять перехватчики).

Из-за автоматического завершения утечка памяти маловероятна, даже если подписки `HttpClient` не снимать. Но, как и с любой асинхронной операцией, подписки лучше снимать, когда компонент уничтожается: иначе колбэк подписки может выполниться и упасть, пытаясь работать с уже уничтоженным компонентом.

!!! tip ""

    Подписка через пайп `async` или операцию `toSignal` снимается корректно.

## Практические приёмы {: #best-practices}

`HttpClient` можно внедрить и вызывать прямо из компонента, но обычно доступ к данным выносят в переиспользуемые внедряемые сервисы. Например, `UserService` прячет запрос данных пользователя по идентификатору:

```ts
@Service()
export class UserService {
  private http = inject(HttpClient);

  getUser(id: string): Observable<User> {
    return this.http.get<User>(`/api/user/${id}`);
  }
}
```

В компоненте `@if` вместе с пайпом `async` рисует интерфейс только после загрузки данных:

```ts
import {AsyncPipe} from '@angular/common';

@Component({
  imports: [AsyncPipe],
  template: `
    @if (user$ | async; as user) {
      <p>Name: {{ user.name }}</p>
      <p>Biography: {{ user.biography }}</p>
    }
  `,
})
export class UserProfile {
  userId = input.required<string>();
  user$!: Observable<User>;

  private userService = inject(UserService);

  constructor(): void {
    effect(() => {
      this.user$ = this.userService.getUser(this.userId());
    });
  }
}
```


---

Источник: [https://angular.dev/guide/http/making-requests](https://angular.dev/guide/http/making-requests)
