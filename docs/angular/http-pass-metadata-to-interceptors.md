# HTTP - Передача метаданных перехватчикам

:date: 15.11.2022

Многие перехватчики требуют или получают пользу от конфигурации. Рассмотрим перехватчик, который повторяет неудачные запросы.

По умолчанию перехватчик может повторить запрос три раза, но вы можете захотеть изменить это количество повторных попыток для особенно подверженных ошибкам или чувствительных запросов.

Запросы `HttpClient` содержат _контекст_, который может содержать метаданные о запросе. Этот контекст доступен для перехватчиков для чтения или изменения, хотя он не передается на внутренний сервер при отправке запроса.

Это позволяет приложениям или другим перехватчикам помечать запросы параметрами конфигурации, например, сколько раз повторять запрос.

## Создание контекстного маркера

Angular хранит и извлекает значение в контексте с помощью `HttpContextToken`. Вы можете создать контекстный токен с помощью оператора `new`, как в следующем примере:

```ts
export const RETRY_COUNT = new HttpContextToken(() => 3);
```

Лямбда-функция `() => 3`, переданная во время создания `HttpContextToken`, служит двум целям:

1.  Она позволяет TypeScript определить тип этого токена:

    `HttpContextToken<number>`.

    Контекст запроса безопасен для типов &mdash; чтение токена из контекста запроса возвращает значение соответствующего типа.

2.  Он устанавливает значение по умолчанию для токена.

    Это значение, которое возвращает контекст запроса, если для этого маркера не было задано никакого другого значения.

    Использование значения по умолчанию избавляет от необходимости проверять, установлено ли конкретное значение.

## Установка значений контекста при выполнении запроса

При выполнении запроса вы можете предоставить экземпляр `HttpContext`, в котором уже заданы значения контекста.

```ts
this.httpClient
    .get('/data/feed', {
        context: new HttpContext().set(RETRY_COUNT, 5),
    })
    .subscribe((results) => {
        /* ... */
    });
```

## Чтение значений контекста в перехватчике

Внутри перехватчика вы можете прочитать значение токена в контексте данного запроса с помощью `HttpContext.get()`. Если вы явно не задали значение для маркера, Angular возвращает значение по умолчанию, указанное в маркере.

```ts
import { retry } from 'rxjs';

export class RetryInterceptor implements HttpInterceptor {
    intercept(
        req: HttpRequest<any>,
        next: HttpHandler
    ): Observable<HttpEvent<any>> {
        const retryCount = req.context.get(RETRY_COUNT);

        return next.handle(req).pipe(
            // Retry the request a configurable number of times.
            retry(retryCount)
        );
    }
}
```

## Контексты являются изменяемыми

В отличие от большинства других аспектов экземпляров `HttpRequest`, контекст запроса является изменяемым и сохраняется при других неизменяемых преобразованиях запроса. Это позволяет перехватчикам координировать операции через контекст.

Например, пример `RetryInterceptor` может использовать второй токен контекста для отслеживания количества ошибок, возникающих во время выполнения данного запроса:

```ts
import { retry, tap } from 'rxjs/operators';
export const RETRY_COUNT = new HttpContextToken(() => 3);
export const ERROR_COUNT = new HttpContextToken(() => 0);

export class RetryInterceptor implements HttpInterceptor {
    intercept(
        req: HttpRequest<any>,
        next: HttpHandler
    ): Observable<HttpEvent<any>> {
        const retryCount = req.context.get(RETRY_COUNT);

        return next.handle(req).pipe(
            tap({
                // An error has occurred, so increment this request's ERROR_COUNT.
                error: () =>
                    req.context.set(
                        ERROR_COUNT,
                        req.context.get(ERROR_COUNT) + 1
                    ),
            }),
            // Retry the request a configurable number of times.
            retry(retryCount)
        );
    }
}
```
