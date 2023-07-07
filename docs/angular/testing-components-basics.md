# Основы тестирования компонентов

:date: 28.02.2022

Компонент, в отличие от всех других частей приложения Angular, сочетает в себе HTML-шаблон и класс TypeScript. Компонент действительно представляет собой шаблон и класс, _работающие вместе_.

Чтобы адекватно протестировать компонент, необходимо проверить, что они работают вместе так, как задумано.

Такие тесты требуют создания основного элемента компонента в DOM браузера, как это делает Angular, и исследования взаимодействия класса компонента с DOM, как описано в его шаблоне.

Angular `TestBed` облегчает этот вид тестирования, как вы увидите в следующих разделах. Но во многих случаях _тестирование класса компонента в одиночку_, без участия DOM, может подтвердить большую часть поведения компонента простым и более очевидным способом.

!!!note ""

    Если вы хотите поэкспериментировать с приложением, которое описано в этом руководстве, [запустите его в браузере](https://angular.io/generated/live-examples/testing/stackblitz.html) или скачайте и запустите его локально.

## Тестирование класса компонента {: #component-class-testing}

Тестируйте класс компонента самостоятельно, как вы тестировали бы класс сервиса.

Тестирование класса компонента должно быть очень чистым и простым. Он должен тестировать только один модуль.

С первого взгляда должно быть понятно, что проверяет тест.

Рассмотрим этот `LightswitchComponent`, который включает и выключает свет (представленный экранным сообщением), когда пользователь нажимает на кнопку.

```ts
@Component({
    selector: 'lightswitch-comp',
    template: ` <button type="button" (click)="clicked()">
            Click me!
        </button>
        <span>{{ message }}</span>`,
})
export class LightswitchComponent {
    isOn = false;
    clicked() {
        this.isOn = !this.isOn;
    }
    get message() {
        return `The light is ${this.isOn ? 'On' : 'Off'}`;
    }
}
```

Вы можете решить только проверить, что метод `clicked()` переключает состояние света _on/off_ и устанавливает соответствующее сообщение.

Этот класс компонента не имеет зависимостей. Чтобы протестировать классы такого типа, выполните те же шаги, что и для службы, не имеющей зависимостей:

1.  Создайте компонент, используя ключевое слово new.
2.  Посмотрите на его API.
3.  Утвердите ожидания для его публичного состояния.

```ts
describe('LightswitchComp', () => {
    it('#clicked() should toggle #isOn', () => {
        const comp = new LightswitchComponent();
        expect(comp.isOn)
            .withContext('off at first')
            .toBe(false);
        comp.clicked();
        expect(comp.isOn)
            .withContext('on after click')
            .toBe(true);
        comp.clicked();
        expect(comp.isOn)
            .withContext('off after second click')
            .toBe(false);
    });

    it('#clicked() should set #message to "is on"', () => {
        const comp = new LightswitchComponent();
        expect(comp.message)
            .withContext('off at first')
            .toMatch(/is off/i);
        comp.clicked();
        expect(comp.message)
            .withContext('on after clicked')
            .toMatch(/is on/i);
    });
});
```

Вот `DashboardHeroComponent` из учебника _Tour of Heroes_.

```ts
export class DashboardHeroComponent {
    @Input() hero!: Hero;
    @Output() selected = new EventEmitter<Hero>();
    click() {
        this.selected.emit(this.hero);
    }
}
```

Он появляется в шаблоне родительского компонента, который связывает _hero_ со свойством `@Input` и слушает событие, вызванное через свойство _selected_ `@Output`.

Вы можете проверить, что код класса работает без создания `DashboardHeroComponent` или его родительского компонента.

```ts
it('raises the selected event when clicked', () => {
    const comp = new DashboardHeroComponent();
    const hero: Hero = { id: 42, name: 'Test' };
    comp.hero = hero;

    comp.selected
        .pipe(first())
        .subscribe((selectedHero: Hero) =>
            expect(selectedHero).toBe(hero)
        );
    comp.click();
});
```

Когда компонент имеет зависимости, вы можете захотеть использовать `TestBed` для создания компонента и его зависимостей.

Следующий `WelcomeComponent` зависит от `UserService`, чтобы узнать имя пользователя для приветствия.

```ts
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

Вы можете начать с создания макета `UserService`, который отвечает минимальным требованиям этого компонента.

```ts
class MockUserService {
    isLoggedIn = true;
    user = { name: 'Test User' };
}
```

Затем предоставьте и внедрите _как_ **компонент** _так и сервис_ в конфигурацию `TestBed`.

```ts
beforeEach(() => {
    TestBed.configureTestingModule({
        // provide the component-under-test and dependent service
        providers: [
            WelcomeComponent,
            {
                provide: UserService,
                useClass: MockUserService,
            },
        ],
    });
    // inject both the component and the dependent service.
    comp = TestBed.inject(WelcomeComponent);
    userService = TestBed.inject(UserService);
});
```

Затем запустите класс компонента, не забыв вызвать методы [lifecycle hooks](lifecycle-hooks.md), как это делает Angular при запуске приложения.

```ts
it('should not have welcome message after construction', () => {
    expect(comp.welcome).toBe('');
});

it('should welcome logged in user after Angular calls ngOnInit', () => {
    comp.ngOnInit();
    expect(comp.welcome).toContain(userService.user.name);
});

it('should ask user to log in if not logged in after ngOnInit', () => {
    userService.isLoggedIn = false;
    comp.ngOnInit();
    expect(comp.welcome).not.toContain(
        userService.user.name
    );
    expect(comp.welcome).toContain('log in');
});
```

## Тестирование DOM компонента

Тестирование _класса_ компонента так же просто, как [тестирование сервиса](testing-services.md).

Но компонент - это нечто большее, чем просто его класс. Компонент взаимодействует с DOM и с другими компонентами.

Тесты _только для класса_ могут рассказать вам о поведении класса.

Они не могут сказать вам, будет ли компонент правильно отображаться, реагировать на пользовательский ввод и жесты или интегрироваться с родительскими и дочерними компонентами.

Ни один из предыдущих _class-only_ тестов не может ответить на ключевые вопросы о том, как компоненты ведут себя на экране.

-   Привязан ли `Lightswitch.clicked()` к чему-либо так, чтобы пользователь мог вызвать его?
-   Отображается ли `Lightswitch.message`?
-   Может ли пользователь выбрать героя, отображаемого `DashboardHeroComponent`?
-   Отображается ли имя героя так, как ожидалось (например, в верхнем регистре)?
-   Отображается ли приветственное сообщение по шаблону `WelcomeComponent`?

Эти вопросы могут не вызывать беспокойства для предыдущих простых компонентов, показанных на рисунке. Но многие компоненты имеют сложное взаимодействие с элементами DOM, описанными в их шаблонах, заставляя HTML появляться и исчезать при изменении состояния компонента.

Чтобы ответить на эти вопросы, необходимо создать элементы DOM, связанные с компонентами, исследовать DOM, чтобы убедиться, что состояние компонента отображается должным образом в нужное время, и смоделировать взаимодействие пользователя с экраном, чтобы определить, вызывают ли эти взаимодействия поведение компонента, как ожидалось.

Чтобы написать эти виды тестов, вы будете использовать дополнительные возможности `TestBed`, а также другие вспомогательные средства тестирования.

### Тесты, создаваемые CLI

CLI по умолчанию создает начальный файл тестов, когда вы просите его сгенерировать новый компонент.

Например, следующая команда CLI генерирует `BannerComponent` в папке `app/banner` (с встроенным шаблоном и стилями):

```shell
ng generate component banner --inline-template --inline-style --module app
```

Он также генерирует начальный тестовый файл для компонента, `banner-external.component.spec.ts`, который выглядит следующим образом:

```ts
import {
    ComponentFixture,
    TestBed,
    waitForAsync,
} from '@angular/core/testing';

import { BannerComponent } from './banner.component';

describe('BannerComponent', () => {
    let component: BannerComponent;
    let fixture: ComponentFixture<BannerComponent>;

    beforeEach(
        waitForAsync(() => {
            TestBed.configureTestingModule({
                declarations: [BannerComponent],
            }).compileComponents();
        })
    );

    beforeEach(() => {
        fixture = TestBed.createComponent(BannerComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeDefined();
    });
});
```

!!!note ""

    Поскольку `compileComponents` является асинхронным, он использует утилиту [`waitForAsync`](https://angular.io/api/core/testing/waitForAsync), импортированную из `@angular/core/testing`.

    Более подробную информацию см. в разделе [waitForAsync](testing-components-scenarios.md#waitForAsync).

### Уменьшить настройку

Только последние три строки этого файла действительно тестируют компонент, и все, что они делают, это утверждают, что Angular может создать компонент.

Остальная часть файла - это код настройки, предвосхищающий более продвинутые тесты, которые _могут_ стать необходимыми, если компонент разовьется во что-то существенное.

Вы узнаете об этих расширенных возможностях тестирования в следующих разделах. Пока же вы можете радикально уменьшить этот файл тестов до более удобного размера:

```ts
describe('BannerComponent (minimal)', () => {
    it('should create', () => {
        TestBed.configureTestingModule({
            declarations: [BannerComponent],
        });
        const fixture = TestBed.createComponent(
            BannerComponent
        );
        const component = fixture.componentInstance;
        expect(component).toBeDefined();
    });
});
```

В этом примере объект метаданных, переданный в `TestBed.configureTestingModule`, просто объявляет `BannerComponent`, компонент для тестирования.

```ts
TestBed.configureTestingModule({
    declarations: [BannerComponent],
});
```

!!!note ""

    Нет необходимости объявлять или импортировать что-либо еще. Модуль тестирования по умолчанию предварительно сконфигурирован с чем-то вроде `BrowserModule` из `@angular/platform-browser`.

    Позже вы вызовете `TestBed.configureTestingModule()` с импортом, провайдерами и другими объявлениями в соответствии с вашими потребностями тестирования. Необязательные методы `override` позволяют еще более точно настроить аспекты конфигурации.

### `createComponent()` {: #create-component}

После настройки `TestBed`, вы вызываете его метод `createComponent()`.

```ts
const fixture = TestBed.createComponent(BannerComponent);
```

`TestBed.createComponent()` создает экземпляр `BannerComponent`, добавляет соответствующий элемент в DOM test-runner и возвращает [`ComponentFixture`](#component-fixture).

!!!warning ""

    Не переконфигурируйте `TestBed` после вызова `createComponent`.

    Метод `createComponent` замораживает текущее определение `TestBed`, закрывая его для дальнейшей конфигурации.

    Вы не можете больше вызывать никаких методов конфигурации `TestBed`, ни `configureTestingModule()`, ни `get()`, ни одного из методов `override...`. Если вы попытаетесь, `TestBed` выдаст ошибку.

### `ComponentFixture` {: #component-fixture}

[ComponentFixture](https://angular.io/api/core/testing/ComponentFixture) - это тестовый набор для взаимодействия с созданным компонентом и его соответствующим элементом.

Получите доступ к экземпляру компонента через фикстуру и подтвердите его существование с помощью ожидания Jasmine:

```ts
const component = fixture.componentInstance;
expect(component).toBeDefined();
```

### `beforeEach()`

Вы будете добавлять больше тестов по мере развития этого компонента. Вместо того, чтобы дублировать конфигурацию `TestBed` для каждого теста, вы рефакторите, чтобы вытащить настройку в Jasmine `beforeEach()` и некоторые вспомогательные переменные:

```ts
describe('BannerComponent (with beforeEach)', () => {
    let component: BannerComponent;
    let fixture: ComponentFixture<BannerComponent>;

    beforeEach(() => {
        TestBed.configureTestingModule({
            declarations: [BannerComponent],
        });
        fixture = TestBed.createComponent(BannerComponent);
        component = fixture.componentInstance;
    });

    it('should create', () => {
        expect(component).toBeDefined();
    });
});
```

Теперь добавьте тест, который получает элемент компонента из `fixture.nativeElement` и ищет ожидаемый текст.

```ts
it('should contain "banner works!"', () => {
    const bannerElement: HTMLElement =
        fixture.nativeElement;
    expect(bannerElement.textContent).toContain(
        'banner works!'
    );
});
```

### `nativeElement` {: #native-element}

Значение `ComponentFixture.nativeElement` имеет тип `any`. Позже вы встретите `DebugElement.nativeElement`, и оно тоже имеет тип `any`.

Angular не может знать во время компиляции, каким типом HTML-элемента является `nativeElement` и является ли он вообще HTML-элементом. Приложение может быть запущено на _небраузерной платформе_, такой как сервер или [Web Worker](https://developer.mozilla.org/docs/Web/API/Web_Workers_API), где элемент может иметь ограниченный API или вообще не существовать.

Тесты в этом руководстве предназначены для запуска в браузере, поэтому значение `nativeElement` всегда будет `HTMLElement` или одним из его производных классов.

Зная, что это какой-то `HTMLElement`, используйте стандартный HTML `querySelector`, чтобы углубиться в дерево элементов.

Вот еще один тест, который вызывает `HTMLElement.querySelector` для получения элемента абзаца и поиска текста баннера:

```ts
it('should have <p> with "banner works!"', () => {
    const bannerElement: HTMLElement =
        fixture.nativeElement;
    const p = bannerElement.querySelector('p')!;
    expect(p.textContent).toEqual('banner works!');
});
```

### `DebugElement` {: #debug-element}

Angular _fixture_ предоставляет элемент компонента напрямую через `fixture.nativeElement`.

```ts
const bannerElement: HTMLElement = fixture.nativeElement;
```

На самом деле это удобный метод, реализованный как `fixture.debugElement.nativeElement`.

```ts
const bannerDe: DebugElement = fixture.debugElement;
const bannerEl: HTMLElement = bannerDe.nativeElement;
```

Для такого извилистого пути к элементу есть веская причина.

Свойства `nativeElement` зависят от среды выполнения. Вы можете выполнять эти тесты на _небраузерной_ платформе, которая не имеет DOM или чья DOM-эмуляция не поддерживает полный API `HTMLElement`.

Angular полагается на абстракцию `DebugElement` для безопасной работы на _всех поддерживаемых платформах_. Вместо создания дерева элементов HTML, Angular создает дерево `DebugElement`, которое оборачивает _нативные элементы_ для платформы выполнения.

Свойство `nativeElement` разворачивает `DebugElement` и возвращает объект элемента для конкретной платформы.

Поскольку примеры тестов для этого руководства предназначены для запуска только в браузере, `nativeElement` в этих тестах всегда является `HTMLElement`, чьи знакомые методы и свойства вы можете исследовать в тесте.

Вот предыдущий тест, повторно реализованный с `fixture.debugElement.nativeElement`:

```ts
it('should find the <p> with fixture.debugElement.nativeElement)', () => {
    const bannerDe: DebugElement = fixture.debugElement;
    const bannerEl: HTMLElement = bannerDe.nativeElement;
    const p = bannerEl.querySelector('p')!;
    expect(p.textContent).toEqual('banner works!');
});
```

У `DebugElement` есть другие методы и свойства, которые полезны в тестах, как вы увидите в других частях этого руководства.

Вы импортируете символ `DebugElement` из библиотеки ядра Angular.

```ts
import { DebugElement } from '@angular/core';
```

### `By.css()` {: #by-css}

Хотя все тесты в этом руководстве выполняются в браузере, некоторые приложения могут работать на другой платформе хотя бы часть времени.

Например, компонент может сначала отрисовываться на сервере в рамках стратегии, направленной на ускорение запуска приложения на устройствах с плохим соединением. Рендерер на стороне сервера может не поддерживать полный API элементов HTML.

Если он не поддерживает `querySelector`, предыдущий тест может оказаться неудачным.

Элемент `DebugElement` предлагает методы запроса, которые работают для всех поддерживаемых платформ. Эти методы запроса принимают функцию _predicate_, которая возвращает `true`, если узел в дереве `DebugElement` соответствует критериям выбора.

Вы создаете _предикат_ с помощью класса `By`, импортированного из библиотеки для платформы выполнения. Вот импорт `By` для платформы браузера:

```ts
import { By } from '@angular/platform-browser';
```

Следующий пример повторно реализует предыдущий тест с помощью `DebugElement.query()` и метода браузера `By.css`.

```ts
it('should find the <p> with fixture.debugElement.query(By.css)', () => {
    const bannerDe: DebugElement = fixture.debugElement;
    const paragraphDe = bannerDe.query(By.css('p'));
    const p: HTMLElement = paragraphDe.nativeElement;
    expect(p.textContent).toEqual('banner works!');
});
```

Некоторые примечательные наблюдения:

-   Статический метод `By.css()` выбирает узлы `DebugElement` со [стандартным CSS-селектором](https://developer.mozilla.org/docs/Web/Guide/CSS/Getting_started/Selectors).
-   Запрос возвращает `DebugElement` для параграфа.
-   Вы должны развернуть этот результат, чтобы получить элемент абзаца.

Когда вы фильтруете по селектору CSS и проверяете только свойства _родного элемента_ браузера, подход `By.css` может оказаться излишним.

Часто проще и понятнее фильтровать с помощью стандартного метода `HTMLElement`, такого как `querySelector()` или `querySelectorAll()`.
