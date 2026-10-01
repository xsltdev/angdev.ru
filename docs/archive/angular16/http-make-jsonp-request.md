# HTTP: Выполните запрос JSONP

:date: 03.11.2022

"JSON with Padding" (JSONP) — это метод обмана веб-браузера для выполнения запросов с тегом `<script>`, который использует атрибут SRC для выполнения специального запроса API.

Приложения могут использовать `HttpClient` для выполнения [JSONP](https://ru.wikipedia.org/wiki/JSONP) запросов через домены, когда сервер не поддерживает [протокол CORS](https://developer.mozilla.org/docs/Web/HTTP/CORS).

Запросы Angular JSONP возвращают `Observable`. Следуйте шаблону подписки на наблюдаемые и используйте оператор RxJS `map` для преобразования ответа перед использованием [async pipe](https://angular.io/api/common/AsyncPipe) для управления результатами.

В Angular используйте JSONP, включив `HttpClientJsonpModule` в импорт `NgModule`. В следующем примере метод `searchHeroes()` использует JSONP-запрос для поиска героев, имена которых содержат поисковый запрос.

```ts
/* GET heroes whose name contains search term */
searchHeroes(term: string): Observable {
  term = term.trim();

  const heroesURL = `${this.heroesURL}?${term}`;
  return this.http.jsonp(heroesUrl, 'callback').pipe(
      catchError(this.handleError('searchHeroes', [])) // then handle the error
    );
}
```

Этот запрос передает `heroesURL` в качестве первого параметра и имя функции обратного вызова в качестве второго параметра. Ответ заворачивается в функцию обратного вызова, которая принимает наблюдаемые данные, возвращенные методом JSONP, и передает их в обработчик ошибок.

## Запрос не JSON-данных

Не все API возвращают данные в формате JSON. В следующем примере метод `DownloaderService` считывает текстовый файл с сервера и регистрирует содержимое файла, а затем возвращает его вызывающей стороне в виде `Observable<string>`.

```ts
getTextFile(filename: string) {
  // The Observable returned by get() is of type Observable<string>
  // because a text response was specified.
  // There's no need to pass a <string> type parameter to get().
  return this.http.get(filename, {responseType: 'text'})
    .pipe(
      tap( // Log the result or error
      {
        next: (data) => this.log(filename, data),
        error: (error) => this.logError(filename, error)
      }
      )
    );
}
```

`HttpClient.get()` возвращает строку, а не JSON по умолчанию из-за опции `responseType`.

Оператор RxJS `tap` позволяет коду проверять значения успехов и ошибок, проходящие через наблюдаемую, не нарушая их.

Метод `download()` в `DownloaderComponent` инициирует запрос, подписываясь на метод сервиса.

```ts
download() {
  this.downloaderService.getTextFile('assets/textfile.txt')
    .subscribe(results => this.contents = results);
}
```
