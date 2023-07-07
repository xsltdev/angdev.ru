# HTTP - случаи использования перехватчиков

:date: 08.11.2022

Ниже перечислены несколько распространенных случаев использования перехватчиков.

## Установка заголовков по умолчанию

Приложения часто используют перехватчик для установки заголовков по умолчанию в исходящих запросах.

В примере приложения есть `AuthService`, который производит токен авторизации. Вот его `AuthInterceptor`, который инжектирует этот сервис для получения токена и добавляет заголовок авторизации с этим токеном к каждому исходящему запросу:

```ts
import { AuthService } from '../auth.service';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
    constructor(private auth: AuthService) {}

    intercept(req: HttpRequest<any>, next: HttpHandler) {
        // Get the auth token from the service.
        const authToken = this.auth.getAuthorizationToken();

        // Clone the request and replace the original headers with
        // cloned headers, updated with the authorization.
        const authReq = req.clone({
            headers: req.headers.set(
                'Authorization',
                authToken
            ),
        });

        // send cloned request with header to the next handler.
        return next.handle(authReq);
    }
}
```

Практика клонирования запроса для установки новых заголовков настолько распространена, что для этого существует ярлык `setHeaders`:

```ts
// Clone the request and set the new header in one step.
const authReq = req.clone({
    setHeaders: { Authorization: authToken },
});
```

Перехватчик, изменяющий заголовки, может быть использован для ряда различных операций, включая:

-   Аутентификация/авторизация
-   Поведение кэширования; например, `If-Modified-Since`.
-   XSRF защита

## Регистрация пар запроса и ответа

Поскольку перехватчики могут обрабатывать запрос и ответ _вместе_, они могут выполнять такие задачи, как определение времени и протоколирование всей операции HTTP.

Рассмотрим следующий `LoggingInterceptor`, который фиксирует время запроса, время ответа и записывает результат в журнал с указанием прошедшего времени с внедренным `MessageService`.

```ts
import { finalize, tap } from 'rxjs/operators';
import { MessageService } from '../message.service';

@Injectable()
export class LoggingInterceptor implements HttpInterceptor {
    constructor(private messenger: MessageService) {}

    intercept(req: HttpRequest<any>, next: HttpHandler) {
        const started = Date.now();
        let ok: string;

        // extend server response observable with logging
        return next.handle(req).pipe(
            tap({
                // Succeeds when there is a response; ignore other events
                next: (event) =>
                    (ok =
                        event instanceof HttpResponse
                            ? 'succeeded'
                            : ''),
                // Operation failed; error is an HttpErrorResponse
                error: (error) => (ok = 'failed'),
            }),
            // Log when response observable either completes or errors
            finalize(() => {
                const elapsed = Date.now() - started;
                const msg = `${req.method} "${req.urlWithParams}"
             ${ok} in ${elapsed} ms.`;
                this.messenger.add(msg);
            })
        );
    }
}
```

Оператор RxJS `tap` фиксирует, был ли запрос успешным или неудачным. Оператор RxJS `finalize` вызывается, когда наблюдаемый ответ либо возвращает ошибку, либо завершается и сообщает о результате в `MessageService`.

Ни `tap`, ни `finalize` не затрагивают значения потока наблюдаемых, возвращаемых вызывающей стороне.

## Пользовательский парсинг JSON {: #custom-json-parser}

Перехватчики могут быть использованы для замены встроенного парсинга JSON на пользовательскую реализацию.

Перехватчик `CustomJsonInterceptor` в следующем примере демонстрирует, как этого добиться. Если перехватываемый запрос ожидает ответ в формате `'json'`, то `responseType` изменяется на `'text'`, чтобы отключить встроенный парсинг JSON.

Затем ответ разбирается с помощью внедренного `JsonParser`.

```ts
// The JsonParser class acts as a base class for custom parsers and as the DI token.
@Injectable()
export abstract class JsonParser {
    abstract parse(text: string): any;
}

@Injectable()
export class CustomJsonInterceptor
    implements HttpInterceptor {
    constructor(private jsonParser: JsonParser) {}

    intercept(
        httpRequest: HttpRequest<any>,
        next: HttpHandler
    ) {
        if (httpRequest.responseType === 'json') {
            // If the expected response type is JSON then handle it here.
            return this.handleJsonResponse(
                httpRequest,
                next
            );
        } else {
            return next.handle(httpRequest);
        }
    }

    private handleJsonResponse(
        httpRequest: HttpRequest<any>,
        next: HttpHandler
    ) {
        // Override the responseType to disable the default JSON parsing.
        httpRequest = httpRequest.clone({
            responseType: 'text',
        });
        // Handle the response using the custom parser.
        return next
            .handle(httpRequest)
            .pipe(
                map((event) =>
                    this.parseJsonResponse(event)
                )
            );
    }

    private parseJsonResponse(event: HttpEvent<any>) {
        if (
            event instanceof HttpResponse &&
            typeof event.body === 'string'
        ) {
            return event.clone({
                body: this.jsonParser.parse(event.body),
            });
        } else {
            return event;
        }
    }
}
```

