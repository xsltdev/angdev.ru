# Сценарии тестирования компонентов

<!-- не закончено #component-with-async-service -->

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

#### Запрос для `<h1>`

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

#### `createComponent()` не связывает данные {: #detect-changes}

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

#### `detectChanges()`

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

#### Автоматическое обнаружение изменений {: #auto-detect-changes}

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

#### Изменение входного значения с помощью `dispatchEvent()` {: #dispatch-event}

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

#### Предоставление дублей для тестирования сервисов {: #service-test-doubles}

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

#### Получение инжектированных сервисов {: #get-injected-service}

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

#### `TestBed.inject()` {: #testbed-inject}

Вы _можете_ также получить сервис из корневого инжектора, используя `TestBed.inject()`. Это проще для запоминания и менее многословно.

Но он работает только тогда, когда Angular инжектирует компонент с экземпляром сервиса в корневой инжектор теста.

В этом тестовом наборе _единственным_ поставщиком `UserService` является корневой модуль тестирования, поэтому безопасно вызывать `TestBed.inject()` следующим образом:

```ts
// UserService from the root injector
userService = TestBed.inject(UserService);
```

!!!note ""

    Случай использования, когда `TestBed.inject()` не работает, смотрите в разделе [_Override component providers_](#component-override), где объясняется, когда и почему вы должны получить сервис из инжектора компонента.

#### Окончательная настройка и тесты {: #welcome-spec-setup}

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

#### Тестирование с помощью spy

При тестировании компонента значение имеет только публичный API сервиса. В целом, сами тесты не должны выполнять вызовы на удаленные серверы.

Они должны эмулировать такие вызовы.

Настройка в этом `app/twain/twain.component.spec.ts` показывает один из способов сделать это:

<code-example header="app/twain/twain.component.spec.ts (setup)" path="testing/src/app/twain/twain.component.spec.ts" region="setup"></code-example>

<a id="service-spy"></a>

Сосредоточьтесь на шпионе.

<code-example path="testing/src/app/twain/twain.component.spec.ts" region="spy"></code-example>.

Шпион устроен таким образом, что при любом вызове `getQuote` получает наблюдаемую с тестовой цитатой. В отличие от реального метода `getQuote()`, этот шпион обходит сервер и возвращает синхронную наблюдаемую, значение которой доступно немедленно.

Вы можете написать много полезных тестов с помощью этого шпиона, несмотря на то, что его `Observable` является синхронным.

<a id="sync-tests"></a>

#### Синхронные тесты

Ключевым преимуществом синхронного `Observable` является то, что вы можете часто превращать асинхронные процессы в синхронные тесты.

<code-example path="testing/src/app/twain/twain.component.spec.ts" region="sync-test"></code-example>.

Поскольку результат шпионажа возвращается синхронно, метод `getQuote()` обновляет сообщение на экране сразу _после_ первого цикла обнаружения изменений, во время которого Angular вызывает `ngOnInit`.

При тестировании пути ошибок вам не так повезет. Хотя сервисный шпион возвращает ошибку синхронно, метод компонента вызывает `setTimeout()`.

Тест должен подождать как минимум один полный оборот движка JavaScript, прежде чем значение станет доступным.

Тест должен стать _асинхронным_.

<a id="fake-async"></a>

#### Асинхронный тест с `fakeAsync()`.

Чтобы использовать функциональность `fakeAsync()`, вы должны импортировать `zone.js/testing` в файл настройки тестов. Если вы создали свой проект с помощью Angular CLI, то `zone-testing` уже импортирован в `src/test.ts`.

Следующий тест подтверждает ожидаемое поведение, когда сервис возвращает `ErrorObservable`.

<code-example path="testing/src/app/twain/twain.component.spec.ts" region="error-test"></code-example>.

<div class="alert is-helpful">

**NOTE**: <br /> The `it()` function receives an argument of the following form.

</div>

<code-example format="javascript" language="javascript">

fakeAsync(() =&gt; { /_ тело теста _/ })

</code-example>

Функция `fakeAsync()` позволяет использовать линейный стиль кодирования, запуская тело теста в специальной тестовой зоне `fakeAsync`. Тело теста кажется синхронным.
В нем нет вложенного синтаксиса\ (например, `Promise.then()`\), который нарушает поток управления.

<div class="alert is-helpful">

Ограничение: Функция `fakeAsync()` не будет работать, если тело теста выполняет вызов `XMLHttpRequest` \(XHR\). Вызовы XHR внутри теста встречаются редко, но если вам необходимо вызвать XHR, смотрите раздел [`waitForAsync()`](#waitForAsync).

</div>

<a id="tick"></a>

#### Функция `tick()`.

Вы должны вызывать [tick()](api/core/testing/tick), чтобы перевести виртуальные часы.

Вызов [tick()](api/core/testing/tick) имитирует течение времени до завершения всех ожидающих асинхронных действий. В данном случае он ожидает `setTimeout()` обработчика ошибок.

Функция [tick()](api/core/testing/tick) принимает в качестве параметров `millis` и `tickOptions`. Параметр `millis` определяет, на сколько продвигаются виртуальные часы, и по умолчанию равен `0`, если не указан. Например, если у вас есть `setTimeout(fn, 100)` в тесте `fakeAsync()`, вам нужно использовать `tick(100)` для запуска обратного вызова fn.

Необязательный параметр `tickOptions` имеет свойство `processNewMacroTasksSynchronously`. Свойство `processNewMacroTasksSynchronously` указывает, следует ли вызывать новые сгенерированные макрозадачи при тике, и по умолчанию имеет значение `true`.

<code-example path="testing/src/app/demo/async-helper.spec.ts" region="fake-async-test-tick"></code-example>.

Функция [tick()](api/core/testing/tick) является одной из утилит тестирования Angular, которую вы импортируете с помощью `TestBed`. Она является компаньоном `fakeAsync()` и вы можете вызывать ее только в теле `fakeAsync()`.

#### tickOptions

В этом примере появилась новая макрозадача - вложенная функция `setTimeout`. По умолчанию, когда `tick` имеет значение setTimeout, срабатывают и `outside`, и `nested`.

<code-example path="testing/src/app/demo/async-helper.spec.ts" region="fake-async-test-tick-new-macro-task-sync"></code-example>.

В некоторых случаях вы не хотите запускать новую макрозадачу при тике. Вы можете использовать `tick(millis, {processNewMacroTasksSynchronously: false})`, чтобы не вызывать новую макрозадачу.

<code-example path="testing/src/app/demo/async-helper.spec.ts" region="fake-async-test-tick-new-macro-task-async"></code-example>.

#### Сравнение дат внутри fakeAsync()

`fakeAsync()` имитирует течение времени, что позволяет вам вычислить разницу между датами внутри `fakeAsync()`.

<code-example path="testing/src/app/demo/async-helper.spec.ts" region="fake-async-test-date"></code-example>.

#### jasmine.clock с fakeAsync()

Jasmine также предоставляет функцию `clock` для имитации дат. Angular автоматически запускает тесты, которые выполняются после вызова `jasmine.clock().install()` внутри метода `fakeAsync()` до вызова `jasmine.clock().uninstall()`.

Метод `fakeAsync()` не нужен и при вложении выдает ошибку.

По умолчанию эта функция отключена. Чтобы включить ее, установите глобальный флаг перед импортом `zone-testing`.

Если вы используете Angular CLI, настройте этот флаг в `src/test.ts`.

<code-example format="typescript" language="typescript">

(window as any)['&lowbar;&lowbar;zone&lowbar;symbol__fakeAsyncPatchLock'] = true; import 'zone.js/testing';

</code-example>

<code-example path="testing/src/app/demo/async-helper.spec.ts" region="fake-async-test-clock"></code-example>.

#### Использование планировщика RxJS внутри fakeAsync()

Вы также можете использовать планировщик RxJS в `fakeAsync()` точно так же, как и `setTimeout()` или `setInterval()`, но вам нужно импортировать `zone.js/plugins/zone-patch-rxjs-fake-async` для патча планировщика RxJS.

<code-example path="testing/src/app/demo/async-helper.spec.ts" region="fake-async-test-rxjs"></code-example>.

#### Поддержка большего количества макрозадач

По умолчанию `fakeAsync()` поддерживает следующие макрозадачи.

-   `setTimeout`

-   `setInterval`

-   `requestAnimationFrame`

-   `webkitRequestAnimationFrame`

-   `mozRequestAnimationFrame`.

Если вы запускаете другие макрозадачи, такие как `HTMLCanvasElement.toBlob()`, возникает ошибка _"Unknown macroTask scheduled in fake async test"_.

<code-tabs> <code-pane header="src/app/shared/canvas.component.spec.ts (failing)" path="testing/src/app/shared/canvas.component.spec.ts" region="without-toBlob-macrotask"></code-pane>
<code-pane header="src/app/shared/canvas.component.ts" path="testing/src/app/shared/canvas.component.ts" region="main"></code-pane>
</code-tabs>

Если вы хотите поддерживать такой случай, вам необходимо определить макрозадачу, которую вы хотите поддерживать, в `beforeEach()`. Например:

<code-example header="src/app/shared/canvas.component.spec.ts (excerpt)" path="testing/src/app/shared/canvas.component.spec.ts" region="enable-toBlob-macrotask"></code-example>

<div class="alert is-helpful">

**NOTE**: <br /> In order to make the `<canvas>` element Zone.js-aware in your app, you need to import the `zone-patch-canvas` patch \(either in `polyfills.ts` or in the specific file that uses `<canvas>`\):

</div>

<code-example header="src/polyfills.ts или src/app/shared/canvas.component.ts" path="testing/src/app/shared/canvas.component.ts" region="import-canvas-patch"></code-example>

#### Асинхронные наблюдаемые

Вы можете быть довольны покрытием этих тестов.

Однако вас может беспокоить тот факт, что реальный сервис ведет себя не совсем так. Реальный сервис посылает запросы на удаленный сервер.

Серверу требуется время для ответа, и ответ, конечно, не будет доступен сразу, как в предыдущих двух тестах.

Ваши тесты будут более точно отражать реальный мир, если вы вернете _асинхронную_ наблюдаемую из шпиона `getQuote()` следующим образом.

<code-example path="testing/src/app/twain/twain.component.spec.ts" region="async-setup"></code-example>.

#### Помощники асинхронных наблюдаемых

Асинхронная наблюдаемая была создана с помощью помощника `asyncData`. Помощник `asyncData` - это служебная функция, которую вам придется написать самостоятельно, или скопировать эту функцию из кода примера.

<code-example header="testing/async-observable-helpers.ts" path="testing/src/testing/async-observable-helpers.ts" region="async-data"></code-example>.

Эта вспомогательная наблюдаемая испускает значение `data` при следующем повороте движка JavaScript.

Оператор [RxJS `defer()`](http://reactivex.io/documentation/operators/defer.html) возвращает наблюдаемую. Он принимает фабричную функцию, которая возвращает либо обещание, либо наблюдаемую.

Когда что-то подписывается на наблюдаемую _defer_, оно добавляет подписчика в новую наблюдаемую, созданную с помощью этой фабрики.

Оператор `defer()` преобразует `Promise.resolve()` в новую наблюдаемую, которая, как и `HttpClient`, испускается один раз и завершается. Подписчики отписываются после получения значения данных.

Существует аналогичный помощник для создания асинхронной ошибки.

<code-example path="testing/src/testing/async-observable-helpers.ts" region="async-error"></code-example>

#### Больше асинхронных тестов

Теперь, когда шпион `getQuote()` возвращает асинхронные наблюдаемые, большинство ваших тестов также должны быть асинхронными.

Вот тест `fakeAsync()`, который демонстрирует поток данных, ожидаемый в реальном мире.

<code-example path="testing/src/app/twain/twain.component.spec.ts" region="fake-async-test"></code-example>.

Заметьте, что элемент quote отображает значение заполнителя \(``...`\) после `ngOnInit()`. Первая цитата еще не пришла.

Чтобы удалить первую котировку из наблюдаемой, вы вызываете [tick()](api/core/testing/tick). Затем вызовите `detectChanges()`, чтобы сообщить Angular об обновлении экрана.

После этого можно утверждать, что элемент цитаты отображает ожидаемый текст.

<a id="waitForAsync"></a>

#### Асинхронный тест с `waitForAsync()`.

Чтобы использовать функциональность `waitForAsync()`, вы должны импортировать `zone.js/testing` в файл настройки тестов. Если вы создали свой проект с помощью Angular CLI, `zone-testing` уже импортирован в `src/test.ts`.

Вот предыдущий тест `fakeAsync()`, переписанный с помощью утилиты `waitForAsync()`.

<code-example path="testing/src/app/twain/twain.component.spec.ts" region="waitForAsync-test"></code-example>.

Утилита `waitForAsync()` скрывает некоторые асинхронные шаблоны, организуя выполнение кода тестировщика в специальной _async test zone_. Вам не нужно передавать `done()` из Jasmine в тест и вызывать `done()`, потому что он `неопределен` в обещаниях или наблюдаемых обратных вызовах.

Но асинхронная природа теста проявляется в вызове `fixture.whenStable()`, который нарушает линейный поток управления.

При использовании `intervalTimer()`, например, `setInterval()` в `waitForAsync()`, не забудьте отменить таймер с помощью `clearInterval()` после выполнения теста, иначе `waitForAsync()` никогда не завершится.

<a id="when-stable"></a>

#### `whenStable`.

Тест должен ждать, пока наблюдаемая `getQuote()` выпустит следующую цитату. Вместо вызова [tick()](api/core/testing/tick), он вызывает `fixture.whenStable()`.

Функция `fixture.whenStable()` возвращает обещание, которое разрешается, когда очередь задач движка JavaScript становится пустой. В этом примере очередь задач становится пустой, когда наблюдаемая испускает первую цитату.

Тест возобновляется в обратном вызове обещания, которое вызывает `detectChanges()` для обновления элемента цитаты ожидаемым текстом.

<a id="jasmine-done"></a>

#### Jasmine `done()`.

Хотя функции `waitForAsync()` и `fakeAsync()` значительно упрощают асинхронное тестирование Angular, вы все еще можете вернуться к традиционной технике и передать `it` функцию, которая принимает [`done` callback](https://jasmine.github.io/2.0/introduction.html#section-Asynchronous_Support).

Вы не можете вызвать `done()` в функциях `waitForAsync()` или `fakeAsync()`, потому что параметр `done` является `неопределенным`.

Теперь вы отвечаете за цепочку обещаний, обработку ошибок и вызов `done()` в нужные моменты.

Написание тестовых функций с `done()` более громоздко, чем `waitForAsync()` и `fakeAsync()`, но иногда это необходимо, когда код включает `intervalTimer()` типа `setInterval`.

Вот еще две версии предыдущего теста, написанные с помощью `done()`. Первая подписывается на `Observable`, выставляемый шаблону свойством `quote` компонента.

<code-example path="testing/src/app/twain/twain.component.spec.ts" region="quote-done-test"></code-example>.

Оператор RxJS `last()` выдает последнее значение наблюдаемой перед завершением, которое будет тестовой цитатой. Обратный вызов `subscribe` вызывает `detectChanges()` для обновления элемента quote тестовой цитатой, аналогично предыдущим тестам.

В некоторых тестах вас больше интересует, как был вызван метод инжектированного сервиса и какие значения он вернул, чем то, что отображается на экране.

Сервисный шпион, такой как `qetQuote()` шпион поддельного `TwainService`, может дать вам эту информацию и сделать утверждения о состоянии представления.

<code-example path="testing/src/app/twain/twain.component.spec.ts" region="spy-done-test"></code-example>.

<a id="marble-testing"></a>

## Компонентные мраморные тесты

Предыдущие тесты `TwainComponent` имитировали асинхронный наблюдаемый ответ от `TwainService` с помощью утилит `asyncData` и `asyncError`.

Это короткие, простые функции, которые вы можете написать самостоятельно. К сожалению, они слишком просты для многих распространенных сценариев.

Наблюдаемая часто испускается несколько раз, возможно, со значительной задержкой.

Компонент может координировать несколько наблюдаемых с перекрывающимися последовательностями значений и ошибок.

**RxJS marble testing** - это отличный способ тестирования сценариев наблюдаемых, как простых, так и сложных. Вы, вероятно, видели [мраморные диаграммы] (https://rxmarbles.com), которые иллюстрируют работу наблюдаемых.

Мраморное тестирование использует аналогичный мраморный язык для определения наблюдаемых потоков и ожиданий в ваших тестах.

Следующие примеры рассматривают два теста `TwainComponent` с помощью мраморного тестирования.

Начните с установки npm-пакета `jasmine-marbles`. Затем импортируйте необходимые вам символы.

<code-example header="app/twain/twain.component.marbles.spec.ts (import marbles)" path="testing/src/app/twain/twain.component.marbles.spec.ts" region="import-marbles"></code-example>.

Вот полный тест для получения цитаты:

<code-example path="testing/src/app/twain/twain.component.marbles.spec.ts" region="get-quote-test"></code-example>.

Обратите внимание, что тест Jasmine является синхронным. Здесь нет `fakeAsync()`.

Мраморное тестирование использует планировщик тестов для имитации течения времени в синхронном тесте.

Красота мраморного тестирования заключается в визуальном определении наблюдаемых потоков. Этот тест определяет [_холодную_ наблюдаемую](#cold-observable), которая ждет три [кадра](#marble-frame) \(`---`\), выдает значение \(`x`\) и завершается \(`|`\).

Во втором аргументе вы сопоставляете маркер значения \(`x`\) с испускаемым значением \(`testQuote`\).

<code-example path="testing/src/app/twain/twain.component.marbles.spec.ts" region="test-quote-marbles"></code-example>.

Библиотека marble создает соответствующую наблюдаемую, которую тест устанавливает в качестве возвращаемого значения шпиона `getQuote`.

Когда вы будете готовы активировать мраморные наблюдаемые, вы скажете `TestScheduler` _промыть_ свою очередь подготовленных задач следующим образом.

<code-example path="testing/src/app/twain/twain.component.marbles.spec.ts" region="test-scheduler-flush"></code-example>.

Этот шаг служит цели, аналогичной [tick()](api/core/testing/tick) и `whenStable()` в предыдущих примерах `fakeAsync()` и `waitForAsync()`. Остальная часть теста такая же, как и в этих примерах.

#### Тестирование ошибок в мраморе

Перед вами мраморная версия теста на ошибку `getQuote()`.

<code-example path="testing/src/app/twain/twain.component.marbles.spec.ts" region="error-test"></code-example>.

Это все еще асинхронный тест, вызывающий `fakeAsync()` и [tick()](api/core/testing/tick), потому что сам компонент вызывает `setTimeout()` при обработке ошибок.

Посмотрите на определение мраморной наблюдаемой.

<code-example path="testing/src/app/twain/twain.component.marbles.spec.ts" region="error-marbles"></code-example>.

Это _холодная_ наблюдаемая, которая ждет три кадра и затем выдает ошибку, хэш \(`#`\) символ указывает на время ошибки, которое указано в третьем аргументе. Второй аргумент равен null, потому что наблюдаемая никогда не выдает значения.

#### Узнайте о тестировании на мраморе

<a id="marble-frame"></a>

Мраморный кадр - это виртуальная единица времени тестирования. Каждый символ \(`-`, `x`, `|`, `#`\) отмечает прохождение одного фрейма.

<a id="cold-observable"></a>

Холодная\_ наблюдаемая не производит значений, пока вы не подпишетесь на нее. Большинство наблюдаемых вашего приложения являются холодными.

Все методы [_HttpClient_](guide/http) возвращают холодные наблюдаемые.

Горячая* наблюдаемая уже производит значения *до* того, как вы на нее подписались. Наблюдаемая [`Router.events`](api/router/Router#events), которая сообщает об активности маршрутизатора, является *горячей\_ наблюдаемой.

Тестирование мрамора RxJS - это обширная тема, выходящая за рамки данного руководства. Узнайте об этом в Интернете, начиная с [официальной документации](https://rxjs.dev/guide/testing/marble-testing).

<a id="component-with-input-output"></a>

## Компонент с входами и выходами

Компонент с входами и выходами обычно появляется внутри шаблона представления главного компонента. Хост использует привязку свойств для установки входного свойства и привязку событий для прослушивания событий, вызванных выходным свойством.

Цель тестирования - проверить, что такие привязки работают так, как ожидается. Тесты должны устанавливать входные значения и прослушивать выходные события.

Компонент `DashboardHeroComponent` - это маленький пример компонента в этой роли. Он отображает отдельного героя, предоставленного `DashboardComponent`.

Щелчок на этом герое сообщает `DashboardComponent`, что пользователь выбрал героя.

Компонент `DashboardHeroComponent` встраивается в шаблон `DashboardComponent` следующим образом:

<code-example header="app/dashboard/dashboard.component.html (excerpt)" path="testing/src/app/dashboard/dashboard.component.html" region="dashboard-hero"></code-example>.

Компонент `DashboardHeroComponent` появляется в повторителе `*ngFor`, который устанавливает входное свойство `hero` каждого компонента в значение цикла и слушает событие `selected` компонента.

Вот полное определение компонента:

<a id="dashboard-hero-component"></a>

<code-example header="app/dashboard/dashboard-hero.component.ts (component)" path="testing/src/app/dashboard/dashboard-hero.component.ts" region="component"></code-example>

Хотя тестирование такого простого компонента имеет небольшую внутреннюю ценность, стоит знать, как это сделать. Используйте один из этих подходов:

-   Протестируйте его как используемый `DashboardComponent`.

-   Тестируйте его как отдельный компонент

-   Протестируйте его в качестве замены `DashboardComponent`.

Беглый взгляд на конструктор `DashboardComponent` отталкивает от первого подхода:

<code-example header="app/dashboard/dashboard.component.ts (constructor)" path="testing/src/app/dashboard/dashboard.component.ts" region="ctor"></code-example>.

Компонент `DashboardComponent` зависит от Angular router и `HeroService`. Скорее всего, вам придется заменить их оба тестовыми дублями, а это большая работа.

Маршрутизатор кажется особенно сложным.

<div class="alert is-helpful">

В [следующем обсуждении](#routing-component) рассматривается тестирование компонентов, для которых требуется маршрутизатор.

</div>

Ближайшей целью является тестирование `DashboardHeroComponent`, а не `DashboardComponent`, поэтому попробуйте второй и третий варианты.

<a id="dashboard-standalone"></a>

#### Тест `DashboardHeroComponent` stand-alone

Вот основная часть настройки файла спецификации.

<code-example header="app/dashboard/dashboard-hero.component.spec.ts (setup)" path="testing/src/app/dashboard/dashboard-hero.component.spec.ts" region="setup"></code-example>.

Обратите внимание, как код установки назначает тестового героя \(`expectedHero`\) свойству компонента `hero`, эмулируя способ, которым `DashboardComponent` установит его с помощью привязки свойства в своем ретрансляторе.

Следующий тест проверяет, что имя героя передается в шаблон с помощью привязки.

<code-example path="testing/src/app/dashboard/dashboard-hero.component.spec.ts" region="name-test"></code-example>.

Поскольку [template](#dashboard-hero-component) передает имя героя через Angular `UpperCasePipe`, тест должен сопоставить значение элемента с именем в верхнем регистре.

<div class="alert is-helpful">

Этот небольшой тест демонстрирует, как тесты Angular могут проверить визуальное представление компонента &mdash; то, что невозможно с помощью [тестов классов компонентов] (guide/testing-components-basics#component-class-testing)&mdash; с небольшими затратами и без использования гораздо более медленных и сложных сквозных тестов.

</div>

#### Щелчок

Нажатие на героя должно вызвать событие `selected`, которое может услышать главный компонент \(`DashboardComponent` предположительно\):

<code-example path="testing/src/app/dashboard/dashboard-hero.component.spec.ts" region="click-test"></code-example>.

Свойство компонента `selected` возвращает `EventEmitter`, который для потребителей выглядит как RxJS синхронный `Observable`. Тест подписывается на него _явно_, так же как и компонент-хозяин _неявно_.

Если компонент ведет себя так, как ожидается, щелчок по элементу героя должен заставить свойство `selected` компонента выдать объект `hero`.

Тест обнаруживает это событие через свою подписку на `selected`.

<a id="trigger-event-handler"></a>

#### `triggerEventHandler`

The `heroDe` in the previous test is a `DebugElement` that represents the hero `<div>`.

It has Angular properties and methods that abstract interaction with the native element. This test calls the `DebugElement.triggerEventHandler` with the "click" event name.

The "click" event binding responds by calling `DashboardHeroComponent.click()`.

The Angular `DebugElement.triggerEventHandler` can raise _any data-bound event_ by its _event name_. The second parameter is the event object passed to the handler.

The test triggered a "click" event.

<code-example path="testing/src/app/dashboard/dashboard-hero.component.spec.ts" region="trigger-event-handler"></code-example>.

В этом случае тест правильно предполагает, что обработчик события во время выполнения, метод `click()` компонента, не заботится об объекте события.

<div class="alert is-helpful">

Другие обработчики менее снисходительны. Например, директива `RouterLink` ожидает объект со свойством `button`, которое определяет, какая кнопка мыши, если таковая имеется, была нажата во время щелчка.
Директива `RouterLink` выбрасывает ошибку, если объект события отсутствует.

</div>

#### Нажмите на элемент

Следующая тестовая альтернатива вызывает собственный метод `click()` родного элемента, что вполне подходит для _этого компонента_.

<code-example path="testing/src/app/dashboard/dashboard-hero.component.spec.ts" region="click-test-2"></code-example>.

<a id="click-helper"></a>

#### `click()` helper

Нажатие на кнопку, якорь или произвольный элемент HTML является распространенной задачей тестирования.

Чтобы сделать ее последовательной и простой, инкапсулируйте процесс _нажатия_ в помощнике, таком как следующая функция `click()`:

<code-example header="testing/index.ts (помощник клика)" path="testing/src/testing/index.ts" region="click-event"></code-example>.

Первый параметр - это _элемент для клика_. Если хотите, передайте пользовательский объект события в качестве второго параметра.

По умолчанию используется частичный [объект события левой кнопки мыши](https://developer.mozilla.org/docs/Web/API/MouseEvent/button), принимаемый многими обработчиками, включая директиву `RouterLink`.

<div class="alert is-important">

Вспомогательная функция `click()` **не** является одной из утилит тестирования Angular. Это функция, определенная в _коде примера этого руководства_.
Все примеры тестов используют ее.

Если она вам нравится, добавьте ее в свою собственную коллекцию помощников.

</div>

Вот предыдущий тест, переписанный с использованием помощника click.

<code-example header="app/dashboard/dashboard-hero.component.spec.ts (тест с помощником click)" path="testing/src/app/dashboard/dashboard-hero.component.spec.ts" region="click-test-3"></code-example>

<a id="component-inside-test-host"></a>

## Компонент внутри тестового хоста

В предыдущих тестах роль хоста `DashboardComponent` выполняли сами компоненты. Но правильно ли работает `DashboardHeroComponent` при правильной привязке данных к компоненту хоста?

Вы могли бы тестировать с помощью фактического `DashboardComponent`. Но это может потребовать много настроек, особенно если в его шаблоне есть повторитель `*ngFor`, другие компоненты, HTML макета, дополнительные привязки, конструктор, который внедряет множество сервисов, и он сразу же начинает взаимодействовать с этими сервисами.

Представьте себе, сколько усилий нужно приложить, чтобы отключить все эти отвлекающие факторы, только чтобы доказать, что можно удовлетворительно доказать с помощью _тестового хоста_, подобного этому:

<code-example header="app/dashboard/dashboard-hero.component.spec.ts (test host)" path="testing/src/app/dashboard/dashboard-hero.component.spec.ts" region="test-host"></code-example>

Этот тестовый хост привязывается к `DashboardHeroComponent`, как и `DashboardComponent`, но без шума `Router`, `HeroService` или повторителя `*ngFor`.

Тестовый хост устанавливает свойство ввода компонента `hero` со своим тестовым героем. Он связывает событие `selected` компонента с его обработчиком `onSelected`, который записывает выданного героя в свойство `selectedHero`.

Позже тесты смогут проверить `selectedHero`, чтобы убедиться, что событие `DashboardHeroComponent.selected` вызвало ожидаемого героя.

Настройка для тестов `test-host` аналогична настройке для автономных тестов:

<code-example header="app/dashboard/dashboard-hero.component.spec.ts (настройка тестового хоста)" path="testing/src/app/dashboard/dashboard-hero.component.spec.ts" region="test-host-setup"></code-example>.

Эта конфигурация модуля тестирования показывает три важных отличия:

-   Он _объявляет_ и `DashboardHeroComponent`, и `TestHostComponent`.

-   Он _создает_ `TestHostComponent` вместо `DashboardHeroComponent`.

-   Компонент `TestHostComponent` устанавливает `DashboardHeroComponent.hero` с привязкой

Функция `createComponent` возвращает `fixture`, содержащий экземпляр `TestHostComponent` вместо экземпляра `DashboardHeroComponent`.

Создание `TestHostComponent` имеет побочный эффект создания `DashboardHeroComponent`, потому что последний появляется в шаблоне первого. Запрос на элемент героя \(`heroEl`\) по-прежнему находит его в тестовом DOM, хотя и на большей глубине дерева элементов, чем раньше.

Сами тесты практически идентичны автономной версии:

<code-example header="app/dashboard/dashboard-hero.component.spec.ts (test-host)" path="testing/src/app/dashboard/dashboard-hero.component.spec.ts" region="test-host-tests"></code-example>.

Отличается только тест выбранного события. Он подтверждает, что выбранный герой `DashboardHeroComponent` действительно находит путь наверх через привязку событий к главному компоненту.

<a id="routing-component"></a>

## Компонент маршрутизации

Компонент _маршрутизации_ - это компонент, который указывает `Router` на переход к другому компоненту. Компонент `DashboardComponent` является компонентом маршрутизации, потому что пользователь может перейти к компоненту `HeroDetailComponent`, нажав на одну из _геройских кнопок_ на приборной панели.

Маршрутизация довольно сложна. Тестирование `DashboardComponent` казалось сложным отчасти потому, что в нем задействован `Router`, который он внедряет вместе с `HeroService`.

<code-example header="app/dashboard/dashboard.component.ts (constructor)" path="testing/src/app/dashboard/dashboard.component.ts" region="ctor"></code-example>

<code-example header="app/dashboard/dashboard.component.ts (goToDetail)" path="testing/src/app/dashboard/dashboard.component.ts" region="goto-detail"></code-example>.

Angular предоставляет вспомогательные средства тестирования для уменьшения количества шаблонов и более эффективного тестирования кода, который зависит от Router и HttpClient.

<code-example header="app/dashboard/dashboard.component.spec.ts" path="testing/src/app/dashboard/dashboard.component.spec.ts" region="router-harness"></code-example>

The following test clicks the displayed hero and confirms that we navigate to the expected URL.

<code-example header="app/dashboard/dashboard.component.spec.ts (navigate test)" path="testing/src/app/dashboard/dashboard.component.spec.ts" region="navigate-test"></code-example>

<a id="routed-component-w-param"></a>

## Маршрутизируемые компоненты

Маршрутизируемый компонент* является конечным пунктом навигации `Router`. Его тестирование может быть более сложным, особенно если маршрут к компоненту *включает параметры\_.

Компонент `HeroDetailComponent` - это _маршрутизируемый компонент_, который является конечным пунктом такого маршрута.

Когда пользователь нажимает на героя _Dashboard_, `DashboardComponent` говорит `Router` перейти к `heroes/:id`. `:id` - это параметр маршрута, значением которого является `id` героя для редактирования.

Маршрутизатор `Router` сопоставляет этот URL с маршрутом к компоненту `HeroDetailComponent`. Он создает объект `ActivatedRoute` с информацией о маршрутизации и вставляет его в новый экземпляр `HeroDetailComponent`.

Вот конструктор `HeroDetailComponent`:

<code-example header="app/hero/hero-detail.component.ts (constructor)" path="testing/src/app/hero/hero-detail.component.ts" region="ctor"></code-example>.

Компоненту `HeroDetail` необходим параметр `id`, чтобы он мог получить соответствующего героя с помощью `HeroDetailService`. Компонент должен получить `id` из свойства `ActivatedRoute.paramMap`, которое является `Observable`.

Он не может просто ссылаться на свойство `id` из `ActivatedRoute.paramMap`. Компонент должен _подписаться_ на наблюдаемую `ActivatedRoute.paramMap` и быть готовым к тому, что `id` может измениться в течение его жизни.

<code-example header="app/hero/hero-detail.component.ts (ngOnInit)" path="testing/src/app/hero/hero-detail.component.ts" region="ng-on-init"></code-example>

<div class="alert is-helpful">

В разделе [ActivatedRoute в действии](guide/router-tutorial-toh#activated-route-in-action) руководства [Router tutorial: tour of heroes](guide/router-tutorial-toh) более подробно рассматривается `ActivatedRoute.paramMap`.

</div>

Тесты могут исследовать, как `HeroDetailComponent` реагирует на различные значения параметра `id`, переходя к различным маршрутам.

#### Тестирование с помощью `RouterTestingHarness`.

Вот тест, демонстрирующий поведение компонента, когда наблюдаемый `id` относится к существующему герою:

<code-example header="app/hero/hero-detail.component.spec.ts (существующий id)" path="testing/src/app/hero/hero-detail.component.spec.ts" region="route-good-id"></code-example>.

<div class="alert is-helpful">

В следующем разделе рассматриваются метод `createComponent()` и объект `page`. Пока полагайтесь на свою интуицию.

</div>

Когда `id` не может быть найден, компонент должен перенаправить на `HeroListComponent`.

При настройке тестового набора был использован тот же жгут маршрутизаторов [описанный выше](#routing-component).

Этот тест ожидает, что компонент попытается перейти к `HeroListComponent`.

<code-example header="app/hero/hero-detail.component.spec.ts (bad id)" path="testing/src/app/hero/hero-detail.component.spec.ts" region="route-bad-id"></code-example>.

## Тесты вложенных компонентов

Шаблоны компонентов часто имеют вложенные компоненты, шаблоны которых могут содержать еще больше компонентов.

Дерево компонентов может быть очень глубоким, и в большинстве случаев вложенные компоненты не играют никакой роли в тестировании компонента, находящегося в верхней части дерева.

Например, `AppComponent` отображает навигационную панель с якорями и их директивами `RouterLink`.

<code-example header="app/app.component.html" path="testing/src/app/app.component.html"></code-example>.

Чтобы проверить ссылки, вам не нужен `Router` для навигации и не нужен `<router-outlet>`, чтобы отметить, куда `Router` вставляет _маршрутизируемые компоненты_.

Компоненты `BannerComponent` и `WelcomeComponent`\ (обозначаемые `<app-banner>` и `<app-welcome>`\) также не имеют значения.

Тем не менее, любой тест, создающий `AppComponent` в DOM, также создает экземпляры этих трех компонентов, и, если вы позволите этому случиться, вам придется настроить `TestBed` на их создание.

Если вы не объявите их, компилятор Angular не распознает теги `<app-banner>`, `<app-welcome>` и `<router-outlet>` в шаблоне `AppComponent` и выдаст ошибку.

Если вы объявите реальные компоненты, вам также придется объявить _их_ вложенные компоненты и обеспечить _все_ сервисы, внедряемые в _любой_ компонент в дереве.

Это слишком много усилий только для того, чтобы ответить на несколько простых вопросов о связях.

В этом разделе описаны две техники для минимизации настройки. Используйте их по отдельности или в комбинации, чтобы сосредоточиться на тестировании основного компонента.

<a id="stub-component"></a>.

##### Создание заглушек ненужных компонентов

В первой технике вы создаете и объявляете заглушки компонентов и директив, которые играют незначительную роль или не играют никакой роли в тестах.

<code-example header="app/app.component.spec.ts (объявление заглушки)" path="testing/src/app/app.component.spec.ts" region="component-stubs"></code-example>.

Селекторы заглушек совпадают с селекторами соответствующих реальных компонентов. Но их шаблоны и классы пусты.

Тогда объявите их в конфигурации `TestBed` рядом с компонентами, директивами и трубами, которые должны быть реальными.

<code-example header="app/app.component.spec.ts (TestBed stubs)" path="testing/src/app/app.component.spec.ts" region="testbed-stubs"></code-example>.

Компонент `AppComponent` является объектом тестирования, поэтому, конечно, вы объявляете реальную версию.

Все остальное - это заглушки.

<a id="no-errors-schema"></a>

#### `NO_ERRORS_SCHEMA`.

При втором подходе добавьте `NO_ERRORS_SCHEMA` в метаданные `TestBed.schemas`.

<code-example header="app/app.component.spec.ts (NO_ERRORS_SCHEMA)" path="testing/src/app/app.component.spec.ts" region="no-errors-schema"></code-example>.

Схема `NO_ERRORS_SCHEMA` указывает компилятору Angular игнорировать нераспознанные элементы и атрибуты.

Компилятор распознает элемент `<app-root>` и атрибут `routerLink`, потому что вы объявили соответствующие `AppComponent` и `RouterLink` в конфигурации `TestBed`.

Но компилятор не выдаст ошибку, когда встретит `<app-banner>`, `<app-welcome>` или `<router-outlet>`. Он просто отображает их как пустые теги, и браузер их игнорирует.

Вам больше не нужны компоненты-заглушки.

#### Используйте обе техники вместе.

Это техники для _Shallow Component Testing_, названные так потому, что они уменьшают визуальную поверхность компонента только до тех элементов в шаблоне компонента, которые важны для тестов.

Подход `NO_ERRORS_SCHEMA` является более простым из двух, но не злоупотребляйте им.

Использование `NO_ERRORS_SCHEMA` также не позволит компилятору сообщить вам о недостающих компонентах и атрибутах, которые вы случайно пропустили или неправильно написали. Вы можете потратить часы в погоне за фантомными ошибками, которые компилятор обнаружил бы мгновенно.

У подхода _компонента-заглушки_ есть еще одно преимущество. Хотя заглушки в _этом_ примере были пустыми, вы можете дать им урезанные шаблоны и классы, если ваши тесты должны каким-то образом взаимодействовать с ними.

На практике вы будете сочетать эти два метода в одной установке, как показано в этом примере.

<code-example header="app/app.component.spec.ts (mixed setup)" path="testing/src/app/app.component.spec.ts" region="mixed-setup"></code-example>.

Компилятор Angular создает `BannerStubComponent` для элемента `<app-banner>` и применяет `RouterLink` к якорям с атрибутом `routerLink`, но игнорирует теги `<app-welcome>` и `<router-outlet>`.

<a id="by-directive"></a> <a id="inject-directive"></a>

#### `By.directive` и инжектируемые директивы

Еще немного настроек запускают начальное связывание данных и получают ссылки на навигационные ссылки:

<code-example header="app/app.component.spec.ts (test setup)" path="testing/src/app/app.component.spec.ts" region="test-setup"></code-example>.

Три точки, представляющие особый интерес:

-   Найдите элементы якоря с вложенной директивой с помощью `By.directive`.

-   Запрос возвращает обертки `DebugElement` вокруг соответствующих элементов.

-   Каждый `DebugElement` раскрывает инжектор зависимости с конкретным экземпляром директивы, прикрепленной к этому элементу.

Ссылки `AppComponent` для проверки следующие:

<code-example header="app/app.component.html (навигационные ссылки)" path="testing/src/app/app.component.html" region="links"></code-example>

<a id="app-component-tests"></a>

Вот несколько тестов, которые подтверждают, что эти ссылки подключены к директивам `routerLink`, как и ожидалось:

<code-example header="app/app.component.spec.ts (выбранные тесты)" path="testing/src/app/app.component.spec.ts" region="tests"></code-example>

<a id="page-object"></a>

## Использование объекта `page`

Компонент `HeroDetailComponent` - это простое представление с заголовком, двумя полями героя и двумя кнопками.

<div class="lightbox">

<img alt="HeroDetailComponent in action" src="generated/images/guide/testing/hero-detail.component.png">

</div>

Но даже в этой простой форме есть много сложностей с шаблонами.

<code-example path="testing/src/app/hero/hero-detail.component.html" header="app/hero/hero-detail.component.html"></code-example>.

Тесты, проверяющие работу компонента, должны &hellip;

-   Дождаться появления героя, прежде чем элементы появятся в DOM

-   Ссылка на текст заголовка

-   Ссылка на поле ввода имени, чтобы проверить и установить его

-   Ссылки на две кнопки, чтобы их можно было нажать

-   Ссылки на некоторые методы компонентов и маршрутизаторов

Даже такая маленькая форма, как эта, может создать беспорядок из мучительных условных настроек и выбора элементов CSS.

Справиться со сложностью можно с помощью класса `Page`, который обрабатывает доступ к свойствам компонента и инкапсулирует логику, которая их устанавливает.

Вот такой класс `Page` для `hero-detail.component.spec.ts`

<code-example header="app/hero/hero-detail.component.spec.ts (Page)" path="testing/src/app/hero/hero-detail.component.spec.ts" region="page"></code-example>.

Теперь важные крючки для манипулирования компонентом и его проверки аккуратно организованы и доступны из экземпляра `Page`.

Метод `createComponent` создает объект `page` и заполняет пустые места, когда появляется `герой`.

<code-example header="app/hero/hero-detail.component.spec.ts (createComponent)" path="testing/src/app/hero/hero-detail.component.spec.ts" region="create-component"></code-example>.

Вот еще несколько тестов `HeroDetailComponent`, чтобы усилить суть.

<code-example header="app/hero/hero-detail.component.spec.ts (selected tests)" path="testing/src/app/hero/hero-detail.component.spec.ts" region="selected-tests"></code-example>

<a id="compile-components"></a>

## Вызов `compileComponents()`

<div class="alert is-helpful">

Игнорируйте этот раздел, если вы _только_ запускаете тесты с помощью команды CLI `ng test`, поскольку CLI компилирует приложение перед запуском тестов.

</div>

Если вы запускаете тесты в **не-CLI-среде**, тесты могут завершиться неудачей с сообщением, подобным этому:

<code-example format="output" hideCopy language="shell">

Ошибка: Этот тестовый модуль использует компонент BannerComponent, который использует "templateUrl" или "styleUrls", но они никогда не были скомпилированы.
Пожалуйста, вызовите "TestBed.compileComponents" перед началом тестирования.

</code-example>

Корень проблемы в том, что хотя бы один из компонентов, участвующих в тестировании, указывает внешний шаблон или CSS файл, как это делает следующая версия `BannerComponent`.

<code-example header="app/banner/banner-external.component.ts (external template & css)" path="testing/src/app/banner/banner-external.component.ts"></code-example>.

Тест терпит неудачу, когда `TestBed` пытается создать компонент.

<code-example avoid header="app/banner/banner-external.component.spec.ts (setup that fails)" path="testing/src/app/banner/banner-external.component.spec.ts" region="setup-may-fail"></code-example>

Напомним, что приложение не было скомпилировано. Поэтому, когда вы вызываете `createComponent()`, `TestBed` компилируется неявно.

Это не проблема, когда исходный код находится в памяти. Но `BannerComponent` требует внешних файлов, которые компилятор должен читать из файловой системы, что по своей сути является _асинхронной_ операцией.

Если бы `TestBed` было разрешено продолжить работу, тесты запустились бы и загадочно провалились, прежде чем компилятор смог бы закончить работу.

Вытесняющее сообщение об ошибке говорит вам о необходимости явной компиляции с помощью `compileComponents()`.

#### `compileComponents()` является асинхронным.

Вы должны вызывать `compileComponents()` внутри асинхронной тестовой функции.

<div class="alert is-critical">

Если вы пренебрежете тем, чтобы сделать тестовую функцию асинхронной (например, забудете использовать `waitForAsync()`, как описано), вы увидите следующее сообщение об ошибке

<code-example format="output" hideCopy language="shell">

Ошибка: ViewDestroyedError: Попытка использования уничтоженного представления

</code-example>

</div>

Типичным подходом является разделение логики настройки на две отдельные функции `beforeEach()`:

| Функции | Подробности | | :-------------------------- | :--------------------------- | .

| Асинхронная `beforeEach()` | Компиляция компонентов | Асинхронная `beforeEach()` | Компиляция компонентов.

| Синхронная `beforeEach()` | Выполняет оставшуюся настройку |

#### Асинхронный `beforeEach`.

Напишите первый асинхронный `beforeEach` следующим образом.

<code-example header="app/banner/banner-external.component.spec.ts (async beforeEach)" path="testing/src/app/banner/banner-external.component.spec.ts" region="async-before-each"></code-example>.

Метод `TestBed.configureTestingModule()` возвращает класс `TestBed`, чтобы вы могли цепочкой вызывать другие статические методы `TestBed`, такие как `compileComponents()`.

В этом примере `BannerComponent` является единственным компонентом, который будет скомпилирован. В других примерах модуль тестирования конфигурируется с несколькими компонентами и может импортировать прикладные модули, содержащие еще больше компонентов.

Для любого из них могут потребоваться внешние файлы.

Метод `TestBed.compileComponents` асинхронно компилирует все компоненты, настроенные в модуле тестирования.

<div class="alert is-important">

Не переконфигурируйте `TestBed` после вызова `compileComponents()`.

</div>

Вызов `compileComponents()` закрывает текущий экземпляр `TestBed` для дальнейшей конфигурации. Вы не можете больше вызывать никаких методов конфигурации `TestBed`, ни `configureTestingModule()`, ни каких-либо методов `override...`.
При попытке вызова `TestBed` выдает ошибку.

Сделайте `compileComponents()` последним шагом перед вызовом `TestBed.createComponent()`.

#### Синхронный `beforeEach`.

Вторая, синхронная `beforeEach()` содержит оставшиеся шаги настройки, которые включают создание компонента и запрос элементов для проверки.

<code-example header="app/banner/banner-external.component.spec.ts (synchronous beforeEach)" path="testing/src/app/banner/banner-external.component.spec.ts" region="sync-before-each"></code-example>.

Рассчитывает на то, что бегунок теста будет ждать завершения первого асинхронного `beforeEach` перед вызовом второго.

#### Консолидированная настройка

Вы можете объединить две функции `beforeEach()` в одну асинхронную `beforeEach()`.

Метод `compileComponents()` возвращает обещание, поэтому вы можете выполнять синхронные задачи настройки _после_ компиляции, перемещая синхронный код после ключевого слова `await`, где обещание было разрешено.

<code-example header="app/banner/banner-external.component.spec.ts (one beforeEach)" path="testing/src/app/banner/banner-external.component.spec.ts" region="one-before-each"></code-example>

#### `compileComponents()` безвреден

Нет никакого вреда в вызове `compileComponents()`, когда это не требуется.

Файл теста компонентов, сгенерированный CLI, вызывает `compileComponents()`, хотя он никогда не требуется при запуске `ng test`.

Тесты в этом руководстве вызывают `compileComponents` только тогда, когда это необходимо.

<a id="import-module"></a>

## Настройка с импортом модуля

В предыдущих компонентных тестах модуль тестирования конфигурировался с помощью нескольких `деклараций`, например, так:

<code-example header="app/dashboard/dashboard-hero.component.spec.ts (configure TestBed)" path="testing/src/app/dashboard/dashboard-hero.component.spec.ts" region="config-testbed"></code-example>.

Компонент `DashboardComponent` прост. Он не нуждается в помощи.

Но более сложные компоненты часто зависят от других компонентов, директив, труб и провайдеров, и они тоже должны быть добавлены в модуль тестирования.

К счастью, параметр `TestBed.configureTestingModule` параллелен метаданным, передаваемым декоратору `@NgModule`, что означает, что вы также можете указать `провайдеры` и `импорты`.

Компонент `HeroDetailComponent` требует много помощи, несмотря на свой небольшой размер и простую конструкцию. В дополнение к поддержке, которую он получает от модуля тестирования по умолчанию `CommonModule`, ему необходимы:

-   `NgModel` и друзья в `FormsModule` для обеспечения двустороннего связывания данных

-   `TitleCasePipe` из папки `shared`.

-   Службы маршрутизатора

-   Службы доступа к данным Hero

Один из подходов заключается в настройке модуля тестирования из отдельных частей, как в этом примере:

<code-example header="app/hero/hero-detail.component.spec.ts (FormsModule setup)" path="testing/src/app/hero/hero-detail.component.spec.ts" region="setup-forms-module"></code-example>.

<div class="alert is-helpful">

Обратите внимание, что `beforeEach()` является асинхронным и вызывает `TestBed.compileComponents`, поскольку `HeroDetailComponent` имеет внешний шаблон и css-файл.

Как объясняется в [Вызов `compileComponents()`](#compile-components), эти тесты могут быть запущены в среде без CLI, где Angular придется компилировать их в браузере.

</div>

#### Импорт общего модуля

Поскольку многие компоненты приложения нуждаются в `FormsModule` и `TitleCasePipe`, разработчик создал `SharedModule` для объединения этих и других часто запрашиваемых частей.

Тестовая конфигурация тоже может использовать `SharedModule`, как показано в этой альтернативной установке:

<code-example header="app/hero/hero-detail.component.spec.ts (SharedModule setup)" path="testing/src/app/hero/hero-detail.component.spec.ts" region="setup-shared-module"></code-example>.

Он немного более плотный и компактный, с меньшим количеством операторов импорта, которые не показаны в этом примере.

<a id="feature-module-import"></a>

#### Импорт функционального модуля

Компонент `HeroDetailComponent` является частью `HeroModule` [Feature Module] (guide/feature-modules), который объединяет большее количество взаимозависимых частей, включая `SharedModule`. Попробуйте тестовую конфигурацию, которая импортирует `HeroModule`, как эта:

<code-example header="app/hero/hero-detail.component.spec.ts (HeroModule setup)" path="testing/src/app/hero/hero-detail.component.spec.ts" region="setup-hero-module"></code-example>.

Остаются только _тестовые двойники_ в `providers`. Даже объявление `HeroDetailComponent` исчезло.

На самом деле, если вы попытаетесь объявить его, Angular выдаст ошибку, потому что `HeroDetailComponent` объявлен и в `HeroModule`, и в `DynamicTestModule`, созданном `TestBed`.

<div class="alert is-helpful">

Импорт функционального модуля компонента может быть лучшим способом настройки тестов, если в модуле много взаимных зависимостей, а сам модуль небольшой, как это обычно бывает с функциональными модулями.

</div>

<a id="component-override"></a>

## Переопределение провайдеров компонента

Компонент `HeroDetailComponent` предоставляет свой собственный `HeroDetailService`.

<code-example header="app/hero/hero-detail.component.ts (prototype)" path="testing/src/app/hero/hero-detail.component.ts" region="prototype"></code-example>.

Невозможно заглушить `HeroDetailService` компонента в `providers` модуля `TestBed.configureTestingModule`. Это провайдеры для _модуля тестирования_, а не для компонента.

Они подготавливают инжектор зависимостей на уровне _компонента_.

Angular создает компонент со своим _собственным_ инжектором, который является _дочерним_ инжектором приспособления. Он регистрирует провайдеров компонента\ (в данном случае `HeroDetailService`) с дочерним инжектором.

Тест не может получить доступ к сервисам дочернего инжектора из инжектора приспособления. И `TestBed.configureTestingModule` также не может их сконфигурировать.

Angular все это время создавал новые экземпляры настоящего `HeroDetailService`!

<div class="alert is-helpful">

Эти тесты могут завершиться неудачей или таймаутом, если `HeroDetailService` выполняет собственные XHR-вызовы к удаленному серверу. А удаленного сервера может и не быть.

К счастью, `HeroDetailService` делегирует ответственность за удаленный доступ к данным инжектированному `HeroService`.

<code-example header="app/hero/hero-detail.service.ts (prototype)" path="testing/src/app/hero/hero-detail.service.ts" region="prototype"></code-example>.

В [предыдущей тестовой конфигурации](#feature-module-import) настоящий `HeroService` заменен на `TestHeroService`, который перехватывает запросы сервера и подделывает их ответы.

</div>

Что, если вам не повезло. Что если подделать `HeroService` сложно?
Что если `HeroDetailService` делает собственные запросы к серверу?

Метод `TestBed.overrideComponent` может заменить `провайдеры` компонента на простые в управлении _тестовые двойники_, как показано в следующем варианте установки:

<code-example header="app/hero/hero-detail.component.spec.ts (Override setup)" path="testing/src/app/hero/hero-detail.component.spec.ts" region="setup-override"></code-example>.

Обратите внимание, что `TestBed.configureTestingModule` больше не предоставляет поддельный `HeroService`, потому что он [не нужен](#spy-stub).

<a id="override-component-method"></a>

#### Метод `overrideComponent`.

Сфокусируйтесь на методе `overrideComponent`.

<code-example header="app/hero/hero-detail.component.spec.ts (overrideComponent)" path="testing/src/app/hero/hero-detail.component.spec.ts" region="override-component-method"></code-example>.

Он принимает два аргумента: тип компонента для переопределения \(`HeroDetailComponent`\) и объект метаданных переопределения. Объект метаданных [override metadata object](guide/testing-utility-apis#metadata-override-object) является общим, определяемым следующим образом:

<code-example language="javascript">

type MetadataOverride&lt;T&gt; = { add? Partial&lt;T&gt;;
remove? Partial&lt;T&gt;;

set?: Partial&lt;T&gt;;

};

</code-example>

Объект переопределения метаданных может либо добавлять и удалять элементы в свойствах метаданных, либо полностью сбрасывать эти свойства. В этом примере сбрасываются метаданные `providers` компонента.

Параметр типа, `T`, является типом метаданных, которые вы передадите декоратору `@Component`:

<code-example language="javascript">

selector?: string; template?: string;
templateUrl?: string;

провайдеры?: any[];

&hellip;

</code-example>

<a id="spy-stub"></a>

#### Предоставление заглушки _шпиона_ (`HeroDetailServiceSpy`)

Этот пример полностью заменяет массив `providers` компонента на новый массив, содержащий `HeroDetailServiceSpy`.

`HeroDetailServiceSpy` - это заглушка настоящей версии `HeroDetailService`, которая имитирует все необходимые функции этого сервиса. Он не инжектирует и не делегирует на более низкий уровень `HeroService`, поэтому нет необходимости предоставлять тестовый дубль для этого.

Соответствующие тесты `HeroDetailComponent` будут утверждать, что методы `HeroDetailService` были вызваны путем шпионажа за методами сервиса. Соответственно, заглушка реализует свои методы как шпионы:

<code-example header="app/hero/hero-detail.component.spec.ts (HeroDetailServiceSpy)" path="testing/src/app/hero/hero-detail.component.spec.ts" region="hds-spy"></code-example>

<a id="override-tests"></a>

#### Тесты переопределения

Теперь тесты могут управлять героем компонента напрямую, манипулируя `testHero` в spy-stub, и подтверждать, что методы сервиса были вызваны.

<code-example header="app/hero/hero-detail.component.spec.ts (override tests)" path="testing/src/app/hero/hero-detail.component.spec.ts" region="override-tests"></code-example>

<a id="more-overrides"></a>

#### Больше переопределений

Метод `TestBed.overrideComponent` может быть вызван несколько раз для одного и того же или разных компонентов. В `TestBed` есть аналогичные методы `overrideDirective`, `overrideModule` и `overridePipe` для поиска и замены частей этих других классов.

Исследуйте варианты и комбинации самостоятельно.

<!-- links -->

<!-- external links -->

<!-- end links -->

:дата: 28.02.2022
