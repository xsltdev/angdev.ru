# HTTP — Оптимизация взаимодействия с сервером с помощью дебаунсинга

:date: 27.02.2023

Если вам нужно сделать HTTP-запрос в ответ на ввод пользователя, неэффективно отправлять запрос на каждое нажатие клавиши. Лучше подождать, пока пользователь перестанет набирать текст, а затем отправить запрос. Эта техника известна как дебаунсинг.

## Реализация дебаунсинга

Рассмотрим следующий шаблон, который позволяет пользователю ввести поисковый запрос, чтобы найти пакет по имени. Когда пользователь вводит имя в поле поиска, `PackageSearchComponent` отправляет запрос на поиск пакета с таким именем в API поиска пакетов.

```html
<input
    type="text"
    (keyup)="search(getValue($event))"
    id="name"
    placeholder="Search"
/>

<ul>
    <li *ngFor="let package of packages$ | async">
        <strong
            >{{package.name}} v.{{package.version}}</strong
        >
        -
        <em>{{package.description}}</em>
    </li>
</ul>
```

Здесь привязка события `keyup` отправляет каждое нажатие клавиши в метод `search()` компонента.

!!!note ""

    Тип `$event.target` в шаблоне только `EventTarget`. В методе `getValue()` цель приводится к `HTMLInputElement`, чтобы type-safe имел доступ к ее свойству `value`.

    ```ts
    getValue(event: Event): string {
    return (event.target as HTMLInputElement).value;
    }
    ```

Следующий фрагмент реализует дебаггинг для этого входа с помощью операторов RxJS.

```ts
withRefresh = false;
packages$!: Observable<NpmPackageInfo[]>;
private searchText$ = new Subject<string>();

search(packageName: string) {
  this.searchText$.next(packageName);
}

ngOnInit() {
  this.packages$ = this.searchText$.pipe(
    debounceTime(500),
    distinctUntilChanged(),
    switchMap(packageName =>
      this.searchService.search(packageName, this.withRefresh))
  );
}

constructor(private searchService: PackageSearchService) { }
```

Текст `searchText$` — это последовательность значений поля поиска, поступающих от пользователя. Он определен как RxJS `Subject`, что означает, что это многоадресный `Observable`, который также может выдавать значения для себя, вызывая `next(value)`, как это происходит в методе `search()`.

Вместо того, чтобы направлять каждое значение `searchText` непосредственно в инжектированный `PackageSearchService`, код в `ngOnInit()` направляет значения поиска через три оператора, так что значение поиска достигает сервиса, только если это новое значение и пользователь остановил ввод.

| Операторы RxJS           | Подробности                                                                                        |
| :----------------------- | :------------------------------------------------------------------------------------------------- |
| `debounceTime(500)`      | Ждать, пока пользователь не перестанет набирать текст, что в данном случае составляет 1/2 секунды. |
| `distinctUntilChanged()` | Подождите, пока текст поиска не изменится.                                                         |
| `switchMap()`            | Отправляем запрос на поиск в службу.                                                               |

Код устанавливает `packages$` в этот перекомпонованный `Observable` результатов поиска. Шаблон подписывается на `packages$` с помощью [AsyncPipe](https://angular.io/api/common/AsyncPipe) и отображает результаты поиска по мере их поступления.

!!!note ""

Подробнее об опции `withRefresh` смотрите в [Использование перехватчиков для запроса нескольких значений](http-interceptor-use-cases.md#cache-refresh).

## Использование оператора `switchMap()`

Оператор `switchMap()` принимает аргумент функции, которая возвращает `Observable`. В примере `PackageSearchService.search` возвращает `Observable`, как и другие методы службы данных.

Если предыдущий запрос на поиск все еще находится в полете, например, при плохом сетевом соединении, оператор отменяет этот запрос и посылает новый.

!!!note ""

    `switchMap()` возвращает ответы сервиса в исходном порядке запроса, даже если сервер возвращает их не по порядку.

!!!note ""

    Если вы думаете, что будете использовать эту логику дебаггинга повторно, подумайте о том, чтобы перенести ее в служебную функцию или в сам `PackageSearchService`.
