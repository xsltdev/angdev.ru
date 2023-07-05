# Тестирование сервисов

:date: 28.02.2022

Чтобы проверить, что ваши сервисы работают так, как вы задумали, вы можете написать тесты специально для них.

!!!note ""

    Если вы хотите поэкспериментировать с приложением, которое описано в этом руководстве, [запустите его в браузере](https://angular.io/generated/live-examples/testing/stackblitz.html) или скачайте и запустите его локально.

Сервисы часто являются самыми гладкими файлами для модульного тестирования. Вот несколько синхронных и асинхронных модульных тестов `ValueService`, написанных без помощи утилит тестирования Angular.

```ts
// Straight Jasmine testing without Angular's testing support
describe('ValueService', () => {
    let service: ValueService;
    beforeEach(() => {
        service = new ValueService();
    });

    it('#getValue should return real value', () => {
        expect(service.getValue()).toBe('real value');
    });

    it('#getObservableValue should return value from observable', (done: DoneFn) => {
        service.getObservableValue().subscribe((value) => {
            expect(value).toBe('observable value');
            done();
        });
    });

    it('#getPromiseValue should return value from a promise', (done: DoneFn) => {
        service.getPromiseValue().then((value) => {
            expect(value).toBe('promise value');
            done();
        });
    });
});
```

## Сервисы с зависимостями {: #services-with-dependencies}

Сервисы часто зависят от других сервисов, которые Angular инжектирует в конструктор. Во многих случаях вы можете создать и _инжектировать_ эти зависимости вручную при вызове конструктора сервиса.

Простым примером является `MasterService`:

```ts
@Injectable()
export class MasterService {
    constructor(private valueService: ValueService) {}
    getValue() {
        return this.valueService.getValue();
    }
}
```

`MasterService` делегирует свой единственный метод, `getValue`, инжектированному `ValueService`.

Вот несколько способов проверить это.

```ts
describe('MasterService without Angular testing support', () => {
    let masterService: MasterService;

    it('#getValue should return real value from the real service', () => {
        masterService = new MasterService(
            new ValueService()
        );
        expect(masterService.getValue()).toBe('real value');
    });

    it('#getValue should return faked value from a fakeService', () => {
        masterService = new MasterService(
            new FakeValueService()
        );
        expect(masterService.getValue()).toBe(
            'faked service value'
        );
    });

    it('#getValue should return faked value from a fake object', () => {
        const fake = { getValue: () => 'fake value' };
        masterService = new MasterService(
            fake as ValueService
        );
        expect(masterService.getValue()).toBe('fake value');
    });

    it('#getValue should return stubbed value from a spy', () => {
        // create `getValue` spy on an object representing the ValueService
        const valueServiceSpy = jasmine.createSpyObj(
            'ValueService',
            ['getValue']
        );

        // set the value to return when the `getValue` spy is called.
        const stubValue = 'stub value';
        valueServiceSpy.getValue.and.returnValue(stubValue);

        masterService = new MasterService(valueServiceSpy);

        expect(masterService.getValue())
            .withContext('service returned stub value')
            .toBe(stubValue);
        expect(valueServiceSpy.getValue.calls.count())
            .withContext('spy method was called once')
            .toBe(1);
        expect(
            valueServiceSpy.getValue.calls.mostRecent()
                .returnValue
        ).toBe(stubValue);
    });
});
```

Первый тест создает `ValueService` с `new` и передает его в конструктор `MasterService`.

Однако инжектирование реального сервиса редко работает хорошо, поскольку большинство зависимых сервисов сложно создавать и контролировать.

Вместо этого высмеивайте зависимость, используйте фиктивное значение или создайте [spy](https://jasmine.github.io/tutorials/your_first_suite#section-Spies) на соответствующем методе сервиса.

!!!note

    Предпочитает шпионов, так как они, как правило, лучший способ поиздеваться над службами.

Эти стандартные методы тестирования отлично подходят для модульного тестирования сервисов в изоляции.

Однако вы почти всегда внедряете сервисы в классы приложения, используя инъекцию зависимостей Angular, и у вас должны быть тесты, отражающие эту модель использования. Утилиты тестирования Angular позволяют легко исследовать поведение внедренных сервисов.

## Тестирование сервисов с помощью `TestBed`.

Ваше приложение полагается на Angular [dependency injection (DI)](dependency-injection.md) для создания сервисов. Когда у сервиса есть зависимый сервис, DI находит или создает этот зависимый сервис.

А если у этого зависимого сервиса есть свои собственные зависимости, DI находит или создает и их.

Как _потребитель_ сервиса, вы не беспокоитесь ни о чем из этого. Вас не волнует порядок аргументов конструктора или то, как они создаются.

Как _тестер_ сервисов, вы должны, по крайней мере, думать о первом уровне зависимостей сервисов, но вы _можете_ позволить Angular DI сделать создание сервиса и разобраться с порядком аргументов конструктора, если используете утилиту тестирования `TestBed` для предоставления и создания сервисов.

## Angular `TestBed` {: #testbed}

`TestBed` является наиболее важной из утилит тестирования Angular. В `TestBed` создается динамически конструируемый модуль Angular _test_, который эмулирует модуль Angular [@NgModule](ngmodules.md).

Метод `TestBed.configureTestingModule()` принимает объект метаданных, который может иметь большинство свойств [@NgModule](ngmodules.md).

Чтобы протестировать сервис, вы задаете свойство метаданных `providers` с массивом сервисов, которые вы будете тестировать или имитировать.

```ts
let service: ValueService;

beforeEach(() => {
    TestBed.configureTestingModule({
        providers: [ValueService],
    });
});
```

Затем внедрите его внутрь теста, вызвав `TestBed.inject()` с классом сервиса в качестве аргумента.

!!!note ""

    Функция `TestBed.get()` была устаревшей начиная с версии 9 Angular.
    Чтобы свести к минимуму взлом изменений, Angular вводит новую функцию `TestBed.inject()`, которую вы должны использовать вместо нее.

    Информацию об удалении `TestBed.get()` можно найти в [Deprecations index](https://angular.io/guide/deprecations#index).

```ts
it('should use ValueService', () => {
    service = TestBed.inject(ValueService);
    expect(service.getValue()).toBe('real value');
});
```

Или внутри `beforeEach()`, если вы предпочитаете инжектировать сервис как часть вашей установки.

```ts
beforeEach(() => {
    TestBed.configureTestingModule({
        providers: [ValueService],
    });
    service = TestBed.inject(ValueService);
});
```

При тестировании сервиса с зависимостью, предоставьте макет в массиве `providers`.

В следующем примере имитатором является объект `spy`.

```ts
let masterService: MasterService;
let valueServiceSpy: jasmine.SpyObj<ValueService>;

beforeEach(() => {
    const spy = jasmine.createSpyObj('ValueService', [
        'getValue',
    ]);

    TestBed.configureTestingModule({
        // Provide both the service-to-test and its (spy) dependency
        providers: [
            MasterService,
            { provide: ValueService, useValue: spy },
        ],
    });
    // Inject both the service-to-test and its (spy) dependency
    masterService = TestBed.inject(MasterService);
    valueServiceSpy = TestBed.inject(
        ValueService
    ) as jasmine.SpyObj<ValueService>;
});
```

Тест потребляет этого шпиона тем же способом, что и ранее.

```ts
it('#getValue should return stubbed value from a spy', () => {
    const stubValue = 'stub value';
    valueServiceSpy.getValue.and.returnValue(stubValue);

    expect(masterService.getValue())
        .withContext('service returned stub value')
        .toBe(stubValue);
    expect(valueServiceSpy.getValue.calls.count())
        .withContext('spy method was called once')
        .toBe(1);
    expect(
        valueServiceSpy.getValue.calls.mostRecent()
            .returnValue
    ).toBe(stubValue);
});
```

## Тестирование без `beforeEach()` {: #no-before-each}

Большинство тестовых наборов в этом руководстве вызывают `beforeEach()` для установки предварительных условий для каждого теста `it()` и полагаются на `TestBed` для создания классов и внедрения сервисов.

Существует и другая школа тестирования, которая никогда не вызывает `beforeEach()` и предпочитает создавать классы явно, а не использовать `TestBed`.

Вот как можно переписать один из тестов `MasterService` в этом стиле.

Начните с размещения повторно используемого, подготовительного кода в функции _setup_ вместо `beforeEach()`.

```ts
function setup() {
    const valueServiceSpy = jasmine.createSpyObj(
        'ValueService',
        ['getValue']
    );
    const stubValue = 'stub value';
    const masterService = new MasterService(
        valueServiceSpy
    );

    valueServiceSpy.getValue.and.returnValue(stubValue);
    return { masterService, stubValue, valueServiceSpy };
}
```

Функция `setup()` возвращает литерал объекта с переменными, такими как `masterService`, на которые может ссылаться тест. Вы не определяете _полуглобальные_ переменные (например, `let masterService: MasterService`) в теле `describe()`.

Затем каждый тест вызывает `setup()` в своей первой строке, прежде чем продолжить шаги, которые манипулируют объектом тестирования и утверждают ожидания.

```ts
it('#getValue should return stubbed value from a spy', () => {
    const {
        masterService,
        stubValue,
        valueServiceSpy,
    } = setup();
    expect(masterService.getValue())
        .withContext('service returned stub value')
        .toBe(stubValue);
    expect(valueServiceSpy.getValue.calls.count())
        .withContext('spy method was called once')
        .toBe(1);
    expect(
        valueServiceSpy.getValue.calls.mostRecent()
            .returnValue
    ).toBe(stubValue);
});
```

Обратите внимание, как тест использует [_деструктурирующее назначение_](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Operators/Destructuring_assignment) для извлечения необходимых ему переменных настройки.

```ts
const {
    masterService,
    stubValue,
    valueServiceSpy,
} = setup();
```

Многие разработчики считают этот подход более чистым и явным, чем традиционный стиль `beforeEach()`.

Хотя это руководство по тестированию следует традиционному стилю, и по умолчанию [CLI схемы](https://github.com/angular/angular-cli) генерируют тестовые файлы с `beforeEach()` и `TestBed`, не стесняйтесь использовать _этот альтернативный подход_ в ваших собственных проектах.

## Тестирование HTTP-сервисов

Сервисы данных, выполняющие HTTP-вызовы к удаленным серверам, обычно инжектируют и делегируют службу Angular [`HttpClient`](http-test-requests.md) для XHR-вызовов.

Вы можете протестировать сервис данных с инжектированным `HttpClient` шпионом, как вы тестировали бы любой сервис с зависимостью.

```ts
let httpClientSpy: jasmine.SpyObj<HttpClient>;
let heroService: HeroService;

beforeEach(() => {
    // TODO: spy on other methods too
    httpClientSpy = jasmine.createSpyObj('HttpClient', [
        'get',
    ]);
    heroService = new HeroService(httpClientSpy);
});

it('should return expected heroes (HttpClient called once)', (done: DoneFn) => {
    const expectedHeroes: Hero[] = [
        { id: 1, name: 'A' },
        { id: 2, name: 'B' },
    ];

    httpClientSpy.get.and.returnValue(
        asyncData(expectedHeroes)
    );

    heroService.getHeroes().subscribe({
        next: (heroes) => {
            expect(heroes)
                .withContext('expected heroes')
                .toEqual(expectedHeroes);
            done();
        },
        error: done.fail,
    });
    expect(httpClientSpy.get.calls.count())
        .withContext('one call')
        .toBe(1);
});

it('should return an error when the server returns a 404', (done: DoneFn) => {
    const errorResponse = new HttpErrorResponse({
        error: 'test 404 error',
        status: 404,
        statusText: 'Not Found',
    });

    httpClientSpy.get.and.returnValue(
        asyncError(errorResponse)
    );

    heroService.getHeroes().subscribe({
        next: (heroes) =>
            done.fail('expected an error, not heroes'),
        error: (error) => {
            expect(error.message).toContain(
                'test 404 error'
            );
            done();
        },
    });
});
```

!!!warning ""

    Методы `HeroService` возвращают `Observables`. Вы должны _подписаться_ на наблюдаемую переменную, чтобы (a) вызвать ее выполнение и (b) подтвердить успех или неудачу метода.

    Метод `subscribe()` принимает обратный вызов успеха (`next`) и отказа (`error`). Убедитесь, что вы предоставили _обои_ обратные вызовы, чтобы перехватить ошибки.

    Пренебрежение этим приводит к асинхронной не пойманной наблюдаемой ошибке, которую программа запуска тестов, скорее всего, отнесет к совершенно другому тесту.

## `HttpClientTestingModule`

Расширенные взаимодействия между сервисом данных и `HttpClient` могут быть сложными и их трудно имитировать с помощью шпионов.

Модуль `HttpClientTestingModule` может сделать эти сценарии тестирования более управляемыми.

Хотя _пример кода_, сопровождающий данное руководство, демонстрирует `HttpClientTestingModule`, эта страница отсылает к [Http guide](http-test-requests.md), где подробно рассматривается тестирование с помощью `HttpClientTestingModule`.
