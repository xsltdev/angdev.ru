# HTTP — Перехват запросов и ответов

:date: 16.03.2023

С помощью перехвата вы объявляете _перехватчики_, которые проверяют и преобразуют HTTP-запросы от вашего приложения к серверу. Эти же перехватчики могут проверять и преобразовывать ответы сервера на обратном пути к приложению.

Несколько перехватчиков образуют цепочку обработчиков запросов/ответов _вперед-назад_.

Перехватчики могут выполнять различные _неявные_ задачи, от аутентификации до протоколирования, обычным, стандартным способом для каждого запроса/ответа HTTP.

Без перехвата разработчикам пришлось бы реализовывать эти задачи _явно_ для каждого вызова метода `HttpClient`.

## Написать перехватчик

Для реализации перехватчика объявите класс, который реализует метод `intercept()` интерфейса `HttpInterceptor`.

Вот перехватчик `noop`, который пропускает запрос через себя, не трогая его:

```ts
import { Injectable } from '@angular/core';
import {
    HttpEvent,
    HttpInterceptor,
    HttpHandler,
    HttpRequest,
} from '@angular/common/http';

import { Observable } from 'rxjs';

/** Pass untouched request through to the next request handler. */
@Injectable()
export class NoopInterceptor implements HttpInterceptor {
    intercept(
        req: HttpRequest<any>,
        next: HttpHandler
    ): Observable<HttpEvent<any>> {
        return next.handle(req);
    }
}
```

Метод `intercept` преобразует запрос в `Observable`, который в итоге возвращает HTTP-ответ. В этом смысле каждый перехватчик способен обрабатывать запрос полностью самостоятельно.

