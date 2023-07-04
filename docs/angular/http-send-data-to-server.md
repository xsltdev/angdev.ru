# HTTP: отправка данных на сервер

:date: 16.03.2023

Помимо получения данных с сервера, `HttpClient` поддерживает другие методы HTTP, такие как PUT, POST и DELETE, которые вы можете использовать для изменения удаленных данных.

Пример приложения для данного руководства включает сокращенную версию примера "Тур по героям", который извлекает героев и позволяет пользователям добавлять, удалять и обновлять их. В следующих разделах приведены примеры методов обновления данных из `HeroesService` примера.

## Выполнить POST-запрос

Приложения часто отправляют данные на сервер с помощью POST-запроса при отправке формы. В следующем примере `HeroesService` делает HTTP POST-запрос при добавлении героя в базу данных.

```ts
/** POST: add a new hero to the database */
addHero(hero: Hero): Observable<Hero> {
  return this.http.post<Hero>(this.heroesUrl, hero, httpOptions)
    .pipe(
      catchError(this.handleError('addHero', hero))
    );
}
```

Метод `HttpClient.post()` похож на `get()` тем, что у него есть параметр type, который вы можете использовать для указания того, что вы ожидаете от сервера возврата данных заданного типа. Метод принимает URL ресурса и два дополнительных параметра:

| Параметр | Подробности                                                                                    |
| :------- | :--------------------------------------------------------------------------------------------- |
| body     | Данные для POST в теле запроса.                                                                |
| options  | Объект, содержащий параметры метода, которые в данном случае определяют необходимые заголовки. |

Пример отлавливает ошибки, как [описано выше](http-handle-request-errors.md#error-details).

Компонент `HeroesComponent` инициирует фактическую операцию POST, подписываясь на `Observable`, возвращаемую этим методом обслуживания.

```ts
this.heroesService
    .addHero(newHero)
    .subscribe((hero) => this.heroes.push(hero));
```

Когда сервер успешно отвечает с новым добавленным героем, компонент добавляет этого героя в отображаемый список `heroes`.

## Выполните запрос DELETE

Это приложение удаляет героя с помощью метода `HttpClient.delete`, передавая ID героя в URL запроса.

```ts
/** DELETE: delete the hero from the server */
deleteHero(id: number): Observable<unknown> {
  const url = `${this.heroesUrl}/${id}`; // DELETE api/heroes/42
  return this.http.delete(url, httpOptions)
    .pipe(
      catchError(this.handleError('deleteHero'))
    );
}
```

Компонент `HeroesComponent` инициирует фактическую операцию DELETE, подписываясь на `Observable`, возвращаемую этим методом службы.

```ts
this.heroesService.deleteHero(hero.id).subscribe();
```

Компонент не ожидает результата от операции удаления, поэтому он подписывается без обратного вызова. Даже если вы не используете результат, вы все равно должны подписаться.

Вызов метода `subscribe()` _исполняет_ наблюдаемую, что и инициирует запрос DELETE.

!!!warning ""

    Вы должны вызвать `subscribe()`, иначе ничего не произойдет. Просто вызов `HeroesService.deleteHero()` не инициирует запрос DELETE.

```ts
// oops ... subscribe() is missing so nothing happens
this.heroesService.deleteHero(hero.id);
```

## Выполните PUT-запрос

Приложение может отправлять PUT-запросы, используя клиентскую службу HTTP. Следующий пример `HeroesService`, как и пример POST, заменяет ресурс обновленными данными.

```ts
/** PUT: update the hero on the server. Returns the updated hero upon success. */
updateHero(hero: Hero): Observable<Hero> {
  return this.http.put<Hero>(this.heroesUrl, hero, httpOptions)
    .pipe(
      catchError(this.handleError('updateHero', hero))
    );
}
```

Как и для любого из HTTP методов, возвращающих наблюдаемую, вызывающий `HeroesComponent.update()` [должен `subscribe()`](http-request-data-from-server.ts#always-subscribe 'Почему вы всегда должны подписываться.') на наблюдаемую, возвращаемую из `HttpClient.put()`, чтобы инициировать запрос.

## Добавление и обновление заголовков

Многие серверы требуют дополнительных заголовков для операций сохранения. Например, сервер может потребовать токен авторизации, или заголовок "Content-Type" для явного объявления MIME-типа тела запроса.

### Добавить заголовки

Сервис `HeroesService` определяет такие заголовки в объекте `httpOptions`, который передается каждому методу сохранения `HttpClient`.

```ts
import { HttpHeaders } from '@angular/common/http';

const httpOptions = {
    headers: new HttpHeaders({
        'Content-Type': 'application/json',
        Authorization: 'my-auth-token',
    }),
};
```

### Обновление заголовков

Вы не можете напрямую изменить существующие заголовки в предыдущем объекте options, потому что экземпляры класса `HttpHeaders` неизменяемы.

Вместо этого используйте метод `set()`, чтобы вернуть клон текущего экземпляра с новыми изменениями.

В следующем примере показано, как при истечении срока действия старого токена можно обновить заголовок авторизации перед выполнением следующего запроса.

```ts
httpOptions.headers = httpOptions.headers.set(
    'Authorization',
    'my-new-auth-token'
);
```
