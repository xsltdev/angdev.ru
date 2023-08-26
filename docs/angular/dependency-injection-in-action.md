---
description: В этом руководстве рассматриваются многие возможности инъекции зависимостей (DI) в Angular
---

# Инъекция зависимостей в действии

:date: 28.02.2022

В этом руководстве рассматриваются многие возможности инъекции зависимостей (DI) в Angular.

!!!note ""

    Смотрите [живой пример](https://angular.io/generated/live-examples/dependency-injection-in-action/stackblitz.html) для рабочего примера, содержащего фрагменты кода из этого руководства.

<a id="multiple-service-instances"></a>

## Множественные экземпляры сервисов (песочница)

Иногда требуется несколько экземпляров сервиса на _одном и том же уровне_ иерархии компонентов.

Хорошим примером является сервис, хранящий состояние для компонента-компаньона. Для каждого компонента требуется отдельный экземпляр сервиса. Каждый сервис имеет свое собственное рабочее состояние, изолированное от состояния сервиса и состояния другого компонента. Это называется _песочницей_, поскольку у каждого сервиса и экземпляра компонента есть своя "песочница", в которой можно играть.

<a id="hero-bios-component"></a>

В данном примере `HeroBiosComponent` представляет три экземпляра `HeroBioComponent`.

```ts
@Component({
    selector: 'app-hero-bios',
    template: ` <app-hero-bio [heroId]="1"></app-hero-bio>
        <app-hero-bio [heroId]="2"></app-hero-bio>
        <app-hero-bio [heroId]="3"></app-hero-bio>`,
    providers: [HeroService],
})
export class HeroBiosComponent {}
```

Каждый `HeroBioComponent` может редактировать биографию одного героя. `HeroBioComponent` полагается на `HeroCacheService` для получения, кэширования и выполнения других операций сохранения для данного героя.

```ts
@Injectable()
export class HeroCacheService {
    hero!: Hero;
    constructor(private heroService: HeroService) {}

    fetchCachedHero(id: number) {
        if (!this.hero) {
            this.hero = this.heroService.getHeroById(id);
        }
        return this.hero;
    }
}
```

Три экземпляра `HeroBioComponent` не могут использовать один и тот же экземпляр `HeroCacheService`, так как они будут конкурировать друг с другом в определении героя для кэширования.

Вместо этого каждый `HeroBioComponent` получает свой собственный экземпляр `HeroCacheService`, указывая `HeroCacheService` в своем массиве метаданных `providers`.

```ts
@Component({
    selector: 'app-hero-bio',
    template: ` <h4>{{ hero.name }}</h4>
        <ng-content></ng-content>
        <textarea
            cols="25"
            [(ngModel)]="hero.description"
        ></textarea>`,
    providers: [HeroCacheService],
})
export class HeroBioComponent implements OnInit {
    @Input() heroId = 0;

    constructor(private heroCache: HeroCacheService) {}

    ngOnInit() {
        this.heroCache.fetchCachedHero(this.heroId);
    }

    get hero() {
        return this.heroCache.hero;
    }
}
```

Родительский `HeroBiosComponent` привязывает значение к `heroId`. При `ngOnInit` этот идентификатор передается сервису, который извлекает и кэширует героя. Геттер для свойства `hero` извлекает кэшированного героя из сервиса. В шаблоне отображается это свойство, связанное с данными.

Найдите этот пример в [live code](https://angular.io/generated/live-examples/dependency-injection-in-action/stackblitz.html) и убедитесь, что три экземпляра `HeroBioComponent` имеют свои собственные кэшированные данные о герое.

![Bios](hero-bios.png)

<a id="qualify-dependency-lookup"></a>

## Квалифицировать поиск зависимостей с помощью декораторов параметров

Когда классу требуется зависимость, она добавляется в конструктор в качестве параметра. Когда Angular необходимо инстанцировать класс, он обращается к DI-фреймворку для предоставления зависимости. По умолчанию DI-фреймворк ищет провайдера в иерархии инжекторов, начиная с локального инжектора компонента и при необходимости поднимаясь вверх по дереву инжекторов, пока не достигнет корневого инжектора.

-   Первый инжектор, сконфигурированный с провайдером, передает зависимость (экземпляр сервиса или значение) в конструктор.
-   Если в корневом инжекторе провайдер не найден, фреймворк DI выдает ошибку.

Существует несколько вариантов модификации стандартного поведения поиска с помощью _декораторов параметров_ на сервисных параметрах конструктора класса.

<a id="optional"></a>

### Сделайте зависимость `@Optional` и ограничьте поиск с помощью `@Host`.

Зависимости могут быть зарегистрированы на любом уровне иерархии компонентов. Когда компонент запрашивает зависимость, Angular начинает с инжектора этого компонента и идет вверх по дереву инжекторов, пока не найдет первого подходящего провайдера. Если во время этого прохода не удается найти зависимость, Angular выдает ошибку.

В некоторых случаях необходимо ограничить поиск или учесть отсутствующую зависимость. Изменить поведение Angular при поиске можно с помощью декораторов `@Host` и `@Optional`, определяющих значение параметра service в конструкторе компонента.

-   Декоратор свойства `@Optional` указывает Angular возвращать null, если он не может найти зависимость
-   Декоратор свойства `@Host` останавливает восходящий поиск на _хостовом компоненте_.

    Обычно хост-компонент — это компонент, запрашивающий зависимость. Однако если этот компонент проецируется на _родительский_ компонент, то родительский компонент становится хостом. В следующем примере рассматривается второй случай.

Эти декораторы могут использоваться как по отдельности, так и вместе, как показано в примере. Этот `HeroBiosAndContactsComponent` является ревизией `HeroBiosComponent`, который вы рассматривали [выше](dependency-injection-in-action.md#hero-bios-component).

```ts
@Component({
    selector: 'app-hero-bios-and-contacts',
    template: ` <app-hero-bio [heroId]="1">
            <app-hero-contact></app-hero-contact>
        </app-hero-bio>
        <app-hero-bio [heroId]="2">
            <app-hero-contact></app-hero-contact>
        </app-hero-bio>
        <app-hero-bio [heroId]="3">
            <app-hero-contact></app-hero-contact>
        </app-hero-bio>`,
    providers: [HeroService],
})
export class HeroBiosAndContactsComponent {
    constructor(logger: LoggerService) {
        logger.logInfo(
            'Creating HeroBiosAndContactsComponent'
        );
    }
}
```

Ориентируйтесь на шаблон:

```ts
template: `
  <app-hero-bio [heroId]="1"> <app-hero-contact></app-hero-contact> </app-hero-bio>
  <app-hero-bio [heroId]="2"> <app-hero-contact></app-hero-contact> </app-hero-bio>
  <app-hero-bio [heroId]="3"> <app-hero-contact></app-hero-contact> </app-hero-bio>`,
```

Теперь между тегами `<hero-contact>` появился новый элемент `<hero-bio>`. Angular _проецирует_, или _трансклюзирует_, соответствующий `HeroContactComponent` в представление `HeroBioComponent`, помещая его в слот `<ng-content>` шаблона `HeroBioComponent`.

```ts
template: `
  <h4>{{hero.name}}</h4>
  <ng-content></ng-content>
  <textarea cols="25" [(ngModel)]="hero.description"></textarea>`,
```

Результат показан ниже, причем номер телефона героя из `HeroContactComponent` проецируется над описанием героя.

![bio and contact](hero-bio-and-content.png)

Приведем `HeroContactComponent`, который демонстрирует квалификационные декораторы.

```ts
@Component({
    selector: 'app-hero-contact',
    template: ` <div>
        Phone #: {{ phoneNumber }}
        <span *ngIf="hasLogger">!!!</span>
    </div>`,
})
export class HeroContactComponent {
    hasLogger = false;

    constructor(
        @Host() // limit to the host component's instance of the HeroCacheService
        private heroCache: HeroCacheService,

        @Host() // limit search for logger; hides the application-wide logger
        @Optional() // ok if the logger doesn't exist
        private loggerService?: LoggerService
    ) {
        if (loggerService) {
            this.hasLogger = true;
            loggerService.logInfo(
                'HeroContactComponent can log!'
            );
        }
    }

    get phoneNumber() {
        return this.heroCache.hero.phone;
    }
}
```

Ориентируйтесь на параметры конструктора.

```ts
@Host() // limit to the host component's instance of the HeroCacheService
private heroCache: HeroCacheService,

@Host()     // limit search for logger; hides the application-wide logger
@Optional() // ok if the logger doesn't exist
private loggerService?: LoggerService
```

Функция `@Host()`, украшающая свойство конструктора `heroCache`, обеспечивает получение ссылки на сервис кэширования от родительского компонента `HeroBioComponent`. Angular выдает ошибку, если в родительском компоненте отсутствует этот сервис, даже если компонент, расположенный выше в дереве компонентов, содержит его.

Вторая функция `@Host()` украшает свойство конструктора `loggerService`. Единственный экземпляр `LoggerService` в приложении предоставляется на уровне `AppComponent`. Хост `HeroBioComponent` не имеет собственного провайдера `LoggerService`.

Angular выдает ошибку, если вы также не украсили свойство параметром `@Optional()`. Если свойство помечено как необязательное, Angular устанавливает значение `loggerService` в null, а остальная часть компонента адаптируется.

Вот `HeroBiosAndContactsComponent` в действии.

![Bios with contact into](hero-bios-and-contacts.png)

Если закомментировать декоратор `@Host()`, то Angular будет подниматься по дереву предков-инжекторов, пока не найдет логгер на уровне `AppComponent`. Логика работы логгера срабатывает, и на экране героя появляется маркер "!!!", указывающий на то, что логгер найден.

![Without @Host](hero-bio-contact-no-host.png)

Если восстановить декоратор `@Host()` и закомментировать `@Optional`, то приложение будет выбрасывать исключение, когда не сможет найти нужный логгер на уровне хост-компонента.

```shell
EXCEPTION: No provider for LoggerService! (HeroContactComponent -> LoggerService)
```

### Предоставление пользовательского провайдера с помощью `@Inject`

Использование пользовательского провайдера позволяет обеспечить конкретную реализацию неявных зависимостей, таких как встроенные API браузера. В следующем примере используется `InjectionToken` для предоставления API браузера [localStorage](https://developer.mozilla.org/docs/Web/API/Window/localStorage) в качестве зависимости в `BrowserStorageService`.

```ts
import {
    Inject,
    Injectable,
    InjectionToken,
} from '@angular/core';

export const BROWSER_STORAGE = new InjectionToken<Storage>(
    'Browser Storage',
    {
        providedIn: 'root',
        factory: () => localStorage,
    }
);

@Injectable({
    providedIn: 'root',
})
export class BrowserStorageService {
    constructor(
        @Inject(BROWSER_STORAGE) public storage: Storage
    ) {}

    get(key: string) {
        return this.storage.getItem(key);
    }

    set(key: string, value: string) {
        this.storage.setItem(key, value);
    }

    remove(key: string) {
        this.storage.removeItem(key);
    }

    clear() {
        this.storage.clear();
    }
}
```

Функция `factory` возвращает свойство `localStorage`, привязанное к объекту окна браузера. Декоратор `Inject` — это параметр конструктора, используемый для указания пользовательского провайдера зависимости. Теперь этот пользовательский провайдер может быть переопределен при тестировании с помощью имитации API `localStorage` вместо взаимодействия с реальными API браузера.

<a id="skip"></a>

### Модифицируйте поиск провайдера с помощью `@Self` и `@SkipSelf`.

Провайдеры также могут быть скопированы инжектором через декораторы параметров конструктора. Следующий пример переопределяет токен `BROWSER_STORAGE` в классе `providers` компонента `Component` с API браузера `sessionStorage`. Один и тот же `BrowserStorageService` дважды инжектируется в конструктор, украшенный параметрами `@Self` и `@SkipSelf` для определения того, какой инжектор обрабатывает зависимость от провайдера.

```ts
import {
    Component,
    OnInit,
    Self,
    SkipSelf,
} from '@angular/core';
import {
    BROWSER_STORAGE,
    BrowserStorageService,
} from './storage.service';

@Component({
    selector: 'app-storage',
    template: `
        Open the inspector to see the local/session storage
        keys:

        <h3>Session Storage</h3>
        <button type="button" (click)="setSession()">
            Set Session Storage
        </button>

        <h3>Local Storage</h3>
        <button type="button" (click)="setLocal()">
            Set Local Storage
        </button>
    `,
    providers: [
        BrowserStorageService,
        {
            provide: BROWSER_STORAGE,
            useFactory: () => sessionStorage,
        },
    ],
})
export class StorageComponent {
    constructor(
        @Self()
        private sessionStorageService: BrowserStorageService,
        @SkipSelf()
        private localStorageService: BrowserStorageService
    ) {}

    setSession() {
        this.sessionStorageService.set(
            'hero',
            'Dr Nice - Session'
        );
    }

    setLocal() {
        this.localStorageService.set(
            'hero',
            'Dr Nice - Local'
        );
    }
}
```

При использовании декоратора `@Self` инжектор обращается к инжектору компонента только для поиска его провайдеров. Декоратор `@SkipSelf` позволяет пропустить локальный инжектор и поискать в иерархии провайдер, удовлетворяющий данной зависимости. Экземпляр `sessionStorageService` взаимодействует с `BrowserStorageService`, используя API браузера `sessionStorage`, а `localStorageService` пропускает локальный инжектор и использует корневой `BrowserStorageService`, который использует API браузера `localStorage`.

<a id="component-element"></a>

## Инжектировать DOM-элемент компонента

Хотя разработчики стараются этого избегать, многие визуальные эффекты и сторонние инструменты, такие как jQuery, требуют доступа к DOM. В результате может потребоваться доступ к DOM-элементу компонента.

В качестве иллюстрации приведем минимальную версию `HighlightDirective` со страницы [Attribute Directives](attribute-directives.md).

```ts
import {
    Directive,
    ElementRef,
    HostListener,
    Input,
} from '@angular/core';

@Directive({
    selector: '[appHighlight]',
})
export class HighlightDirective {
    @Input('appHighlight') highlightColor = '';

    private el: HTMLElement;

    constructor(el: ElementRef) {
        this.el = el.nativeElement;
    }

    @HostListener('mouseenter') onMouseEnter() {
        this.highlight(this.highlightColor || 'cyan');
    }

    @HostListener('mouseleave') onMouseLeave() {
        this.highlight('');
    }

    private highlight(color: string) {
        this.el.style.backgroundColor = color;
    }
}
```

Директива устанавливает фон на цвет выделения, когда пользователь наводит курсор мыши на элемент DOM, к которому применена директива.

При этом Angular устанавливает параметр `el` конструктора в инжектированный `ElementRef`. ("ElementRef" — это обертка вокруг элемента DOM, свойство `nativeElement` которой раскрывает элемент DOM для манипулирования директивой).

В примере к двум тегам `<div>` применяется атрибут директивы `appHighlight`, сначала без значения (цвет по умолчанию), а затем с заданным значением цвета.

```html
<div id="highlight" class="di-component" appHighlight>
    <h3>Hero Bios and Contacts</h3>
    <div appHighlight="yellow">
        <app-hero-bios-and-contacts></app-hero-bios-and-contacts>
    </div>
</div>
```

На следующем рисунке показан эффект от наведения курсора мыши на тег `<hero-bios-and-contacts>`.

![Highlighted bios](highlight.png)

<a id="defining-providers"></a>

### Определение поставщиков

Зависимость не всегда может быть создана стандартным методом инстанцирования класса. О некоторых других методах вы узнали в разделе [Dependency Providers](dependency-injection-providers.md). Следующий пример `HeroOfTheMonthComponent` демонстрирует многие из альтернатив и то, зачем они нужны. Визуально он прост: несколько свойств и журналы, создаваемые логгером.

![Hero of the month](hero-of-month.png)

Код, стоящий за ним, настраивает, как и где фреймворк DI предоставляет зависимости. Примеры использования иллюстрируют различные способы применения объектного литерала _provide_ для связывания объекта определения с маркером DI.

```ts
import { Component, Inject } from '@angular/core';

import { DateLoggerService } from './date-logger.service';
import { Hero } from './hero';
import { HeroService } from './hero.service';
import { LoggerService } from './logger.service';
import { MinimalLogger } from './minimal-logger.service';
import { RUNNERS_UP, runnersUpFactory } from './runners-up';

@Component({
    selector: 'app-hero-of-the-month',
    templateUrl: './hero-of-the-month.component.html',
    providers: [
        { provide: Hero, useValue: someHero },
        { provide: TITLE, useValue: 'Hero of the Month' },
        { provide: HeroService, useClass: HeroService },
        {
            provide: LoggerService,
            useClass: DateLoggerService,
        },
        {
            provide: MinimalLogger,
            useExisting: LoggerService,
        },
        {
            provide: RUNNERS_UP,
            useFactory: runnersUpFactory(2),
            deps: [Hero, HeroService],
        },
    ],
})
export class HeroOfTheMonthComponent {
    logs: string[] = [];

    constructor(
        logger: MinimalLogger,
        public heroOfTheMonth: Hero,
        @Inject(RUNNERS_UP) public runnersUp: string,
        @Inject(TITLE) public title: string
    ) {
        this.logs = logger.logs;
        logger.logInfo('starting up');
    }
}
```

Массив `providers` показывает, как можно использовать различные ключи определения провайдера: `useValue`, `useClass`, `useExisting` или `useFactory`.

<a id="usevalue"></a>

#### Провайдеры значений: `useValue`.

Ключ `useValue` позволяет связать фиксированное значение с маркером DI. Эта техника используется для предоставления констант конфигурации времени выполнения, таких как базовые адреса сайтов и флаги возможностей. Также можно использовать провайдер значений в модульном тесте для предоставления имитационных данных вместо производственного сервиса данных.

В примере `HeroOfTheMonthComponent` имеется два провайдера значений.

```ts
{ provide: Hero,  useValue: someHero },
{ provide: TITLE, useValue: 'Hero of the Month' },
```

-   Первый предоставляет существующий экземпляр класса `Hero` для использования в качестве маркера `Hero`, а не требует от инжектора создавать новый экземпляр с помощью `new` или использовать свой собственный кэшированный экземпляр.

    Здесь маркером является сам класс.

-   Во втором случае для маркера `TITLE` используется литеральный строковый ресурс.

    Токен провайдера `TITLE` не является классом, а представляет собой специальный вид ключа поиска провайдера, называемый [injection token](dependency-injection-in-action.md#injection-token), представленный экземпляром `InjectionToken`.

Токен инъекции можно использовать для любого типа провайдера, но он особенно полезен, когда зависимость представляет собой простое значение, например строку, число или функцию.

Значение _провайдера значений_ должно быть определено до того, как вы укажете его здесь. Строковый литерал `title` доступен сразу. Переменная `someHero` в этом примере была задана ранее в файле, как показано ниже. Нельзя использовать переменную, значение которой будет определено позже.

```ts
const someHero = new Hero(
    42,
    'Magma',
    'Had a great month!',
    '555-555-5555'
);
```

Другие типы провайдеров могут создавать свои значения _одномоментно_, то есть тогда, когда они нужны для инъекции.

<a id="useclass"></a>

#### Провайдеры классов: `useClass`.

Ключ провайдера `useClass` позволяет создавать и возвращать новый экземпляр указанного класса.

Этот тип провайдера можно использовать для подстановки _альтернативной реализации_ общего класса или класса по умолчанию. Альтернативная реализация может, например, реализовать другую стратегию, расширить класс по умолчанию или эмулировать поведение реального класса в тестовом случае.

В следующем коде показаны два примера в `HeroOfTheMonthComponent`.

```ts
{ provide: HeroService,   useClass: HeroService },
{ provide: LoggerService, useClass: DateLoggerService },
```

Первый провайдер представляет собой _упрощенную_, расширенную форму наиболее типичного случая, когда создаваемый класс (`HeroService`) является также маркером инъекции зависимостей провайдера. Как правило, предпочтительнее использовать короткую форму; в этой длинной форме все детали выражены явно.

Второй провайдер заменяет `DateLoggerService` на `LoggerService`. `LoggerService` уже зарегистрирован на уровне `AppComponent`. Когда этот дочерний компонент запрашивает `LoggerService`, он получает вместо него экземпляр `DateLoggerService`.

!!!note ""

    Этот компонент и дерево его дочерних компонентов получают экземпляр `DateLoggerService`. Компоненты вне дерева продолжают получать оригинальный экземпляр `LoggerService`.

`DateLoggerService` наследует от `LoggerService`; он добавляет текущую дату/время к каждому сообщению:

```ts
@Injectable({
  providedIn: 'root'
})
export class DateLoggerService extends LoggerService
{
  override logInfo(msg: any)  { super.logInfo(stamp(msg)); }
  override logDebug(msg: any) { super.logInfo(stamp(msg)); }
  override logError(msg: any) { super.logError(stamp(msg)); }
}

function stamp(msg: any) { return msg + ' at ' + new Date(); }
```

<a id="useexisting"></a>

#### Псевдонимы провайдеров: `useExisting`.

Ключ провайдера `useExisting` позволяет сопоставить один токен с другим. По сути, первый маркер является _алиасом_ для сервиса, связанного со вторым маркером, создавая два способа доступа к одному и тому же объекту сервиса.

```ts
{ provide: MinimalLogger, useExisting: LoggerService },
```

Этот прием можно использовать для сужения API через интерфейс псевдонимов. В следующем примере показан псевдоним, введенный для этой цели.

Представьте, что `LoggerService` имеет большой API, гораздо больший, чем реальные три метода и свойство. Возможно, вы захотите сократить эту поверхность API до тех членов, которые вам действительно нужны. В этом примере `MinimalLogger` [class-interface](#class-interface) сокращает API до двух членов:

```ts
// Class used as a "narrowing" interface that exposes a minimal logger
// Other members of the actual implementation are invisible
export abstract class MinimalLogger {
    abstract logs: string[];
    abstract logInfo: (msg: string) => void;
}
```

В следующем примере `MinimalLogger` используется в упрощенной версии `HeroOfTheMonthComponent`.

```ts
@Component({
    selector: 'app-hero-of-the-month',
    templateUrl: './hero-of-the-month.component.html',
    // TODO: move this aliasing, `useExisting` provider to the AppModule
    providers: [
        {
            provide: MinimalLogger,
            useExisting: LoggerService,
        },
    ],
})
export class HeroOfTheMonthComponent {
    logs: string[] = [];
    constructor(logger: MinimalLogger) {
        logger.logInfo('starting up');
    }
}
```

Параметр `logger` конструктора `HeroOfTheMonthComponent` типизирован как `MinimalLogger`, поэтому в редакторе, поддерживающем TypeScript, видны только члены `logs` и `logInfo`.

![MinimalLogger restricted API](minimal-logger-intellisense.png)

За кулисами Angular устанавливает параметр `logger` в полный сервис, зарегистрированный под токеном `LoggingService`, которым оказался экземпляр `DateLoggerService`, который был [предоставлен выше](dependency-injection-in-action.md#useclass).

!!!note ""

    Это показано на следующем рисунке, где отображается дата регистрации.

    ![DateLoggerService entry](date-logger-entry.png)

<a id="usefactory"></a>

#### Провайдеры фабрики: `useFactory`

Ключ провайдера `useFactory` позволяет создать объект зависимости путем вызова функции-фабрики, как показано в следующем примере.

```ts
{ provide: RUNNERS_UP, useFactory: runnersUpFactory(2), deps: [Hero, HeroService] }
```

Инжектор предоставляет значение зависимости, вызывая фабричную функцию, которую вы указываете в качестве значения ключа `useFactory`. Обратите внимание, что у этой формы провайдера есть третий ключ, `deps`, который задает зависимости для функции `useFactory`.

С помощью этой техники можно создать объект зависимости с фабричной функцией, входные данные которой представляют собой комбинацию _инжектируемых сервисов_ и _локальных состояний_.

Объект зависимости (возвращаемый фабричной функцией) обычно представляет собой экземпляр класса, но может быть и другим. В данном примере объект зависимости — это строка с именами победителей конкурса "Герой месяца".

В примере локальное состояние — это число `2`, количество участников конкурса, которое должен показать компонент. Значение состояния передается в качестве аргумента в `runnersUpFactory()`. Функция `runnersUpFactory()` возвращает фабричную функцию _провайдера_, которая может использовать как переданное значение состояния, так и инжектированные сервисы `Hero` и `HeroService`.

```ts
export function runnersUpFactory(take: number) {
  return (winner: Hero, heroService: HeroService): string =>
    /* ... */
}
```

Функция фабрики провайдеров (возвращаемая функцией `runnersUpFactory()`) возвращает фактический объект зависимости — строку имен.

-   В качестве аргументов функция принимает победителя `Hero` и `HeroService`.

    Angular предоставляет эти аргументы из инжектируемых значений, идентифицируемых двумя _токенами_ в массиве `deps`.

-   Функция возвращает строку имен, которую Angular затем инжектирует в параметр `runnersUp` компонента `HeroOfTheMonthComponent`.

!!!note ""

    Функция получает из `HeroService` героев-кандидатов, принимает `2` из них за победителей и возвращает их скомбинированные имена. Полный исходный текст смотрите в [живом примере](https://angular.io/generated/live-examples/dependency-injection-in-action/stackblitz.html).

<a id="tokens"></a>

## Альтернативы маркера поставщика: интерфейс класса и 'InjectionToken'

Инъекция зависимостей в Angular наиболее проста, когда маркер провайдера представляет собой класс, который также является типом возвращаемого объекта зависимости или сервиса.

Однако токен не обязательно должен быть классом, и даже если он является классом, он не обязательно должен быть того же типа, что и возвращаемый объект. Этому посвящен следующий раздел.

<a id="class-interface"></a>

### Интерфейс класса

В предыдущем примере _Hero of the Month_ в качестве маркера для провайдера `LoggerService` использовался класс `MinimalLogger`.

```ts
{ provide: MinimalLogger, useExisting: LoggerService },
```

`MinimalLogger` — это абстрактный класс.

```ts
// Class used as a "narrowing" interface that exposes a minimal logger
// Other members of the actual implementation are invisible
export abstract class MinimalLogger {
    abstract logs: string[];
    abstract logInfo: (msg: string) => void;
}
```

Абстрактный класс обычно является базовым классом, который можно расширять. В данном приложении, однако, нет класса, который бы наследовался от `MinimalLogger`. Сервисы `LoggerService` и `DateLoggerService` могли бы наследоваться от `MinimalLogger` или реализовать его в виде интерфейса. Но они не сделали ни того, ни другого. `MinimalLogger` используется только в качестве маркера для инъекции зависимостей.

Когда вы используете класс таким образом, это называется _интерфейсом класса_.

Как уже упоминалось в [Configuring dependency providers](dependency-injection-providers.md), интерфейс не является корректным маркером DI, поскольку это артефакт TypeScript, не существующий во время выполнения. Используйте этот абстрактный интерфейс класса, чтобы получить сильную типизацию интерфейса, а также использовать его в качестве маркера провайдера так же, как и обычный класс.

Интерфейс класса должен определять _только_ те члены, которые разрешено вызывать его потребителям. Такой сужающийся интерфейс помогает отделить конкретный класс от его потребителей.

!!!note ""

    Использование класса в качестве интерфейса позволяет получить характеристики интерфейса в реальном объекте JavaScript. Однако для минимизации затрат памяти класс не должен иметь _реализации_. Для конструктора `MinimalLogger` транспилируется в этот неоптимизированный, предварительно минимизированный JavaScript.

    ```ts
    var MinimalLogger = (function () {
    	function MinimalLogger() {}
    	return MinimalLogger;
    })();
    exports('MinimalLogger', MinimalLogger);
    ```

    У него нет членов. Он никогда не вырастет, сколько бы членов вы ни добавили в класс, если эти члены типизированы, но не реализованы.

    Посмотрите еще раз на класс TypeScript `MinimalLogger`, чтобы убедиться, что у него нет реализации.

<a id="injection-token"></a>

### Объекты 'InjectionToken'

Объекты зависимостей могут представлять собой простые значения, такие как даты, числа и строки, или бесформенные объекты, такие как массивы и функции.

Такие объекты не имеют прикладных интерфейсов и поэтому не могут быть представлены классом. Их лучше представлять с помощью токена, который одновременно уникален и символичен — объекта JavaScript, имеющего дружественное имя, но не конфликтующего с другим токеном, который случайно имеет такое же имя.

Такими характеристиками обладает `InjectionToken`. Вы дважды встречали их в примере _Герой месяца_, в поставщике значения _title_ и в поставщике фабрики _runnersUp_.

```ts
{ provide: TITLE,         useValue:   'Hero of the Month' },
{ provide: RUNNERS_UP,    useFactory:  runnersUpFactory(2), deps: [Hero, HeroService] }
```

Вы создали токен `TITLE` следующим образом:

```ts
import { InjectionToken } from '@angular/core';

export const TITLE = new InjectionToken<string>('title');
```

Параметр `type`, хотя и является необязательным, передает тип зависимости разработчикам и инструментальным средствам. Описание маркера является еще одним вспомогательным параметром для разработчиков.

<a id="di-inheritance"></a>

## Инжектирование в производный класс

Будьте внимательны при написании компонента, наследующего от другого компонента. Если базовый компонент имеет инжектированные зависимости, то их необходимо заново предоставить и инжектировать в производном классе, а затем передать в базовый класс через конструктор.

В данном примере `SortedHeroesComponent` наследуется от `HeroesBaseComponent` для отображения _отсортированного_ списка героев.

![Sorted Heroes](sorted-heroes.png)

Компонент `HeroesBaseComponent` может быть самостоятельным. Он требует свой экземпляр `HeroService` для получения героев и отображает их в порядке поступления из базы данных.

```ts
@Component({
    selector: 'app-unsorted-heroes',
    template:
        '<div *ngFor="let hero of heroes">{{hero.name}}</div>',
    providers: [HeroService],
})
export class HeroesBaseComponent implements OnInit {
    constructor(private heroService: HeroService) {}

    heroes: Hero[] = [];

    ngOnInit() {
        this.heroes = this.heroService.getAllHeroes();
        this.afterGetHeroes();
    }

    // Post-process heroes in derived class override.
    protected afterGetHeroes() {}
}
```

!!!note ""

    ### Сохраняйте конструкторы простыми

    Конструкторы должны делать не более чем инициализацию переменных. Это правило позволяет безопасно конструировать компонент при тестировании, не опасаясь, что он сделает что-то драматическое, например, обратится к серверу. Именно поэтому вы вызываете `HeroService` из `ngOnInit`, а не из конструктора.

Пользователи хотят видеть героев в алфавитном порядке. Вместо того чтобы модифицировать исходный компонент, создайте его подкласс и `SortedHeroesComponent`, который сортирует героев перед их отображением. Компонент `SortedHeroesComponent` позволяет базовому классу получать героев.

К сожалению, Angular не может инжектировать `HeroService` непосредственно в базовый класс. Вы должны предоставить `HeroService` еще раз для _этого_ компонента, а затем передать его базовому классу внутри конструктора.

```ts
@Component({
  selector: 'app-sorted-heroes',
  template: '<div *ngFor="let hero of heroes">{{hero.name}}</div>',
  providers: [HeroService]
})
export class SortedHeroesComponent extends HeroesBaseComponent {
  constructor(heroService: HeroService) {
    super(heroService);
  }

  protected override afterGetHeroes() {
    this.heroes = this.heroes.sort((h1, h2) => h1.name < h2.name ? -1 :
            (h1.name > h2.name ? 1 : 0));
  }
}
```

Теперь обратите внимание на метод `afterGetHeroes()`. Первый инстинкт — создать метод `ngOnInit` в `SortedHeroesComponent` и выполнить сортировку там. Но Angular вызывает `ngOnInit` _производного_ класса _перед_ вызовом `ngOnInit` базового класса, поэтому сортировка массива героев будет происходить _до их появления_. Это приводит к неприятной ошибке.

Переопределение метода `afterGetHeroes()` базового класса решает эту проблему.

Эти сложности говорят в пользу отказа от наследования компонентов.

<a id="forwardref"></a>

## Разрешение круговых зависимостей с помощью прямой ссылки на класс (_forwardRef_)

Порядок объявления классов имеет значение в TypeScript. Вы не можете напрямую ссылаться на класс, пока он не определен.

Обычно это не является проблемой, особенно если вы придерживаетесь рекомендуемого правила _один класс на файл_. Но иногда круговые ссылки неизбежны. Например, когда класс 'A' ссылается на класс 'B', а 'B' ссылается на 'A'. Один из них должен быть определен первым.

Функция Angular `forwardRef()` создает _непрямую_ ссылку, которую Angular может разрешить позже.

Пример _Parent Finder_ полон круговых ссылок на классы, которые невозможно разорвать.

Вы сталкиваетесь с этой дилеммой, когда класс делает _ссылку на самого себя_, как это делает `AlexComponent` в своем массиве `providers`. Массив `providers` является свойством функции-декоратора `@Component()`, которая должна появиться _выше_ определения класса.

Разорвите замкнутый круг с помощью `forwardRef`.

```ts
providers: [{ provide: Parent, useExisting: forwardRef(() => AlexComponent) }],
```

## Ссылки

-   [Dependency injection in action](https://angular.io/guide/dependency-injection-in-action)
