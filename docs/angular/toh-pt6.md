---
description: В этом руководстве добавлены следующие возможности сохранения данных с помощью HttpClient от Angular
---

# Получение данных с сервера

:date: 28.02.2022

В этом руководстве добавлены следующие возможности сохранения данных с помощью `HttpClient` от Angular.

-   Сервис `HeroService` получает данные о героях с помощью HTTP-запросов.
-   Пользователи могут добавлять, редактировать и удалять героев и сохранять эти изменения по HTTP
-   Пользователи могут искать героев по имени

!!!note ""

    Пример приложения, которое описывается на этой странице, см.:

    -   [Живой пример](https://angular.io/generated/live-examples/toh-pt6/stackblitz.html)
    -   [Скачать](https://angular.io/generated/zips/toh-pt6/toh-pt6.zip)

## Включите HTTP-сервисы

`HttpClient` — это механизм Angular для связи с удаленным сервером по HTTP.

Сделайте `HttpClient` доступным везде в приложении в два шага. Во-первых, добавьте его в корневой `AppModule`, импортировав его:

```ts
import { HttpClientModule } from '@angular/common/http';
```

Далее, все еще в `AppModule`, добавьте `HttpClientModule` в массив `imports`:

```ts
@NgModule({
  imports: [
    HttpClientModule,
  ],
})
```

## Имитация сервера данных

Этот учебный пример имитирует связь с удаленным сервером данных с помощью модуля [In-memory Web API](https://github.com/angular/angular/tree/main/packages/misc/angular-in-memory-web-api 'In-memory Web API').

После установки модуля приложение делает запросы к `HttpClient` и получает ответы от него. Приложение не знает, что _In-memory Web API_ перехватывает эти запросы, применяет их к хранилищу данных в памяти и возвращает имитированные ответы.

Используя In-memory Web API, вам не придется настраивать сервер, чтобы узнать о `HttpClient`.

!!!warning ""

    Модуль In-memory Web API не имеет никакого отношения к HTTP в Angular.

    Если вы читаете этот учебник, чтобы узнать о `HttpClient`, то можете [пропустить](#import-heroes) этот шаг. Если же вы кодите вместе с этим руководством, оставайтесь здесь и добавьте In-memory Web API прямо сейчас.

Установите пакет In-memory Web API из npm с помощью следующей команды:

```shell
npm install angular-in-memory-web-api --save
```

Сгенерируйте класс `src/app/in-memory-data.service.ts` с помощью следующей команды:

```shell
ng generate service InMemoryData
```

Замените стандартное содержимое `in-memory-data.service.ts` на следующее:

```ts
import { Injectable } from '@angular/core';
import { InMemoryDbService } from 'angular-in-memory-web-api';
import { Hero } from './hero';

@Injectable({
    providedIn: 'root',
})
export class InMemoryDataService
    implements InMemoryDbService {
    createDb() {
        const heroes = [
            { id: 12, name: 'Dr. Nice' },
            { id: 13, name: 'Bombasto' },
            { id: 14, name: 'Celeritas' },
            { id: 15, name: 'Magneta' },
            { id: 16, name: 'RubberMan' },
            { id: 17, name: 'Dynama' },
            { id: 18, name: 'Dr. IQ' },
            { id: 19, name: 'Magma' },
            { id: 20, name: 'Tornado' },
        ];
        return { heroes };
    }

    // Overrides the genId method to ensure that a hero always has an id.
    // If the heroes array is empty,
    // the method below returns the initial number (11).
    // if the heroes array is not empty, the method below returns the highest
    // hero id + 1.
    genId(heroes: Hero[]): number {
        return heroes.length > 0
            ? Math.max(...heroes.map((hero) => hero.id)) + 1
            : 11;
    }
}
```

В `AppModule` импортируйте `HttpClientInMemoryWebApiModule` и класс `InMemoryDataService`, который вы создадите следующим.

```ts
import { HttpClientInMemoryWebApiModule } from 'angular-in-memory-web-api';
import { InMemoryDataService } from './in-memory-data.service';
```

После `HttpClientModule` добавьте `HttpClientInMemoryWebApiModule` в массив `импортов` `AppModule` и сконфигурируйте его с `InMemoryDataService`.

```ts
HttpClientModule,
    // The HttpClientInMemoryWebApiModule module intercepts HTTP requests
    // and returns simulated server responses.
    // Remove it when a real server is ready to receive requests.
    HttpClientInMemoryWebApiModule.forRoot(
        InMemoryDataService,
        { dataEncapsulation: false }
    );
```

Метод конфигурации `forRoot()` принимает класс `InMemoryDataService`, который заправляет базу данных in-memory.

Файл `in-memory-data.service.ts` берет на себя функцию `mock-heroes.ts`. Пока не удаляйте `mock-heroes.ts`. Он еще понадобится вам для нескольких шагов этого руководства.

После того как сервер будет готов, отсоедините In-memory Web API, чтобы запросы приложения могли проходить через сервер.

## Герои и HTTP {#import-heroes}

В `HeroService` импортируйте `HttpClient` и `HttpHeaders`:

```ts
import {
    HttpClient,
    HttpHeaders,
} from '@angular/common/http';
```

Все еще в `HeroService`, инжектируйте `HttpClient` в конструктор в частное свойство `http`.

```ts
constructor(
  private http: HttpClient,
  private messageService: MessageService) { }
```

Обратите внимание, что вы продолжаете инжектировать `MessageService`, но поскольку ваше приложение вызывает его так часто, оберните его в частный метод `log()`:

```ts
/** Log a HeroService message with the MessageService */
private log(message: string) {
  this.messageService.add(`HeroService: ${message}`);
}
```

Определите `heroesUrl` вида `:base/:collectionName` с адресом ресурса heroes на сервере. Здесь `base` — это ресурс, к которому делаются запросы, а `collectionName` — это объект данных heroes в `in-memory-data-service.ts`.

```ts
private heroesUrl = 'api/heroes';  // URL to web api
```

### Получение героев с помощью `HttpClient`

Текущий `HeroService.getHeroes()` использует функцию RxJS `of()` для возврата массива подражаемых героев в виде `Observable<Hero[]>`.

```ts
getHeroes(): Observable<Hero[]> {
  const heroes = of(HEROES);
  return heroes;
}
```

Преобразуйте этот метод для использования `HttpClient` следующим образом:

```ts
/** GET heroes from the server */
getHeroes(): Observable<Hero[]> {
  return this.http.get<Hero[]>(this.heroesUrl)
}
```

Обновите браузер. Данные о героях должны успешно загрузиться с имитационного сервера.

Вы поменяли `of()` на `http.get()`, и приложение продолжает работать без каких-либо других изменений, потому что обе функции возвращают `Observable<Hero[]>`.

### Методы `HttpClient` возвращают одно значение

Все методы `HttpClient` возвращают RxJS `Observable` чего-либо.

HTTP — это протокол запроса/ответа. Вы делаете запрос, он возвращает один ответ.

В общем, наблюдаемая _может_ возвращать более одного значения в течение времени. Наблюдаемая `HttpClient` всегда выдает одно значение и затем завершается, чтобы больше никогда не выдавать его.

Этот конкретный вызов `HttpClient.get()` возвращает `Observable<Hero[]>`, который является _наблюдаемым массивом героев_. На практике он возвращает только один массив героев.

### `HttpClient.get()` возвращает данные ответа

По умолчанию `HttpClient.get()` возвращает тело ответа в виде нетипизированного объекта JSON. Применение дополнительного спецификатора типа, `<Hero[]>`, добавляет возможности TypeScript, которые уменьшают количество ошибок во время компиляции.

API данных сервера определяет форму данных JSON. API данных _Tour of Heroes_ возвращает данные о героях в виде массива.

!!!note ""

    В других API нужные вам данные могут быть спрятаны внутри объекта. Возможно, вам придется выкапывать эти данные, обрабатывая результат `Observable` с помощью оператора RxJS `map()`.

    Хотя здесь это не рассматривается, пример использования `map()` есть в методе `getHeroNo404()`, включенном в исходный код примера.

### Обработка ошибок

Все идет не так, особенно когда вы получаете данные с удаленного сервера. Метод `HeroService.getHeroes()` должен отлавливать ошибки и делать что-то соответствующее.

Чтобы отлавливать ошибки, вы **"передаете" наблюдаемый** результат из `http.get()` через оператор RxJS `catchError()`.

Импортируйте символ `catchError` из `rxjs/operators`, а также некоторые другие операторы, которые будут использоваться позже.

```ts
import { catchError, map, tap } from 'rxjs/operators';
```

Теперь расширьте наблюдаемый результат методом `pipe()` и дайте ему оператор `catchError()`.

```ts
getHeroes(): Observable<Hero[]> {
  return this.http.get<Hero[]>(this.heroesUrl)
    .pipe(
      catchError(this.handleError<Hero[]>('getHeroes', []))
    );
}
```

Оператор `catchError()` перехватывает **`Observable``, который потерпел неудачу**. Затем оператор передает ошибку в функцию обработки ошибок.

Следующий метод `handleError()` сообщает об ошибке, а затем возвращает безобидный результат, чтобы приложение продолжало работать.

#### `handleError`

Следующий метод `handleError()` может быть общим для многих методов `HeroService`, поэтому он обобщен для удовлетворения их различных потребностей.

Вместо того, чтобы обрабатывать ошибку напрямую, она возвращает функцию обработчика ошибок `catchError`. Эта функция настраивается как на имя операции, которая завершилась неудачей, так и на безопасное возвращаемое значение.

```ts
/**
 * Handle Http operation that failed.
 * Let the app continue.
 *
 * @param operation - name of the operation that failed
 * @param result - optional value to return as the observable result
 */
private handleError<T>(operation = 'operation', result?: T) {
  return (error: any): Observable<T> => {

    // TODO: send the error to remote logging infrastructure
    console.error(error); // log to console instead

    // TODO: better job of transforming error for user consumption
    this.log(`${operation} failed: ${error.message}`);

    // Let the app keep running by returning an empty result.
    return of(result as T);
  };
}
```

После сообщения об ошибке в консоль обработчик строит дружественное сообщение и возвращает безопасное значение, чтобы приложение могло продолжать работу.

Поскольку каждый метод сервиса возвращает результат типа `Observable`, `handleError()` принимает параметр типа, чтобы вернуть безопасное значение в том виде, который ожидает приложение.

### Tap into the Observable

Метод `getHeros()` подключается к потоку наблюдаемых значений и отправляет сообщение, используя метод `log()`, в область сообщений в нижней части страницы.

Оператор RxJS `tap()` обеспечивает эту возможность, просматривая наблюдаемые значения, делая что-то с этими значениями и передавая их. Обратный вызов `tap()` не обращается к самим значениям.

Вот окончательная версия `getHeroes()` с `tap()`, который регистрирует операцию.

```ts
/** GET heroes from the server */
getHeroes(): Observable<Hero[]> {
  return this.http.get<Hero[]>(this.heroesUrl)
    .pipe(
      tap(_ => this.log('fetched heroes')),
      catchError(this.handleError<Hero[]>('getHeroes', []))
    );
}
```

### Получение героя по идентификатору

Большинство веб-интерфейсов поддерживают запрос _get by id_ в форме `:baseURL/:id`.

Здесь _базовый URL_ — это `heroesURL`, определенный в разделе [Heroes and HTTP](toh-pt6.md#heroes-and-http) в `api/heroes`, а _id_ — это номер героя, который вы хотите получить. Например, `api/heroes/11`.

Обновите метод `HeroService` `getHero()` следующим образом, чтобы сделать этот запрос:

```ts
/** GET hero by id. Will 404 if id not found */
getHero(id: number): Observable<Hero> {
  const url = `${this.heroesUrl}/${id}`;
  return this.http.get<Hero>(url).pipe(
    tap(_ => this.log(`fetched hero id=${id}`)),
    catchError(this.handleError<Hero>(`getHero id=${id}`))
  );
}
```

`getHero()` имеет три существенных отличия от `getHeroes()`:

-   `getHero()` конструирует URL запроса с идентификатором нужного героя.
-   Сервер должен ответить одним героем, а не массивом героев
-   `getHero()` возвращает `Observable<Hero>`, который является наблюдаемым из `Hero` _объектов_, а не наблюдаемым из `Hero` _массивов_.

## Обновление героев

Редактирование имени героя в представлении подробной информации о герое. По мере ввода имя героя обновляет заголовок в верхней части страницы, однако
когда вы нажимаете **Назад**, ваши изменения теряются.

Если вы хотите, чтобы изменения сохранялись, вы должны записать их обратно на сервер.

В конце шаблона детализации героя добавьте кнопку сохранения с привязкой события `click`, которая вызывает новый метод компонента с именем `save()`.

```html
<button type="button" (click)="save()">save</button>
```

В класс компонента `HeroDetail` добавьте следующий метод `save()`, который сохраняет изменения имени героя с помощью метода сервиса hero `updateHero()` и затем переходит к предыдущему представлению.

```ts
save(): void {
  if (this.hero) {
    this.heroService.updateHero(this.hero)
      .subscribe(() => this.goBack());
  }
}
```

### Добавьте `HeroService.updateHero()`

Структура метода `updateHero()` похожа на структуру метода `getHeroes()`, но он использует `http.put()` для сохранения измененного героя на сервере. Добавьте следующее в `HeroService`.

```ts
/** PUT: update the hero on the server */
updateHero(hero: Hero): Observable<any> {
  return this.http.put(this.heroesUrl, hero, this.httpOptions).pipe(
    tap(_ => this.log(`updated hero id=${hero.id}`)),
    catchError(this.handleError<any>('updateHero'))
  );
}
```

Метод `HttpClient.put()` принимает три параметра:

-   URL
-   Данные для обновления, которые в данном случае являются измененным героем
-   Параметры

URL остается неизменным. Веб-интерфейс heroes знает, какого героя нужно обновить, глядя на `id` героя.

Веб-интерфейс heroes ожидает специальный заголовок в HTTP-запросах на сохранение. Этот заголовок находится в константе `httpOptions`, определенной в `HeroService`.

Добавьте следующее в класс `HeroService`.

```ts
httpOptions = {
    headers: new HttpHeaders({
        'Content-Type': 'application/json',
    }),
};
```

Обновите браузер, измените имя героя и сохраните изменения. Метод `save()` в `HeroDetailComponent` осуществляет переход к предыдущему виду.

Теперь герой отображается в списке с измененным именем.

## Добавление нового героя

Для добавления героя этому приложению требуется только его имя. Для этого можно использовать элемент `<input>` в паре с кнопкой добавления.

Вставьте в шаблон `HeroesComponent` после заголовка следующее:

```html
<div>
    <label for="new-hero">Hero name: </label>
    <input id="new-hero" #heroName />

    <!-- (click) passes input value to add() and then clears the input -->
    <button
        type="button"
        class="add-button"
        (click)="add(heroName.value); heroName.value=''"
    >
        Add hero
    </button>
</div>
```

В ответ на событие щелчка вызовите обработчик щелчка компонента `add()`, а затем очистите поле ввода, чтобы оно было готово для другого имени. Добавьте следующее в класс `HeroesComponent`:

```ts
add(name: string): void {
  name = name.trim();
  if (!name) { return; }
  this.heroService.addHero({ name } as Hero)
    .subscribe(hero => {
      this.heroes.push(hero);
    });
}
```

Если заданное имя не является пустым, обработчик создает объект на основе имени героя. Обработчик передает имя объекта методу сервиса `addHero()`.

Когда `addHero()` создает новый объект, обратный вызов `subscribe()` получает нового героя и помещает его в список `heroes` для отображения.

Добавьте следующий метод `addHero()` в класс `HeroService`.

```ts
/** POST: add a new hero to the server */
addHero(hero: Hero): Observable<Hero> {
  return this.http.post<Hero>(this.heroesUrl, hero, this.httpOptions).pipe(
    tap((newHero: Hero) => this.log(`added hero w/ id=${newHero.id}`)),
    catchError(this.handleError<Hero>('addHero'))
  );
}
```

`addHero()` отличается от `updateHero()` двумя особенностями:

-   вызывает `HttpClient.post()` вместо `put()`.
-   ожидает, что сервер создаст идентификатор для нового героя, который он возвращает в `Observable<Hero>` вызывающей стороне.

Обновите браузер и добавьте несколько героев.

## Удалить героя

Каждый герой в списке героев должен иметь кнопку удаления.

Добавьте в шаблон `HeroesComponent` следующий элемент button после имени героя в повторяющемся элементе `<li>`.

```html
<button
    type="button"
    class="delete"
    title="delete hero"
    (click)="delete(hero)"
>
    x
</button>
```

HTML для списка героев должен выглядеть следующим образом:

```html
<ul class="heroes">
    <li *ngFor="let hero of heroes">
        <a routerLink="/detail/{{hero.id}}">
            <span class="badge">{{hero.id}}</span>
            {{hero.name}}
        </a>
        <button
            type="button"
            class="delete"
            title="delete hero"
            (click)="delete(hero)"
        >
            x
        </button>
    </li>
</ul>
```

Чтобы расположить кнопку удаления в крайнем правом углу записи героя, добавьте некоторые CSS из [финального кода обзора](#heroescomponent) в `heroes.component.css`.

Добавьте обработчик `delete()` в класс компонента.

```ts
delete(hero: Hero): void {
  this.heroes = this.heroes.filter(h => h !== hero);
  this.heroService.deleteHero(hero.id).subscribe();
}
```

Хотя компонент делегирует удаление героев `HeroService`, он остается ответственным за обновление своего собственного списка героев. Метод компонента `delete()` немедленно удаляет _героя, подлежащего удалению_ из этого списка, ожидая, что `HeroService` преуспеет на сервере.

Компоненту действительно нечего делать с `Observable`, возвращаемым `heroService.deleteHero()` **но он должен подписаться в любом случае**.

Далее, добавьте метод `deleteHero()` к `HeroService` следующим образом.

```ts
/** DELETE: delete the hero from the server */
deleteHero(id: number): Observable<Hero> {
  const url = `${this.heroesUrl}/${id}`;

  return this.http.delete<Hero>(url, this.httpOptions).pipe(
    tap(_ => this.log(`deleted hero id=${id}`)),
    catchError(this.handleError<Hero>('deleteHero'))
  );
}
```

Обратите внимание на следующие ключевые моменты:

-   `deleteHero()` вызывает `HttpClient.delete()`.
-   URL — это URL ресурса героев плюс `id` героя, которого нужно удалить.
-   Вы не отправляете данные, как это было с `put()` и `post()`.
-   Вы по-прежнему отправляете `httpOptions`.

Обновите браузер и попробуйте новую возможность удаления.

!!!warning ""

    Если вы пренебрежете `subscribe()`, сервис не сможет отправить запрос на удаление на сервер. Как правило, `Observable` _ничего не делает_, пока на него не подпишутся.

    Убедитесь в этом сами, временно удалив `subscribe()`, нажав **Dashboard**, затем **Heroes**. Это снова покажет полный список героев.

## Поиск по имени

В последнем упражнении вы научитесь объединять операторы `Observable` в цепочки, чтобы уменьшить количество одинаковых HTTP-запросов для экономного расходования пропускной способности сети.

### Добавьте функцию поиска героев в приборную панель

Когда пользователь вводит имя в поле поиска, ваше приложение делает повторные HTTP-запросы на героев, отфильтрованных по этому имени. Ваша цель — сделать только столько запросов, сколько необходимо.

#### `HeroService.searchHeroes()`

Начните с добавления метода `searchHeroes()` к `HeroService`.

```ts
/* GET heroes whose name contains search term */
searchHeroes(term: string): Observable<Hero[]> {
  if (!term.trim()) {
    // if not search term, return empty hero array.
    return of([]);
  }
  return this.http.get<Hero[]>(`${this.heroesUrl}/?name=${term}`).pipe(
    tap(x => x.length ?
       this.log(`found heroes matching "${term}"`) :
       this.log(`no heroes matching "${term}"`)),
    catchError(this.handleError<Hero[]>('searchHeroes', []))
  );
}
```

Метод возвращает сразу пустой массив, если нет поискового запроса. В остальном он очень похож на `getHeroes()`, единственным существенным отличием является URL, который включает строку запроса с поисковым запросом.

### Добавление поиска в приборную панель

Откройте шаблон `DashboardComponent` и добавьте элемент поиска героев, `<app-hero-search>`, в нижнюю часть разметки.

```html
<h2>Top Heroes</h2>
<div class="heroes-menu">
    <a
        *ngFor="let hero of heroes"
        routerLink="/detail/{{hero.id}}"
    >
        {{hero.name}}
    </a>
</div>

<app-hero-search></app-hero-search>
```

Этот шаблон очень похож на повторитель `*ngFor` в шаблоне `HeroesComponent`.

Чтобы это работало, следующим шагом будет добавление компонента с селектором, который соответствует `<app-hero-search>`.

### Создайте `HeroSearchComponent`

Запустите `ng generate` для создания `HeroSearchComponent`.

```shell
ng generate component hero-search
```

`ng generate` создает три файла `HeroSearchComponent` и добавляет компонент в декларации `AppModule`.

Замените шаблон `HeroSearchComponent` на `<input>` и список подходящих результатов поиска, как показано ниже.

```html
<div id="search-component">
    <label for="search-box">Hero Search</label>
    <input
        #searchBox
        id="search-box"
        (input)="search(searchBox.value)"
    />

    <ul class="search-result">
        <li *ngFor="let hero of heroes$ | async">
            <a routerLink="/detail/{{hero.id}}">
                {{hero.name}}
            </a>
        </li>
    </ul>
</div>
```

Добавьте частные CSS стили в `hero-search.component.css`, как указано в [финальном обзоре кода](#herosearchcomponent) ниже.

Когда пользователь набирает текст в поле поиска, привязка события ввода вызывает метод компонента `search()` с новым значением поля поиска.

### `AsyncPipe` {#asyncpipe}

Функция `*ngFor` повторяет объекты героев. Обратите внимание, что `*ngFor` итерирует список `heroes$`, а не `heroes`.

Символ `$` — это соглашение, указывающее, что `heroes$` — это `Observable`, а не массив.

```html
<li *ngFor="let hero of heroes$ | async"></li>
```

Поскольку `*ngFor` не может ничего сделать с `Observable`, используйте символ пайпы `|`, за которым следует `async`. Это идентифицирует `AsyncPipe` от Angular и подписывается на `Observable` автоматически, так что вам не придется делать это в классе компонента.

### Отредактируйте класс `HeroSearchComponent`

Замените класс `HeroSearchComponent` и метаданные следующим образом.

```ts
import { Component, OnInit } from '@angular/core';

import { Observable, Subject } from 'rxjs';

import {
    debounceTime,
    distinctUntilChanged,
    switchMap,
} from 'rxjs/operators';

import { Hero } from '../hero';
import { HeroService } from '../hero.service';

@Component({
    selector: 'app-hero-search',
    templateUrl: './hero-search.component.html',
    styleUrls: ['./hero-search.component.css'],
})
export class HeroSearchComponent implements OnInit {
    heroes$!: Observable<Hero[]>;
    private searchTerms = new Subject<string>();

    constructor(private heroService: HeroService) {}

    // Push a search term into the observable stream.
    search(term: string): void {
        this.searchTerms.next(term);
    }

    ngOnInit(): void {
        this.heroes$ = this.searchTerms.pipe(
            // wait 300ms after each keystroke before considering the term
            debounceTime(300),

            // ignore new term if same as previous term
            distinctUntilChanged(),

            // switch to new search observable each time the term changes
            switchMap((term: string) =>
                this.heroService.searchHeroes(term)
            )
        );
    }
}
```

Обратите внимание на объявление `heroes$` как `Observable`:

```ts
heroes$!: Observable<Hero[]>;
```

Установите это в [`ngOnInit()`](#search-pipe). Прежде чем это сделать, обратите внимание на определение `searchTerms`.

### Объект `searchTerms` RxJS

Свойство `searchTerms` является RxJS `Subject`.

```ts
private searchTerms = new Subject<string>();

// Push a search term into the observable stream.
search(term: string): void {
  this.searchTerms.next(term);
}
```

Объект `Subject` является как источником наблюдаемых значений, так и самой `Observable`. Вы можете подписаться на `Subject`, как и на любую `Observable`.

Вы также можете добавлять значения в эту `Observable`, вызывая ее метод `next(value)`, как это делает метод `search()`.

Привязка к событию `input` текстового поля вызывает метод `search()`.

```html
<input
    #searchBox
    id="search-box"
    (input)="search(searchBox.value)"
/>
```

Каждый раз, когда пользователь набирает текст в текстовом поле, привязка вызывает `search()` со значением текстового поля в качестве _термина поиска_. `searchTerms` становится `Observable`, испускающим постоянный поток поисковых терминов.

### Цепочка операторов RxJS {#search-pipe}

Передача нового поискового запроса непосредственно в `searchHeroes()` после каждого нажатия клавиши пользователем создает чрезмерное количество HTTP-запросов, что нагружает ресурсы сервера и сжигает тарифные планы.

Вместо этого метод `ngOnInit()` передает наблюдаемую `searchTerms` через последовательность операторов RxJS, которые уменьшают количество обращений к `searchHeroes()`. В конечном итоге, возвращается наблюдаемая таблица результатов поиска своевременных героев, каждый из которых является `Hero[]`.

Вот более подробный взгляд на код.

```ts
this.heroes$ = this.searchTerms.pipe(
    // wait 300ms after each keystroke before considering the term
    debounceTime(300),

    // ignore new term if same as previous term
    distinctUntilChanged(),

    // switch to new search observable each time the term changes
    switchMap((term: string) =>
        this.heroService.searchHeroes(term)
    )
);
```

Каждый оператор работает следующим образом:

-   `debounceTime(300)` ждет, пока поток новых строковых событий не приостановится на 300 миллисекунд, прежде чем передать последнюю строку.

    Запросы вряд ли будут происходить чаще, чем 300&nbsp;мс.

-   Функция `distinctUntilChanged()` гарантирует, что запрос будет отправлен только в том случае, если текст фильтра изменился.

-   `switchMap()` вызывает службу поиска для каждого поискового термина, который проходит через `debounce()` и `distinctUntilChanged()`.

    Он отменяет и отбрасывает предыдущие наблюдения за поиском, возвращая только последнее наблюдение за службой поиска.

!!!note ""

    С помощью оператора [`switchMap`](https://www.learnrxjs.io/learn-rxjs/operators/transformation/switchmap) каждое определяющее ключевое событие может вызвать вызов метода `HttpClient.get()`. Даже с паузой в 300&nbsp;мс между запросами, у вас может быть много HTTP-запросов в полете, и они могут возвращаться не в том порядке, в котором были отправлены.

    Функция `switchMap()` сохраняет исходный порядок запросов, возвращая только наблюдаемую из самого последнего вызова метода HTTP. Результаты предыдущих вызовов отменяются и отбрасываются.


    Отмена предыдущей наблюдаемой `searchHeroes()` на самом деле не отменяет ожидающий HTTP-запрос. Нежелательные результаты отбрасываются до того, как они достигнут кода вашего приложения.

Помните, что компонент _class_ не подписывается на _наблюдаемую_ `героев$`. Это работа [`AsyncPipe`](#asyncpipe) в шаблоне.

#### Попробуйте

Запустите приложение снова. В _Панели_ введите текст в поле поиска.

Введите символы, которые совпадают с любыми существующими именами героев, и ищите что-то вроде этого.

![Hero Search field with the letters](toh-hero-search.gif)

## Окончательный обзор кода

Вот файлы кода, рассмотренные на этой странице. Они находятся в директории `src/app/`.

### `HeroService`, `InMemoryDataService`, `AppModule`

=== "hero.service.ts"

    ```ts
    import { Injectable } from '@angular/core';
    import {
    	HttpClient,
    	HttpHeaders,
    } from '@angular/common/http';

    import { Observable, of } from 'rxjs';
    import { catchError, map, tap } from 'rxjs/operators';

    import { Hero } from './hero';
    import { MessageService } from './message.service';

    @Injectable({ providedIn: 'root' })
    export class HeroService {
    	private heroesUrl = 'api/heroes'; // URL to web api

    	httpOptions = {
    		headers: new HttpHeaders({
    			'Content-Type': 'application/json',
    		}),
    	};

    	constructor(
    		private http: HttpClient,
    		private messageService: MessageService
    	) {}

    	/** GET heroes from the server */
    	getHeroes(): Observable<Hero[]> {
    		return this.http.get<Hero[]>(this.heroesUrl).pipe(
    			tap((_) => this.log('fetched heroes')),
    			catchError(
    				this.handleError<Hero[]>('getHeroes', [])
    			)
    		);
    	}

    	/** GET hero by id. Return `undefined` when id not found */
    	getHeroNo404<Data>(id: number): Observable<Hero> {
    		const url = `${this.heroesUrl}/?id=${id}`;
    		return this.http.get<Hero[]>(url).pipe(
    			map((heroes) => heroes[0]), // returns a {0|1} element array
    			tap((h) => {
    				const outcome = h
    					? 'fetched'
    					: 'did not find';
    				this.log(`${outcome} hero id=${id}`);
    			}),
    			catchError(
    				this.handleError<Hero>(`getHero id=${id}`)
    			)
    		);
    	}

    	/** GET hero by id. Will 404 if id not found */
    	getHero(id: number): Observable<Hero> {
    		const url = `${this.heroesUrl}/${id}`;
    		return this.http.get<Hero>(url).pipe(
    			tap((_) => this.log(`fetched hero id=${id}`)),
    			catchError(
    				this.handleError<Hero>(`getHero id=${id}`)
    			)
    		);
    	}

    	/* GET heroes whose name contains search term */
    	searchHeroes(term: string): Observable<Hero[]> {
    		if (!term.trim()) {
    			// if not search term, return empty hero array.
    			return of([]);
    		}
    		return this.http
    			.get<Hero[]>(`${this.heroesUrl}/?name=${term}`)
    			.pipe(
    				tap((x) =>
    					x.length
    						? this.log(
    							`found heroes matching "${term}"`
    						)
    						: this.log(
    							`no heroes matching "${term}"`
    						)
    				),
    				catchError(
    					this.handleError<Hero[]>(
    						'searchHeroes',
    						[]
    					)
    				)
    			);
    	}

    	//////// Save methods //////////

    	/** POST: add a new hero to the server */
    	addHero(hero: Hero): Observable<Hero> {
    		return this.http
    			.post<Hero>(
    				this.heroesUrl,
    				hero,
    				this.httpOptions
    			)
    			.pipe(
    				tap((newHero: Hero) =>
    					this.log(
    						`added hero w/ id=${newHero.id}`
    					)
    				),
    				catchError(
    					this.handleError<Hero>('addHero')
    				)
    			);
    	}

    	/** DELETE: delete the hero from the server */
    	deleteHero(id: number): Observable<Hero> {
    		const url = `${this.heroesUrl}/${id}`;

    		return this.http
    			.delete<Hero>(url, this.httpOptions)
    			.pipe(
    				tap((_) =>
    					this.log(`deleted hero id=${id}`)
    				),
    				catchError(
    					this.handleError<Hero>('deleteHero')
    				)
    			);
    	}

    	/** PUT: update the hero on the server */
    	updateHero(hero: Hero): Observable<any> {
    		return this.http
    			.put(this.heroesUrl, hero, this.httpOptions)
    			.pipe(
    				tap((_) =>
    					this.log(`updated hero id=${hero.id}`)
    				),
    				catchError(
    					this.handleError<any>('updateHero')
    				)
    			);
    	}

    	/**
    	 * Handle Http operation that failed.
    	 * Let the app continue.
    	 *
    	 * @param operation - name of the operation that failed
    	 * @param result - optional value to return as the observable result
    	 */
    	private handleError<T>(
    		operation = 'operation',
    		result?: T
    	) {
    		return (error: any): Observable<T> => {
    			// TODO: send the error to remote logging infrastructure
    			console.error(error); // log to console instead

    			// TODO: better job of transforming error for user consumption
    			this.log(
    				`${operation} failed: ${error.message}`
    			);

    			// Let the app keep running by returning an empty result.
    			return of(result as T);
    		};
    	}

    	/** Log a HeroService message with the MessageService */
    	private log(message: string) {
    		this.messageService.add(`HeroService: ${message}`);
    	}
    }
    ```

=== "in-memory-data.service.ts"

    ```ts
    import { Injectable } from '@angular/core';
    import { InMemoryDbService } from 'angular-in-memory-web-api';
    import { Hero } from './hero';

    @Injectable({
    	providedIn: 'root',
    })
    export class InMemoryDataService
    	implements InMemoryDbService {
    	createDb() {
    		const heroes = [
    			{ id: 12, name: 'Dr. Nice' },
    			{ id: 13, name: 'Bombasto' },
    			{ id: 14, name: 'Celeritas' },
    			{ id: 15, name: 'Magneta' },
    			{ id: 16, name: 'RubberMan' },
    			{ id: 17, name: 'Dynama' },
    			{ id: 18, name: 'Dr. IQ' },
    			{ id: 19, name: 'Magma' },
    			{ id: 20, name: 'Tornado' },
    		];
    		return { heroes };
    	}

    	// Overrides the genId method to ensure that a hero always has an id.
    	// If the heroes array is empty,
    	// the method below returns the initial number (11).
    	// if the heroes array is not empty, the method below returns the highest
    	// hero id + 1.
    	genId(heroes: Hero[]): number {
    		return heroes.length > 0
    			? Math.max(...heroes.map((hero) => hero.id)) + 1
    			: 11;
    	}
    }
    ```

=== "app.module.ts"

    ```ts
    import { NgModule } from '@angular/core';
    import { BrowserModule } from '@angular/platform-browser';
    import { FormsModule } from '@angular/forms';
    import { HttpClientModule } from '@angular/common/http';

    import { HttpClientInMemoryWebApiModule } from 'angular-in-memory-web-api';
    import { InMemoryDataService } from './in-memory-data.service';

    import { AppRoutingModule } from './app-routing.module';

    import { AppComponent } from './app.component';
    import { DashboardComponent } from './dashboard/dashboard.component';
    import { HeroDetailComponent } from './hero-detail/hero-detail.component';
    import { HeroesComponent } from './heroes/heroes.component';
    import { HeroSearchComponent } from './hero-search/hero-search.component';
    import { MessagesComponent } from './messages/messages.component';

    @NgModule({
    	imports: [
    		BrowserModule,
    		FormsModule,
    		AppRoutingModule,
    		HttpClientModule,

    		// The HttpClientInMemoryWebApiModule module intercepts HTTP requests
    		// and returns simulated server responses.
    		// Remove it when a real server is ready to receive requests.
    		HttpClientInMemoryWebApiModule.forRoot(
    			InMemoryDataService,
    			{ dataEncapsulation: false }
    		),
    	],
    	declarations: [
    		AppComponent,
    		DashboardComponent,
    		HeroesComponent,
    		HeroDetailComponent,
    		MessagesComponent,
    		HeroSearchComponent,
    	],
    	bootstrap: [AppComponent],
    })
    export class AppModule {}
    ```

### `HeroesComponent`

=== "heroes/heroes.component.html"

    ```html
    <h2>My Heroes</h2>

    <div>
    	<label for="new-hero">Hero name: </label>
    	<input id="new-hero" #heroName />

    	<!-- (click) passes input value to add() and then clears the input -->
    	<button
    		type="button"
    		class="add-button"
    		(click)="add(heroName.value); heroName.value=''"
    	>
    		Add hero
    	</button>
    </div>

    <ul class="heroes">
    	<li *ngFor="let hero of heroes">
    		<a routerLink="/detail/{{hero.id}}">
    			<span class="badge">{{hero.id}}</span>
    			{{hero.name}}
    		</a>
    		<button
    			type="button"
    			class="delete"
    			title="delete hero"
    			(click)="delete(hero)"
    		>
    			x
    		</button>
    	</li>
    </ul>
    ```

=== "heroes/heroes.component.ts"

    ```ts
    import { Component, OnInit } from '@angular/core';

    import { Hero } from '../hero';
    import { HeroService } from '../hero.service';

    @Component({
    	selector: 'app-heroes',
    	templateUrl: './heroes.component.html',
    	styleUrls: ['./heroes.component.css'],
    })
    export class HeroesComponent implements OnInit {
    	heroes: Hero[] = [];

    	constructor(private heroService: HeroService) {}

    	ngOnInit(): void {
    		this.getHeroes();
    	}

    	getHeroes(): void {
    		this.heroService
    			.getHeroes()
    			.subscribe((heroes) => (this.heroes = heroes));
    	}

    	add(name: string): void {
    		name = name.trim();
    		if (!name) {
    			return;
    		}
    		this.heroService
    			.addHero({ name } as Hero)
    			.subscribe((hero) => {
    				this.heroes.push(hero);
    			});
    	}

    	delete(hero: Hero): void {
    		this.heroes = this.heroes.filter((h) => h !== hero);
    		this.heroService.deleteHero(hero.id).subscribe();
    	}
    }
    ```

=== "heroes/heroes.component.css"

    ```css
    /* HeroesComponent's private CSS styles */
    .heroes {
    	margin: 0 0 2em 0;
    	list-style-type: none;
    	padding: 0;
    	width: 15em;
    }

    input {
    	display: block;
    	width: 100%;
    	padding: 0.5rem;
    	margin: 1rem 0;
    	box-sizing: border-box;
    }

    .heroes li {
    	position: relative;
    	cursor: pointer;
    }

    .heroes li:hover {
    	left: 0.1em;
    }

    .heroes a {
    	color: #333;
    	text-decoration: none;
    	background-color: #eee;
    	margin: 0.5em;
    	padding: 0.3em 0;
    	height: 1.6em;
    	border-radius: 4px;
    	display: block;
    	width: 100%;
    }

    .heroes a:hover {
    	color: #2c3a41;
    	background-color: #e6e6e6;
    }

    .heroes a:active {
    	background-color: #525252;
    	color: #fafafa;
    }

    .heroes .badge {
    	display: inline-block;
    	font-size: small;
    	color: white;
    	padding: 0.8em 0.7em 0 0.7em;
    	background-color: #405061;
    	line-height: 1em;
    	position: relative;
    	left: -1px;
    	top: -4px;
    	height: 1.8em;
    	min-width: 16px;
    	text-align: right;
    	margin-right: 0.8em;
    	border-radius: 4px 0 0 4px;
    }

    .add-button {
    	padding: 0.5rem 1.5rem;
    	font-size: 1rem;
    	margin-bottom: 2rem;
    }

    .add-button:hover {
    	color: white;
    	background-color: #42545c;
    }

    button.delete {
    	position: absolute;
    	left: 210px;
    	top: 5px;
    	background-color: white;
    	color: #525252;
    	font-size: 1.1rem;
    	margin: 0;
    	padding: 1px 10px 3px 10px;
    }

    button.delete:hover {
    	background-color: #525252;
    	color: white;
    }
    ```

### `HeroDetailComponent`

=== "hero-detail/hero-detail.component.html"

    ```html
    <div *ngIf="hero">
    	<h2>{{hero.name | uppercase}} Details</h2>
    	<div><span>id: </span>{{hero.id}}</div>
    	<div>
    		<label for="hero-name">Hero name: </label>
    		<input
    			id="hero-name"
    			[(ngModel)]="hero.name"
    			placeholder="Hero name"
    		/>
    	</div>
    	<button type="button" (click)="goBack()">
    		go back
    	</button>
    	<button type="button" (click)="save()">save</button>
    </div>
    ```

=== "hero-detail/hero-detail.component.ts"

    ```ts
    import { Component, OnInit } from '@angular/core';
    import { ActivatedRoute } from '@angular/router';
    import { Location } from '@angular/common';

    import { Hero } from '../hero';
    import { HeroService } from '../hero.service';

    @Component({
    	selector: 'app-hero-detail',
    	templateUrl: './hero-detail.component.html',
    	styleUrls: ['./hero-detail.component.css'],
    })
    export class HeroDetailComponent implements OnInit {
    	hero: Hero | undefined;

    	constructor(
    		private route: ActivatedRoute,
    		private heroService: HeroService,
    		private location: Location
    	) {}

    	ngOnInit(): void {
    		this.getHero();
    	}

    	getHero(): void {
    		const id = parseInt(
    			this.route.snapshot.paramMap.get('id')!,
    			10
    		);
    		this.heroService
    			.getHero(id)
    			.subscribe((hero) => (this.hero = hero));
    	}

    	goBack(): void {
    		this.location.back();
    	}

    	save(): void {
    		if (this.hero) {
    			this.heroService
    				.updateHero(this.hero)
    				.subscribe(() => this.goBack());
    		}
    	}
    }
    ```

=== "hero-detail/hero-detail.component.css"

    ```css
    /* HeroDetailComponent's private CSS styles */
    label {
    	color: #435960;
    	font-weight: bold;
    }
    input {
    	font-size: 1em;
    	padding: 0.5rem;
    }
    button {
    	margin-top: 20px;
    	margin-right: 0.5rem;
    	background-color: #eee;
    	padding: 1rem;
    	border-radius: 4px;
    	font-size: 1rem;
    }
    button:hover {
    	background-color: #cfd8dc;
    }
    button:disabled {
    	background-color: #eee;
    	color: #ccc;
    	cursor: auto;
    }
    ```

### `DashboardComponent`

=== "dashboard/dashboard.component.html"

    ```html
    <h2>Top Heroes</h2>
    <div class="heroes-menu">
    	<a
    		*ngFor="let hero of heroes"
    		routerLink="/detail/{{hero.id}}"
    	>
    		{{hero.name}}
    	</a>
    </div>

    <app-hero-search></app-hero-search>
    ```

=== "dashboard/dashboard.component.ts"

    ```ts
    import { Component, OnInit } from '@angular/core';
    import { Hero } from '../hero';
    import { HeroService } from '../hero.service';

    @Component({
    	selector: 'app-dashboard',
    	templateUrl: './dashboard.component.html',
    	styleUrls: ['./dashboard.component.css'],
    })
    export class DashboardComponent implements OnInit {
    	heroes: Hero[] = [];

    	constructor(private heroService: HeroService) {}

    	ngOnInit(): void {
    		this.getHeroes();
    	}

    	getHeroes(): void {
    		this.heroService
    			.getHeroes()
    			.subscribe(
    				(heroes) =>
    					(this.heroes = heroes.slice(1, 5))
    			);
    	}
    }
    ```

=== "dashboard/dashboard.component.css"

    ```css
    /* DashboardComponent's private CSS styles */

    h2 {
    	text-align: center;
    }

    .heroes-menu {
    	padding: 0;
    	margin: auto;
    	max-width: 1000px;

    	/* flexbox */
    	display: -webkit-box;
    	display: -moz-box;
    	display: -ms-flexbox;
    	display: -webkit-flex;
    	display: flex;
    	flex-direction: row;
    	flex-wrap: wrap;
    	justify-content: space-around;
    	align-content: flex-start;
    	align-items: flex-start;
    }

    a {
    	background-color: #3f525c;
    	border-radius: 2px;
    	padding: 1rem;
    	font-size: 1.2rem;
    	text-decoration: none;
    	display: inline-block;
    	color: #fff;
    	text-align: center;
    	width: 100%;
    	min-width: 70px;
    	margin: 0.5rem auto;
    	box-sizing: border-box;

    	/* flexbox */
    	order: 0;
    	flex: 0 1 auto;
    	align-self: auto;
    }

    @media (min-width: 600px) {
    	a {
    		width: 18%;
    		box-sizing: content-box;
    	}
    }

    a:hover {
    	background-color: black;
    }
    ```

### `HeroSearchComponent`

=== "hero-search/hero-search.component.html"

    ```html
    <div id="search-component">
    	<label for="search-box">Hero Search</label>
    	<input
    		#searchBox
    		id="search-box"
    		(input)="search(searchBox.value)"
    	/>

    	<ul class="search-result">
    		<li *ngFor="let hero of heroes$ | async">
    			<a routerLink="/detail/{{hero.id}}">
    				{{hero.name}}
    			</a>
    		</li>
    	</ul>
    </div>
    ```

=== "hero-search/hero-search.component.ts"

    ```ts
    import { Component, OnInit } from '@angular/core';

    import { Observable, Subject } from 'rxjs';

    import {
    	debounceTime,
    	distinctUntilChanged,
    	switchMap,
    } from 'rxjs/operators';

    import { Hero } from '../hero';
    import { HeroService } from '../hero.service';

    @Component({
    	selector: 'app-hero-search',
    	templateUrl: './hero-search.component.html',
    	styleUrls: ['./hero-search.component.css'],
    })
    export class HeroSearchComponent implements OnInit {
    	heroes$!: Observable<Hero[]>;
    	private searchTerms = new Subject<string>();

    	constructor(private heroService: HeroService) {}

    	// Push a search term into the observable stream.
    	search(term: string): void {
    		this.searchTerms.next(term);
    	}

    	ngOnInit(): void {
    		this.heroes$ = this.searchTerms.pipe(
    			// wait 300ms after each keystroke before considering the term
    			debounceTime(300),

    			// ignore new term if same as previous term
    			distinctUntilChanged(),

    			// switch to new search observable each time the term changes
    			switchMap((term: string) =>
    				this.heroService.searchHeroes(term)
    			)
    		);
    	}
    }
    ```

=== "hero-search/hero-search.component.css"

    ```css
    /* HeroSearch private styles */

    label {
    	display: block;
    	font-weight: bold;
    	font-size: 1.2rem;
    	margin-top: 1rem;
    	margin-bottom: 0.5rem;
    }
    input {
    	padding: 0.5rem;
    	width: 100%;
    	max-width: 600px;
    	box-sizing: border-box;
    	display: block;
    }

    input:focus {
    	outline: #336699 auto 1px;
    }

    li {
    	list-style-type: none;
    }
    .search-result li a {
    	border-bottom: 1px solid gray;
    	border-left: 1px solid gray;
    	border-right: 1px solid gray;
    	display: inline-block;
    	width: 100%;
    	max-width: 600px;
    	padding: 0.5rem;
    	box-sizing: border-box;
    	text-decoration: none;
    	color: black;
    }

    .search-result li a:hover {
    	background-color: #435a60;
    	color: white;
    }

    ul.search-result {
    	margin-top: 0;
    	padding-left: 0;
    }
    ```

## Резюме

Вы находитесь в конце своего пути и многого достигли.

-   Вы добавили необходимые зависимости для использования HTTP в приложении
-   Вы рефакторизовали `HeroService` для загрузки героев из веб-API
-   Вы расширили `HeroService` для поддержки методов `post()`, `put()` и `delete()`.
-   Вы обновили компоненты, чтобы позволить добавлять, редактировать и удалять героев
-   Вы настроили веб-интерфейс API in-memory
-   Вы узнали, как использовать наблюдаемые объекты

На этом мы завершаем учебник "Тур по героям". Вы готовы узнать больше о разработке Angular в разделе "Основы", начиная с руководства [Architecture](architecture.md 'Architecture').

## Ссылки

-   [Get data from a server](https://angular.io/tutorial/tour-of-heroes/toh-pt6)
