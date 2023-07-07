# HTTP: Запрос данных с сервера

:date: 27.02.2023

Используйте метод [`HttpClient.get()`](https://angular.io/api/common/http/HttpClient#get) для получения данных с сервера. Асинхронный метод посылает HTTP-запрос и возвращает Observable, который выдает запрошенные данные при получении ответа.

Тип возвращаемых данных зависит от значений `observe` и `responseType`, которые вы передаете в вызов.

Метод `get()` принимает два аргумента: URL конечной точки, с которой нужно получить данные, и объект _options_, который используется для настройки запроса.

```ts
options: {
  headers?: HttpHeaders | {[header: string]: string | string[]},
  observe?: 'body' | 'events' | 'response',
  params?: HttpParams|{[param: string]: string | number | boolean | ReadonlyArray<string | number | boolean>},
  reportProgress?: boolean,
  responseType?: 'arraybuffer'|'blob'|'json'|'text',
  withCredentials?: boolean,
}
```

Важные параметры включают свойства _observe_ и _responseType_.

-   Параметр _observe_ определяет, какую часть ответа возвращать.
-   Параметр _responseType_ определяет формат, в котором будут возвращаться данные

!!!note ""

    Используйте объект `options` для настройки различных других аспектов исходящего запроса. Например, при добавлении заголовков служба устанавливает заголовки по умолчанию, используя свойство `headers`.

    Используйте свойство `params` для настройки запроса с параметрами HTTP URL, а также опцию `reportProgress` для прослушивания событий о ходе выполнения при передаче больших объемов данных.

Приложения часто запрашивают JSON-данные с сервера. В примере `ConfigService` приложению нужен файл конфигурации на сервере, `config.json`, в котором указаны URL-адреса ресурсов.

```json
{
    "heroesUrl": "api/heroes",
    "textfile": "assets/textfile.txt",
    "date": "2020-01-29"
}
```

Чтобы получить такие данные, вызов `get()` должен содержать следующие параметры: `{observe: 'body', responseType: 'json'}`. Это значения по умолчанию для этих опций, поэтому в следующих примерах объект options не передается.

В последующих разделах показаны некоторые дополнительные возможности опций.

Пример соответствует лучшим практикам создания масштабируемых решений путем определения повторно используемого [injectable service](glossary.md#service) для выполнения функциональности обработки данных. В дополнение к получению данных, сервис может пост-обработать данные, добавить обработку ошибок и логику повторных попыток.

Служба `ConfigService` получает этот файл с помощью метода `HttpClient.get()`.

```ts
configUrl = 'assets/config.json';

getConfig() {
  return this.http.get<Config>(this.configUrl);
}
```

Компонент `ConfigComponent` инжектирует `ConfigService` и вызывает метод сервиса `getConfig`.

Поскольку метод сервиса возвращает `Observable` данных конфигурации, компонент _подписывается_ на возвращаемое значение метода. Обратный вызов подписки выполняет минимальную постобработку.

Он копирует поля данных в объект `config` компонента, который привязывается к данным в шаблоне компонента для отображения.

```ts
showConfig() {
  this.configService.getConfig()
    .subscribe((data: Config) => this.config = {
        heroesUrl: data.heroesUrl,
        textfile:  data.textfile,
        date: data.date,
    });
}
```

## Начало запроса {: #always-subscribe}

Для всех методов `HttpClient`, метод не начинает свой HTTP запрос, пока вы не вызовете `subscribe()` на наблюдаемой, которую возвращает метод.

Это верно для _всех_ `HttpClient` _методов_.

!!!note ""

    Вы всегда должны отписываться от наблюдаемого компонента, когда компонент уничтожается.

Все наблюдаемые, возвращаемые из методов `HttpClient`, по своей конструкции являются _холодными_. Выполнение HTTP-запроса _отложено_, что позволяет вам расширить наблюдаемую таблицу дополнительными операциями, такими как `tap` и `catchError`, прежде чем что-то произойдет.

Вызов `subscribe()` запускает выполнение наблюдаемой таблицы и заставляет `HttpClient` составить и отправить HTTP-запрос на сервер.

Рассматривайте эти наблюдаемые как _блюпринты_ для реальных HTTP-запросов.

!!!note ""

    Фактически, каждая `subscribe()` инициирует отдельное, независимое выполнение наблюдаемой. Подписка дважды приводит к двум HTTP-запросам.

    ```js
    const req = http.get<Heroes>('/api/heroes');
    // 0 requests made - .subscribe() not called.
    req.subscribe();
    // 1 request made.
    req.subscribe();
    // 2 requests made.
    ```

## Запрос типизированного ответа {: #typed-response}

Структурируйте ваш запрос `HttpClient`, чтобы объявить тип объекта ответа, чтобы сделать потребление вывода более простым и очевидным. Указание типа ответа действует как утверждение типа во время компиляции.

!!!warning ""

    Указание типа ответа - это заявление TypeScript о том, что он должен рассматривать ваш ответ как объект данного типа. Это проверка во время сборки и не гарантирует, что сервер действительно ответит объектом данного типа.
    Сервер должен убедиться, что в ответ будет получен тип, указанный API сервера.

Чтобы задать тип объекта ответа, сначала определите интерфейс с необходимыми свойствами. Используйте интерфейс, а не класс, потому что ответ - это обычный объект, который не может быть автоматически преобразован в экземпляр класса.

```ts
export interface Config {
    heroesUrl: string;
    textfile: string;
    date: any;
}
```

Затем укажите этот интерфейс в качестве параметра типа вызова `HttpClient.get()` в сервисе.

```ts
getConfig() {
  // now returns an Observable of Config
  return this.http.get<Config>(this.configUrl);
}
```

!!!node ""

    Когда вы передаете интерфейс в качестве параметра типа в метод `HttpClient.get()`, используйте оператор [RxJS `map`](rx-library.md#operators) для преобразования данных ответа в соответствии с требованиями пользовательского интерфейса. Затем вы можете передать преобразованные данные в [async pipe](https://angular.io/api/common/AsyncPipe).

Обратный вызов в методе обновленного компонента получает типизированный объект данных, который проще и безопаснее потреблять:

```ts
config: Config | undefined;

showConfig() {
  this.configService.getConfig()
    // clone the data object, using its known Config shape
    .subscribe((data: Config) => this.config = { ...data });
}
```

Чтобы получить доступ к свойствам, определенным в интерфейсе, вы должны явно преобразовать простой объект, полученный из JSON, в требуемый тип ответа. Например, следующий обратный вызов `subscribe` получает `data` как Object, а затем преобразует его в тип, чтобы получить доступ к свойствам.

```ts
.subscribe(data => this.config = {
  heroesUrl: (data as any).heroesUrl,
  textfile:  (data as any).textfile,
});
```

!!!warning "`observe` и `response` типы"

    Типы опций `observe` и `response` являются _строковыми союзами_, а не обычными строками.

    ```ts
    options: {
    …
    observe?: 'body' | 'events' | 'response',
    …
    responseType?: 'arraybuffer'|'blob'|'json'|'text',
    …
    }
    ```

    Это может привести к путанице. Например:

    ```ts
    // this works
    client.get('/foo', { responseType: 'text' });

    // but this does NOT work
    const options = {
    	responseType: 'text',
    };
    client.get('/foo', options);
    ```

    Во втором случае TypeScript определяет тип `options` как `{responseType: string}`. Этот тип слишком широк, чтобы передать его в `HttpClient.get`, который ожидает, что тип `responseType` будет одной из _специфических_ строк.
    `HttpClient` явно типизирован таким образом, чтобы компилятор мог сообщить правильный возвращаемый тип на основе предоставленных вами опций.

    Используйте `as const`, чтобы дать понять TypeScript, что вы действительно хотите использовать постоянный тип строки:

    ```ts
    const options = {
    	responseType: 'text' as const,
    };
    client.get('/foo', options);
    ```

## Чтение полного ответа

В предыдущем примере вызов `HttpClient.get()` не указывал никаких опций. По умолчанию он возвращает данные в формате JSON, содержащиеся в теле ответа.

Вам может понадобиться больше информации о транзакции, чем содержится в теле ответа. Иногда серверы возвращают специальные заголовки или коды состояния для указания определенных условий, важных для рабочего процесса приложения.

Сообщите `HttpClient`, что вам нужен полный ответ с помощью опции `observe` метода `get()`:

```ts
getConfigResponse(): Observable<HttpResponse<Config>> {
  return this.http.get<Config>(
    this.configUrl, { observe: 'response' });
}
```

Теперь `HttpClient.get()` возвращает `Observable` типа `HttpResponse`, а не просто JSON данные, содержащиеся в теле.

Метод компонента `showConfigResponse()` отображает заголовки ответа, а также конфигурацию:

```ts
showConfigResponse() {
  this.configService.getConfigResponse()
    // resp is of type `HttpResponse<Config>`
    .subscribe(resp => {
      // display its headers
      const keys = resp.headers.keys();
      this.headers = keys.map(key =>
        `${key}: ${resp.headers.get(key)}`);

      // access the body directly, which is typed as `Config`.
      this.config = { ...resp.body! };
    });
}
```

Как вы можете видеть, объект ответа имеет свойство `body` правильного типа.
