# HTTP — Настройка параметров URL

:date: 08.11.2022

Используйте класс `HttpParams` с параметром запроса `params` для добавления строк запроса URL в ваш `HttpRequest`.

## Создание параметра URL с помощью метода поиска

В следующем примере метод `searchHeroes()` запрашивает героев, имена которых содержат поисковый запрос.

Начните с импорта класса `HttpParams`.

```ts
import { HttpParams } from '@angular/common/http';
```

```ts
/* GET heroes whose name contains search term */
searchHeroes(term: string): Observable<Hero[]> {
  term = term.trim();

  // Add safe, URL encoded search parameter if there is a search term
  const options = term ?
   { params: new HttpParams().set('name', term) } : {};

  return this.http.get<Hero[]>(this.heroesUrl, options)
    .pipe(
      catchError(this.handleError<Hero[]>('searchHeroes', []))
    );
}
```

Если есть поисковый запрос, код создает объект options с параметром поиска в HTML URL-кодировке. Например, если термин "cat", то URL GET-запроса будет `api/heroes?name=cat`.

Объект `HttpParams` является неизменяемым. Если вам нужно обновить параметры, сохраните возвращаемое значение метода `.set()`.

## Создание параметров URL из запроса

Вы также можете создавать параметры HTTP непосредственно из строки запроса, используя переменную `fromString`:

```ts
const params = new HttpParams({ fromString: 'name=foo' });
```
