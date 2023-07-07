# HTTP - отслеживание и отображение хода выполнения запроса

:date: 27.02.2023

Иногда приложения передают большие объемы данных, и эти передачи могут занимать много времени. Типичным примером является загрузка файлов. Вы можете улучшить работу пользователей, обеспечив обратную связь о ходе выполнения таких передач.

## Сделать запрос

Чтобы сделать запрос с включенными событиями прогресса, создайте экземпляр `HttpRequest` с опцией `reportProgress`, установленной в true, чтобы включить отслеживание событий прогресса.

```ts
const req = new HttpRequest('POST', '/upload/file', file, {
    reportProgress: true,
});
```

!!!note ""

    Каждое событие прогресса запускает обнаружение изменений, поэтому включайте их, только если вам нужно сообщить о прогрессе в пользовательском интерфейсе.

    При использовании `HttpClient.request()` с HTTP-методом, настройте метод с `observe: 'events'`, чтобы видеть все события, включая прогресс передачи.

## Отслеживание выполнения запроса

Далее, передайте этот объект запроса методу `HttpClient.request()`, который возвращает `Observable` из `HttpEvents` (те же события, обрабатываемые [перехватчиками](http-intercept-requests-and-responses.md#interceptor-events)).

```ts
// The `HttpClient.request` API produces a raw event stream
// which includes start (sent), progress, and response events.
return this.http.request(req).pipe(
    map((event) => this.getEventMessage(event, file)),
    tap((message) => this.showProgress(message)),
    last(), // return last (completed) message to caller
    catchError(this.handleError(file))
);
```

Метод `getEventMessage` интерпретирует каждый тип `HttpEvent` в потоке событий.

```ts
/** Return distinct message for sent, upload progress, & response events */
private getEventMessage(event: HttpEvent<any>, file: File) {
  switch (event.type) {
    case HttpEventType.Sent:
      return `Uploading file "${file.name}" of size ${file.size}.`;

    case HttpEventType.UploadProgress:
      // Compute and show the % done:
      const percentDone = event.total ? Math.round(100 * event.loaded / event.total) : 0;
      return `File "${file.name}" is ${percentDone}% uploaded.`;

    case HttpEventType.Response:
      return `File "${file.name}" was completely uploaded!`;

    default:
      return `File "${file.name}" surprising upload event: ${event.type}.`;
  }
}
```

!!!note ""

    В примере приложения для этого руководства нет сервера, принимающего загруженные файлы. Перехватчик `UploadInterceptor` в `app/http-interceptors/upload-interceptor.ts` перехватывает и сокращает запросы на загрузку, возвращая наблюдаемую таблицу симулированных событий.
