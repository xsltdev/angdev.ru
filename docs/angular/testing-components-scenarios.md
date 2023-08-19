# Сценарии тестирования компонентов

:date: 28.02.2022

В этом руководстве рассматриваются общие сценарии использования тестирования компонентов.

!!!note ""

    Если вы хотите поэкспериментировать с приложением, которое описано в этом руководстве, [запустите его в браузере](https://angular.io/generated/live-examples/testing/stackblitz.html) или скачайте и запустите его локально.

## Привязка компонентов

В примере приложения `BannerComponent` представляет статический текст заголовка в шаблоне HTML.

После нескольких изменений `BannerComponent` представляет динамический заголовок, привязываясь к свойству `title` компонента следующим образом.

```ts
@Component({
    selector: 'app-banner',
    template: '<h1>{{title}}</h1>',
    styles: ['h1 { color: green; font-size: 350%}'],
})
export class BannerComponent {
    title = 'Test Tour of Heroes';
}
```

Как бы минимально это ни было, вы решили добавить тест, чтобы подтвердить, что компонент действительно отображает нужное содержимое там, где вы думаете.

### Запрос для `<h1>`

Вы напишете последовательность тестов, которые проверяют значение элемента `<h1>`, который обертывает привязку интерполяции свойства _title_.

Вы обновите `beforeEach`, чтобы найти этот элемент с помощью стандартного HTML `querySelector` и присвоить его переменной `h1`.

```ts
let component: BannerComponent;
let fixture: ComponentFixture<BannerComponent>;
let h1: HTMLElement;

beforeEach(() => {
    TestBed.configureTestingModule({
        declarations: [BannerComponent],
    });
    fixture = TestBed.createComponent(BannerComponent);
    component = fixture.componentInstance; // BannerComponent test instance
    h1 = fixture.nativeElement.querySelector('h1');
});
```

### `createComponent()` не связывает данные {: #detect-changes}

Для первого теста вы хотите убедиться, что на экране отображается стандартный `title`. Ваш инстинкт подсказывает вам написать тест, который сразу же проверяет `<h1>` следующим образом:

```ts
it('should display original title', () => {
    expect(h1.textContent).toContain(component.title);
});
```

Этот тест проваливается с сообщением:

```
expected '' to contain 'Test Tour of Heroes'.
```

Привязка происходит, когда Angular выполняет **обнаружение изменений**.

В продакшене обнаружение изменений срабатывает автоматически, когда Angular создает компонент, пользователь нажимает клавишу или завершается асинхронная активность (например, AJAX).

Функция `TestBed.createComponent` _не_ запускает обнаружение изменений; этот факт подтверждается в пересмотренном тесте:

```ts
it('no title in the DOM after createComponent()', () => {
    expect(h1.textContent).toEqual('');
});
```

### `detectChanges()`

Вы должны указать `TestBed` на выполнение привязки данных, вызвав `fixture.detectChanges()`. Только тогда `<h1>` будет иметь ожидаемый заголовок.

```ts
it('should display original title after detectChanges()', () => {
    fixture.detectChanges();
    expect(h1.textContent).toContain(component.title);
});
```

Отложенное обнаружение изменений является намеренным и полезным. Она дает тестеру возможность проверить и изменить состояние компонента _до того, как Angular инициирует привязку данных и вызовет [lifecycle hooks](lifecycle-hooks.md)_.

Вот еще один тест, который изменяет свойство `title` компонента _до_ вызова `fixture.detectChanges()`.

```ts
it('should display a different test title', () => {
    component.title = 'Test Title';
    fixture.detectChanges();
    expect(h1.textContent).toContain('Test Title');
});
```

### Автоматическое обнаружение изменений {: #auto-detect-changes}

Тесты `BannerComponent` часто вызывают `detectChanges`. Некоторые тестировщики предпочитают, чтобы тестовая среда Angular выполняла обнаружение изменений автоматически.

Это возможно, если настроить `TestBed` с провайдером `ComponentFixtureAutoDetect`. Сначала импортируйте его из библиотеки утилит для тестирования:

```ts
import { ComponentFixtureAutoDetect } from '@angular/core/testing';
```

Затем добавьте его в массив `providers` конфигурации модуля тестирования:

```ts
TestBed.configureTestingModule({
    declarations: [BannerComponent],
    providers: [
        {
            provide: ComponentFixtureAutoDetect,
            useValue: true,
        },
    ],
});
```

Вот три теста, которые иллюстрируют работу автоматического обнаружения изменений.

```ts
it('should display original title', () => {
    // Hooray! No `fixture.detectChanges()` needed
    expect(h1.textContent).toContain(comp.title);
});

it('should still see original title after comp.title change', () => {
    const oldTitle = comp.title;
    comp.title = 'Test Title';
    // Displayed title is old because Angular didn't hear the change :(
    expect(h1.textContent).toContain(oldTitle);
});

it('should display updated title after detectChanges', () => {
    comp.title = 'Test Title';
    fixture.detectChanges(); // detect changes explicitly
    expect(h1.textContent).toContain(comp.title);
});
```

Первый тест показывает преимущество автоматического обнаружения изменений.

Второй и третий тесты показывают важное ограничение. Среда тестирования Angular _не_ знает, что тест изменил `заголовок` компонента.

Служба `ComponentFixtureAutoDetect` реагирует на _асинхронные действия_, такие как разрешение обещаний, таймеры и события DOM.

Но прямое, синхронное обновление свойства компонента невидимо.

Тест должен вызвать `fixture.detectChanges()` вручную, чтобы запустить очередной цикл обнаружения изменений.

!!!note ""

    Вместо того, чтобы гадать, когда тестовое приспособление будет или не будет выполнять обнаружение изменений, примеры в этом руководстве _всегда_ вызывают `detectChanges()` _явно_. Нет никакого вреда в том, чтобы вызывать `detectChanges()` чаще, чем это необходимо.

### Изменение входного значения с помощью `dispatchEvent()` {: #dispatch-event}

Чтобы имитировать ввод данных пользователем, найдите элемент input и установите его свойство `value`.

Вы вызовете `fixture.detectChanges()`, чтобы запустить обнаружение изменений Angular. Но есть важный, промежуточный шаг.

Angular не знает, что вы установили свойство `value` элемента ввода. Он не будет читать это свойство, пока вы не поднимете событие `input` элемента, вызвав `dispatchEvent()`.

Тогда вы вызываете `detectChanges()`.

Следующий пример демонстрирует правильную последовательность действий.

```ts
it('should convert hero name to Title Case', () => {
    // get the name's input and display elements from the DOM
    const hostElement: HTMLElement = harness.routeNativeElement!;
    const nameInput: HTMLInputElement = hostElement.querySelector(
        'input'
    )!;
    const nameDisplay: HTMLElement = hostElement.querySelector(
        'span'
    )!;

    // simulate user entering a new name into the input box
    nameInput.value = 'quick BROWN  fOx';

    // Dispatch a DOM event so that Angular learns of input value change.
    nameInput.dispatchEvent(new Event('input'));

    // Tell Angular to update the display binding through the title pipe
    harness.detectChanges();

    expect(nameDisplay.textContent).toBe(
        'Quick Brown  Fox'
    );
});
```

## Компонент с внешними файлами

Предыдущий `BannerComponent` определен с _inline template_ и _inline css_, указанными в свойствах `@Component.template` и `@Component.styles` соответственно.

Многие компоненты определяют _внешние шаблоны_ и _внешние css_ с помощью свойств `@Component.templateUrl` и `@Component.styleUrls` соответственно, как это делает следующий вариант `BannerComponent`.

```ts
@Component({
  selector: 'app-banner',
  templateUrl: './banner-external.component.html',
  styleUrls:  ['./banner-external.component.css']
})
```

Этот синтаксис указывает компилятору Angular читать внешние файлы во время компиляции компонента.

Это не проблема, когда вы выполняете команду CLI `ng test`, потому что она _компилирует приложение перед запуском тестов_.

Однако, если вы запускаете тесты в **не-CLI окружении**, тесты этого компонента могут не пройти. Например, если вы запустите тесты `BannerComponent` в среде веб-кодирования, такой как [plunker](https://plnkr.co), вы увидите сообщение, подобное этому:

```
Error: This test module uses the component BannerComponent
which is using a "templateUrl" or "styleUrls", but they were never compiled.
Please call "TestBed.compileComponents" before your test.
```

Вы получаете это сообщение о сбое теста, когда среда выполнения компилирует исходный код _во время выполнения самих тестов_.

Чтобы устранить проблему, вызовите `compileComponents()`, как объясняется в следующем разделе [Вызов compileComponents](#compile-components).

## Компонент с зависимостью {: #component-with-dependency}

Компоненты часто имеют зависимости от сервисов.

Компонент `WelcomeComponent` отображает приветственное сообщение для вошедшего в систему пользователя. Он знает, кто этот пользователь, на основе свойства инжектированного `UserService`:

```ts
import { Component, OnInit } from '@angular/core';
import { UserService } from '../model/user.service';

@Component({
    selector: 'app-welcome',
    template: '<h3 class="welcome"><i>{{welcome}}</i></h3>',
})
export class WelcomeComponent implements OnInit {
    welcome = '';
    constructor(private userService: UserService) {}

    ngOnInit(): void {
        this.welcome = this.userService.isLoggedIn
            ? 'Welcome, ' + this.userService.user.name
            : 'Please log in.';
    }
}
```

В `WelcomeComponent` есть логика принятия решений, которая взаимодействует с сервисом, логика, которая делает этот компонент достойным тестирования. Вот конфигурация модуля тестирования для файла спецификации:

```ts
TestBed.configureTestingModule({
    declarations: [WelcomeComponent],
    // providers: [ UserService ],  // NO! Don't provide the real service!
    // Provide a test-double instead
    providers: [
        { provide: UserService, useValue: userServiceStub },
    ],
});
```

На этот раз, в дополнение к объявлению _component-under-test_, конфигурация добавляет провайдера `UserService` в список `providers`.

Но не настоящий `UserService`.

### Предоставление дублей для тестирования сервисов {: #service-test-doubles}

В _компонент под тестом_ не обязательно должны быть внедрены реальные сервисы. На самом деле, обычно лучше, если это будут тестовые дубликаты, такие как заглушки, подделки, шпионы или моки.

Целью спецификации является тестирование компонента, а не сервиса, а с реальными сервисами могут возникнуть проблемы.

Внедрение настоящего `UserService` может стать кошмаром. Настоящая служба может запросить у пользователя учетные данные для входа в систему и попытаться связаться с сервером аутентификации.

Такое поведение может быть трудно перехватить.

Гораздо проще и безопаснее создать и зарегистрировать тестового двойника вместо настоящего `UserService`.

Этот конкретный набор тестов предоставляет минимальный макет `UserService`, который удовлетворяет потребности `WelcomeComponent` и его тестов:

```ts
let userServiceStub: Partial<UserService>;

userServiceStub = {
    isLoggedIn: true,
    user: { name: 'Test User' },
};
```

### Получение инжектированных сервисов {: #get-injected-service}

Тестам нужен доступ к заглушке `UserService`, инжектированной в `WelcomeComponent`.

Angular имеет иерархическую систему инъекций. Инжекторы могут быть на нескольких уровнях, начиная с корневого инжектора, созданного `TestBed`, и заканчивая деревом компонентов.

Самый безопасный способ получить инжектируемый сервис, способ, который **_всегда работает_**, это **получить его из инжектора _компонента, который тестируется_**.

Инжектор компонента является свойством `DebugElement` приспособления.

```ts
// UserService actually injected into the component
userService = fixture.debugElement.injector.get(
    UserService
);
```

### `TestBed.inject()` {: #testbed-inject}

Вы _можете_ также получить сервис из корневого инжектора, используя `TestBed.inject()`. Это проще для запоминания и менее многословно.

Но он работает только тогда, когда Angular инжектирует компонент с экземпляром сервиса в корневой инжектор теста.

В этом тестовом наборе _единственным_ поставщиком `UserService` является корневой модуль тестирования, поэтому безопасно вызывать `TestBed.inject()` следующим образом:

```ts
// UserService from the root injector
userService = TestBed.inject(UserService);
```

!!!note ""

    Случай использования, когда `TestBed.inject()` не работает, смотрите в разделе [_Override component providers_](#component-override), где объясняется, когда и почему вы должны получить сервис из инжектора компонента.

### Окончательная настройка и тесты {: #welcome-spec-setup}

Вот полный `beforeEach()`, использующий `TestBed.inject()`:

```ts
let userServiceStub: Partial<UserService>;

beforeEach(() => {
    // stub UserService for test purposes
    userServiceStub = {
        isLoggedIn: true,
        user: { name: 'Test User' },
    };

    TestBed.configureTestingModule({
        declarations: [WelcomeComponent],
        providers: [
            {
                provide: UserService,
                useValue: userServiceStub,
            },
        ],
    });

    fixture = TestBed.createComponent(WelcomeComponent);
    comp = fixture.componentInstance;

    // UserService from the root injector
    userService = TestBed.inject(UserService);

    //  get the "welcome" element by CSS selector (e.g., by class name)
    el = fixture.nativeElement.querySelector('.welcome');
});
```

И вот несколько тестов:

```ts
it('should welcome the user', () => {
    fixture.detectChanges();
    const content = el.textContent;
    expect(content)
        .withContext('"Welcome ..."')
        .toContain('Welcome');
    expect(content)
        .withContext('expected name')
        .toContain('Test User');
});

it('should welcome "Bubba"', () => {
    userService.user.name = 'Bubba'; // welcome message hasn't been shown yet
    fixture.detectChanges();
    expect(el.textContent).toContain('Bubba');
});

it('should request login if not logged in', () => {
    userService.isLoggedIn = false; // welcome message hasn't been shown yet
    fixture.detectChanges();
    const content = el.textContent;
    expect(content)
        .withContext('not welcomed')
        .not.toContain('Welcome');
    expect(content)
        .withContext('"log in"')
        .toMatch(/log in/i);
});
```

Первый тест - это тест на вменяемость; он подтверждает, что заглушка `UserService` вызвана и работает.

!!!note ""

    Второй параметр (например, `'expected name'`) является необязательной меткой отказа. Если ожидание не сработало, Jasmine добавляет эту метку к сообщению о неудаче ожидания.

    В спецификации с несколькими ожиданиями это может помочь прояснить, что пошло не так и какое ожидание не сработало.

Остальные тесты подтверждают логику работы компонента, когда сервис возвращает различные значения. Второй тест проверяет эффект от изменения имени пользователя.
Третий тест проверяет, что компонент выводит правильное сообщение, когда нет зарегистрированного пользователя.

## Компонент с асинхронным сервисом {: #component-with-async-service}

В этом примере шаблон `AboutComponent` содержит `TwainComponent`. Компонент `TwainComponent` отображает цитаты Марка Твена.

```ts
template: `
  <p class="twain"><i>{{quote | async}}</i></p>
  <button type="button" (click)="getQuote()">Next quote</button>
  <p class="error" *ngIf="errorMessage">{{ errorMessage }}</p>`,
```

!!!note ""

    Значение свойства `quote` компонента проходит через `AsyncPipe`. Это означает, что свойство возвращает либо `Promise`, либо `Observable`.

В этом примере метод `TwainComponent.getQuote()` сообщает, что свойство `quote` возвращает `Observable`.

```ts
getQuote() {
  this.errorMessage = '';
  this.quote = this.twainService.getQuote().pipe(
    startWith('...'),
    catchError( (err: any) => {
      // Wait a turn because errorMessage already set once this turn
      setTimeout(() => this.errorMessage = err.message || err.toString());
      return of('...'); // reset message to placeholder
    })
  );
};
```

Компонент `TwainComponent` получает цитаты от инжектированного `TwainService`. Компонент запускает возвращаемую `Observable` со значением заполнителя (`'...'`), прежде чем сервис сможет вернуть свою первую цитату.

Компонент `catchError` перехватывает ошибки сервиса, подготавливает сообщение об ошибке и возвращает значение placeholder на канале успеха. Он должен подождать тик для установки `errorMessage`, чтобы избежать двойного обновления сообщения в одном и том же цикле обнаружения изменений.

Все эти функции вы захотите протестировать.

### Тестирование с помощью spy

При тестировании компонента значение имеет только публичный API сервиса. В целом, сами тесты не должны выполнять вызовы на удаленные серверы.

Они должны эмулировать такие вызовы.

Настройка в этом `app/twain/twain.component.spec.ts` показывает один из способов сделать это:

```ts
beforeEach(() => {
    testQuote = 'Test Quote';

    // Create a fake TwainService object with a `getQuote()` spy
    const twainService = jasmine.createSpyObj(
        'TwainService',
        ['getQuote']
    );
    // Make the spy return a synchronous Observable with the test data
    getQuoteSpy = twainService.getQuote.and.returnValue(
        of(testQuote)
    );

    TestBed.configureTestingModule({
        declarations: [TwainComponent],
        providers: [
            {
                provide: TwainService,
                useValue: twainService,
            },
        ],
    });

    fixture = TestBed.createComponent(TwainComponent);
    component = fixture.componentInstance;
    quoteEl = fixture.nativeElement.querySelector('.twain');
});
```

Сосредоточьтесь на шпионе.

```ts
// Create a fake TwainService object with a `getQuote()` spy
const twainService = jasmine.createSpyObj('TwainService', [
    'getQuote',
]);
// Make the spy return a synchronous Observable with the test data
getQuoteSpy = twainService.getQuote.and.returnValue(
    of(testQuote)
);
```

Шпион устроен таким образом, что при любом вызове `getQuote` получает наблюдаемую с тестовой цитатой. В отличие от реального метода `getQuote()`, этот шпион обходит сервер и возвращает синхронную наблюдаемую, значение которой доступно немедленно.

Вы можете написать много полезных тестов с помощью этого шпиона, несмотря на то, что его `Observable` является синхронным.

### Синхронные тесты {: #sync-tests}

Ключевым преимуществом синхронного `Observable` является то, что вы можете часто превращать асинхронные процессы в синхронные тесты.

```ts
it('should show quote after component initialized', () => {
    fixture.detectChanges(); // onInit()

    // sync spy result shows testQuote immediately after init
    expect(quoteEl.textContent).toBe(testQuote);
    expect(getQuoteSpy.calls.any())
        .withContext('getQuote called')
        .toBe(true);
});
```

Поскольку результат шпионажа возвращается синхронно, метод `getQuote()` обновляет сообщение на экране сразу _после_ первого цикла обнаружения изменений, во время которого Angular вызывает `ngOnInit`.

При тестировании пути ошибок вам не так повезет. Хотя сервисный шпион возвращает ошибку синхронно, метод компонента вызывает `setTimeout()`.

Тест должен подождать как минимум один полный оборот движка JavaScript, прежде чем значение станет доступным.

Тест должен стать _асинхронным_.

### Асинхронный тест с `fakeAsync()` {: #fake-async}

Чтобы использовать функциональность `fakeAsync()`, вы должны импортировать `zone.js/testing` в файл настройки тестов. Если вы создали свой проект с помощью Angular CLI, то `zone-testing` уже импортирован в `src/test.ts`.

Следующий тест подтверждает ожидаемое поведение, когда сервис возвращает `ErrorObservable`.

```ts
it('should display error when TwainService fails', fakeAsync(() => {
    // tell spy to return an error observable
    getQuoteSpy.and.returnValue(
        throwError(
            () => new Error('TwainService test failure')
        )
    );
    fixture.detectChanges(); // onInit()
    // sync spy errors immediately after init

    tick(); // flush the component's setTimeout()

    fixture.detectChanges(); // update errorMessage within setTimeout()

    expect(errorMessage())
        .withContext('should display error')
        .toMatch(/test failure/);
    expect(quoteEl.textContent)
        .withContext('should show placeholder')
        .toBe('...');
}));
```

!!!note ""

    Функция `it()` принимает аргумент следующего вида.

```ts
fakeAsync(() => {
    /* test body */
});
```

Функция `fakeAsync()` позволяет использовать линейный стиль кодирования, запуская тело теста в специальной тестовой зоне `fakeAsync`. Тело теста кажется синхронным.
В нем нет вложенного синтаксиса (например, `Promise.then()`), который нарушает поток управления.

!!!note ""

    Ограничение: Функция `fakeAsync()` не будет работать, если тело теста выполняет вызов `XMLHttpRequest` (XHR). Вызовы XHR внутри теста встречаются редко, но если вам необходимо вызвать XHR, смотрите раздел [`waitForAsync()`](#waitForAsync).

### Функция `tick()` {: #tick}

Вы должны вызывать [tick()](https://angular.io/api/core/testing/tick), чтобы перевести виртуальные часы.

Вызов [tick()](https://angular.io/api/core/testing/tick) имитирует течение времени до завершения всех ожидающих асинхронных действий. В данном случае он ожидает `setTimeout()` обработчика ошибок.

Функция [tick()](https://angular.io/api/core/testing/tick) принимает в качестве параметров `millis` и `tickOptions`. Параметр `millis` определяет, на сколько продвигаются виртуальные часы, и по умолчанию равен `0`, если не указан. Например, если у вас есть `setTimeout(fn, 100)` в тесте `fakeAsync()`, вам нужно использовать `tick(100)` для запуска обратного вызова fn.

Необязательный параметр `tickOptions` имеет свойство `processNewMacroTasksSynchronously`. Свойство `processNewMacroTasksSynchronously` указывает, следует ли вызывать новые сгенерированные макрозадачи при тике, и по умолчанию имеет значение `true`.

```ts
it('should run timeout callback with delay after call tick with millis', fakeAsync(() => {
    let called = false;
    setTimeout(() => {
        called = true;
    }, 100);
    tick(100);
    expect(called).toBe(true);
}));
```

Функция [tick()](https://angular.io/api/core/testing/tick) является одной из утилит тестирования Angular, которую вы импортируете с помощью `TestBed`. Она является компаньоном `fakeAsync()` и вы можете вызывать ее только в теле `fakeAsync()`.

### tickOptions

В этом примере появилась новая макрозадача - вложенная функция `setTimeout`. По умолчанию, когда `tick` имеет значение setTimeout, срабатывают и `outside`, и `nested`.

```ts
it('should run new macro task callback with delay after call tick with millis', fakeAsync(() => {
    function nestedTimer(cb: () => any): void {
        setTimeout(() => setTimeout(() => cb()));
    }
    const callback = jasmine.createSpy('callback');
    nestedTimer(callback);
    expect(callback).not.toHaveBeenCalled();
    tick(0);
    // the nested timeout will also be triggered
    expect(callback).toHaveBeenCalled();
}));
```

В некоторых случаях вы не хотите запускать новую макрозадачу при тике. Вы можете использовать `tick(millis, {processNewMacroTasksSynchronously: false})`, чтобы не вызывать новую макрозадачу.

```ts
it('should not run new macro task callback with delay after call tick with millis', fakeAsync(() => {
    function nestedTimer(cb: () => any): void {
        setTimeout(() => setTimeout(() => cb()));
    }
    const callback = jasmine.createSpy('callback');
    nestedTimer(callback);
    expect(callback).not.toHaveBeenCalled();
    tick(0, { processNewMacroTasksSynchronously: false });
    // the nested timeout will not be triggered
    expect(callback).not.toHaveBeenCalled();
    tick(0);
    expect(callback).toHaveBeenCalled();
}));
```

### Сравнение дат внутри fakeAsync()

`fakeAsync()` имитирует течение времени, что позволяет вам вычислить разницу между датами внутри `fakeAsync()`.

```ts
it('should get Date diff correctly in fakeAsync', fakeAsync(() => {
    const start = Date.now();
    tick(100);
    const end = Date.now();
    expect(end - start).toBe(100);
}));
```

### jasmine.clock с fakeAsync()

Jasmine также предоставляет функцию `clock` для имитации дат. Angular автоматически запускает тесты, которые выполняются после вызова `jasmine.clock().install()` внутри метода `fakeAsync()` до вызова `jasmine.clock().uninstall()`.

Метод `fakeAsync()` не нужен и при вложении выдает ошибку.

По умолчанию эта функция отключена. Чтобы включить ее, установите глобальный флаг перед импортом `zone-testing`.

Если вы используете Angular CLI, настройте этот флаг в `src/test.ts`.

```ts
(window as any)['__zone_symbol__fakeAsyncPatchLock'] = true;
import 'zone.js/testing';
```

```ts
describe('use jasmine.clock()', () => {
    // need to config __zone_symbol__fakeAsyncPatchLock flag
    // before loading zone.js/testing
    beforeEach(() => {
        jasmine.clock().install();
    });
    afterEach(() => {
        jasmine.clock().uninstall();
    });
    it('should auto enter fakeAsync', () => {
        // is in fakeAsync now, don't need to call fakeAsync(testFn)
        let called = false;
        setTimeout(() => {
            called = true;
        }, 100);
        jasmine.clock().tick(100);
        expect(called).toBe(true);
    });
});
```

### Использование планировщика RxJS внутри fakeAsync()

Вы также можете использовать планировщик RxJS в `fakeAsync()` точно так же, как и `setTimeout()` или `setInterval()`, но вам нужно импортировать `zone.js/plugins/zone-patch-rxjs-fake-async` для патча планировщика RxJS.

```ts
it('should get Date diff correctly in fakeAsync with rxjs scheduler', fakeAsync(() => {
    // need to add `import 'zone.js/plugins/zone-patch-rxjs-fake-async'
    // to patch rxjs scheduler
    let result = '';
    of('hello')
        .pipe(delay(1000))
        .subscribe((v) => {
            result = v;
        });
    expect(result).toBe('');
    tick(1000);
    expect(result).toBe('hello');

    const start = new Date().getTime();
    let dateDiff = 0;
    interval(1000)
        .pipe(take(2))
        .subscribe(
            () => (dateDiff = new Date().getTime() - start)
        );

    tick(1000);
    expect(dateDiff).toBe(1000);
    tick(1000);
    expect(dateDiff).toBe(2000);
}));
```

### Поддержка большего количества макрозадач

По умолчанию `fakeAsync()` поддерживает следующие макрозадачи.

-   `setTimeout`
-   `setInterval`
-   `requestAnimationFrame`
-   `webkitRequestAnimationFrame`
-   `mozRequestAnimationFrame`

Если вы запускаете другие макрозадачи, такие как `HTMLCanvasElement.toBlob()`, возникает ошибка _"Unknown macroTask scheduled in fake async test"_.

=== "src/app/shared/canvas.component.spec.ts (failing)"

    ```ts
    import {
    	fakeAsync,
    	TestBed,
    	tick,
    } from '@angular/core/testing';

    import { CanvasComponent } from './canvas.component';

    describe('CanvasComponent', () => {
    	beforeEach(async () => {
    		await TestBed.configureTestingModule({
    			declarations: [CanvasComponent],
    		}).compileComponents();
    	});

    	it('should be able to generate blob data from canvas', fakeAsync(() => {
    		const fixture = TestBed.createComponent(
    			CanvasComponent
    		);
    		const canvasComp = fixture.componentInstance;

    		fixture.detectChanges();
    		expect(canvasComp.blobSize).toBe(0);

    		tick();
    		expect(canvasComp.blobSize).toBeGreaterThan(0);
    	}));
    });
    ```

=== "src/app/shared/canvas.component.ts"

    ```ts
    import {
    	Component,
    	AfterViewInit,
    	ViewChild,
    	ElementRef,
    } from '@angular/core';

    @Component({
    	selector: 'sample-canvas',
    	template:
    		'<canvas #sampleCanvas width="200" height="200"></canvas>',
    })
    export class CanvasComponent implements AfterViewInit {
    	blobSize = 0;
    	@ViewChild('sampleCanvas') sampleCanvas!: ElementRef;

    	ngAfterViewInit() {
    		const canvas: HTMLCanvasElement = this.sampleCanvas
    			.nativeElement;
    		const context = canvas.getContext('2d')!;

    		context.clearRect(0, 0, 200, 200);
    		context.fillStyle = '#FF1122';
    		context.fillRect(0, 0, 200, 200);

    		canvas.toBlob((blob) => {
    			this.blobSize = blob?.size ?? 0;
    		});
    	}
    }
    ```

Если вы хотите поддерживать такой случай, вам необходимо определить макрозадачу, которую вы хотите поддерживать, в `beforeEach()`. Например:

```ts
beforeEach(() => {
    (window as any).__zone_symbol__FakeAsyncTestMacroTask = [
        {
            source: 'HTMLCanvasElement.toBlob',
            callbackArgs: [{ size: 200 }],
        },
    ];
});
```

!!!note ""

    Чтобы сделать элемент `<canvas>` Zone.js-aware в вашем приложении, вам необходимо импортировать патч `zone-patch-canvas` (либо в `polyfills.ts`, либо в конкретный файл, который использует `<canvas>`):

    ```ts
    // Import patch to make async `HTMLCanvasElement` methods (such as `.toBlob()`) Zone.js-aware.
    // Either import in `polyfills.ts` (if used in more than one places in the app) or in the component
    // file using `HTMLCanvasElement` (if it is only used in a single file).
    import 'zone.js/plugins/zone-patch-canvas';
    ```

### Асинхронные наблюдаемые

Вы можете быть довольны покрытием этих тестов.

Однако вас может беспокоить тот факт, что реальный сервис ведет себя не совсем так. Реальный сервис посылает запросы на удаленный сервер.

Серверу требуется время для ответа, и ответ, конечно, не будет доступен сразу, как в предыдущих двух тестах.

Ваши тесты будут более точно отражать реальный мир, если вы вернете _асинхронную_ наблюдаемую из шпиона `getQuote()` следующим образом.

```ts
// Simulate delayed observable values with the `asyncData()` helper
getQuoteSpy.and.returnValue(asyncData(testQuote));
```

### Помощники асинхронных наблюдаемых

Асинхронная наблюдаемая была создана с помощью помощника `asyncData`. Помощник `asyncData` - это служебная функция, которую вам придется написать самостоятельно, или скопировать эту функцию из кода примера.

```ts
/**
 * Create async observable that emits-once and completes
 * after a JS engine turn
 */
export function asyncData<T>(data: T) {
    return defer(() => Promise.resolve(data));
}
```

Эта вспомогательная наблюдаемая испускает значение `data` при следующем повороте движка JavaScript.

Оператор [RxJS `defer()`](http://reactivex.io/documentation/operators/defer.html) возвращает наблюдаемую. Он принимает фабричную функцию, которая возвращает либо обещание, либо наблюдаемую.

Когда что-то подписывается на наблюдаемую _defer_, оно добавляет подписчика в новую наблюдаемую, созданную с помощью этой фабрики.

Оператор `defer()` преобразует `Promise.resolve()` в новую наблюдаемую, которая, как и `HttpClient`, испускается один раз и завершается. Подписчики отписываются после получения значения данных.

Существует аналогичный помощник для создания асинхронной ошибки.

```ts
/**
 * Create async observable error that errors
 * after a JS engine turn
 */
export function asyncError<T>(errorObject: any) {
    return defer(() => Promise.reject(errorObject));
}
```

### Больше асинхронных тестов

Теперь, когда шпион `getQuote()` возвращает асинхронные наблюдаемые, большинство ваших тестов также должны быть асинхронными.

Вот тест `fakeAsync()`, который демонстрирует поток данных, ожидаемый в реальном мире.

```ts
it('should show quote after getQuote (fakeAsync)', fakeAsync(() => {
    fixture.detectChanges(); // ngOnInit()
    expect(quoteEl.textContent)
        .withContext('should show placeholder')
        .toBe('...');

    tick(); // flush the observable to get the quote
    fixture.detectChanges(); // update view

    expect(quoteEl.textContent)
        .withContext('should show quote')
        .toBe(testQuote);
    expect(errorMessage())
        .withContext('should not show error')
        .toBeNull();
}));
```

Заметьте, что элемент quote отображает значение заполнителя (`...`) после `ngOnInit()`. Первая цитата еще не пришла.

Чтобы удалить первую котировку из наблюдаемой, вы вызываете [tick()](https://angular.io/api/core/testing/tick). Затем вызовите `detectChanges()`, чтобы сообщить Angular об обновлении экрана.

После этого можно утверждать, что элемент цитаты отображает ожидаемый текст.

### Асинхронный тест с `waitForAsync()` {: #waitForAsync}

Чтобы использовать функциональность `waitForAsync()`, вы должны импортировать `zone.js/testing` в файл настройки тестов. Если вы создали свой проект с помощью Angular CLI, `zone-testing` уже импортирован в `src/test.ts`.

Вот предыдущий тест `fakeAsync()`, переписанный с помощью утилиты `waitForAsync()`.

```ts
it(
    'should show quote after getQuote (waitForAsync)',
    waitForAsync(() => {
        fixture.detectChanges(); // ngOnInit()
        expect(quoteEl.textContent)
            .withContext('should show placeholder')
            .toBe('...');

        fixture.whenStable().then(() => {
            // wait for async getQuote
            fixture.detectChanges(); // update view with quote
            expect(quoteEl.textContent).toBe(testQuote);
            expect(errorMessage())
                .withContext('should not show error')
                .toBeNull();
        });
    })
);
```

Утилита `waitForAsync()` скрывает некоторые асинхронные шаблоны, организуя выполнение кода тестировщика в специальной _async test zone_. Вам не нужно передавать `done()` из Jasmine в тест и вызывать `done()`, потому что он `неопределен` в обещаниях или наблюдаемых обратных вызовах.

Но асинхронная природа теста проявляется в вызове `fixture.whenStable()`, который нарушает линейный поток управления.

При использовании `intervalTimer()`, например, `setInterval()` в `waitForAsync()`, не забудьте отменить таймер с помощью `clearInterval()` после выполнения теста, иначе `waitForAsync()` никогда не завершится.

### `whenStable` {: #when-stable}

Тест должен ждать, пока наблюдаемая `getQuote()` выпустит следующую цитату. Вместо вызова [tick()](https://angular.io/api/core/testing/tick), он вызывает `fixture.whenStable()`.

Функция `fixture.whenStable()` возвращает обещание, которое разрешается, когда очередь задач движка JavaScript становится пустой. В этом примере очередь задач становится пустой, когда наблюдаемая испускает первую цитату.

Тест возобновляется в обратном вызове обещания, которое вызывает `detectChanges()` для обновления элемента цитаты ожидаемым текстом.

### Jasmine `done()` {: #jasmine-done}

Хотя функции `waitForAsync()` и `fakeAsync()` значительно упрощают асинхронное тестирование Angular, вы все еще можете вернуться к традиционной технике и передать `it` функцию, которая принимает [`done` callback](https://jasmine.github.io/2.0/introduction.html#section-Asynchronous_Support).

Вы не можете вызвать `done()` в функциях `waitForAsync()` или `fakeAsync()`, потому что параметр `done` является `неопределенным`.

Теперь вы отвечаете за цепочку обещаний, обработку ошибок и вызов `done()` в нужные моменты.

Написание тестовых функций с `done()` более громоздко, чем `waitForAsync()` и `fakeAsync()`, но иногда это необходимо, когда код включает `intervalTimer()` типа `setInterval`.

Вот еще две версии предыдущего теста, написанные с помощью `done()`. Первая подписывается на `Observable`, выставляемый шаблону свойством `quote` компонента.

```ts
it('should show last quote (quote done)', (done: DoneFn) => {
    fixture.detectChanges();

    component.quote.pipe(last()).subscribe(() => {
        fixture.detectChanges(); // update view with quote
        expect(quoteEl.textContent).toBe(testQuote);
        expect(errorMessage())
            .withContext('should not show error')
            .toBeNull();
        done();
    });
});
```

Оператор RxJS `last()` выдает последнее значение наблюдаемой перед завершением, которое будет тестовой цитатой. Обратный вызов `subscribe` вызывает `detectChanges()` для обновления элемента quote тестовой цитатой, аналогично предыдущим тестам.

В некоторых тестах вас больше интересует, как был вызван метод инжектированного сервиса и какие значения он вернул, чем то, что отображается на экране.

Сервисный шпион, такой как `qetQuote()` шпион поддельного `TwainService`, может дать вам эту информацию и сделать утверждения о состоянии представления.

```ts
it('should show quote after getQuote (spy done)', (done: DoneFn) => {
    fixture.detectChanges();

    // the spy's most recent call returns the observable with the test quote
    getQuoteSpy.calls
        .mostRecent()
        .returnValue.subscribe(() => {
            fixture.detectChanges(); // update view with quote
            expect(quoteEl.textContent).toBe(testQuote);
            expect(errorMessage())
                .withContext('should not show error')
                .toBeNull();
            done();
        });
});
```

## Компонентные мраморные тесты {: #marble-testing}

Предыдущие тесты `TwainComponent` имитировали асинхронный наблюдаемый ответ от `TwainService` с помощью утилит `asyncData` и `asyncError`.

Это короткие, простые функции, которые вы можете написать самостоятельно. К сожалению, они слишком просты для многих распространенных сценариев.

Наблюдаемая часто испускается несколько раз, возможно, со значительной задержкой.

Компонент может координировать несколько наблюдаемых с перекрывающимися последовательностями значений и ошибок.

**RxJS marble testing** - это отличный способ тестирования сценариев наблюдаемых, как простых, так и сложных. Вы, вероятно, видели [мраморные диаграммы](https://rxmarbles.com), которые иллюстрируют работу наблюдаемых.

Мраморное тестирование использует аналогичный мраморный язык для определения наблюдаемых потоков и ожиданий в ваших тестах.

Следующие примеры рассматривают два теста `TwainComponent` с помощью мраморного тестирования.

Начните с установки npm-пакета `jasmine-marbles`. Затем импортируйте необходимые вам символы.

```ts
import { cold, getTestScheduler } from 'jasmine-marbles';
```

Вот полный тест для получения цитаты:

```ts
it('should show quote after getQuote (marbles)', () => {
    // observable test quote value and complete(), after delay
    const q$ = cold('---x|', { x: testQuote });
    getQuoteSpy.and.returnValue(q$);

    fixture.detectChanges(); // ngOnInit()
    expect(quoteEl.textContent)
        .withContext('should show placeholder')
        .toBe('...');

    getTestScheduler().flush(); // flush the observables

    fixture.detectChanges(); // update view

    expect(quoteEl.textContent)
        .withContext('should show quote')
        .toBe(testQuote);
    expect(errorMessage())
        .withContext('should not show error')
        .toBeNull();
});
```

Обратите внимание, что тест Jasmine является синхронным. Здесь нет `fakeAsync()`.

Мраморное тестирование использует планировщик тестов для имитации течения времени в синхронном тесте.

Красота мраморного тестирования заключается в визуальном определении наблюдаемых потоков. Этот тест определяет [_холодную_ наблюдаемую](#cold-observable), которая ждет три [кадра](#marble-frame) (`---`), выдает значение (`x`) и завершается (`|`).

Во втором аргументе вы сопоставляете маркер значения (`x`) с испускаемым значением (`testQuote`).

```ts
const q$ = cold('---x|', { x: testQuote });
```

Библиотека marble создает соответствующую наблюдаемую, которую тест устанавливает в качестве возвращаемого значения шпиона `getQuote`.

Когда вы будете готовы активировать мраморные наблюдаемые, вы скажете `TestScheduler` _промыть_ свою очередь подготовленных задач следующим образом.

```ts
getTestScheduler().flush(); // flush the observables
```

Этот шаг служит цели, аналогичной [tick()](https://angular.io/api/core/testing/tick) и `whenStable()` в предыдущих примерах `fakeAsync()` и `waitForAsync()`. Остальная часть теста такая же, как и в этих примерах.

### Тестирование ошибок в мраморе

Перед вами мраморная версия теста на ошибку `getQuote()`.

```ts
it('should display error when TwainService fails', fakeAsync(() => {
    // observable error after delay
    const q$ = cold(
        '---#|',
        null,
        new Error('TwainService test failure')
    );
    getQuoteSpy.and.returnValue(q$);

    fixture.detectChanges(); // ngOnInit()
    expect(quoteEl.textContent)
        .withContext('should show placeholder')
        .toBe('...');

    getTestScheduler().flush(); // flush the observables
    tick(); // component shows error after a setTimeout()
    fixture.detectChanges(); // update error message

    expect(errorMessage())
        .withContext('should display error')
        .toMatch(/test failure/);
    expect(quoteEl.textContent)
        .withContext('should show placeholder')
        .toBe('...');
}));
```

Это все еще асинхронный тест, вызывающий `fakeAsync()` и [tick()](https://angular.io/api/core/testing/tick), потому что сам компонент вызывает `setTimeout()` при обработке ошибок.

Посмотрите на определение мраморной наблюдаемой.

```ts
const q$ = cold(
    '---#|',
    null,
    new Error('TwainService test failure')
);
```

Это _холодная_ наблюдаемая, которая ждет три кадра и затем выдает ошибку, хэш (`#`) символ указывает на время ошибки, которое указано в третьем аргументе. Второй аргумент равен null, потому что наблюдаемая никогда не выдает значения.

### Узнайте о тестировании на мраморе {: #marble-frame}

Мраморный кадр - это виртуальная единица времени тестирования. Каждый символ (`-`, `x`, `|`, `#`) отмечает прохождение одного фрейма.

_Холодная_ наблюдаемая не производит значений, пока вы не подпишетесь на нее. Большинство наблюдаемых вашего приложения являются холодными.

Все методы [_HttpClient_](http.md) возвращают холодные наблюдаемые.

_Горячая_ наблюдаемая уже производит значения _до_ того, как вы на нее подписались. Наблюдаемая [`Router.events`](https://angular.io/api/router/Router#events), которая сообщает об активности маршрутизатора, является _горячей_ наблюдаемой.

Тестирование мрамора RxJS - это обширная тема, выходящая за рамки данного руководства. Узнайте об этом в Интернете, начиная с [официальной документации](https://rxjs.dev/guide/testing/marble-testing).

## Компонент с входами и выходами {: #component-with-input-output}

Компонент с входами и выходами обычно появляется внутри шаблона представления главного компонента. Хост использует привязку свойств для установки входного свойства и привязку событий для прослушивания событий, вызванных выходным свойством.

Цель тестирования - проверить, что такие привязки работают так, как ожидается. Тесты должны устанавливать входные значения и прослушивать выходные события.

Компонент `DashboardHeroComponent` - это маленький пример компонента в этой роли. Он отображает отдельного героя, предоставленного `DashboardComponent`.

Щелчок на этом герое сообщает `DashboardComponent`, что пользователь выбрал героя.

Компонент `DashboardHeroComponent` встраивается в шаблон `DashboardComponent` следующим образом:

```html
<dashboard-hero
    *ngFor="let hero of heroes"
    class="col-1-4"
    [hero]="hero"
    (selected)="gotoDetail($event)"
>
</dashboard-hero>
```

Компонент `DashboardHeroComponent` появляется в повторителе `*ngFor`, который устанавливает входное свойство `hero` каждого компонента в значение цикла и слушает событие `selected` компонента.

Вот полное определение компонента:

```ts
@Component({
    selector: 'dashboard-hero',
    template: `
        <button
            type="button"
            (click)="click()"
            class="hero"
        >
            {{ hero.name | uppercase }}
        </button>
    `,
    styleUrls: ['./dashboard-hero.component.css'],
})
export class DashboardHeroComponent {
    @Input() hero!: Hero;
    @Output() selected = new EventEmitter<Hero>();
    click() {
        this.selected.emit(this.hero);
    }
}
```

Хотя тестирование такого простого компонента имеет небольшую внутреннюю ценность, стоит знать, как это сделать. Используйте один из этих подходов:

-   Протестируйте его как используемый `DashboardComponent`.
-   Тестируйте его как отдельный компонент
-   Протестируйте его в качестве замены `DashboardComponent`.

Беглый взгляд на конструктор `DashboardComponent` отталкивает от первого подхода:

```ts
constructor(private router: Router, private heroService: HeroService) {}
```

Компонент `DashboardComponent` зависит от Angular router и `HeroService`. Скорее всего, вам придется заменить их оба тестовыми дублями, а это большая работа.

Маршрутизатор кажется особенно сложным.

!!!note ""

    В [следующем обсуждении](#routing-component) рассматривается тестирование компонентов, для которых требуется маршрутизатор.

Ближайшей целью является тестирование `DashboardHeroComponent`, а не `DashboardComponent`, поэтому попробуйте второй и третий варианты.

### Тест `DashboardHeroComponent` stand-alone {: #dashboard-standalone}

Вот основная часть настройки файла спецификации.

```ts
TestBed.configureTestingModule({
    declarations: [DashboardHeroComponent],
});
fixture = TestBed.createComponent(DashboardHeroComponent);
comp = fixture.componentInstance;

// find the hero's DebugElement and element
heroDe = fixture.debugElement.query(By.css('.hero'));
heroEl = heroDe.nativeElement;

// mock the hero supplied by the parent component
expectedHero = { id: 42, name: 'Test Name' };

// simulate the parent setting the input property with that hero
comp.hero = expectedHero;

// trigger initial data binding
fixture.detectChanges();
```

Обратите внимание, как код установки назначает тестового героя (`expectedHero`) свойству компонента `hero`, эмулируя способ, которым `DashboardComponent` установит его с помощью привязки свойства в своем ретрансляторе.

Следующий тест проверяет, что имя героя передается в шаблон с помощью привязки.

```ts
it('should display hero name in uppercase', () => {
    const expectedPipedName = expectedHero.name.toUpperCase();
    expect(heroEl.textContent).toContain(expectedPipedName);
});
```

Поскольку [template](#dashboard-hero-component) передает имя героя через Angular `UpperCasePipe`, тест должен сопоставить значение элемента с именем в верхнем регистре.

!!!note ""

    Этот небольшой тест демонстрирует, как тесты Angular могут проверить визуальное представление компонента &mdash; то, что невозможно с помощью [тестов классов компонентов](testing-components-basics.md#component-class-testing) &mdash; с небольшими затратами и без использования гораздо более медленных и сложных сквозных тестов.

### Щелчок

Нажатие на героя должно вызвать событие `selected`, которое может услышать главный компонент (`DashboardComponent` предположительно):

```ts
it('should raise selected event when clicked (triggerEventHandler)', () => {
    let selectedHero: Hero | undefined;
    comp.selected
        .pipe(first())
        .subscribe((hero: Hero) => (selectedHero = hero));

    heroDe.triggerEventHandler('click');
    expect(selectedHero).toBe(expectedHero);
});
```

Свойство компонента `selected` возвращает `EventEmitter`, который для потребителей выглядит как RxJS синхронный `Observable`. Тест подписывается на него _явно_, так же как и компонент-хозяин _неявно_.

Если компонент ведет себя так, как ожидается, щелчок по элементу героя должен заставить свойство `selected` компонента выдать объект `hero`.

Тест обнаруживает это событие через свою подписку на `selected`.

### `triggerEventHandler` {: #trigger-event-handler}

`heroDe` в предыдущем тесте - это `DebugElement`, который представляет героя `<div>`.

Он имеет свойства и методы Angular, которые абстрагируют взаимодействие с родным элементом. Этот тест вызывает `DebugElement.triggerEventHandler` с именем события "click".

Привязка события "click" отвечает вызовом `DashboardHeroComponent.click()`.

Angular `DebugElement.triggerEventHandler` может вызывать _любое связанное с данными событие_ по своему _имени события_. Вторым параметром является объект события, переданный обработчику.

Тест вызвал событие "клик".

```ts
heroDe.triggerEventHandler('click');
```

В этом случае тест правильно предполагает, что обработчик события во время выполнения, метод `click()` компонента, не заботится об объекте события.

!!!note ""

    Другие обработчики менее снисходительны. Например, директива `RouterLink` ожидает объект со свойством `button`, которое определяет, какая кнопка мыши, если таковая имеется, была нажата во время щелчка.

    Директива `RouterLink` выбрасывает ошибку, если объект события отсутствует.

### Клик по элементу

Следующая тестовая альтернатива вызывает собственный метод `click()` родного элемента, что вполне подходит для _этого компонента_.

```ts
it('should raise selected event when clicked (element.click)', () => {
    let selectedHero: Hero | undefined;
    comp.selected
        .pipe(first())
        .subscribe((hero: Hero) => (selectedHero = hero));

    heroEl.click();
    expect(selectedHero).toBe(expectedHero);
});
```

### `click()` helper {: #click-helper}

Нажатие на кнопку, якорь или произвольный элемент HTML является распространенной задачей тестирования.

Чтобы сделать ее последовательной и простой, инкапсулируйте процесс _нажатия_ в помощнике, таком как следующая функция `click()`:

```ts
/** Button events to pass to `DebugElement.triggerEventHandler` for RouterLink event handler */
export const ButtonClickEvents = {
    left: { button: 0 },
    right: { button: 2 },
};

/** Simulate element click. Defaults to mouse left-button click event. */
export function click(
    el: DebugElement | HTMLElement,
    eventObj: any = ButtonClickEvents.left
): void {
    if (el instanceof HTMLElement) {
        el.click();
    } else {
        el.triggerEventHandler('click', eventObj);
    }
}
```

Первый параметр - это _элемент для клика_. Если хотите, передайте пользовательский объект события в качестве второго параметра.

По умолчанию используется частичный [объект события левой кнопки мыши](https://developer.mozilla.org/docs/Web/API/MouseEvent/button), принимаемый многими обработчиками, включая директиву `RouterLink`.

!!!warning ""

    Вспомогательная функция `click()` **не** является одной из утилит тестирования Angular. Это функция, определенная в _коде примера этого руководства_.
    Все примеры тестов используют ее.

    Если она вам нравится, добавьте ее в свою собственную коллекцию помощников.

Вот предыдущий тест, переписанный с использованием помощника `click`.

```ts
it('should raise selected event when clicked (click helper with DebugElement)', () => {
    let selectedHero: Hero | undefined;
    comp.selected
        .pipe(first())
        .subscribe((hero: Hero) => (selectedHero = hero));

    click(heroDe); // click helper with DebugElement

    expect(selectedHero).toBe(expectedHero);
});
```

## Компонент внутри тестового хоста {: #component-inside-test-host}

В предыдущих тестах роль хоста `DashboardComponent` выполняли сами компоненты. Но правильно ли работает `DashboardHeroComponent` при правильной привязке данных к компоненту хоста?

Вы могли бы тестировать с помощью фактического `DashboardComponent`. Но это может потребовать много настроек, особенно если в его шаблоне есть повторитель `*ngFor`, другие компоненты, HTML макета, дополнительные привязки, конструктор, который внедряет множество сервисов, и он сразу же начинает взаимодействовать с этими сервисами.

Представьте себе, сколько усилий нужно приложить, чтобы отключить все эти отвлекающие факторы, только чтобы доказать, что можно удовлетворительно доказать с помощью _тестового хоста_, подобного этому:

```ts
@Component({
    template: ` <dashboard-hero
        [hero]="hero"
        (selected)="onSelected($event)"
    >
    </dashboard-hero>`,
})
class TestHostComponent {
    hero: Hero = { id: 42, name: 'Test Name' };
    selectedHero: Hero | undefined;
    onSelected(hero: Hero) {
        this.selectedHero = hero;
    }
}
```

Этот тестовый хост привязывается к `DashboardHeroComponent`, как и `DashboardComponent`, но без шума `Router`, `HeroService` или повторителя `*ngFor`.

Тестовый хост устанавливает свойство ввода компонента `hero` со своим тестовым героем. Он связывает событие `selected` компонента с его обработчиком `onSelected`, который записывает выданного героя в свойство `selectedHero`.

Позже тесты смогут проверить `selectedHero`, чтобы убедиться, что событие `DashboardHeroComponent.selected` вызвало ожидаемого героя.

Настройка для тестов `test-host` аналогична настройке для автономных тестов:

```ts
TestBed.configureTestingModule({
    declarations: [
        DashboardHeroComponent,
        TestHostComponent,
    ],
});
// create TestHostComponent instead of DashboardHeroComponent
fixture = TestBed.createComponent(TestHostComponent);
testHost = fixture.componentInstance;
heroEl = fixture.nativeElement.querySelector('.hero');
fixture.detectChanges(); // trigger initial data binding
```

Эта конфигурация модуля тестирования показывает три важных отличия:

-   Он _объявляет_ и `DashboardHeroComponent`, и `TestHostComponent`.
-   Он _создает_ `TestHostComponent` вместо `DashboardHeroComponent`.
-   Компонент `TestHostComponent` устанавливает `DashboardHeroComponent.hero` с привязкой

Функция `createComponent` возвращает `fixture`, содержащий экземпляр `TestHostComponent` вместо экземпляра `DashboardHeroComponent`.

Создание `TestHostComponent` имеет побочный эффект создания `DashboardHeroComponent`, потому что последний появляется в шаблоне первого. Запрос на элемент героя (`heroEl`) по-прежнему находит его в тестовом DOM, хотя и на большей глубине дерева элементов, чем раньше.

Сами тесты практически идентичны автономной версии:

```ts
it('should display hero name', () => {
    const expectedPipedName = testHost.hero.name.toUpperCase();
    expect(heroEl.textContent).toContain(expectedPipedName);
});

it('should raise selected event when clicked', () => {
    click(heroEl);
    // selected hero should be the same data bound hero
    expect(testHost.selectedHero).toBe(testHost.hero);
});
```

Отличается только тест выбранного события. Он подтверждает, что выбранный герой `DashboardHeroComponent` действительно находит путь наверх через привязку событий к главному компоненту.

## Компонент маршрутизации {: #routing-component}

Компонент _маршрутизации_ - это компонент, который указывает `Router` на переход к другому компоненту. Компонент `DashboardComponent` является компонентом маршрутизации, потому что пользователь может перейти к компоненту `HeroDetailComponent`, нажав на одну из _геройских кнопок_ на приборной панели.

Маршрутизация довольно сложна. Тестирование `DashboardComponent` казалось сложным отчасти потому, что в нем задействован `Router`, который он внедряет вместе с `HeroService`.

```ts
constructor(private router: Router, private heroService: HeroService) {}
```

```ts
gotoDetail(hero: Hero) {
  const url = `/heroes/${hero.id}`;
  this.router.navigateByUrl(url);
}
```

Angular предоставляет вспомогательные средства тестирования для уменьшения количества шаблонов и более эффективного тестирования кода, который зависит от `Router` и `HttpClient`.

```ts
TestBed.configureTestingModule({
    providers: [
        provideRouter([
            { path: '**', component: DashboardComponent },
        ]),
        provideHttpClient(),
        provideHttpClientTesting(),
        HeroService,
    ],
})
    .compileComponents()
    .then(async () => {
        harness = await RouterTestingHarness.create();
        comp = await harness.navigateByUrl(
            '/',
            DashboardComponent
        );
        TestBed.inject(HttpTestingController)
            .expectOne('api/heroes')
            .flush(getTestHeroes());
    });
```

Следующий тест нажимает на отображаемого героя и подтверждает, что мы переходим на ожидаемый URL.

```ts
it('should tell navigate when hero clicked', async () => {
    await heroClick(); // trigger click on first inner <div class="hero">

    // expecting to navigate to id of the component's first hero
    const id = comp.heroes[0].id;
    expect(TestBed.inject(Router).url)
        .withContext(
            'should nav to HeroDetail for first hero'
        )
        .toEqual(`/heroes/${id}`);
});
```

## Маршрутизируемые компоненты {: #routed-component-w-param}

_Маршрутизируемый компонент_ является конечным пунктом навигации `Router`. Его тестирование может быть более сложным, особенно если маршрут к компоненту _включает параметры_.

Компонент `HeroDetailComponent` - это _маршрутизируемый компонент_, который является конечным пунктом такого маршрута.

Когда пользователь нажимает на героя _Dashboard_, `DashboardComponent` говорит `Router` перейти к `heroes/:id`. `:id` - это параметр маршрута, значением которого является `id` героя для редактирования.

Маршрутизатор `Router` сопоставляет этот URL с маршрутом к компоненту `HeroDetailComponent`. Он создает объект `ActivatedRoute` с информацией о маршрутизации и вставляет его в новый экземпляр `HeroDetailComponent`.

Вот конструктор `HeroDetailComponent`:

```ts
constructor(
  private heroDetailService: HeroDetailService,
  private route: ActivatedRoute,
  private router: Router) {
}
```

Компоненту `HeroDetail` необходим параметр `id`, чтобы он мог получить соответствующего героя с помощью `HeroDetailService`. Компонент должен получить `id` из свойства `ActivatedRoute.paramMap`, которое является `Observable`.

Он не может просто ссылаться на свойство `id` из `ActivatedRoute.paramMap`. Компонент должен _подписаться_ на наблюдаемую `ActivatedRoute.paramMap` и быть готовым к тому, что `id` может измениться в течение его жизни.

```ts
ngOnInit(): void {
  // get hero when `id` param changes
  this.route.paramMap.subscribe(pmap => this.getHero(pmap.get('id')));
}
```

!!!note ""

    В разделе [ActivatedRoute в действии](router-tutorial-toh.md#activated-route-in-action) руководства [Router tutorial: tour of heroes](router-tutorial-toh.md) более подробно рассматривается `ActivatedRoute.paramMap`.

Тесты могут исследовать, как `HeroDetailComponent` реагирует на различные значения параметра `id`, переходя к различным маршрутам.

### Тестирование с помощью `RouterTestingHarness`

Вот тест, демонстрирующий поведение компонента, когда наблюдаемый `id` относится к существующему герою:

```ts
describe('when navigate to existing hero', () => {
  let expectedHero: Hero;

  beforeEach(async () => {
    expectedHero = firstHero;
    await createComponent(expectedHero.id);
  });
  it('should display that hero\'s name', () => {
    expect(page.nameDisplay.textContent).toBe(expectedHero.name);
  });
```

!!!note ""

    В следующем разделе рассматриваются метод `createComponent()` и объект `page`. Пока полагайтесь на свою интуицию.

Когда `id` не может быть найден, компонент должен перенаправить на `HeroListComponent`.

При настройке тестового набора был использован тот же жгут маршрутизаторов [описанный выше](#routing-component).

Этот тест ожидает, что компонент попытается перейти к `HeroListComponent`.

```ts
describe('when navigate to non-existent hero id', () => {
    beforeEach(async () => {
        await createComponent(999);
    });

    it('should try to navigate back to hero list', () => {
        expect(TestBed.inject(Router).url).toEqual(
            '/heroes'
        );
    });
});
```

## Тесты вложенных компонентов

Шаблоны компонентов часто имеют вложенные компоненты, шаблоны которых могут содержать еще больше компонентов.

Дерево компонентов может быть очень глубоким, и в большинстве случаев вложенные компоненты не играют никакой роли в тестировании компонента, находящегося в верхней части дерева.

Например, `AppComponent` отображает навигационную панель с якорями и их директивами `RouterLink`.

```html
<app-banner></app-banner>
<app-welcome></app-welcome>
<nav>
    <a routerLink="/dashboard">Dashboard</a>
    <a routerLink="/heroes">Heroes</a>
    <a routerLink="/about">About</a>
</nav>
<router-outlet></router-outlet>
```

Чтобы проверить ссылки, вам не нужен `Router` для навигации и не нужен `<router-outlet>`, чтобы отметить, куда `Router` вставляет _маршрутизируемые компоненты_.

Компоненты `BannerComponent` и `WelcomeComponent` (обозначаемые `<app-banner>` и `<app-welcome>`) также не имеют значения.

Тем не менее, любой тест, создающий `AppComponent` в DOM, также создает экземпляры этих трех компонентов, и, если вы позволите этому случиться, вам придется настроить `TestBed` на их создание.

Если вы не объявите их, компилятор Angular не распознает теги `<app-banner>`, `<app-welcome>` и `<router-outlet>` в шаблоне `AppComponent` и выдаст ошибку.

Если вы объявите реальные компоненты, вам также придется объявить _их_ вложенные компоненты и обеспечить _все_ сервисы, внедряемые в _любой_ компонент в дереве.

Это слишком много усилий только для того, чтобы ответить на несколько простых вопросов о связях.

В этом разделе описаны две техники для минимизации настройки. Используйте их по отдельности или в комбинации, чтобы сосредоточиться на тестировании основного компонента.

### Создание заглушек ненужных компонентов {: #stub-component}

В первой технике вы создаете и объявляете заглушки компонентов и директив, которые играют незначительную роль или не играют никакой роли в тестах.

```ts
@Component({ selector: 'app-banner', template: '' })
class BannerStubComponent {}

@Component({ selector: 'router-outlet', template: '' })
class RouterOutletStubComponent {}

@Component({ selector: 'app-welcome', template: '' })
class WelcomeStubComponent {}
```

Селекторы заглушек совпадают с селекторами соответствующих реальных компонентов. Но их шаблоны и классы пусты.

Тогда объявите их в конфигурации `TestBed` рядом с компонентами, директивами и пайпами, которые должны быть реальными.

```ts
TestBed.configureTestingModule({
    imports: [RouterLink],
    providers: [provideRouter([])],
    declarations: [
        AppComponent,
        BannerStubComponent,
        RouterOutletStubComponent,
        WelcomeStubComponent,
    ],
});
```

Компонент `AppComponent` является объектом тестирования, поэтому, конечно, вы объявляете реальную версию.

Все остальное - это заглушки.

### `NO_ERRORS_SCHEMA` {: #no-errors-schema}

При втором подходе добавьте `NO_ERRORS_SCHEMA` в метаданные `TestBed.schemas`.

```ts
TestBed.configureTestingModule({
    declarations: [AppComponent],
    providers: [provideRouter([])],
    imports: [RouterLink],
    schemas: [NO_ERRORS_SCHEMA],
});
```

Схема `NO_ERRORS_SCHEMA` указывает компилятору Angular игнорировать нераспознанные элементы и атрибуты.

Компилятор распознает элемент `<app-root>` и атрибут `routerLink`, потому что вы объявили соответствующие `AppComponent` и `RouterLink` в конфигурации `TestBed`.

Но компилятор не выдаст ошибку, когда встретит `<app-banner>`, `<app-welcome>` или `<router-outlet>`. Он просто отображает их как пустые теги, и браузер их игнорирует.

Вам больше не нужны компоненты-заглушки.

### Используйте обе техники вместе.

Это техники для _Shallow Component Testing_, названные так потому, что они уменьшают визуальную поверхность компонента только до тех элементов в шаблоне компонента, которые важны для тестов.

Подход `NO_ERRORS_SCHEMA` является более простым из двух, но не злоупотребляйте им.

Использование `NO_ERRORS_SCHEMA` также не позволит компилятору сообщить вам о недостающих компонентах и атрибутах, которые вы случайно пропустили или неправильно написали. Вы можете потратить часы в погоне за фантомными ошибками, которые компилятор обнаружил бы мгновенно.

У подхода _компонента-заглушки_ есть еще одно преимущество. Хотя заглушки в _этом_ примере были пустыми, вы можете дать им урезанные шаблоны и классы, если ваши тесты должны каким-то образом взаимодействовать с ними.

На практике вы будете сочетать эти два метода в одной установке, как показано в этом примере.

```ts
TestBed.configureTestingModule({
    declarations: [AppComponent, BannerStubComponent],
    providers: [provideRouter([])],
    imports: [RouterLink],
    schemas: [NO_ERRORS_SCHEMA],
});
```

Компилятор Angular создает `BannerStubComponent` для элемента `<app-banner>` и применяет `RouterLink` к якорям с атрибутом `routerLink`, но игнорирует теги `<app-welcome>` и `<router-outlet>`.

### `By.directive` и инжектируемые директивы {: #by-directive}

Еще немного настроек запускают начальное связывание данных и получают ссылки на навигационные ссылки:

```ts
beforeEach(() => {
    fixture.detectChanges(); // trigger initial data binding

    // find DebugElements with an attached RouterLinkStubDirective
    linkDes = fixture.debugElement.queryAll(
        By.directive(RouterLink)
    );

    // get attached link directive instances
    // using each DebugElement's injector
    routerLinks = linkDes.map((de) =>
        de.injector.get(RouterLink)
    );
});
```

Три точки, представляющие особый интерес:

-   Найдите элементы якоря с вложенной директивой с помощью `By.directive`.
-   Запрос возвращает обертки `DebugElement` вокруг соответствующих элементов.
-   Каждый `DebugElement` раскрывает инжектор зависимости с конкретным экземпляром директивы, прикрепленной к этому элементу.

Ссылки `AppComponent` для проверки следующие:

```html
<nav>
    <a routerLink="/dashboard">Dashboard</a>
    <a routerLink="/heroes">Heroes</a>
    <a routerLink="/about">About</a>
</nav>
```

Вот несколько тестов, которые подтверждают, что эти ссылки подключены к директивам `routerLink`, как и ожидалось:

```ts
it('can get RouterLinks from template', () => {
    expect(routerLinks.length)
        .withContext('should have 3 routerLinks')
        .toBe(3);
    expect(routerLinks[0].href).toBe('/dashboard');
    expect(routerLinks[1].href).toBe('/heroes');
    expect(routerLinks[2].href).toBe('/about');
});

it('can click Heroes link in template', fakeAsync(() => {
    const heroesLinkDe = linkDes[1]; // heroes link DebugElement

    TestBed.inject(Router).resetConfig([
        { path: '**', children: [] },
    ]);
    heroesLinkDe.triggerEventHandler('click', {
        button: 0,
    });
    tick();
    fixture.detectChanges();

    expect(TestBed.inject(Router).url).toBe('/heroes');
}));
```

## Использование объекта `page` {: #page-object}

Компонент `HeroDetailComponent` - это простое представление с заголовком, двумя полями героя и двумя кнопками.

![HeroDetailComponent in action](hero-detail.component.png)

Но даже в этой простой форме есть много сложностей с шаблонами.

```html
<div *ngIf="hero">
    <h2><span>{{hero.name | titlecase}}</span> Details</h2>
    <div><span>id: </span>{{hero.id}}</div>
    <div>
        <label for="name">name: </label>
        <input
            id="name"
            [(ngModel)]="hero.name"
            placeholder="name"
        />
    </div>
    <button type="button" (click)="save()">Save</button>
    <button type="button" (click)="cancel()">Cancel</button>
</div>
```

Тесты, проверяющие работу компонента, должны &hellip;

-   Дождаться появления героя, прежде чем элементы появятся в DOM
-   Ссылка на текст заголовка
-   Ссылка на поле ввода имени, чтобы проверить и установить его
-   Ссылки на две кнопки, чтобы их можно было нажать
-   Ссылки на некоторые методы компонентов и маршрутизаторов

Даже такая маленькая форма, как эта, может создать беспорядок из мучительных условных настроек и выбора элементов CSS.

Справиться со сложностью можно с помощью класса `Page`, который обрабатывает доступ к свойствам компонента и инкапсулирует логику, которая их устанавливает.

Вот такой класс `Page` для `hero-detail.component.spec.ts`

```ts
class Page {
    // getter properties wait to query the DOM until called.
    get buttons() {
        return this.queryAll<HTMLButtonElement>('button');
    }
    get saveBtn() {
        return this.buttons[0];
    }
    get cancelBtn() {
        return this.buttons[1];
    }
    get nameDisplay() {
        return this.query<HTMLElement>('span');
    }
    get nameInput() {
        return this.query<HTMLInputElement>('input');
    }

    //// query helpers ////
    private query<T>(selector: string): T {
        return harness.routeNativeElement!.querySelector(
            selector
        )! as T;
    }

    private queryAll<T>(selector: string): T[] {
        return (harness.routeNativeElement!.querySelectorAll(
            selector
        ) as any) as T[];
    }
}
```

Теперь важные крючки для манипулирования компонентом и его проверки аккуратно организованы и доступны из экземпляра `Page`.

Метод `createComponent` создает объект `page` и заполняет пустые места, когда появляется `герой`.

```ts
async function createComponent(id: number) {
    harness = await RouterTestingHarness.create();
    component = await harness.navigateByUrl(
        `/heroes/${id}`,
        HeroDetailComponent
    );
    page = new Page();

    const request = TestBed.inject(
        HttpTestingController
    ).expectOne(`api/heroes/?id=${id}`);
    const hero = getTestHeroes().find(
        (h) => h.id === Number(id)
    );
    request.flush(hero ? [hero] : []);
    harness.detectChanges();
}
```

Вот еще несколько тестов `HeroDetailComponent`, чтобы усилить суть.

```ts
it("should display that hero's name", () => {
    expect(page.nameDisplay.textContent).toBe(
        expectedHero.name
    );
});

it('should navigate when click cancel', () => {
    click(page.cancelBtn);
    expect(TestBed.inject(Router).url).toEqual(
        `/heroes/${expectedHero.id}`
    );
});

it('should save when click save but not navigate immediately', () => {
    click(page.saveBtn);
    expect(
        TestBed.inject(HttpTestingController).expectOne({
            method: 'PUT',
            url: 'api/heroes',
        })
    );
    expect(TestBed.inject(Router).url).toEqual(
        '/heroes/41'
    );
});

it('should navigate when click save and save resolves', fakeAsync(() => {
    click(page.saveBtn);
    tick(); // wait for async save to complete
    expect(TestBed.inject(Router).url).toEqual(
        '/heroes/41'
    );
}));

it('should convert hero name to Title Case', () => {
    // get the name's input and display elements from the DOM
    const hostElement: HTMLElement = harness.routeNativeElement!;
    const nameInput: HTMLInputElement = hostElement.querySelector(
        'input'
    )!;
    const nameDisplay: HTMLElement = hostElement.querySelector(
        'span'
    )!;

    // simulate user entering a new name into the input box
    nameInput.value = 'quick BROWN  fOx';

    // Dispatch a DOM event so that Angular learns of input value change.
    nameInput.dispatchEvent(new Event('input'));

    // Tell Angular to update the display binding through the title pipe
    harness.detectChanges();

    expect(nameDisplay.textContent).toBe(
        'Quick Brown  Fox'
    );
});
```

## Вызов `compileComponents()` {: #compile-components}

!!!note ""

    Игнорируйте этот раздел, если вы _только_ запускаете тесты с помощью команды CLI `ng test`, поскольку CLI компилирует приложение перед запуском тестов.

Если вы запускаете тесты в **не-CLI-среде**, тесты могут завершиться неудачей с сообщением, подобным этому:

```shell
Error: This test module uses the component BannerComponent
which is using a "templateUrl" or "styleUrls", but they were never compiled.
Please call "TestBed.compileComponents" before your test.
```

Корень проблемы в том, что хотя бы один из компонентов, участвующих в тестировании, указывает внешний шаблон или CSS файл, как это делает следующая версия `BannerComponent`.

```ts
import { Component } from '@angular/core';

@Component({
    selector: 'app-banner',
    templateUrl: './banner-external.component.html',
    styleUrls: ['./banner-external.component.css'],
})
export class BannerComponent {
    title = 'Test Tour of Heroes';
}
```

Тест терпит неудачу, когда `TestBed` пытается создать компонент.

```ts
beforeEach(async () => {
    await TestBed.configureTestingModule({
        declarations: [BannerComponent],
    }); // missing call to compileComponents()
    fixture = TestBed.createComponent(BannerComponent);
});
```

Напомним, что приложение не было скомпилировано. Поэтому, когда вы вызываете `createComponent()`, `TestBed` компилируется неявно.

Это не проблема, когда исходный код находится в памяти. Но `BannerComponent` требует внешних файлов, которые компилятор должен читать из файловой системы, что по своей сути является _асинхронной_ операцией.

Если бы `TestBed` было разрешено продолжить работу, тесты запустились бы и загадочно провалились, прежде чем компилятор смог бы закончить работу.

Вытесняющее сообщение об ошибке говорит вам о необходимости явной компиляции с помощью `compileComponents()`.

### `compileComponents()` является асинхронным

Вы должны вызывать `compileComponents()` внутри асинхронной тестовой функции.

!!!danger ""

    Если вы пренебрежете тем, чтобы сделать тестовую функцию асинхронной (например, забудете использовать `waitForAsync()`, как описано), вы увидите следующее сообщение об ошибке

    ```shell
    Error: ViewDestroyedError: Attempt to use a destroyed view
    ```

Типичным подходом является разделение логики настройки на две отдельные функции `beforeEach()`:

| Функции                    | Подробности                    |
| :------------------------- | :----------------------------- |
| Асинхронная `beforeEach()` | Компиляция компонентов         |
| Синхронная `beforeEach()`  | Выполняет оставшуюся настройку |

### Асинхронный `beforeEach`

Напишите первый асинхронный `beforeEach` следующим образом.

```ts
beforeEach(async () => {
    await TestBed.configureTestingModule({
        declarations: [BannerComponent],
    }).compileComponents(); // compile template and css
});
```

Метод `TestBed.configureTestingModule()` возвращает класс `TestBed`, чтобы вы могли цепочкой вызывать другие статические методы `TestBed`, такие как `compileComponents()`.

В этом примере `BannerComponent` является единственным компонентом, который будет скомпилирован. В других примерах модуль тестирования конфигурируется с несколькими компонентами и может импортировать прикладные модули, содержащие еще больше компонентов.

Для любого из них могут потребоваться внешние файлы.

Метод `TestBed.compileComponents` асинхронно компилирует все компоненты, настроенные в модуле тестирования.

!!!warning ""

    Не переконфигурируйте `TestBed` после вызова `compileComponents()`.

Вызов `compileComponents()` закрывает текущий экземпляр `TestBed` для дальнейшей конфигурации. Вы не можете больше вызывать никаких методов конфигурации `TestBed`, ни `configureTestingModule()`, ни каких-либо методов `override...`.
При попытке вызова `TestBed` выдает ошибку.

Сделайте `compileComponents()` последним шагом перед вызовом `TestBed.createComponent()`.

### Синхронный `beforeEach`

Вторая, синхронная `beforeEach()` содержит оставшиеся шаги настройки, которые включают создание компонента и запрос элементов для проверки.

```ts
beforeEach(() => {
    fixture = TestBed.createComponent(BannerComponent);
    component = fixture.componentInstance; // BannerComponent test instance
    h1 = fixture.nativeElement.querySelector('h1');
});
```

Рассчитывает на то, что бегунок теста будет ждать завершения первого асинхронного `beforeEach` перед вызовом второго.

### Консолидированная настройка

Вы можете объединить две функции `beforeEach()` в одну асинхронную `beforeEach()`.

Метод `compileComponents()` возвращает обещание, поэтому вы можете выполнять синхронные задачи настройки _после_ компиляции, перемещая синхронный код после ключевого слова `await`, где обещание было разрешено.

```ts
beforeEach(async () => {
    await TestBed.configureTestingModule({
        declarations: [BannerComponent],
    }).compileComponents();
    fixture = TestBed.createComponent(BannerComponent);
    component = fixture.componentInstance;
    h1 = fixture.nativeElement.querySelector('h1');
});
```

### `compileComponents()` безвреден

Нет никакого вреда в вызове `compileComponents()`, когда это не требуется.

Файл теста компонентов, сгенерированный CLI, вызывает `compileComponents()`, хотя он никогда не требуется при запуске `ng test`.

Тесты в этом руководстве вызывают `compileComponents` только тогда, когда это необходимо.

## Настройка с импортом модуля {: #import-module}

В предыдущих компонентных тестах модуль тестирования конфигурировался с помощью нескольких `деклараций`, например, так:

```ts
TestBed.configureTestingModule({
    declarations: [DashboardHeroComponent],
});
```

Компонент `DashboardComponent` прост. Он не нуждается в помощи.

Но более сложные компоненты часто зависят от других компонентов, директив, пайпов и провайдеров, и они тоже должны быть добавлены в модуль тестирования.

К счастью, параметр `TestBed.configureTestingModule` параллелен метаданным, передаваемым декоратору `@NgModule`, что означает, что вы также можете указать `провайдеры` и `импорты`.

Компонент `HeroDetailComponent` требует много помощи, несмотря на свой небольшой размер и простую конструкцию. В дополнение к поддержке, которую он получает от модуля тестирования по умолчанию `CommonModule`, ему необходимы:

-   `NgModel` и друзья в `FormsModule` для обеспечения двустороннего связывания данных
-   `TitleCasePipe` из папки `shared`
-   Службы маршрутизатора
-   Службы доступа к данным Hero

Один из подходов заключается в настройке модуля тестирования из отдельных частей, как в этом примере:

```ts
beforeEach(async () => {
    await TestBed.configureTestingModule({
        imports: [FormsModule],
        declarations: [HeroDetailComponent, TitleCasePipe],
        providers: [
            provideHttpClient(),
            provideHttpClientTesting(),
            provideRouter([
                {
                    path: 'heroes/:id',
                    component: HeroDetailComponent,
                },
            ]),
        ],
    }).compileComponents();
});
```

!!!note ""

    Обратите внимание, что `beforeEach()` является асинхронным и вызывает `TestBed.compileComponents`, поскольку `HeroDetailComponent` имеет внешний шаблон и css-файл.

    Как объясняется в [Вызов `compileComponents()`](#compile-components), эти тесты могут быть запущены в среде без CLI, где Angular придется компилировать их в браузере.

### Импорт общего модуля

Поскольку многие компоненты приложения нуждаются в `FormsModule` и `TitleCasePipe`, разработчик создал `SharedModule` для объединения этих и других часто запрашиваемых частей.

Тестовая конфигурация тоже может использовать `SharedModule`, как показано в этой альтернативной установке:

```ts
beforeEach(async () => {
    await TestBed.configureTestingModule({
        imports: [SharedModule],
        declarations: [HeroDetailComponent],
        providers: [
            provideRouter([
                {
                    path: 'heroes/:id',
                    component: HeroDetailComponent,
                },
            ]),
            provideHttpClient(),
            provideHttpClientTesting(),
        ],
    }).compileComponents();
});
```

Он немного более плотный и компактный, с меньшим количеством операторов импорта, которые не показаны в этом примере.

### Импорт функционального модуля {: #feature-module-import}

Компонент `HeroDetailComponent` является частью `HeroModule` [Feature Module](feature-modules.md), который объединяет большее количество взаимозависимых частей, включая `SharedModule`. Попробуйте тестовую конфигурацию, которая импортирует `HeroModule`, как эта:

```ts
beforeEach(async () => {
    await TestBed.configureTestingModule({
        imports: [HeroModule],
        //  declarations: [ HeroDetailComponent ], // NO!  DOUBLE DECLARATION
        providers: [
            provideRouter([
                {
                    path: 'heroes/:id',
                    component: HeroDetailComponent,
                },
                {
                    path: 'heroes',
                    component: HeroListComponent,
                },
            ]),
            provideHttpClient(),
            provideHttpClientTesting(),
        ],
    }).compileComponents();
});
```

Остаются только _тестовые двойники_ в `providers`. Даже объявление `HeroDetailComponent` исчезло.

На самом деле, если вы попытаетесь объявить его, Angular выдаст ошибку, потому что `HeroDetailComponent` объявлен и в `HeroModule`, и в `DynamicTestModule`, созданном `TestBed`.

!!!note ""

    Импорт функционального модуля компонента может быть лучшим способом настройки тестов, если в модуле много взаимных зависимостей, а сам модуль небольшой, как это обычно бывает с функциональными модулями.

## Переопределение провайдеров компонента {: #component-override}

Компонент `HeroDetailComponent` предоставляет свой собственный `HeroDetailService`.

```ts
@Component({
    selector: 'app-hero-detail',
    templateUrl: './hero-detail.component.html',
    styleUrls: ['./hero-detail.component.css'],
    providers: [HeroDetailService],
})
export class HeroDetailComponent implements OnInit {
    constructor(
        private heroDetailService: HeroDetailService,
        private route: ActivatedRoute,
        private router: Router
    ) {}
}
```

Невозможно заглушить `HeroDetailService` компонента в `providers` модуля `TestBed.configureTestingModule`. Это провайдеры для _модуля тестирования_, а не для компонента.

Они подготавливают инжектор зависимостей на уровне _компонента_.

Angular создает компонент со своим _собственным_ инжектором, который является _дочерним_ инжектором приспособления. Он регистрирует провайдеров компонента (в данном случае `HeroDetailService`) с дочерним инжектором.

Тест не может получить доступ к сервисам дочернего инжектора из инжектора приспособления. И `TestBed.configureTestingModule` также не может их сконфигурировать.

Angular все это время создавал новые экземпляры настоящего `HeroDetailService`!

!!!note ""

    Эти тесты могут завершиться неудачей или таймаутом, если `HeroDetailService` выполняет собственные XHR-вызовы к удаленному серверу. А удаленного сервера может и не быть.

    К счастью, `HeroDetailService` делегирует ответственность за удаленный доступ к данным инжектированному `HeroService`.

    ```ts
    @Injectable({ providedIn: 'root' })
    export class HeroDetailService {
    	constructor(private heroService: HeroService) {}
    	/* . . . */
    }
    ```

    В [предыдущей тестовой конфигурации](#feature-module-import) настоящий `HeroService` заменен на `TestHeroService`, который перехватывает запросы сервера и подделывает их ответы.

Что, если вам не повезло. Что если подделать `HeroService` сложно?
Что если `HeroDetailService` делает собственные запросы к серверу?

Метод `TestBed.overrideComponent` может заменить `провайдеры` компонента на простые в управлении _тестовые двойники_, как показано в следующем варианте установки:

```ts
beforeEach(async () => {
    await TestBed.configureTestingModule({
        imports: [HeroModule],
        providers: [
            provideRouter([
                {
                    path: 'heroes/:id',
                    component: HeroDetailComponent,
                },
            ]),
            // HeroDetailService at this level is IRRELEVANT!
            { provide: HeroDetailService, useValue: {} },
        ],
    })
        .overrideComponent(HeroDetailComponent, {
            set: {
                providers: [
                    {
                        provide: HeroDetailService,
                        useClass: HeroDetailServiceSpy,
                    },
                ],
            },
        })
        .compileComponents();
});
```

Обратите внимание, что `TestBed.configureTestingModule` больше не предоставляет поддельный `HeroService`, потому что он [не нужен](#spy-stub).

### Метод `overrideComponent` {: #override-component-method}

Сфокусируйтесь на методе `overrideComponent`.

```ts
.overrideComponent(
    HeroDetailComponent,
    {set: {providers: [{provide: HeroDetailService, useClass: HeroDetailServiceSpy}]}})
```

Он принимает два аргумента: тип компонента для переопределения (`HeroDetailComponent`) и объект метаданных переопределения. Объект метаданных [override metadata object](testing-utility-apis.md#metadata-override-object) является общим, определяемым следующим образом:

```ts
type MetadataOverride<T> = {
    add?: Partial<T>;
    remove?: Partial<T>;
    set?: Partial<T>;
};
```

Объект переопределения метаданных может либо добавлять и удалять элементы в свойствах метаданных, либо полностью сбрасывать эти свойства. В этом примере сбрасываются метаданные `providers` компонента.

Параметр типа, `T`, является типом метаданных, которые вы передадите декоратору `@Component`:

```js
selector?: string;
template?: string;
templateUrl?: string;
providers?: any[];
…
```

### Предоставление заглушки _шпиона_ (`HeroDetailServiceSpy`) {: #spy-stub}

Этот пример полностью заменяет массив `providers` компонента на новый массив, содержащий `HeroDetailServiceSpy`.

`HeroDetailServiceSpy` - это заглушка настоящей версии `HeroDetailService`, которая имитирует все необходимые функции этого сервиса. Он не инжектирует и не делегирует на более низкий уровень `HeroService`, поэтому нет необходимости предоставлять тестовый дубль для этого.

Соответствующие тесты `HeroDetailComponent` будут утверждать, что методы `HeroDetailService` были вызваны путем шпионажа за методами сервиса. Соответственно, заглушка реализует свои методы как шпионы:

```ts
class HeroDetailServiceSpy {
    testHero: Hero = { ...testHero };

    /* emit cloned test hero */
    getHero = jasmine
        .createSpy('getHero')
        .and.callFake(() =>
            asyncData(Object.assign({}, this.testHero))
        );

    /* emit clone of test hero, with changes merged in */
    saveHero = jasmine
        .createSpy('saveHero')
        .and.callFake((hero: Hero) =>
            asyncData(Object.assign(this.testHero, hero))
        );
}
```

### Тесты переопределения {: #override-tests}

Теперь тесты могут управлять героем компонента напрямую, манипулируя `testHero` в spy-stub, и подтверждать, что методы сервиса были вызваны.

```ts
let hdsSpy: HeroDetailServiceSpy;

  beforeEach(async () => {
    harness = await RouterTestingHarness.create();
    component = await harness.navigateByUrl(`/heroes/${testHero.id}`, HeroDetailComponent);
    page = new Page();
    // get the component's injected HeroDetailServiceSpy
    hdsSpy = harness.routeDebugElement!.injector.get(HeroDetailService) as any;

    harness.detectChanges();
  });

  it('should have called `getHero`', () => {
    expect(hdsSpy.getHero.calls.count())
        .withContext('getHero called once')
        .toBe(1, 'getHero called once');
  });

  it('should display stub hero\'s name', () => {
    expect(page.nameDisplay.textContent).toBe(hdsSpy.testHero.name);
  });

  it('should save stub hero change', fakeAsync(() => {
       const origName = hdsSpy.testHero.name;
       const newName = 'New Name';

       page.nameInput.value = newName;

       page.nameInput.dispatchEvent(new Event('input'));  // tell Angular

       expect(component.hero.name).withContext('component hero has new name').toBe(newName);
       expect(hdsSpy.testHero.name)
           .withContext('service hero unchanged before save')
           .toBe(origName);

       click(page.saveBtn);
       expect(hdsSpy.saveHero.calls.count()).withContext('saveHero called once').toBe(1);

       tick();  // wait for async save to complete
       expect(hdsSpy.testHero.name)
           .withContext('service hero has new name after save')
           .toBe(newName);
       expect(TestBed.inject(Router).url).toEqual('/heroes');
     }));
}

////////////////////
import {getTestHeroes} from '../model/testing/test-hero.service';

const firstHero = getTestHeroes()[0];

function heroModuleSetup() {
  beforeEach(async () => {
    await TestBed
        .configureTestingModule({
          imports: [HeroModule],
          //  declarations: [ HeroDetailComponent ], // NO!  DOUBLE DECLARATION
          providers: [
            provideRouter([
              {path: 'heroes/:id', component: HeroDetailComponent},
              {path: 'heroes', component: HeroListComponent},
            ]),
            provideHttpClient(),
            provideHttpClientTesting(),
          ]
        })
        .compileComponents();
  });

  describe('when navigate to existing hero', () => {
    let expectedHero: Hero;

    beforeEach(async () => {
      expectedHero = firstHero;
      await createComponent(expectedHero.id);
    });
    it('should display that hero\'s name', () => {
      expect(page.nameDisplay.textContent).toBe(expectedHero.name);
    });

    it('should navigate when click cancel', () => {
      click(page.cancelBtn);
      expect(TestBed.inject(Router).url).toEqual(`/heroes/${expectedHero.id}`);
    });

    it('should save when click save but not navigate immediately', () => {
      click(page.saveBtn);
      expect(TestBed.inject(HttpTestingController).expectOne({method: 'PUT', url: 'api/heroes'}));
      expect(TestBed.inject(Router).url).toEqual('/heroes/41');
    });

    it('should navigate when click save and save resolves', fakeAsync(() => {
         click(page.saveBtn);
         tick();  // wait for async save to complete
         expect(TestBed.inject(Router).url).toEqual('/heroes/41');
       }));

    it('should convert hero name to Title Case', () => {
      // get the name's input and display elements from the DOM
      const hostElement: HTMLElement = harness.routeNativeElement!;
      const nameInput: HTMLInputElement = hostElement.querySelector('input')!;
      const nameDisplay: HTMLElement = hostElement.querySelector('span')!;

      // simulate user entering a new name into the input box
      nameInput.value = 'quick BROWN  fOx';

      // Dispatch a DOM event so that Angular learns of input value change.
      nameInput.dispatchEvent(new Event('input'));

      // Tell Angular to update the display binding through the title pipe
      harness.detectChanges();

      expect(nameDisplay.textContent).toBe('Quick Brown  Fox');
    });

  });

  describe('when navigate to non-existent hero id', () => {
    beforeEach(async () => {
      await createComponent(999);
    });

    it('should try to navigate back to hero list', () => {
      expect(TestBed.inject(Router).url).toEqual('/heroes');
    });
  });
}

/////////////////////
import {FormsModule} from '@angular/forms';
import {TitleCasePipe} from '../shared/title-case.pipe';

function formsModuleSetup() {
  beforeEach(async () => {
    await TestBed
        .configureTestingModule({
          imports: [FormsModule],
          declarations: [HeroDetailComponent, TitleCasePipe],
          providers: [
            provideHttpClient(),
            provideHttpClientTesting(),
            provideRouter([{path: 'heroes/:id', component: HeroDetailComponent}]),
          ]
        })
        .compileComponents();
  });

  it('should display 1st hero\'s name', async () => {
    const expectedHero = firstHero;
    await createComponent(expectedHero.id).then(() => {
      expect(page.nameDisplay.textContent).toBe(expectedHero.name);
    });
  });
}

///////////////////////

function sharedModuleSetup() {
  beforeEach(async () => {
    await TestBed
        .configureTestingModule({
          imports: [SharedModule],
          declarations: [HeroDetailComponent],
          providers: [
            provideRouter([{path: 'heroes/:id', component: HeroDetailComponent}]),
            provideHttpClient(),
            provideHttpClientTesting(),
          ]
        })
        .compileComponents();
  });

  it('should display 1st hero\'s name', async () => {
    const expectedHero = firstHero;
    await createComponent(expectedHero.id).then(() => {
      expect(page.nameDisplay.textContent).toBe(expectedHero.name);
    });
  });
}

/////////// Helpers /////

/** Create the HeroDetailComponent, initialize it, set test variables  */
async function createComponent(id: number) {
  harness = await RouterTestingHarness.create();
  component = await harness.navigateByUrl(`/heroes/${id}`, HeroDetailComponent);
  page = new Page();

  const request = TestBed.inject(HttpTestingController).expectOne(`api/heroes/?id=${id}`);
  const hero = getTestHeroes().find(h => h.id === Number(id));
  request.flush(hero ? [hero] : []);
  harness.detectChanges();
}

class Page {
  // getter properties wait to query the DOM until called.
  get buttons() {
    return this.queryAll<HTMLButtonElement>('button');
  }
  get saveBtn() {
    return this.buttons[0];
  }
  get cancelBtn() {
    return this.buttons[1];
  }
  get nameDisplay() {
    return this.query<HTMLElement>('span');
  }
  get nameInput() {
    return this.query<HTMLInputElement>('input');
  }

  //// query helpers ////
  private query<T>(selector: string): T {
    return harness.routeNativeElement!.querySelector(selector)! as T;
  }

  private queryAll<T>(selector: string): T[] {
    return harness.routeNativeElement!.querySelectorAll(selector) as any as T[];
  }
}
```

### Больше переопределений {: #more-overrides}

Метод `TestBed.overrideComponent` может быть вызван несколько раз для одного и того же или разных компонентов. В `TestBed` есть аналогичные методы `overrideDirective`, `overrideModule` и `overridePipe` для поиска и замены частей этих других классов.

Исследуйте варианты и комбинации самостоятельно.
