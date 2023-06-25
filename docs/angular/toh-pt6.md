# Получение данных с сервера

В этом руководстве добавлены следующие возможности сохранения данных с помощью `HttpClient` от Angular.

-   Сервис `HeroService` получает данные о героях с помощью HTTP-запросов.

-   Пользователи могут добавлять, редактировать и удалять героев и сохранять эти изменения по HTTP

-   Пользователи могут искать героев по имени

<div class="alert is-helpful">

Пример приложения, которое описывается на этой странице, см. в <live-example></live-example>.

</div>

## Включите HTTP-сервисы

`HttpClient` - это механизм Angular для связи с удаленным сервером по HTTP.

Сделайте `HttpClient` доступным везде в приложении в два шага. Во-первых, добавьте его в корневой `AppModule`, импортировав его:

<code-example header="src/app/app.module.ts (импорт HttpClientModule)" path="toh-pt6/src/app/app/app.module.ts" region="import-http-client"></code-example>.

Далее, все еще в `AppModule`, добавьте `HttpClientModule` в массив `imports`:

<code-example header="src/app/app.module.ts (отрывок массива импорта)" path="toh-pt6/src/app/app/app.module.ts" region="import-httpclientmodule"></code-example>.

## Имитация сервера данных

Этот учебный пример имитирует связь с удаленным сервером данных с помощью модуля [In-memory Web API](https://github.com/angular/angular/tree/main/packages/misc/angular-in-memory-web-api 'In-memory Web API').

После установки модуля приложение делает запросы к `HttpClient` и получает ответы от него. Приложение не знает, что _In-memory Web API_ перехватывает эти запросы, применяет их к хранилищу данных в памяти и возвращает имитированные ответы.

Используя In-memory Web API, вам не придется настраивать сервер, чтобы узнать о `HttpClient`.

<div class="alert is-important">

**IMPORTANT**: <br /> The In-memory Web API module has nothing to do with HTTP in Angular.

If you're reading this tutorial to learn about `HttpClient`, you can [skip over](#import-heroes) this step. If you're coding along with this tutorial, stay here and add the In-memory Web API now.

</div>

Установите пакет In-memory Web API из npm с помощью следующей команды:

<code-example format="shell" language="shell">

npm install angular-in-memory-web-api --save

</code-example>

Сгенерируйте класс `src/app/in-memory-data.service.ts` с помощью следующей команды:

<code-example format="shell" language="shell">

ng generate service InMemoryData

</code-example>

Замените стандартное содержимое `in-memory-data.service.ts` на следующее:

<code-example header="src/app/in-memory-data.service.ts" path="toh-pt6/src/app/in-memory-data.service.ts" region="init"></code-example>.

В `AppModule` импортируйте `HttpClientInMemoryWebApiModule` и класс `InMemoryDataService`, который вы создадите следующим.

<code-example header="src/app/app.module.ts (Импорт In-memory Web API)" path="toh-pt6/src/app/app.module.ts" region="import-in-mem-stuff"></code-example>.

После `HttpClientModule` добавьте `HttpClientInMemoryWebApiModule` в массив `импортов` `AppModule` и сконфигурируйте его с `InMemoryDataService`.

<code-example header="src/app/app.module.ts (отрывок массива импортов)" path="toh-pt6/src/app/app/app.module.ts" region="in-mem-web-api-imports"></code-example>.

Метод конфигурации `forRoot()` принимает класс `InMemoryDataService`, который заправляет базу данных in-memory.

Файл `in-memory-data.service.ts` берет на себя функцию `mock-heroes.ts`. Пока не удаляйте `mock-heroes.ts`. Он еще понадобится вам для нескольких шагов этого руководства.

После того как сервер будет готов, отсоедините In-memory Web API, чтобы запросы приложения могли проходить через сервер.

<a id="import-heroes"></a>

## Герои и HTTP

В `HeroService` импортируйте `HttpClient` и `HttpHeaders`:

<code-example header="src/app/hero.service.ts (импорт символов HTTP)" path="toh-pt6/src/app/hero.service.ts" region="import-httpclient"></code-example>.

Все еще в `HeroService`, инжектируйте `HttpClient` в конструктор в частное свойство `http`.

<code-example path="toh-pt6/src/app/hero.service.ts" header="src/app/hero.service.ts" region="ctor"></code-example>.

Обратите внимание, что вы продолжаете инжектировать `MessageService`, но поскольку ваше приложение вызывает его так часто, оберните его в частный метод `log()`:

<code-example path="toh-pt6/src/app/hero.service.ts" header="src/app/hero.service.ts" region="log"></code-example>.

Определите `heroesUrl` вида `:base/:collectionName` с адресом ресурса heroes на сервере. Здесь `base` - это ресурс, к которому делаются запросы, а `collectionName` - это объект данных heroes в `in-memory-data-service.ts`.

<code-example path="toh-pt6/src/app/hero.service.ts" header="src/app/hero.service.ts" region="heroesUrl" ></code-example>.

### Получение героев с помощью `HttpClient`.

Текущий `HeroService.getHeroes()` использует функцию RxJS `of()` для возврата массива подражаемых героев в виде `Observable<Hero[]>`.

<code-example header="src/app/hero.service.ts (getHeroes with RxJs 'of()')" path="toh-pt4/src/app/hero.service.ts" region="getHeroes-1"></code-example>.

Преобразуйте этот метод для использования `HttpClient` следующим образом:

<code-example header="src/app/hero.service.ts" path="toh-pt6/src/app/hero.service.ts" region="getHeroes-1"></code-example>.

Обновите браузер. Данные о героях должны успешно загрузиться с имитационного сервера.

Вы поменяли `of()` на `http.get()`, и приложение продолжает работать без каких-либо других изменений, потому что обе функции возвращают `Observable<Hero[]>`.

### Методы `HttpClient` возвращают одно значение

Все методы `HttpClient` возвращают RxJS `Observable` чего-либо.

HTTP - это протокол запроса/ответа. Вы делаете запрос, он возвращает один ответ.

В общем, наблюдаемая _может_ возвращать более одного значения в течение времени. Наблюдаемая `HttpClient` всегда выдает одно значение и затем завершается, чтобы больше никогда не выдавать его.

Этот конкретный вызов `HttpClient.get()` возвращает `Observable<Hero[]>`, который является _наблюдаемым массивом героев_. На практике он возвращает только один массив героев.

### `HttpClient.get()` возвращает данные ответа

По умолчанию `HttpClient.get()` возвращает тело ответа в виде нетипизированного объекта JSON. Применение дополнительного спецификатора типа, `<Hero[]>`, добавляет возможности TypeScript, которые уменьшают количество ошибок во время компиляции.

API данных сервера определяет форму данных JSON. API данных _Tour of Heroes_ возвращает данные о героях в виде массива.

<div class="alert is-helpful">

В других API нужные вам данные могут быть спрятаны внутри объекта. Возможно, вам придется выкапывать эти данные, обрабатывая результат `Observable` с помощью оператора RxJS `map()`.

Хотя здесь это не рассматривается, пример использования `map()` есть в методе `getHeroNo404()`, включенном в исходный код примера.

</div>

### Обработка ошибок

Все идет не так, особенно когда вы получаете данные с удаленного сервера. Метод `HeroService.getHeroes()` должен отлавливать ошибки и делать что-то соответствующее.

Чтобы отлавливать ошибки, вы **"передаете" наблюдаемый** результат из `http.get()` через оператор RxJS `catchError()`.

Импортируйте символ `catchError` из `rxjs/operators`, а также некоторые другие операторы, которые будут использоваться позже.

<code-example header="src/app/hero.service.ts" path="toh-pt6/src/app/hero.service.ts" region="import-rxjs-operators"></code-example>.

Теперь расширьте наблюдаемый результат методом `pipe()` и дайте ему оператор `catchError()`.

<code-example header="src/app/hero.service.ts" path="toh-pt6/src/app/hero.service.ts" region="getHeroes-2"></code-example>.

Оператор `catchError()` перехватывает **`Observable``, который потерпел неудачу**. Затем оператор передает ошибку в функцию обработки ошибок.

Следующий метод `handleError()` сообщает об ошибке, а затем возвращает безобидный результат, чтобы приложение продолжало работать.

#### `handleError`.

Следующий метод `handleError()` может быть общим для многих методов `HeroService`, поэтому он обобщен для удовлетворения их различных потребностей.

Вместо того, чтобы обрабатывать ошибку напрямую, она возвращает функцию обработчика ошибок `catchError`. Эта функция настраивается как на имя операции, которая завершилась неудачей, так и на безопасное возвращаемое значение.

<code-example header="src/app/hero.service.ts" path="toh-pt6/src/app/hero.service.ts" region="handleError"></code-example>.

После сообщения об ошибке в консоль обработчик строит дружественное сообщение и возвращает безопасное значение, чтобы приложение могло продолжать работу.

Поскольку каждый метод сервиса возвращает результат типа `Observable`, `handleError()` принимает параметр типа, чтобы вернуть безопасное значение в том виде, который ожидает приложение.

### Tap into the Observable

Метод `getHeros()` подключается к потоку наблюдаемых значений и отправляет сообщение, используя метод `log()`, в область сообщений в нижней части страницы.

Оператор RxJS `tap()` обеспечивает эту возможность, просматривая наблюдаемые значения, делая что-то с этими значениями и передавая их. Обратный вызов `tap()` не обращается к самим значениям.

Вот окончательная версия `getHeroes()` с `tap()`, который регистрирует операцию.

<code-example path="toh-pt6/src/app/hero.service.ts" header="src/app/hero.service.ts" region="getHeroes" ></code-example>

### Получение героя по идентификатору

Большинство веб-интерфейсов поддерживают запрос _get by id_ в форме `:baseURL/:id`.

Здесь _базовый URL_ - это `heroesURL`, определенный в разделе [Heroes and HTTP](tutorial/tour-of-heroes/toh-pt6#heroes-and-http) в `api/heroes`, а _id_ - это номер героя, который вы хотите получить. Например, `api/heroes/11`.

Обновите метод `HeroService` `getHero()` следующим образом, чтобы сделать этот запрос:

<code-example header="src/app/hero.service.ts" path="toh-pt6/src/app/hero.service.ts" region="getHero"></code-example>.

`getHero()` имеет три существенных отличия от `getHeroes()`:

-   `getHero()` конструирует URL запроса с идентификатором нужного героя.

-   Сервер должен ответить одним героем, а не массивом героев

-   `getHero()` возвращает `Observable<Hero>`, который является наблюдаемым из `Hero` _объектов_, а не наблюдаемым из `Hero` _массивов_.

## Обновление героев

<!-- markdownlint-disable MD001 -->

Редактирование имени героя в представлении подробной информации о герое. По мере ввода имя героя обновляет заголовок в верхней части страницы, однако
когда вы нажимаете **Назад**, ваши изменения теряются.

Если вы хотите, чтобы изменения сохранялись, вы должны записать их обратно на сервер.

В конце шаблона детализации героя добавьте кнопку сохранения с привязкой события `click`, которая вызывает новый метод компонента с именем `save()`.

<code-example header="src/app/hero-detail/hero-detail.component.html (save)" path="toh-pt6/src/app/hero-detail/hero-detail.component.html" region="save"></code-example>.

В класс компонента `HeroDetail` добавьте следующий метод `save()`, который сохраняет изменения имени героя с помощью метода сервиса hero `updateHero()` и затем переходит к предыдущему представлению.

<code-example header="src/app/hero-detail/hero-detail.component.ts (save)" path="toh-pt6/src/app/hero-detail/hero-detail.component.ts" region="save"></code-example>

#### Добавьте `HeroService.updateHero()`.

Структура метода `updateHero()` похожа на структуру метода `getHeroes()`, но он использует `http.put()` для сохранения измененного героя на сервере. Добавьте следующее в `HeroService`.

<code-example header="src/app/hero.service.ts (update)" path="toh-pt6/src/app/hero.service.ts" region="updateHero"></code-example>.

Метод `HttpClient.put()` принимает три параметра:

-   URL

-   Данные для обновления, которые в данном случае являются измененным героем

-   Параметры

URL остается неизменным. Веб-интерфейс heroes знает, какого героя нужно обновить, глядя на `id` героя.

Веб-интерфейс heroes ожидает специальный заголовок в HTTP-запросах на сохранение. Этот заголовок находится в константе `httpOptions`, определенной в `HeroService`.

Добавьте следующее в класс `HeroService`.

<code-example header="src/app/hero.service.ts" path="toh-pt6/src/app/hero.service.ts" region="http-options"></code-example>

Refresh the browser, change a hero name and save your change. The `save()` method in `HeroDetailComponent` navigates to the previous view.

The hero now appears in the list with the changed name.

## Add a new hero

To add a hero, this application only needs the hero's name. You can use an `<input>` element paired with an add button.

Insert the following into the `HeroesComponent` template, after the heading:

<code-example header="src/app/heroes/heroes.component.html (add)" path="toh-pt6/src/app/heroes/heroes.component.html" region="add"></code-example>.

В ответ на событие щелчка вызовите обработчик щелчка компонента `add()`, а затем очистите поле ввода, чтобы оно было готово для другого имени. Добавьте следующее в класс `HeroesComponent`:

<code-example header="src/app/heroes/heroes.component.ts (add)" path="toh-pt6/src/app/heroes/heroes.component.ts" region="add"></code-example>.

Если заданное имя не является пустым, обработчик создает объект на основе имени героя. Обработчик передает имя объекта методу сервиса `addHero()`.

Когда `addHero()` создает новый объект, обратный вызов `subscribe()` получает нового героя и помещает его в список `heroes` для отображения.

Добавьте следующий метод `addHero()` в класс `HeroService`.

<code-example header="src/app/hero.service.ts (addHero)" path="toh-pt6/src/app/hero.service.ts" region="addHero"></code-example>

`addHero()` differs from `updateHero()` in two ways:

-   It calls `HttpClient.post()` instead of `put()`

-   It expects the server to create an id for the new hero, which it returns in the `Observable<Hero>` to the caller

Refresh the browser and add some heroes.

## Delete a hero

Each hero in the heroes list should have a delete button.

Add the following button element to the `HeroesComponent` template, after the hero name in the repeated `<li>` element.

<code-example header="src/app/heroes/heroes.component.html" path="toh-pt6/src/app/heroes/heroes.component.html" region="delete"></code-example>.

HTML для списка героев должен выглядеть следующим образом:

<code-example header="src/app/heroes/heroes.component.html (список героев)" path="toh-pt6/src/app/heroes/heroes.component.html" region="list"></code-example>.

Чтобы расположить кнопку удаления в крайнем правом углу записи героя, добавьте некоторые CSS из [финального кода обзора](#heroescomponent) в `heroes.component.css`.

Добавьте обработчик `delete()` в класс компонента.

<code-example header="src/app/heroes/heroes.component.ts (delete)" path="toh-pt6/src/app/heroes/heroes.component.ts" region="delete"></code-example>.

Хотя компонент делегирует удаление героев `HeroService`, он остается ответственным за обновление своего собственного списка героев. Метод компонента `delete()` немедленно удаляет _героя, подлежащего удалению_ из этого списка, ожидая, что `HeroService` преуспеет на сервере.

Компоненту действительно нечего делать с `Observable`, возвращаемым `heroService.deleteHero()` **но он должен подписаться в любом случае**.

Далее, добавьте метод `deleteHero()` к `HeroService` следующим образом.

<code-example header="src/app/hero.service.ts (delete)" path="toh-pt6/src/app/hero.service.ts" region="deleteHero"></code-example>.

Обратите внимание на следующие ключевые моменты:

-   `deleteHero()` вызывает `HttpClient.delete()`.

-   URL - это URL ресурса героев плюс `id` героя, которого нужно удалить.

-   Вы не отправляете данные, как это было с `put()` и `post()`.

-   Вы по-прежнему отправляете `httpOptions`.

Обновите браузер и попробуйте новую возможность удаления.

<div class="alert is-important">

Если вы пренебрежете `subscribe()`, сервис не сможет отправить запрос на удаление на сервер. Как правило, `Observable` _ничего не делает_, пока на него не подпишутся.

Убедитесь в этом сами, временно удалив `subscribe()`, нажав **Dashboard**, затем **Heroes**. Это снова покажет полный список героев.

</div>

## Поиск по имени

В последнем упражнении вы научитесь объединять операторы `Observable` в цепочки, чтобы уменьшить количество одинаковых HTTP-запросов для экономного расходования пропускной способности сети.

### Добавьте функцию поиска героев в приборную панель

Когда пользователь вводит имя в поле поиска, ваше приложение делает повторные HTTP-запросы на героев, отфильтрованных по этому имени. Ваша цель - сделать только столько запросов, сколько необходимо.

#### `HeroService.searchHeroes()`.

Начните с добавления метода `searchHeroes()` к `HeroService`.

<code-example header="src/app/hero.service.ts" path="toh-pt6/src/app/hero.service.ts" region="searchHeroes"></code-example>.

Метод возвращает сразу пустой массив, если нет поискового запроса. В остальном он очень похож на `getHeroes()`, единственным существенным отличием является URL, который включает строку запроса с поисковым запросом.

### Добавление поиска в приборную панель

Откройте шаблон `DashboardComponent` и добавьте элемент поиска героев, `<app-hero-search>`, в нижнюю часть разметки.

<code-example header="src/app/dashboard/dashboard.component.html" path="toh-pt6/src/app/dashboard/dashboard.component.html"></code-example>

Этот шаблон очень похож на повторитель `*ngFor` в шаблоне `HeroesComponent`.

Чтобы это работало, следующим шагом будет добавление компонента с селектором, который соответствует `<app-hero-search>`.

### Создайте `HeroSearchComponent`.

Запустите `ng generate` для создания `HeroSearchComponent`.

<code-example format="shell" language="shell">

ng generate компонент hero-search

</code-example>

`ng generate` creates the three `HeroSearchComponent` files and adds the component to the `AppModule` declarations.

Replace the `HeroSearchComponent` template with an `<input>` and a list of matching search results, as follows.

<code-example header="src/app/hero-search/hero-search.component.html" path="toh-pt6/src/app/hero-search/hero-search.component.html"></code-example>.

Добавьте частные CSS стили в `hero-search.component.css`, как указано в [финальном обзоре кода](#herosearchcomponent) ниже.

Когда пользователь набирает текст в поле поиска, привязка события ввода вызывает метод компонента `search()` с новым значением поля поиска.

<a id="asyncpipe"></a>

### `AsyncPipe`.

Функция `*ngFor` повторяет объекты героев. Обратите внимание, что `*ngFor` итерирует список `heroes$`, а не `heroes`.

Символ `$` - это соглашение, указывающее, что `heroes$` - это `Observable`, а не массив.

<code-example header="src/app/hero-search/hero-search.component.html" path="toh-pt6/src/app/hero-search/hero-search.component.html" region="async"></code-example>.

Поскольку `*ngFor` не может ничего сделать с `Observable`, используйте символ трубы `|`, за которым следует `async`. Это идентифицирует `AsyncPipe` от Angular и подписывается на `Observable` автоматически, так что вам не придется делать это в классе компонента.

### Отредактируйте класс `HeroSearchComponent`.

Замените класс `HeroSearchComponent` и метаданные следующим образом.

<code-example header="src/app/hero-search/hero-search.component.ts" path="toh-pt6/src/app/hero-search/hero-search.component.ts"></code-example>.

Обратите внимание на объявление `heroes$` как `Observable`:

<code-example header="src/app/hero-search/hero-search.component.ts" path="toh-pt6/src/app/hero-search/hero-search.component.ts" region="heroes-stream"></code-example>.

Установите это в [`ngOnInit()`](#search-pipe). Прежде чем это сделать, обратите внимание на определение `searchTerms`.

### Объект `searchTerms` RxJS

Свойство `searchTerms` является RxJS `Subject`.

<code-example header="src/app/hero-search/hero-search.component.ts" path="toh-pt6/src/app/hero-search/hero-search.component.ts" region="searchTerms"></code-example>.

Объект `Subject` является как источником наблюдаемых значений, так и самой `Observable`. Вы можете подписаться на `Subject`, как и на любую `Observable`.

Вы также можете добавлять значения в эту `Observable`, вызывая ее метод `next(value)`, как это делает метод `search()`.

Привязка к событию `input` текстового поля вызывает метод `search()`.

<code-example header="src/app/hero-search/hero-search.component.html" path="toh-pt6/src/app/hero-search/hero-search.component.html" region="input"></code-example>.

Каждый раз, когда пользователь набирает текст в текстовом поле, привязка вызывает `search()` со значением текстового поля в качестве _термина поиска_. `searchTerms` становится `Observable`, испускающим постоянный поток поисковых терминов.

<a id="search-pipe"></a>

### Цепочка операторов RxJS

Передача нового поискового запроса непосредственно в `searchHeroes()` после каждого нажатия клавиши пользователем создает чрезмерное количество HTTP-запросов, что нагружает ресурсы сервера и сжигает тарифные планы.

Вместо этого метод `ngOnInit()` передает наблюдаемую `searchTerms` через последовательность операторов RxJS, которые уменьшают количество обращений к `searchHeroes()`. В конечном итоге, возвращается наблюдаемая таблица результатов поиска своевременных героев, каждый из которых является `Hero[]`.

Вот более подробный взгляд на код.

<code-example header="src/app/hero-search/hero-search.component.ts" path="toh-pt6/src/app/hero-search/hero-search.component.ts" region="search"></code-example>.

Каждый оператор работает следующим образом:

-   `debounceTime(300)` ждет, пока поток новых строковых событий не приостановится на 300 миллисекунд, прежде чем передать последнюю строку.

    Запросы вряд ли будут происходить чаще, чем 300&nbsp;мс.

-   Функция `distinctUntilChanged()` гарантирует, что запрос будет отправлен только в том случае, если текст фильтра изменился.

-   `switchMap()` вызывает службу поиска для каждого поискового термина, который проходит через `debounce()` и `distinctUntilChanged()`.

    Он отменяет и отбрасывает предыдущие наблюдения за поиском, возвращая только последнее наблюдение за службой поиска.

<div class="alert is-helpful">

С помощью оператора [`switchMap`](https://www.learnrxjs.io/learn-rxjs/operators/transformation/switchmap) каждое определяющее ключевое событие может вызвать вызов метода `HttpClient.get()`. Даже с паузой в 300&nbsp;мс между запросами, у вас может быть много HTTP-запросов в полете, и они могут возвращаться не в том порядке, в котором были отправлены.

Функция `switchMap()` сохраняет исходный порядок запросов, возвращая только наблюдаемую из самого последнего вызова метода HTTP. Результаты предыдущих вызовов отменяются и отбрасываются.

<div class="alert is-helpful">

Отмена предыдущей наблюдаемой `searchHeroes()` на самом деле не отменяет ожидающий HTTP-запрос. Нежелательные результаты отбрасываются до того, как они достигнут кода вашего приложения.

</div>

</div>

Помните, что компонент _class_ не подписывается на _наблюдаемую_ `героев$`. Это работа [`AsyncPipe`](#asyncpipe) в шаблоне.

#### Попробуйте.

Запустите приложение снова. В _Панели_ введите текст в поле поиска.

Введите символы, которые совпадают с любыми существующими именами героев, и ищите что-то вроде этого.

<div class="lightbox">

<img alt="Hero Search field with the letters 'm' and 'a' along with four search results that match the query displayed in a list beneath the search input" src="generated/images/guide/toh/toh-hero-search.gif">

</div>

## Окончательный обзор кода

Вот файлы кода, рассмотренные на этой странице. Они находятся в директории `src/app/`.

<a id="heroservice"></a> <a id="inmemorydataservice"></a>

<a id="appmodule"></a>

### `HeroService`, `InMemoryDataService`, `AppModule`

<code-tabs> <code-pane header="hero.service.ts" path="toh-pt6/src/app/hero.service.ts"></code-pane>
<code-pane header="in-memory-data.service.ts" path="toh-pt6/src/app/in-memory-data.service.ts"></code-pane>
<code-pane header="app.module.ts" path="toh-pt6/src/app/app.module.ts"></code-pane>
</code-tabs>

<a id="heroescomponent"></a>

### `HeroesComponent`

<code-tabs> <code-pane header="heroes/heroes.component.html" path="toh-pt6/src/app/heroes/heroes.component.html"></code-pane>
<code-pane header="heroes/heroes.component.ts" path="toh-pt6/src/app/heroes/heroes.component.ts"></code-pane>
<code-pane header="heroes/heroes.component.css" path="toh-pt6/src/app/heroes/heroes.component.css"></code-pane>
</code-tabs>

<a id="herodetailcomponent"></a>

### `HeroDetailComponent`

<code-tabs> <code-pane header="hero-detail/hero-detail.component.html" path="toh-pt6/src/app/hero-detail/hero-detail.component.html"></code-pane>
<code-pane header="hero-detail/hero-detail.component.ts" path="toh-pt6/src/app/hero-detail/hero-detail.component.ts"></code-pane>
<code-pane header="hero-detail/hero-detail.component.css" path="toh-pt6/src/app/hero-detail/hero-detail.component.css"></code-pane>
</code-tabs>

<a id="dashboardcomponent"></a>

### `DashboardComponent`

<code-tabs> <code-pane header="dashboard/dashboard.component.html" path="toh-pt6/src/app/dashboard/dashboard.component.html"></code-pane>
<code-pane header="dashboard/dashboard.component.ts" path="toh-pt6/src/app/dashboard/dashboard.component.ts"></code-pane>
<code-pane header="dashboard/dashboard.component.css" path="toh-pt6/src/app/dashboard/dashboard.component.css"></code-pane>
</code-tabs>

<a id="herosearchcomponent"></a>

### `HeroSearchComponent`

<code-tabs> <code-pane header="hero-search/hero-search.component.html" path="toh-pt6/src/app/hero-search/hero-search.component.html"></code-pane>
<code-pane header="hero-search/hero-search.component.ts" path="toh-pt6/src/app/hero-search/hero-search.component.ts"></code-pane>
<code-pane header="hero-search/hero-search.component.css" path="toh-pt6/src/app/hero-search/hero-search.component.css"></code-pane>
</code-tabs>

## Резюме

Вы находитесь в конце своего пути и многого достигли.

-   Вы добавили необходимые зависимости для использования HTTP в приложении

-   Вы рефакторизовали `HeroService` для загрузки героев из веб-API

-   Вы расширили `HeroService` для поддержки методов `post()`, `put()` и `delete()`.

-   Вы обновили компоненты, чтобы позволить добавлять, редактировать и удалять героев

-   Вы настроили веб-интерфейс API in-memory

-   Вы узнали, как использовать наблюдаемые объекты

На этом мы завершаем учебник "Тур по героям". Вы готовы узнать больше о разработке Angular в разделе "Основы", начиная с руководства [Architecture](guide/architecture 'Architecture').

:date: 28.02.2022
