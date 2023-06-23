# Общение с внутренними службами с помощью HTTP

Большинству внешних приложений необходимо взаимодействовать с сервером по протоколу HTTP для загрузки или выгрузки данных и доступа к другим внутренним сервисам. Angular предоставляет клиентский HTTP API для приложений Angular, класс сервиса `HttpClient` в `@angular/common/http`.

Клиентская служба HTTP предлагает следующие основные возможности.

-   Возможность запрашивать [типизированные объекты ответа](#typed-response)

-   Оптимизированная [обработка ошибок](#error-handling)

-   Особенности [тестируемости](#testing-requests)

-   Перехват [запросов и ответов](#intercepting-requests-and-responses)

## Предварительные условия

Перед работой с `HttpClientModule`, вы должны иметь базовое понимание следующего:

-   программирование на TypeScript

-   Использование протокола HTTP

-   Основы проектирования приложений Angular, как описано в [Angular Concepts](руководство/архитектура)

-   Техники и операторы наблюдаемых.

    См. руководство [Observables](guide/observables).

## Настройка для взаимодействия с сервером

Прежде чем использовать `HttpClient`, вам необходимо импортировать модуль Angular `HttpClientModule`. Большинство приложений делают это в корневом `AppModule`.

<code-example header="app/app.module.ts (excerpt)" path="http/src/app/app.module.ts" region="sketch"></code-example>.

Затем вы можете внедрить сервис `HttpClient` в качестве зависимости класса приложения, как показано в следующем примере `ConfigService`.

<code-example header="app/config/config.service.ts (excerpt)" path="http/src/app/config/config.service.ts" region="proto"></code-example>.

Сервис `HttpClient` использует [observables](guide/glossary#observable 'Observable definition') для всех транзакций. Вы должны импортировать символы RxJS observable и операторов, которые появляются в фрагментах примера.

Эти импорты `ConfigService` являются типичными.

<code-example header="app/config/config.service.ts (RxJS imports)" path="http/src/app/config/config.service.ts" region="rxjs-imports"></code-example>.

<div class="alert is-helpful">

Вы можете запустить <live-example></live-example>, который сопровождает данное руководство.

Пример приложения не требует сервера данных. Он полагается на [Angular _in-memory-web-api_](https://github.com/angular/angular/tree/main/packages/misc/angular-in-memory-web-api), который заменяет `HttpBackend` модуля _HttpClient_.

Заменяющий сервис имитирует поведение REST-подобного бэкенда.

Посмотрите на _импорты_ модуля `AppModule`, чтобы увидеть, как он настроен.

</div>

## Запрос данных с сервера

Используйте метод [`HttpClient.get()`](api/common/http/HttpClient#get) для получения данных с сервера. Асинхронный метод посылает HTTP-запрос и возвращает Observable, который выдает запрошенные данные при получении ответа.

Тип возвращаемых данных зависит от значений `observe` и `responseType`, которые вы передаете в вызов.

Метод `get()` принимает два аргумента: URL конечной точки, с которой нужно получить данные, и объект _options_, который используется для настройки запроса.

<code-example format="typescript" language="typescript">

options: { headers?: HttpHeaders &verbar; {[header: string]: string &verbar; string[]},
observe?: 'body' &verbar; 'events' &verbar; 'response',

params? HttpParams&verbar;{[param: string]: string &verbar; number &verbar; boolean &verbar; ReadonlyArray&lt;string &verbar; number &verbar; boolean&gt;},

reportProgress?: boolean,

responseType?: 'arraybuffer'&verbar;'blob'&verbar;'json'&verbar;'text',

withCredentials?: boolean,

}

</code-example>

Важные параметры включают свойства _observe_ и _responseType_.

-   Параметр _observe_ определяет, какую часть ответа возвращать.

-   Параметр _responseType_ определяет формат, в котором следует возвращать данные

<div class="alert is-helpful">

Используйте объект `options` для настройки различных других аспектов исходящего запроса. Например, в [Adding headers](#adding-headers) сервис устанавливает заголовки по умолчанию, используя свойство `headers`.

Используйте свойство `params` для настройки запроса с [HTTP URL параметрами](#url-params), а опцию `reportProgress` для [прослушивания событий прогресса](#report-progress) при передаче больших объемов данных.

</div>

Приложения часто запрашивают JSON-данные с сервера. В примере `ConfigService` приложению нужен файл конфигурации на сервере, `config.json`, в котором указаны URL-адреса ресурсов.

<code-example header="assets/config.json" path="http/src/assets/config.json"></code-example>.

Чтобы получить такие данные, вызов `get()` должен содержать следующие параметры: `{observe: 'body', responseType: 'json'}`. Это значения по умолчанию для этих опций, поэтому в следующих примерах объект options не передается.

В последующих разделах показаны некоторые дополнительные возможности опций.

<a id="config-service"></a>

Пример соответствует лучшим практикам создания масштабируемых решений путем определения повторно используемого [injectable service](guide/glossary#service 'service definition') для выполнения функциональности обработки данных. В дополнение к получению данных, сервис может пост-обрабатывать данные, добавлять обработку ошибок и логику повторных попыток.

Сервис `ConfigService` получает этот файл с помощью метода `HttpClient.get()`.

<code-example header="app/config/config.service.ts (getConfig v.1)" path="http/src/app/config/config.service.ts" region="getConfig_1"></code-example>.

Компонент `ConfigComponent` инжектирует `ConfigService` и вызывает метод сервиса `getConfig`.

Поскольку метод сервиса возвращает `Observable` данных конфигурации, компонент _подписывается_ на возвращаемое значение метода. Обратный вызов подписки выполняет минимальную постобработку.

Он копирует поля данных в объект `config` компонента, который привязывается к данным в шаблоне компонента для отображения.

<code-example header="app/config/config.component.ts (showConfig v.1)" path="http/src/app/config/config.component.ts" region="v1"></code-example>

<a id="always-subscribe"></a>

### Начало запроса

Для всех методов `HttpClient` метод не начинает свой HTTP-запрос, пока вы не вызовете `subscribe()` на наблюдаемой, которую возвращает метод.

Это верно для _всех_ `HttpClient` _методов_.

<div class="alert is-helpful">

Вы всегда должны отписываться от наблюдаемого компонента, когда компонент уничтожается.

</div>

Все наблюдаемые, возвращаемые из методов `HttpClient`, по своей конструкции являются _холодными_. Выполнение HTTP-запроса _отложено_, что позволяет вам расширить наблюдаемую таблицу дополнительными операциями, такими как `tap` и `catchError`, прежде чем что-то произойдет.

Вызов `subscribe()` запускает выполнение наблюдаемой таблицы и заставляет `HttpClient` составить и отправить HTTP-запрос на сервер.

Рассматривайте эти наблюдаемые как _синие отпечатки_ для реальных HTTP-запросов.

<div class="alert is-helpful">

Фактически, каждая `subscribe()` инициирует отдельное, независимое выполнение наблюдаемой. Подписка дважды приводит к двум HTTP-запросам.

<code-example format="javascript" language="javascript">

const req = http.get&lt;Heroes&gt;('/api/heroes'); // Сделано 0 запросов - .subscribe() не вызывается.
req.subscribe();

// Выполнен 1 запрос.

req.subscribe();

// 2 запроса сделано.

</code-example>

</div>

<a id="typed-response"></a>

### Запрос типизированного ответа

Структурируйте ваш запрос `HttpClient`, чтобы объявить тип объекта ответа, чтобы сделать потребление вывода более простым и очевидным. Указание типа ответа действует как утверждение типа во время компиляции.

<div class="alert is-important">

Указание типа ответа - это заявление TypeScript о том, что он должен рассматривать ваш ответ как объект данного типа. Это проверка во время сборки и не гарантирует, что сервер действительно ответит объектом данного типа.
Сервер должен убедиться, что в ответ будет получен тип, указанный API сервера.

</div>

Чтобы задать тип объекта ответа, сначала определите интерфейс с необходимыми свойствами. Используйте интерфейс, а не класс, потому что ответ - это обычный объект, который не может быть автоматически преобразован в экземпляр класса.

<code-example path="http/src/app/config/config.service.ts" region="config-interface"></code-example>.

Затем укажите этот интерфейс в качестве параметра типа вызова `HttpClient.get()` в сервисе.

<code-example header="app/config/config.service.ts (getConfig v.2)" path="http/src/app/config/config.service.ts" region="getConfig_2"></code-example>

<div class="alert is-helpful">

Когда вы передаете интерфейс в качестве параметра типа в метод `HttpClient.get()`, используйте оператор [RxJS `map`](guide/rx-library#operators) для преобразования данных ответа в соответствии с требованиями пользовательского интерфейса. Затем вы можете передать преобразованные данные в [async pipe](api/common/AsyncPipe).

</div>

Обратный вызов в методе обновленного компонента получает типизированный объект данных, который проще и безопаснее потреблять:

<code-example header="app/config/config.component.ts (showConfig v.2)" path="http/src/app/config/config.component.ts" region="v2"></code-example>.

Чтобы получить доступ к свойствам, определенным в интерфейсе, вы должны явно преобразовать простой объект, полученный из JSON, в требуемый тип ответа. Например, следующий обратный вызов `subscribe` получает `data` как Object, а затем преобразует его в тип, чтобы получить доступ к свойствам.

<code-example format="typescript" language="typescript">

.subscribe(data =&gt; this.config = { heroesUrl: (data as any).heroesUrl,
textfile: (data as any).textfile,

});

</code-example>

<a id="string-union-types"></a>

<div class="callout is-important">

<header><code>observe</code> and <code>response</code> types</header>

Типы опций `observe` и `response` являются _строковыми союзами_, а не обычными строками.

<code-example format="typescript" language="typescript">

опции: { &hellip;
observe?: 'body' &verbar; 'events' &verbar; 'response',

&hellip;

responseType?: 'arraybuffer'&verbar; 'blob'&verbar; 'json'&verbar; 'text',

&hellip;

}

</code-example>

Это может привести к путанице. Например:

<code-example format="typescript" language="typescript">

// это работает client.get('/foo', {responseType: 'text'})

// но это НЕ работает const options = {

responseType: 'text',

};

client.get('/foo', options)

</code-example>

Во втором случае TypeScript определяет тип `options` как `{responseType: string}`. Этот тип слишком широк, чтобы передать его в `HttpClient.get`, который ожидает, что тип `responseType` будет одной из _специфических_ строк.
`HttpClient` явно типизирован таким образом, чтобы компилятор мог сообщить правильный возвращаемый тип на основе предоставленных вами опций.

Используйте `as const`, чтобы дать понять TypeScript, что вы действительно хотите использовать постоянный тип строки:

<code-example format="typescript" language="typescript">

const options = { responseType: 'text' as const,
};

client.get('/foo', options);

</code-example>

</div>

### Чтение полного ответа

В предыдущем примере вызов `HttpClient.get()` не указывал никаких опций. По умолчанию он возвращает данные в формате JSON, содержащиеся в теле ответа.

Вам может понадобиться больше информации о транзакции, чем содержится в теле ответа. Иногда серверы возвращают специальные заголовки или коды состояния для указания определенных условий, важных для рабочего процесса приложения.

Сообщите `HttpClient`, что вам нужен полный ответ с помощью опции `observe` метода `get()`:

<code-example path="http/src/app/config/config.service.ts" region="getConfigResponse"></code-example>.

Теперь `HttpClient.get()` возвращает `Observable` типа `HttpResponse`, а не просто JSON данные, содержащиеся в теле.

Метод компонента `showConfigResponse()` отображает заголовки ответа, а также конфигурацию:

<code-example header="app/config/config.component.ts (showConfigResponse)" path="http/src/app/config/config.component.ts" region="showConfigResponse"></code-example>.

Как вы можете видеть, объект ответа имеет свойство `body` правильного типа.

### Создание JSONP-запроса

Приложения могут использовать `HttpClient` для выполнения [JSONP](https://en.wikipedia.org/wiki/JSONP) запросов через домены, когда сервер не поддерживает [CORS протокол](https://developer.mozilla.org/docs/Web/HTTP/CORS).

Запросы Angular JSONP возвращают `Observable`. Следуйте шаблону подписки на наблюдаемые и используйте оператор RxJS `map` для преобразования ответа перед использованием [async pipe](api/common/AsyncPipe) для управления результатами.

В Angular используйте JSONP, включив `HttpClientJsonpModule` в импорт `NgModule`. В следующем примере метод `searchHeroes()` использует JSONP-запрос для поиска героев, имена которых содержат поисковый запрос.

<code-example format="typescript" language="typescript">

/_ GET героев, чье имя содержит поисковый запрос _/ searchHeroes(term: string): Наблюдаемый {
term = term.trim();

const heroesURL = `&dollar;{this.heroesURL}?&dollar;{term}`; return this.http.jsonp(heroesUrl, 'callback').pipe(

catchError(this.handleError('searchHeroes', [])) // затем обработать ошибку

);

}

</code-example>

Этот запрос передает `heroesURL` в качестве первого параметра и имя функции обратного вызова в качестве второго параметра. Ответ заворачивается в функцию обратного вызова, которая принимает наблюдаемые данные, возвращенные методом JSONP, и передает их в обработчик ошибок.

### Запрос данных не в формате JSON

Не все API возвращают данные в формате JSON. В следующем примере метод `DownloaderService` считывает текстовый файл с сервера и регистрирует содержимое файла, а затем возвращает его вызывающей стороне в виде `Observable<string>`.

<code-example header="app/downloader/downloader.service.ts (getTextFile)" linenums="false" path="http/src/app/downloader/downloader.service.ts" region="getTextFile"></code-example>.

`HttpClient.get()` возвращает строку, а не JSON по умолчанию из-за опции `responseType`.

Оператор RxJS `tap` позволяет коду проверять значения успехов и ошибок, проходящие через наблюдаемую, не нарушая их.

Метод `download()` в `DownloaderComponent` инициирует запрос, подписываясь на метод сервиса.

<code-example header="app/downloader/downloader.component.ts (download)" linenums="false" path="http/src/app/downloader/downloader.component.ts" region="download"></code-example>

<a id="error-handling"></a>

## Обработка ошибок запроса

Если запрос не проходит на сервере, `HttpClient` возвращает объект _error_ вместо успешного ответа.

Тот же сервис, который выполняет ваши серверные транзакции, должен также выполнять проверку, интерпретацию и разрешение ошибок.

При возникновении ошибки вы можете получить подробную информацию о том, что именно не удалось сделать, чтобы сообщить об этом пользователю. В некоторых случаях вы также можете автоматически [повторить запрос](#retry).

<a id="error-details"></a>

### Получение подробной информации об ошибке

Приложение должно предоставлять пользователю полезную обратную связь при неудачном доступе к данным. Необработанный объект ошибки не особенно полезен в качестве обратной связи.

В дополнение к обнаружению того, что произошла ошибка, вам необходимо получить подробности ошибки и использовать их для составления удобного для пользователя ответа.

Ошибки могут быть двух типов.

-   Бэкэнд сервера может отклонить запрос, вернув HTTP-ответ с кодом состояния 404 или 500.

    Это _ответы об ошибках_.

-   Что-то может пойти не так на стороне клиента, например, сетевая ошибка, которая не позволяет успешно завершить запрос, или исключение, брошенное в операторе RxJS.

    У этих ошибок `status` установлен в `0`, а свойство `error` содержит объект `ProgressEvent`, чей `type` может предоставить дополнительную информацию.

`HttpClient` фиксирует оба вида ошибок в своем `HttpErrorResponse`. Проанализируйте этот ответ, чтобы определить причину ошибки.

Следующий пример определяет обработчик ошибок в ранее определенном [ConfigService](#config-service 'ConfigService defined').

<code-example header="app/config/config.service.ts (handleError)" path="http/src/app/config/config.service.ts" region="handleError"></code-example>.

Обработчик возвращает RxJS `ErrorObservable` с удобным для пользователя сообщением об ошибке. Следующий код обновляет метод `getConfig()`, используя [pipe](guide/pipes 'Pipes guide') для отправки всех наблюдаемых, возвращенных вызовом `HttpClient.get()` в обработчик ошибок.

<code-example header="app/config/config.service.ts (getConfig v.3 с обработчиком ошибок)" path="http/src/app/config/config.service.ts" region="getConfig_3"></code-example>

<a id="retry"></a>

### Повторная попытка неудачного запроса

Иногда ошибка носит временный характер и исчезает автоматически при повторной попытке. Например, в мобильных сценариях часто случаются перебои в работе сети, и повторная попытка может привести к успешному результату.

Библиотека [RxJS](guide/rx-library) предлагает несколько операторов _retry_. Например, оператор `retry()` автоматически повторно подписывается на неудачный `Observable` заданное количество раз.

Переподписка\_ на результат вызова метода `HttpClient` имеет эффект повторной выдачи HTTP-запроса.

В следующем примере показано, как передать неудачный запрос оператору `retry()` перед передачей его в обработчик ошибок.

<code-example header="app/config/config.service.ts (getConfig with retry)" path="http/src/app/config/config.service.ts" region="getConfig"></code-example>

## Отправка данных на сервер

Помимо получения данных с сервера, `HttpClient` поддерживает другие методы HTTP, такие как PUT, POST и DELETE, которые вы можете использовать для изменения удаленных данных.

Пример приложения для данного руководства включает сокращенную версию примера "Тур по героям", который извлекает героев и позволяет пользователям добавлять, удалять и обновлять их. В следующих разделах приведены примеры методов обновления данных из `HeroesService` примера.

### Выполнение POST-запроса

Приложения часто отправляют данные на сервер с помощью POST-запроса при отправке формы. В следующем примере `HeroesService` делает HTTP POST-запрос при добавлении героя в базу данных.

<code-example header="app/heroes/heroes.service.ts (addHero)" path="http/src/app/heroes/heroes.service.ts" region="addHero"></code-example>.

Метод `HttpClient.post()` похож на `get()` тем, что у него есть параметр type, который вы можете использовать для указания того, что вы ожидаете от сервера возврата данных заданного типа. Метод принимает URL ресурса и два дополнительных параметра:

| Parameter | Details | | :-------- | :---------------------------------------------------------------------------------------------------- |.

| body | Данные для POST в теле запроса. |

| | options | Объект, содержащий параметры метода, которые, в данном случае, [указывают необходимые заголовки](#adding-headers). |

В примере отлавливаются ошибки, как [описано выше](#error-details).

Компонент `HeroesComponent` инициирует фактическую операцию POST, подписываясь на `Observable`, возвращаемую этим методом обслуживания.

<code-example header="app/heroes/heroes.component.ts (addHero)" path="http/src/app/heroes/heroes.component.ts" region="add-hero-subscribe"></code-example>.

Когда сервер успешно отвечает с новым добавленным героем, компонент добавляет этого героя в отображаемый список `героев`.

### Выполнение запроса DELETE

Это приложение удаляет героя с помощью метода `HttpClient.delete`, передавая ID героя в URL запроса.

<code-example header="app/heroes/heroes.service.ts (deleteHero)" path="http/src/app/heroes/heroes.service.ts" region="deleteHero"></code-example>.

Компонент `HeroesComponent` инициирует фактическую операцию DELETE, подписываясь на `Observable`, возвращаемую этим методом службы.

<code-example header="app/heroes/heroes.component.ts (deleteHero)" path="http/src/app/heroes/heroes.component.ts" region="delete-hero-subscribe"></code-example>.

Компонент не ожидает результата от операции удаления, поэтому он подписывается без обратного вызова. Даже если вы не используете результат, вы все равно должны подписаться.

Вызов метода `subscribe()` _исполняет_ наблюдаемую, что и инициирует запрос DELETE.

<div class="alert is-important">

Вы должны вызвать `subscribe()`, иначе ничего не произойдет. Просто вызов `HeroesService.deleteHero()` не инициирует запрос DELETE.

</div>

<code-example path="http/src/app/heroes/heroes.component.ts" region="delete-hero-no-subscribe"></code-example>.

### Выполнение PUT-запроса

Приложение может отправлять PUT-запросы, используя клиентскую службу HTTP. Следующий пример `HeroesService`, как и пример POST, заменяет ресурс обновленными данными.

<code-example header="app/heroes/heroes.service.ts (updateHero)" path="http/src/app/heroes/heroes.service.ts" region="updateHero"></code-example>.

Как и для любого из HTTP методов, которые возвращают наблюдаемую, вызывающий `HeroesComponent.update()` [должен `subscribe()`](#always-subscribe 'Почему вы всегда должны подписываться.') на наблюдаемую, возвращенную из `HttpClient.put()` для того, чтобы инициировать запрос.

### Добавление и обновление заголовков

Многие серверы требуют дополнительных заголовков для операций сохранения. Например, сервер может потребовать токен авторизации или заголовок "Content-Type" для явного объявления MIME-типа тела запроса.

##### Добавление заголовков

Служба `HeroesService` определяет такие заголовки в объекте `httpOptions`, который передается каждому методу сохранения `HttpClient`.

<code-example header="app/heroes/heroes.service.ts (httpOptions)" path="http/src/app/heroes/heroes.service.ts" region="http-options"></code-example>

##### Обновление заголовков

Вы не можете напрямую изменить существующие заголовки внутри предыдущего объекта options, поскольку экземпляры класса `HttpHeaders` неизменяемы.

Вместо этого используйте метод `set()`, чтобы вернуть клон текущего экземпляра с новыми изменениями.

В следующем примере показано, как при истечении срока действия старого токена можно обновить заголовок авторизации перед выполнением следующего запроса.

<code-example linenums="false" path="http/src/app/heroes/heroes.service.ts" region="update-headers"></code-example>.

<a id="url-params"></a>

## Настройка параметров URL HTTP

Используйте класс `HttpParams` с параметром запроса `params` для добавления строк запроса URL в ваш `HttpRequest`.

В следующем примере метод `searchHeroes()` запрашивает героев, имена которых содержат поисковый запрос.

Начните с импорта класса `HttpParams`.

<code-example hideCopy language="typescript">

import {HttpParams} from "&commat;angular/common/http";

</code-example>

<code-example linenums="false" path="http/src/app/heroes/heroes.service.ts" region="searchHeroes"></code-example>.

Если есть поисковый запрос, код создает объект options с параметром поиска в HTML URL-кодировке. Например, если термин "cat", то URL GET-запроса будет `api/heroes?name=cat`.

Объект `HttpParams` является неизменяемым. Если вам нужно обновить параметры, сохраните возвращаемое значение метода `.set()`.

Вы также можете создавать параметры HTTP непосредственно из строки запроса, используя переменную `fromString`:

<code-example hideCopy language="typescript">

const params = new HttpParams({fromString: 'name=foo'});

</code-example>

<a id="intercepting-requests-and-responses"></a>

## Перехват запросов и ответов

При перехвате вы объявляете _перехватчики_, которые проверяют и преобразуют HTTP-запросы от вашего приложения к серверу. Эти же перехватчики могут проверять и преобразовывать ответы сервера на обратном пути к приложению.

Несколько перехватчиков образуют _прямую и обратную_ цепочку обработчиков запросов/ответов.

Перехватчики могут выполнять различные _неявные_ задачи, от аутентификации до протоколирования, обычным, стандартным способом для каждого запроса/ответа HTTP.

Без перехвата разработчикам пришлось бы реализовывать эти задачи _явно_ для каждого вызова метода `HttpClient`.

### Написать перехватчик

Для реализации перехватчика объявите класс, который реализует метод `intercept()` интерфейса `HttpInterceptor`.

Вот перехватчик `noop`, который пропускает запрос через себя, не трогая его:

<code-example header="app/http-interceptors/noop-interceptor.ts" path="http/src/app/http-interceptors/noop-interceptor.ts"></code-example>

Метод `intercept` преобразует запрос в `Observable`, который в итоге возвращает HTTP-ответ. В этом смысле каждый перехватчик способен обрабатывать запрос полностью самостоятельно.

Большинство перехватчиков проверяют запрос на входе и передают потенциально измененный запрос в метод `handle()` объекта `next`, который реализует интерфейс [`HttpHandler`](api/common/http/HttpHandler).

<code-example format="javascript" language="javascript">

export abstract class HttpHandler { abstract handle(req: HttpRequest&lt;any&gt;): Observable&lt;HttpEvent&lt;any&gt;&gt;;
}

</code-example>

Как и `intercept()`, метод `handle()` преобразует HTTP-запрос в `Observable` из [`HttpEvents`](#interceptor-events), которые в конечном итоге включают ответ сервера. Метод `intercept()` может проверить эту наблюдаемую и изменить ее, прежде чем вернуть ее вызывающей стороне.

Этот `no-op` перехватчик вызывает `next.handle()` с исходным запросом и возвращает наблюдаемую, ничего не делая.

### Объект `next`

Объект `next` представляет следующий перехватчик в цепочке перехватчиков. Последний `next` в цепочке - это обработчик бэкенда `HttpClient`, который посылает запрос на сервер и получает ответ сервера.

Большинство перехватчиков вызывают `next.handle()`, чтобы запрос перешел к следующему перехватчику и, в конечном счете, к внутреннему обработчику. Перехватчик _может_ пропустить вызов `next.handle()`, замкнуть цепочку и [вернуть свою собственную `Observable`](#caching) с искусственным ответом сервера.

Это распространенный паттерн промежуточного ПО, встречающийся в таких фреймворках, как Express.js.

### Предоставить перехватчик

Перехватчик `NoopInterceptor` - это сервис, управляемый системой [dependency injection (DI)](guide/dependency-injection) Angular. Как и другие сервисы, вы должны предоставить класс перехватчика, прежде чем приложение сможет его использовать.

Поскольку перехватчики являются необязательными зависимостями сервиса `HttpClient`, вы должны предоставлять их в том же инжекторе или в родительском инжекторе, который предоставляет `HttpClient`. Перехватчики, предоставленные _после_ того, как DI создаст `HttpClient`, игнорируются.

Это приложение предоставляет `HttpClient` в корневом инжекторе приложения, как побочный эффект импорта `HttpClientModule` в `AppModule`. Вы также должны предоставить перехватчики в `AppModule`.

После импорта инжекторного маркера `HTTP_INTERCEPTORS` из `@angular/common/http`, напишите провайдер `NoopInterceptor` следующим образом:

<code-example path="http/src/app/http-interceptors/index.ts" region="noop-provider"></code-example>.

Обратите внимание на опцию `multi: true`. Этот обязательный параметр сообщает Angular, что `HTTP_INTERCEPTORS` является маркером для _мультипровайдера_, который вводит массив значений, а не одно значение.

Вы _могли бы_ добавить этот провайдер непосредственно в массив провайдеров `AppModule`. Однако это довольно многословно, и велика вероятность, что вы создадите больше перехватчиков и предоставите их таким же образом.

Вы также должны обратить [пристальное внимание на порядок](#interceptor-order), в котором вы предоставляете эти перехватчики.

Подумайте о создании "бочкового" файла, который собирает все провайдеры перехватчиков в массив `httpInterceptorProviders`, начиная с этого первого, `NoopInterceptor`.

<code-example header="app/http-interceptors/index.ts" path="http/src/app/http-interceptors/index.ts" region="interceptor-providers"></code-example>.

Затем импортируйте и добавьте его в `AppModule` `providers array` следующим образом:

<code-example header="app/app.module.ts (interceptor providers)" path="http/src/app/app.module.ts" region="interceptor-providers"></code-example>.

По мере создания новых перехватчиков, добавляйте их в массив `httpInterceptorProviders`, и вам не придется снова обращаться к `AppModule`.

<div class="alert is-helpful">

В полном коде примера перехватчиков гораздо больше.

</div>

### Порядок перехватчиков

Angular применяет перехватчики в том порядке, в котором вы их предоставляете. Например, рассмотрим ситуацию, в которой вы хотите обрабатывать аутентификацию ваших HTTP-запросов и записывать их в журнал перед отправкой на сервер.

Для выполнения этой задачи вы можете предоставить службу `AuthInterceptor`, а затем службу `LoggingInterceptor`.

Исходящие запросы будут поступать от `AuthInterceptor` к `LoggingInterceptor`.

Ответы на эти запросы будут поступать в обратном направлении, от `LoggingInterceptor` обратно к `AuthInterceptor`.

Ниже представлено визуальное представление этого процесса:

<div class="lightbox">

<img alt="Interceptor in order of HttpClient, AuthInterceptor, AuthInterceptor, HttpBackend, Server, and back in opposite order to show the two-way flow" src="generated/images/guide/http/interceptor-order.svg">

</div>

<div class="alert is-helpful">

Последним перехватчиком в процессе всегда является `HttpBackend`, который обрабатывает связь с сервером.

</div>

Вы не сможете изменить порядок или удалить перехватчики позже. Если вам нужно включать и отключать перехватчик динамически, вам придется встроить эту возможность в сам перехватчик.

<a id="interceptor-events"></a>

### Обработка событий перехватчика

Большинство методов `HttpClient` возвращают наблюдаемые `HttpResponse<any>`. Сам класс `HttpResponse` фактически является событием, тип которого `HttpEventType.Response`.

Однако один HTTP-запрос может генерировать несколько событий других типов, включая события о ходе загрузки и выгрузки.

Методы `HttpInterceptor.intercept()` и `HttpHandler.handle()` возвращают наблюдаемые `HttpEvent<any>`.

Многие перехватчики занимаются только исходящим запросом и возвращают поток событий из `next.handle()`, не изменяя его. Некоторые перехватчики, однако, должны изучить и модифицировать ответ от `next.handle()`; эти операции могут видеть все эти события в потоке.

<a id="immutability"></a>

Хотя перехватчики способны изменять запросы и ответы, свойства экземпляров `HttpRequest` и `HttpResponse` являются `readonly`, что делает их в значительной степени неизменяемыми. Они неизменяемы по веской причине:

Приложение может повторять запрос несколько раз, прежде чем он увенчается успехом, что означает, что цепочка перехватчиков может обрабатывать один и тот же запрос несколько раз.

Если перехватчик может изменить исходный объект запроса, то повторная операция будет начинаться с измененного запроса, а не с исходного.

Неизменность гарантирует, что перехватчики видят один и тот же запрос при каждой попытке.

<div class="alert is-helpful">

Ваш перехватчик должен возвращать каждое событие без изменений, если только у него нет веских причин поступать иначе.

</div>

TypeScript не позволяет устанавливать свойства `HttpRequest` только для чтения.

<code-example format="javascript" language="javascript">

// Typescript запрещает следующее присвоение, поскольку req.url доступен только для чтения req.url = req.url.replace('http://', 'https://');

</code-example>

Если вам необходимо изменить запрос, сначала клонируйте его и измените клон перед передачей его в `next.handle()`. Вы можете клонировать и изменить запрос за один шаг, как показано в следующем примере.

<code-example header="app/http-interceptors/ensure-https-interceptor.ts (excerpt)" path="http/src/app/http-interceptors/ensure-https-interceptor.ts" region="excerpt"></code-example>.

Хэш-аргумент метода `clone()` позволяет вам изменять определенные свойства запроса, копируя остальные.

#### Изменение тела запроса

Защита присваивания `readonly` не может предотвратить глубокие обновления и, в частности, не может помешать вам изменить свойство объекта тела запроса.

<code-example format="javascript" language="javascript">

req.body.name = req.body.name.trim(); // плохая идея!

</code-example>

Если вам необходимо изменить тело запроса, выполните следующие действия.

1.  Скопируйте тело запроса и внесите изменения в копию.

1.  Клонируйте объект запроса, используя его метод `clone()`.

1.  Замените тело клона измененной копией.

<code-example header="app/http-interceptors/trim-name-interceptor.ts (excerpt)" path="http/src/app/http-interceptors/trim-name-interceptor.ts" region="excerpt"></code-example>

#### Очистка тела запроса в клоне

Иногда требуется очистить тело запроса, а не заменить его. Для этого установите для клонированного тела запроса значение `null`.

<div class="alert is-helpful">

**TIP**: <br /> If you set the cloned request body to `undefined`, Angular assumes you intend to leave the body as is.

</div>

<code-example format="javascript" language="javascript">

newReq = req.clone({ &hellip; }); // тело не упоминается =&gt; сохраняем исходное тело newReq = req.clone({ body: undefined }); // сохраняем исходное тело
newReq = req.clone({ body: null }); // очистить тело

</code-example>

## Примеры использования Http-перехватчиков

Ниже перечислены несколько распространенных случаев использования перехватчиков.

### Установка заголовков по умолчанию

Приложения часто используют перехватчик для установки заголовков по умолчанию в исходящих запросах.

В примере приложения есть `AuthService`, который производит токен авторизации. Вот его `AuthInterceptor`, который инжектирует этот сервис для получения токена и добавляет заголовок авторизации с этим токеном к каждому исходящему запросу:

<code-example header="app/http-interceptors/auth-interceptor.ts" path="http/src/app/http-interceptors/auth-interceptor.ts"></code-example>.

Практика клонирования запроса для установки новых заголовков настолько распространена, что для этого существует ярлык `setHeaders`:

<code-example path="http/src/app/http-interceptors/auth-interceptor.ts" region="set-header-shortcut"></code-example>.

Перехватчик, изменяющий заголовки, может быть использован для ряда различных операций, включая:

-   Аутентификация/авторизация

-   Поведение кэширования; например, `If-Modified-Since`.

-   XSRF защита

### Протоколирование пар запроса и ответа

Поскольку перехватчики могут обрабатывать запрос и ответ _вместе_, они могут выполнять такие задачи, как определение времени и протоколирование всей операции HTTP.

Рассмотрим следующий `LoggingInterceptor`, который фиксирует время запроса, время ответа и записывает результат в журнал с указанием прошедшего времени

с внедренным `MessageService`.

<code-example header="app/http-interceptors/logging-interceptor.ts)" path="http/src/app/http-interceptors/logging-interceptor.ts" region="excerpt"></code-example>

Оператор RxJS `tap` фиксирует, был ли запрос успешным или неудачным. Оператор RxJS `finalize` вызывается, когда наблюдаемый ответ либо возвращает ошибку, либо завершается и сообщает о результате в `MessageService`.

Ни `tap`, ни `finalize` не затрагивают значения потока наблюдаемых, возвращаемых вызывающей стороне.

<a id="custom-json-parser"></a>

### Пользовательский парсинг JSON

Перехватчики могут быть использованы для замены встроенного парсинга JSON на пользовательскую реализацию.

Перехватчик `CustomJsonInterceptor` в следующем примере демонстрирует, как этого добиться. Если перехватываемый запрос ожидает ответ в формате `'json'', то `responseType'' изменяется на `'text'', чтобы отключить встроенный парсинг JSON.

Затем ответ разбирается с помощью внедренного `JsonParser`.

<code-example header="app/http-interceptors/custom-json-interceptor.ts" path="http/src/app/http-interceptors/custom-json-interceptor.ts" region="custom-json-interceptor"></code-example>.

Затем вы можете реализовать свой собственный пользовательский `JsonParser`. Вот пользовательский JsonParser, который имеет специальное средство восстановления даты.

<code-example header="app/http-interceptors/custom-json-interceptor.ts" path="http/src/app/http-interceptors/custom-json-interceptor.ts" region="custom-json-parser"></code-example>.

Вы предоставляете `CustomParser` вместе с `CustomJsonInterceptor`.

<code-example header="app/http-interceptors/index.ts" path="http/src/app/http-interceptors/index.ts" region="custom-json-interceptor"></code-example>

<a id="caching"></a>

### Кэширование запросов

Перехватчики могут обрабатывать запросы самостоятельно, без переадресации на `next.handle()`.

Например, вы можете решить кэшировать определенные запросы и ответы для повышения производительности. Вы можете делегировать кэширование перехватчику, не нарушая работу существующих служб данных.

Перехватчик `CachingInterceptor` в следующем примере демонстрирует этот подход.

<code-example header="app/http-interceptors/caching-interceptor.ts)" path="http/src/app/http-interceptors/caching-interceptor.ts" region="v1"></code-example>.

-   Функция `isCacheable()` определяет, является ли запрос кэшируемым.

    В данном примере кэшируемыми являются только GET-запросы к API поиска пакетов.

-   Если запрос не является кэшируемым, перехватчик пересылает запрос следующему обработчику в цепочке.

-   Если кэшируемый запрос найден в кэше, перехватчик возвращает `of()` _observable_ с кэшированным ответом, минуя обработчик `next` и все остальные перехватчики ниже по течению.

-   Если кэшируемый запрос не находится в кэше, код вызывает `sendRequest()`.

    Эта функция передает запрос в `next.handle()`, который в конечном итоге вызывает сервер и возвращает ответ сервера.

<a id="send-request"></a>

<code-example path="http/src/app/http-interceptors/caching-interceptor.ts" region="send-request"></code-example>

<div class="alert is-helpful">

Обратите внимание, как `sendRequest()` перехватывает ответ на обратном пути к приложению. Этот метод передает ответ через оператор `tap()`, обратный вызов которого добавляет ответ в кэш.

Исходный ответ продолжает нетронутым возвращаться по цепочке перехватчиков к вызывающему приложению.

Службы данных, такие как `PackageSearchService`, не знают, что некоторые из их запросов `HttpClient` на самом деле возвращают кэшированные ответы.

</div>

<a id="cache-refresh"></a>

### Использование перехватчиков для запроса нескольких значений

Метод `HttpClient.get()` обычно возвращает наблюдаемую, которая выдает одно значение, либо данные, либо ошибку. Перехватчик может изменить это на наблюдаемую, которая выдает [несколько значений](guide/observables).

Следующая измененная версия `CachingInterceptor` по желанию возвращает наблюдаемую, которая немедленно выдает кэшированный ответ, посылает запрос API поиска пакетов и выдает его позже с обновленными результатами поиска.

<code-example path="http/src/app/http-interceptors/caching-interceptor.ts" region="intercept-refresh"></code-example>.

<div class="alert is-helpful">

Опция _cache-then-refresh_ срабатывает при наличии пользовательского заголовка `x-refresh`.

Флажок на `PackageSearchComponent` устанавливает флаг `withRefresh`, который является одним из аргументов метода `PackageSearchService.search()`. Этот метод `search()` создает пользовательский заголовок `x-refresh` и добавляет его в запрос перед вызовом `HttpClient.get()`.

</div>

Переработанный `CachingInterceptor` устанавливает запрос на сервер независимо от того, есть ли кэшированное значение или нет, используя тот же метод `sendRequest()`, который описан [выше] (#send-request). Наблюдаемая `results$` выполняет запрос при подписке.

-   Если кэшированного значения нет, перехватчик возвращает `results$`.

-   Если кэшированное значение есть, код _переводит_ кэшированный ответ на `results$`. В результате получается перекомпонованная наблюдаемая, которая испускает два ответа, поэтому подписчики будут видеть последовательность этих двух ответов:

-   Кэшированный ответ, который выдается немедленно.

-   Ответ от сервера, который выдается позже.

<a id="report-progress"></a>

## Отслеживание и отображение хода выполнения запроса

Иногда приложения передают большие объемы данных, и такая передача может занять много времени. Загрузка файлов - типичный пример.

Вы можете улучшить работу пользователей, предоставив им обратную связь о ходе выполнения таких передач.

Чтобы сделать запрос с включенными событиями прогресса, создайте экземпляр `HttpRequest` с опцией `reportProgress`, установленной в true, чтобы включить отслеживание событий прогресса.

<code-example header="app/uploader/uploader.service.ts (запрос на загрузку)" path="http/src/app/uploader/uploader.service.ts" region="upload-request"></code-example>.

<div class="alert is-important">

**TIP**: <br /> Every progress event triggers change detection, so only turn them on if you need to report progress in the UI.

When using [`HttpClient.request()`](api/common/http/HttpClient#request) with an HTTP method, configure the method with [`observe: 'events'`](api/common/http/HttpClient#request) to see all events, including the progress of transfers.

</div>

Затем передайте этот объект запроса методу `HttpClient.request()`, который возвращает `Observable` из `HttpEvents` \ (те же события, обрабатываемые [перехватчиками](#interceptor-events)\).

<code-example header="app/uploader/uploader.service.ts (upload body)" path="http/src/app/uploader/uploader.service.ts" region="upload-body"></code-example>.

Метод `getEventMessage` интерпретирует каждый тип `HttpEvent` в потоке событий.

<code-example header="app/uploader/uploader.service.ts (getEventMessage)" path="http/src/app/uploader/uploader.service.ts" region="getEventMessage"></code-example>

<div class="alert is-helpful">

В примере приложения для этого руководства нет сервера, принимающего загруженные файлы. Перехватчик `UploadInterceptor` в `app/http-interceptors/upload-interceptor.ts` перехватывает и сокращает запросы на загрузку, возвращая наблюдаемую таблицу симулированных событий.

</div>

## Оптимизация взаимодействия с сервером с помощью дебаунсинга

Если вам нужно сделать HTTP-запрос в ответ на ввод пользователя, неэффективно посылать запрос на каждое нажатие клавиши. Лучше подождать, пока пользователь перестанет набирать текст, а затем отправить запрос.

Эта техника известна как дебаунсинг.

Рассмотрим следующий шаблон, который позволяет пользователю ввести поисковый запрос, чтобы найти пакет по имени. Когда пользователь вводит имя в поле поиска, `PackageSearchComponent` отправляет запрос на поиск пакета с таким именем в API поиска пакетов.

<code-example header="app/package-search/package-search.component.html (search)" path="http/src/app/package-search/package-search.component.html" region="search"></code-example>.

Здесь привязка события `keyup` отправляет каждое нажатие клавиши в метод `search()` компонента.

<div class="alert is-helpful">

Тип `$event.target` в шаблоне только `EventTarget`. В методе `getValue()` цель приводится к `HTMLInputElement`, чтобы type-safe имел доступ к ее свойству `value`.

<code-example path="http/src/app/package-search/package-search.component.ts" region="getValue"></code-example>.

</div>

Следующий фрагмент реализует дебаггинг для этого входа с помощью операторов RxJS.

<code-example header="app/package-search/package-search.component.ts (excerpt)" path="http/src/app/package-search/package-search.component.ts" region="debounce"></code-example>.

Текст `searchText$` - это последовательность значений поля поиска, поступающих от пользователя. Он определен как RxJS `Subject`, что означает, что это многоадресный `Observable`, который также может выдавать значения для себя, вызывая `next(value)`, как это происходит в методе `search()`.

Вместо того, чтобы направлять каждое значение `searchText` непосредственно в инжектированный `PackageSearchService`, код в `ngOnInit()` направляет значения поиска через три оператора, так что значение поиска достигает сервиса, только если это новое значение и пользователь остановил ввод.

| Операторы RxJS | Подробности | | | :----------------------- | :------------------------------------------------------------------ | |

| `debounceTime(500)` | Ждать, пока пользователь перестанет набирать текст, что в данном случае составляет 1/2 секунды. |

| `distinctUntilChanged()` | Подождите, пока текст поиска не изменится. |

| | `switchMap()` | Отправляем запрос на поиск в службу. |

Код устанавливает `packages$` в этот перекомпонованный `Observable` результатов поиска. Шаблон подписывается на `packages$` с помощью [AsyncPipe](api/common/AsyncPipe) и отображает результаты поиска по мере их поступления.

<div class="alert is-helpful">

Подробнее об опции `withRefresh` смотрите в [Использование перехватчиков для запроса нескольких значений](#cache-refresh).

</div>

### Использование оператора `switchMap()`

Оператор `switchMap()` принимает аргумент функции, которая возвращает `Observable`. В примере `PackageSearchService.search` возвращает `Observable`, как и другие методы службы данных.

Если предыдущий запрос на поиск все еще находится в полете, например, при плохом сетевом соединении, оператор отменяет этот запрос и посылает новый.

<div class="alert is-helpful">

**NOTE**: <br /> `switchMap()` returns service responses in their original request order, even if the server returns them out of order.

</div>

<div class="alert is-helpful">

Если вы думаете, что будете использовать эту логику дебаггинга повторно, подумайте о том, чтобы перенести ее в служебную функцию или в сам `PackageSearchService`.

</div>

## Безопасность: Защита от XSRF

[Cross-Site Request Forgery (XSRF или CSRF)](https://en.wikipedia.org/wiki/Cross-site_request_forgery) - это техника атаки, с помощью которой злоумышленник может обманом заставить аутентифицированного пользователя неосознанно выполнить действия на вашем сайте. `HttpClient` поддерживает [общий механизм](https://en.wikipedia.org/wiki/Cross-site_request_forgery#Cookie-to-header_token), используемый для предотвращения XSRF-атак.

При выполнении HTTP-запросов перехватчик считывает маркер из cookie, по умолчанию `XSRF-TOKEN`, и устанавливает его в качестве HTTP-заголовка `X-XSRF-TOKEN`.

Поскольку прочитать cookie может только код, работающий на вашем домене, бэкенд может быть уверен, что HTTP-запрос пришел от вашего клиентского приложения, а не от злоумышленника.

По умолчанию перехватчик отправляет этот заголовок на все мутирующие запросы\(такие как POST\) к относительным URL, но не на GET/HEAD запросы или на запросы с абсолютным URL.

Чтобы воспользоваться этим преимуществом, ваш сервер должен установить маркер в JavaScript-читаемой сессионной cookie под названием `XSRF-TOKEN` либо при загрузке страницы, либо при первом GET-запросе. При последующих запросах сервер может проверить, что cookie соответствует HTTP-заголовку `X-XSRF-TOKEN`, и таким образом быть уверенным, что запрос мог отправить только код, запущенный на вашем домене.

Токен должен быть уникальным для каждого пользователя и проверяться сервером; это не позволит клиенту придумывать свои собственные токены.

Для повышения безопасности установите в качестве маркера дайджест cookie аутентификации вашего сайта с солью.

Для предотвращения коллизий в средах, где несколько приложений Angular используют один и тот же домен или поддомен, присвойте каждому приложению уникальное имя cookie.

<div class="alert is-important">

_`HttpClient` поддерживает только клиентскую половину схемы защиты XSRF._ Ваш внутренний сервис должен быть настроен на установку cookie для вашей страницы, а также на проверку наличия заголовка во всех подходящих запросах.
Если этого не сделать, защита Angular по умолчанию станет неэффективной.

</div>

### Настройка пользовательских имен куки/заголовков

Если ваш внутренний сервис использует другие имена для куки или заголовков токенов XSRF, используйте `HttpClientXsrfModule.withOptions()` для переопределения значений по умолчанию.

<code-example path="http/src/app/app.module.ts" region="xsrf"></code-example>

<a id="testing-requests"></a>

## Тестирование HTTP-запросов

Как и для любой внешней зависимости, вы должны подражать HTTP-бэкенду, чтобы ваши тесты могли имитировать взаимодействие с удаленным сервером. Библиотека `@angular/common/http/testing` позволяет легко настроить такое моделирование.

Библиотека тестирования HTTP в Angular предназначена для модели тестирования, в которой приложение сначала выполняет код и делает запросы. Затем тест ожидает, что определенные запросы были или не были сделаны, выполняет утверждения против этих запросов и, наконец, предоставляет ответы путем "промывки" каждого ожидаемого запроса.

В конце тесты могут проверить, что приложение не делало неожиданных запросов.

<div class="alert is-helpful">

Вы можете запустить <live-example stackblitz="specs">эти примеры тестов</live-example> в живой среде кодирования.

Тесты, описанные в этом руководстве, находятся в `src/testing/http-client.spec.ts`. Также в `src/app/heroes/heroes.service.spec.ts` находятся тесты сервиса данных приложения, которые вызывают `HttpClient`.

</div>

### Настройка для тестирования

Чтобы начать тестирование вызовов `HttpClient`, импортируйте `HttpClientTestingModule` и мокинг-контроллер `HttpTestingController`, а также другие символы, необходимые вашим тестам.

<code-example header="app/testing/http-client.spec.ts (imports)" path="http/src/testing/http-client.spec.ts" region="imports"></code-example>.

Затем добавьте `HttpClientTestingModule` в `TestBed` и продолжите настройку тестируемого сервиса.

<code-example header="app/testing/http-client.spec.ts(setup)" path="http/src/testing/http-client.spec.ts" region="setup"></code-example>.

Теперь запросы, сделанные в ходе тестирования, попадают на тестирующий бэкенд вместо обычного бэкенда.

Эта установка также вызывает `TestBed.inject()` для инъекции сервиса `HttpClient` и контроллера мокинга, чтобы на них можно было ссылаться во время тестирования.

### Ожидание и ответ на запросы

Теперь вы можете написать тест, который ожидает появления GET-запроса и предоставляет имитационный ответ.

<code-example header="app/testing/http-client.spec.ts (HttpClient.get)" path="http/src/testing/http-client.spec.ts" region="get-test"></code-example>.

Последний шаг, проверяющий, что ни один запрос не остался невыполненным, является достаточно распространенным, чтобы перенести его в шаг `afterEach()`:

<code-example path="http/src/testing/http-client.spec.ts" region="afterEach"></code-example>

#### Ожидания пользовательских запросов

Если сопоставление по URL недостаточно, можно реализовать собственную функцию сопоставления. Например, вы можете искать исходящий запрос, содержащий заголовок авторизации:

<code-example path="http/src/testing/http-client.spec.ts" region="predicate"></code-example>.

Как и в случае с предыдущим `expectOne()`, тест завершается неудачно, если 0 или 2+ запросов удовлетворяют этому предикату.

#### Обработка более чем одного запроса

Если вам нужно ответить на дублирующиеся запросы в вашем тесте, используйте API `match()` вместо `expectOne()`. Он принимает те же аргументы, но возвращает массив совпадающих запросов.

После возврата эти запросы удаляются из будущего поиска, и вы несете ответственность за их очистку и проверку.

<code-example path="http/src/testing/http-client.spec.ts" region="multi-request"></code-example>.

### Тестирование на ошибки

Вы должны протестировать защиту приложения от HTTP-запросов, которые не выполняются.

Вызовите `request.flush()` с сообщением об ошибке, как показано в следующем примере.

<code-example path="http/src/testing/http-client.spec.ts" region="404"></code-example>.

В качестве альтернативы, вызовите `request.error()` с `ProgressEvent`.

<code-example path="http/src/testing/http-client.spec.ts" region="network-error"></code-example>

## Передача метаданных перехватчикам

Многие перехватчики требуют или получают пользу от конфигурации. Рассмотрим перехватчик, который повторяет неудачные запросы.

По умолчанию перехватчик может повторить запрос три раза, но вы можете захотеть изменить это количество повторных попыток для особенно подверженных ошибкам или чувствительных запросов.

Запросы `HttpClient` содержат _контекст_, который может содержать метаданные о запросе. Этот контекст доступен для перехватчиков для чтения или изменения, хотя он не передается на внутренний сервер при отправке запроса.

Это позволяет приложениям или другим перехватчикам помечать запросы параметрами конфигурации, например, сколько раз повторять запрос.

### Создание контекстного маркера

Angular хранит и извлекает значение в контексте с помощью `HttpContextToken`. Вы можете создать контекстный токен с помощью оператора `new`, как в следующем примере:

<code-example header="создание контекстного токена" path="http/src/app/http-interceptors/retry-interceptor.ts" region="context-token"></code-example>.

Лямбда-функция `() => 3`, переданная во время создания `HttpContextToken`, служит двум целям:

1.  Она позволяет TypeScript определить тип этого токена:

    `HttpContextToken<number>`.

    Контекст запроса безопасен для типов &mdash; чтение токена из контекста запроса возвращает значение соответствующего типа.

1.  Он устанавливает значение по умолчанию для токена.

    Это значение, которое возвращает контекст запроса, если для этого маркера не было задано никакого другого значения.

    Использование значения по умолчанию избавляет от необходимости проверять, установлено ли конкретное значение.

### Установка значений контекста при выполнении запроса

При выполнении запроса вы можете предоставить экземпляр `HttpContext`, в котором уже заданы значения контекста.

<code-example header="setting context values" path="http/src/app/http-interceptors/retry-interceptor.ts" region="set-context"></code-example>

### Чтение значений контекста в перехватчике

Внутри перехватчика вы можете прочитать значение токена в контексте данного запроса с помощью `HttpContext.get()`. Если вы явно не задали значение для маркера, Angular возвращает значение по умолчанию, указанное в маркере.

<code-example header="чтение значений контекста в перехватчике" path="http/src/app/http-interceptors/retry-interceptor.ts" region="reading-context"></code-example>.

### Контексты являются изменяемыми

В отличие от большинства других аспектов экземпляров `HttpRequest`, контекст запроса является изменяемым и сохраняется при других неизменяемых преобразованиях запроса. Это позволяет перехватчикам координировать операции через контекст.

Например, пример `RetryInterceptor` может использовать второй токен контекста для отслеживания количества ошибок, возникающих во время выполнения данного запроса:

<code-example header="координация операций через контекст" path="http/src/app/http-interceptors/retry-interceptor.ts" region="mutable-context"></code-example>.

<!-- links -->

<!-- external links -->

<!-- end links -->

:date: 28.02.2022
