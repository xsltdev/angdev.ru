# HTTP-клиент — Тестовые запросы

:date: 14.11.2022

Как и для любой другой внешней зависимости, вы должны подражать HTTP-бэкенду, чтобы ваши тесты могли имитировать взаимодействие с удаленным сервером. Библиотека `@angular/common/http/testing` позволяет легко настроить такое моделирование.

## Библиотека HTTP-тестирования

Библиотека тестирования HTTP в Angular предназначена для модели тестирования, при которой приложение сначала выполняет код и делает запросы. Затем тест ожидает, что определенные запросы были или не были сделаны, выполняет утверждения против этих запросов и, наконец, предоставляет ответы путем "промывки" каждого ожидаемого запроса.

В конце тесты могут проверить, что приложение не делало неожиданных запросов.

!!!note ""

    Вы можете запустить [эти примеры тестов](https://angular.io/generated/live-examples/http-test-requests/specs.stackblitz.html) в живой среде кодирования.

    Тесты, описанные в этом руководстве, находятся в `src/testing/http-client.spec.ts`. Также в `src/app/heroes/heroes.service.spec.ts` находятся тесты сервиса данных приложения, которые вызывают `HttpClient`.

## Настройка для тестирования

Чтобы начать тестирование вызовов `HttpClient`, импортируйте `HttpClientTestingModule` и мокинг-контроллер `HttpTestingController`, а также другие символы, необходимые вашим тестам.

```ts
// Http testing module and mocking controller
import {
    HttpClientTestingModule,
    HttpTestingController,
} from '@angular/common/http/testing';

// Other imports
import { TestBed } from '@angular/core/testing';
import {
    HttpClient,
    HttpErrorResponse,
} from '@angular/common/http';
```

Затем добавьте `HttpClientTestingModule` в `TestBed` и продолжите настройку _тестируемого сервиса_.

```ts
describe('HttpClient testing', () => {
    let httpClient: HttpClient;
    let httpTestingController: HttpTestingController;

    beforeEach(() => {
        TestBed.configureTestingModule({
            imports: [HttpClientTestingModule],
        });

        // Inject the http service and test controller for each test
        httpClient = TestBed.inject(HttpClient);
        httpTestingController = TestBed.inject(
            HttpTestingController
        );
    });
    /// Tests begin ///
});
```

Теперь запросы, сделанные в ходе тестирования, попадают на тестирующий бэкенд вместо обычного бэкенда.

Эта установка также вызывает `TestBed.inject()` для инъекции сервиса `HttpClient` и контроллера мокинга, чтобы на них можно было ссылаться во время тестирования.

## Ожидать и отвечать на запросы

Теперь вы можете написать тест, который ожидает появления GET-запроса и предоставляет имитационный ответ.

```ts
it('can test HttpClient.get', () => {
    const testData: Data = { name: 'Test Data' };

    // Make an HTTP GET request
    httpClient.get<Data>(testUrl).subscribe((data) =>
        // When observable resolves, result should match test data
        expect(data).toEqual(testData)
    );

    // The following `expectOne()` will match the request's URL.
    // If no requests or multiple requests matched that URL
    // `expectOne()` would throw.
    const req = httpTestingController.expectOne('/data');

    // Assert that the request is a GET.
    expect(req.request.method).toEqual('GET');

    // Respond with mock data, causing Observable to resolve.
    // Subscribe callback asserts that correct data was returned.
    req.flush(testData);

    // Finally, assert that there are no outstanding requests.
    httpTestingController.verify();
});
```

Последний шаг, проверяющий, что ни один запрос не остался невыполненным, является достаточно распространенным, чтобы перенести его в шаг `afterEach()`:

```ts
afterEach(() => {
    // After every test, assert that there are no more pending requests.
    httpTestingController.verify();
});
```

### Ожидания пользовательских запросов

Если сопоставление по URL недостаточно, можно реализовать собственную функцию сопоставления. Например, вы можете искать исходящий запрос с заголовком авторизации:

```ts
// Expect one request with an authorization header
const req = httpTestingController.expectOne((request) =>
    request.headers.has('Authorization')
);
```

Как и в предыдущем `expectOne()`, тест завершается неудачно, если 0 или 2+ запросов удовлетворяют этому предикату.

### Обработка более чем одного запроса

Если вам нужно ответить на дублирующиеся запросы в вашем тесте, используйте API `match()` вместо `expectOne()`. Он принимает те же аргументы, но возвращает массив совпадающих запросов.

После возврата эти запросы удаляются из будущего поиска, и вы несете ответственность за их очистку и проверку.

```ts
// get all pending requests that match the given URL
const requests = httpTestingController.match(testUrl);
expect(requests.length).toEqual(3);

// Respond to each request with different results
requests[0].flush([]);
requests[1].flush([testData[0]]);
requests[2].flush(testData);
```

## Тест на ошибки

Вы должны проверить защиту приложения от неудачных HTTP-запросов.

Вызовите `request.flush()` с сообщением об ошибке, как показано в следующем примере.

```ts
it('can test for 404 error', () => {
    const emsg = 'deliberate 404 error';

    httpClient.get<Data[]>(testUrl).subscribe({
        next: () =>
            fail('should have failed with the 404 error'),
        error: (error: HttpErrorResponse) => {
            expect(error.status)
                .withContext('status')
                .toEqual(404);
            expect(error.error)
                .withContext('message')
                .toEqual(emsg);
        },
    });

    const req = httpTestingController.expectOne(testUrl);

    // Respond with mock error
    req.flush(emsg, {
        status: 404,
        statusText: 'Not Found',
    });
});
```

В качестве альтернативы, вызовите `request.error()` с `ProgressEvent`.

```ts
it('can test for network error', (done) => {
    // Create mock ProgressEvent with type `error`, raised when something goes wrong
    // at network level. e.g. Connection timeout, DNS error, offline, etc.
    const mockError = new ProgressEvent('error');

    httpClient.get<Data[]>(testUrl).subscribe({
        next: () =>
            fail(
                'should have failed with the network error'
            ),
        error: (error: HttpErrorResponse) => {
            expect(error.error).toBe(mockError);
            done();
        },
    });

    const req = httpTestingController.expectOne(testUrl);

    // Respond with mock error
    req.error(mockError);
});
```