Большинство перехватчиков проверяют запрос на входе и передают потенциально измененный запрос в метод `handle()` объекта `next`, который реализует интерфейс [`HttpHandler`](https://angular.io/api/common/http/HttpHandler).

```js
export abstract class HttpHandler {
  abstract handle(req: HttpRequest<any>): Observable<HttpEvent<any>>;
}
```

Как и `intercept()`, метод `handle()` преобразует HTTP-запрос в `Observable` из [`HttpEvents`](#interceptor-events), которые в конечном итоге включают ответ сервера. Метод `intercept()` может проверить эту наблюдаемую и изменить ее, прежде чем вернуть ее вызывающей стороне.

Этот `no-op` перехватчик вызывает `next.handle()` с исходным запросом и возвращает наблюдаемую, ничего не делая.

## Объект `next`

Объект `next` представляет следующий перехватчик в цепочке перехватчиков. Последний `next` в цепочке — это обработчик бэкенда `HttpClient`, который посылает запрос на сервер и получает ответ сервера.

Большинство перехватчиков вызывают `next.handle()`, так что запрос проходит через следующий перехватчик и, в конечном счете, через внутренний обработчик. Перехватчик _может_ пропустить вызов `next.handle()`, замкнуть цепочку и [вернуть свою собственную `Observable`](http-interceptor-use-cases.md#caching) с искусственным ответом сервера.

Это распространенный паттерн промежуточного ПО, встречающийся в таких фреймворках, как Express.js.

## Предоставьте перехватчик

Перехватчик `NoopInterceptor` — это сервис, управляемый системой [dependency injection (DI)](dependency-injection.md) Angular. Как и другие сервисы, вы должны предоставить класс перехватчика, прежде чем приложение сможет его использовать.

Поскольку перехватчики являются необязательными зависимостями сервиса `HttpClient`, вы должны предоставить их в том же инжекторе или в родительском инжекторе, который предоставляет `HttpClient`. Перехватчики, предоставленные _после_ того, как DI создаст `HttpClient`, игнорируются.

Это приложение предоставляет `HttpClient` в корневом инжекторе приложения, как побочный эффект импорта `HttpClientModule` в `AppModule`. Вы также должны предоставить перехватчики в `AppModule`.

После импорта инжекторного маркера `HTTP_INTERCEPTORS` из `@angular/common/http`, напишите провайдер `NoopInterceptor` следующим образом:

```ts
{ provide: HTTP_INTERCEPTORS, useClass: NoopInterceptor, multi: true },
```

Обратите внимание на опцию `multi: true`. Этот обязательный параметр сообщает Angular, что `HTTP_INTERCEPTORS` является маркером для _мультипровайдера_, который инжектирует массив значений, а не одно значение.

Вы _можете_ добавить этот провайдер непосредственно в массив провайдеров `AppModule`. Однако это довольно многословно, и велика вероятность того, что вы создадите больше перехватчиков и предоставите их таким же образом.

Вы также должны обратить [пристальное внимание на порядок](#interceptor-order), в котором вы предоставляете эти перехватчики.

Подумайте о создании "бочкового" файла, который собирает все провайдеры перехватчиков в массив `httpInterceptorProviders`, начиная с этого первого, `NoopInterceptor`.

```ts
/* "Barrel" of Http Interceptors */
import { HTTP_INTERCEPTORS } from '@angular/common/http';

import { NoopInterceptor } from './noop-interceptor';

/** Http interceptor providers in outside-in order */
export const httpInterceptorProviders = [
    {
        provide: HTTP_INTERCEPTORS,
        useClass: NoopInterceptor,
        multi: true,
    },
];
```

Затем импортируйте и добавьте его в `AppModule` `providers array` следующим образом:

```ts
providers: [
  httpInterceptorProviders
],
```

По мере создания новых перехватчиков, добавляйте их в массив `httpInterceptorProviders`, и вам не придется снова обращаться к `AppModule`.

!!!note ""

    В полном коде примера перехватчиков гораздо больше.

## Порядок перехватчиков

Angular применяет перехватчики в том порядке, в котором вы их предоставляете. Например, рассмотрим ситуацию, в которой вы хотите обрабатывать аутентификацию ваших HTTP-запросов и записывать их в журнал перед отправкой на сервер.

Для выполнения этой задачи вы можете предоставить службу `AuthInterceptor`, а затем службу `LoggingInterceptor`.

Исходящие запросы будут поступать от `AuthInterceptor` к `LoggingInterceptor`.

Ответы на эти запросы будут поступать в обратном направлении, от `LoggingInterceptor` обратно к `AuthInterceptor`.

Ниже представлено визуальное представление этого процесса:

![Перехватчик в порядке HttpClient, AuthInterceptor, AuthInterceptor, HttpBackend, Server, и обратно в обратном порядке, чтобы показать двусторонний поток](interceptor-order.svg)

!!!note ""

    Последним перехватчиком в процессе всегда является `HttpBackend`, который обрабатывает связь с сервером.

Вы не сможете изменить порядок или удалить перехватчики позже. Если вам нужно включать и отключать перехватчик динамически, вам придется встроить эту возможность в сам перехватчик.

## Обработка событий перехватчика {: #interceptor-events}

Большинство методов `HttpClient` возвращают наблюдаемые `HttpResponse<any>`. Сам класс `HttpResponse` фактически является событием, тип которого `HttpEventType.Response`.

Однако один HTTP-запрос может генерировать несколько событий других типов, включая события о ходе загрузки и выгрузки.

Методы `HttpInterceptor.intercept()` и `HttpHandler.handle()` возвращают наблюдаемые `HttpEvent<any>`.

Многие перехватчики занимаются только исходящим запросом и возвращают поток событий из `next.handle()`, не изменяя его. Некоторые перехватчики, однако, должны изучить и модифицировать ответ от `next.handle()`; эти операции могут видеть все эти события в потоке.

Хотя перехватчики способны изменять запросы и ответы, свойства экземпляров `HttpRequest` и `HttpResponse` являются `readonly`, что делает их в значительной степени неизменяемыми. Они неизменяемы по веской причине:

Приложение может повторять запрос несколько раз, прежде чем он увенчается успехом, что означает, что цепочка перехватчиков может обрабатывать один и тот же запрос несколько раз.

Если перехватчик может изменить исходный объект запроса, то повторная операция будет начинаться с измененного запроса, а не с исходного.

Неизменность гарантирует, что перехватчики видят один и тот же запрос при каждой попытке.

!!!note ""

    Ваш перехватчик должен возвращать каждое событие без изменений, если только у него нет веских причин поступать иначе.

TypeScript не позволяет устанавливать свойства `HttpRequest` только для чтения.

```js
// Typescript disallows the following assignment because req.url is readonly
req.url = req.url.replace('http://', 'https://');
```

Если вам необходимо изменить запрос, сначала клонируйте его и измените клон перед передачей его в `next.handle()`. Вы можете клонировать и изменить запрос за один шаг, как показано в следующем примере.

```ts
// clone request and replace 'http://' with 'https://' at the same time
const secureReq = req.clone({
    url: req.url.replace('http://', 'https://'),
});
// send the cloned, "secure" request to the next handler.
return next.handle(secureReq);
```

Хэш-аргумент метода `clone()` позволяет вам изменять определенные свойства запроса, копируя остальные.

### Изменение тела запроса

Защита присваивания `readonly` не может предотвратить глубокие обновления и, в частности, не может помешать вам изменить свойство объекта тела запроса.

```js
req.body.name = req.body.name.trim(); // bad idea!
```

Если вам необходимо изменить тело запроса, выполните следующие действия.

1.  Скопируйте тело запроса и внесите изменения в копию.
2.  Клонируйте объект запроса, используя его метод `clone()`.
3.  Замените тело клона измененной копией.

```ts
// copy the body and trim whitespace from the name property
const newBody = { ...body, name: body.name.trim() };
// clone request and set its body
const newReq = req.clone({ body: newBody });
// send the cloned request to the next handler.
return next.handle(newReq);
```

### Очистка тела запроса в клоне

Иногда требуется очистить тело запроса, а не заменить его. Для этого установите для клонированного тела запроса значение `null`.

!!!tip ""

    Если вы установите для клонированного тела запроса значение `undefined`, Angular предположит, что вы намерены оставить тело как есть.

```js
newReq = req.clone({ … }); // body not mentioned => preserve original body
newReq = req.clone({ body: undefined }); // preserve original body
newReq = req.clone({ body: null }); // clear the body
```