Затем вы можете реализовать свой собственный пользовательский `JsonParser`. Вот пользовательский JsonParser, который имеет специальное средство восстановления даты.

```ts
@Injectable()
export class CustomJsonParser implements JsonParser {
    parse(text: string): any {
        return JSON.parse(text, dateReviver);
    }
}

function dateReviver(key: string, value: any) {
    /* . . . */
}
```

Вы предоставляете `CustomParser` вместе с `CustomJsonInterceptor`.

```ts
{ provide: HTTP_INTERCEPTORS, useClass: CustomJsonInterceptor, multi: true },
{ provide: JsonParser, useClass: CustomJsonParser },
```

## Кэширование запросов {: #caching}

Перехватчики могут обрабатывать запросы самостоятельно, без переадресации на `next.handle()`.

Например, вы можете решить кэшировать определенные запросы и ответы для повышения производительности. Вы можете делегировать кэширование перехватчику, не нарушая работу существующих служб данных.

Перехватчик `CachingInterceptor` в следующем примере демонстрирует этот подход.

```ts
@Injectable()
export class CachingInterceptor implements HttpInterceptor {
    constructor(private cache: RequestCache) {}

    intercept(req: HttpRequest<any>, next: HttpHandler) {
        // continue if not cacheable.
        if (!isCacheable(req)) {
            return next.handle(req);
        }

        const cachedResponse = this.cache.get(req);
        return cachedResponse
            ? of(cachedResponse)
            : sendRequest(req, next, this.cache);
    }
}
```

-   Функция `isCacheable()` определяет, является ли запрос кэшируемым.

    В данном примере кэшируемыми являются только GET-запросы к API поиска пакетов.

-   Если запрос не является кэшируемым, перехватчик пересылает запрос следующему обработчику в цепочке.

-   Если кэшируемый запрос найден в кэше, перехватчик возвращает `of()` _observable_ с кэшированным ответом, минуя обработчик `next` и все другие перехватчики ниже по течению

-   Если кэшируемый запрос не находится в кэше, код вызывает `sendRequest()`.

    Эта функция передает запрос в `next.handle()`, который в конечном итоге вызывает сервер и возвращает ответ сервера.

```ts
/**
 * Get server response observable by sending request to `next()`.
 * Will add the response to the cache on the way out.
 */
function sendRequest(
    req: HttpRequest<any>,
    next: HttpHandler,
    cache: RequestCache
): Observable<HttpEvent<any>> {
    return next.handle(req).pipe(
        tap((event) => {
            // There may be other events besides the response.
            if (event instanceof HttpResponse) {
                cache.put(req, event); // Update the cache.
            }
        })
    );
}
```

!!!note ""

    Обратите внимание, как `sendRequest()` перехватывает ответ на обратном пути к приложению. Этот метод передает ответ через оператор `tap()`, обратный вызов которого добавляет ответ в кэш.

    Исходный ответ продолжает нетронутым возвращаться по цепочке перехватчиков к вызывающему приложению.

    Службы данных, такие как `PackageSearchService`, не знают, что некоторые из их запросов `HttpClient` на самом деле возвращают кэшированные ответы.

## Используйте перехватчики для запроса нескольких значений {: #cache-refresh}

Метод `HttpClient.get()` обычно возвращает наблюдаемую, которая выдает одно значение, либо данные, либо ошибку. Перехватчик может изменить это на наблюдаемую, которая выдает [несколько значений](observables.md).

Следующая измененная версия `CachingInterceptor` по желанию возвращает наблюдаемую, которая немедленно выдает кэшированный ответ, посылает запрос API поиска пакетов и выдает его позже с обновленными результатами поиска.

```ts
// cache-then-refresh
if (req.headers.get('x-refresh')) {
    const results$ = sendRequest(req, next, this.cache);
    return cachedResponse
        ? results$.pipe(startWith(cachedResponse))
        : results$;
}
// cache-or-fetch
return cachedResponse
    ? of(cachedResponse)
    : sendRequest(req, next, this.cache);
```

!!!note ""

    Опция _cache-then-refresh_ срабатывает при наличии пользовательского заголовка `x-refresh`.

    Флажок на `PackageSearchComponent` устанавливает флаг `withRefresh`, который является одним из аргументов метода `PackageSearchService.search()`. Этот метод `search()` создает пользовательский заголовок `x-refresh` и добавляет его в запрос перед вызовом `HttpClient.get()`.

Переработанный `CachingInterceptor` устанавливает запрос на сервер независимо от того, есть ли кэшированное значение или нет, используя тот же метод `sendRequest()`, который описан [выше] (#send-request). Наблюдаемая `results$` выполняет запрос при подписке.

-   Если нет кэшированного значения, перехватчик возвращает `results$`.

-   Если есть кэшированное значение, код _переводит_ кэшированный ответ на `results$`. В результате создается перекомпонованная наблюдаемая, которая выдает два ответа, поэтому подписчики будут видеть последовательность этих двух ответов:

    -   кэшированный ответ, который выдается немедленно.

    -   Ответ от сервера, который выдается позже.
