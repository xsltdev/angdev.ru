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

In this example, `HeroBiosComponent` presents three instances of `HeroBioComponent`.

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

Each `HeroBioComponent` can edit a single hero's biography.
`HeroBioComponent` relies on `HeroCacheService` to fetch, cache, and perform other persistence operations on that hero.

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

Three instances of `HeroBioComponent` can't share the same instance of `HeroCacheService`, as they'd be competing with each other to determine which hero to cache.

Instead, each `HeroBioComponent` gets its _own_ `HeroCacheService` instance by listing `HeroCacheService` in its metadata `providers` array.

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

The parent `HeroBiosComponent` binds a value to `heroId`. `ngOnInit` passes that ID to the service, which fetches and caches the hero. The getter for the `hero` property pulls the cached hero from the service. The template displays this data-bound property.

Find this example in [live code](https://angular.io/generated/live-examples/dependency-injection-in-action/stackblitz.html) and confirm that the three `HeroBioComponent` instances have their own cached hero data.

![Bios](hero-bios.png)

<a id="qualify-dependency-lookup"></a>

## Qualify dependency lookup with parameter decorators

When a class requires a dependency, that dependency is added to the constructor as a parameter. When Angular needs to instantiate the class, it calls upon the DI framework to supply the dependency. By default, the DI framework searches for a provider in the injector hierarchy, starting at the component's local injector, and if necessary bubbling up through the injector tree until it reaches the root injector.

-   The first injector configured with a provider supplies the dependency (a service instance or value) to the constructor
-   If no provider is found in the root injector, the DI framework throws an error

There are a number of options for modifying the default search behavior, using _parameter decorators_ on the service-valued parameters of a class constructor.

<a id="optional"></a>

### Make a dependency `@Optional` and limit search with `@Host`

Dependencies can be registered at any level in the component hierarchy. When a component requests a dependency, Angular starts with that component's injector and walks up the injector tree until it finds the first suitable provider. Angular throws an error if it can't find the dependency during that walk.

In some cases, you need to limit the search or accommodate a missing dependency. You can modify Angular's search behavior with the `@Host` and `@Optional` qualifying decorators on a service-valued parameter of the component's constructor.

-   The `@Optional` property decorator tells Angular to return null when it can't find the dependency
-   The `@Host` property decorator stops the upward search at the _host component_.
    The host component is typically the component requesting the dependency.
    However, when this component is projected into a _parent_ component, that parent component becomes the host.
    The following example covers this second case.

These decorators can be used individually or together, as shown in the example. This `HeroBiosAndContactsComponent` is a revision of `HeroBiosComponent` which you looked at [above](dependency-injection-in-action.md#hero-bios-component).

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

Focus on the template:

```ts
template: `
  <app-hero-bio [heroId]="1"> <app-hero-contact></app-hero-contact> </app-hero-bio>
  <app-hero-bio [heroId]="2"> <app-hero-contact></app-hero-contact> </app-hero-bio>
  <app-hero-bio [heroId]="3"> <app-hero-contact></app-hero-contact> </app-hero-bio>`,
```

Now there's a new `<hero-contact>` element between the `<hero-bio>` tags.
Angular _projects_, or _transcludes_, the corresponding `HeroContactComponent` into the `HeroBioComponent` view, placing it in the `<ng-content>` slot of the `HeroBioComponent` template.

```ts
template: `
  <h4>{{hero.name}}</h4>
  <ng-content></ng-content>
  <textarea cols="25" [(ngModel)]="hero.description"></textarea>`,
```

The result is shown below, with the hero's telephone number from `HeroContactComponent` projected above the hero description.

![bio and contact](hero-bio-and-content.png)

Here's `HeroContactComponent`, which demonstrates the qualifying decorators.

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

Focus on the constructor parameters.

```ts
@Host() // limit to the host component's instance of the HeroCacheService
private heroCache: HeroCacheService,

@Host()     // limit search for logger; hides the application-wide logger
@Optional() // ok if the logger doesn't exist
private loggerService?: LoggerService
```

The `@Host()` function decorating the `heroCache` constructor property ensures that you get a reference to the cache service from the parent `HeroBioComponent`. Angular throws an error if the parent lacks that service, even if a component higher in the component tree includes it.

A second `@Host()` function decorates the `loggerService` constructor property. The only `LoggerService` instance in the application is provided at the `AppComponent` level. The host `HeroBioComponent` doesn't have its own `LoggerService` provider.

Angular throws an error if you haven't also decorated the property with `@Optional()`. When the property is marked as optional, Angular sets `loggerService` to null and the rest of the component adapts.

Here's `HeroBiosAndContactsComponent` in action.

![Bios with contact into](hero-bios-and-contacts.png)

If you comment out the `@Host()` decorator, Angular walks up the injector ancestor tree until it finds the logger at the `AppComponent` level. The logger logic kicks in and the hero display updates with the "!!!" marker to indicate that the logger was found.

![Without @Host](hero-bio-contact-no-host.png)

If you restore the `@Host()` decorator and comment out `@Optional`, the application throws an exception when it cannot find the required logger at the host component level.

```shell
EXCEPTION: No provider for LoggerService! (HeroContactComponent -> LoggerService)
```

### Supply a custom provider with `@Inject`

Using a custom provider allows you to provide a concrete implementation for implicit dependencies, such as built-in browser APIs. The following example uses an `InjectionToken` to provide the [localStorage](https://developer.mozilla.org/docs/Web/API/Window/localStorage) browser API as a dependency in the `BrowserStorageService`.

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

The `factory` function returns the `localStorage` property that is attached to the browser window object. The `Inject` decorator is a constructor parameter used to specify a custom provider of a dependency. This custom provider can now be overridden during testing with a mock API of `localStorage` instead of interacting with real browser APIs.

<a id="skip"></a>

### Modify the provider search with `@Self` and `@SkipSelf`

Providers can also be scoped by injector through constructor parameter decorators. The following example overrides the `BROWSER_STORAGE` token in the `Component` class `providers` with the `sessionStorage` browser API. The same `BrowserStorageService` is injected twice in the constructor, decorated with `@Self` and `@SkipSelf` to define which injector handles the provider dependency.

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

Using the `@Self` decorator, the injector only looks at the component's injector for its providers. The `@SkipSelf` decorator allows you to skip the local injector and look up in the hierarchy to find a provider that satisfies this dependency. The `sessionStorageService` instance interacts with the `BrowserStorageService` using the `sessionStorage` browser API, while the `localStorageService` skips the local injector and uses the root `BrowserStorageService` that uses the `localStorage` browser API.

<a id="component-element"></a>

## Inject the component's DOM element

Although developers strive to avoid it, many visual effects and third-party tools, such as jQuery, require DOM access. As a result, you might need to access a component's DOM element.

To illustrate, here's a minimal version of `HighlightDirective` from the [Attribute Directives](attribute-directives.md) page.

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

The directive sets the background to a highlight color when the user mouses over the DOM element to which the directive is applied.

Angular sets the constructor's `el` parameter to the injected `ElementRef`. (An `ElementRef` is a wrapper around a DOM element, whose `nativeElement` property exposes the DOM element for the directive to manipulate.)

The sample code applies the directive's `appHighlight` attribute to two `<div>` tags, first without a value (yielding the default color) and then with an assigned color value.

```html
<div id="highlight" class="di-component" appHighlight>
    <h3>Hero Bios and Contacts</h3>
    <div appHighlight="yellow">
        <app-hero-bios-and-contacts></app-hero-bios-and-contacts>
    </div>
</div>
```

The following image shows the effect of mousing over the `<hero-bios-and-contacts>` tag.

![Highlighted bios](highlight.png)

<a id="defining-providers"></a>

### Defining providers

A dependency can't always be created by the default method of instantiating a class. You learned about some other methods in [Dependency Providers](dependency-injection-providers.md). The following `HeroOfTheMonthComponent` example demonstrates many of the alternatives and why you need them. It's visually simple: a few properties and the logs produced by a logger.

![Hero of the month](hero-of-month.png)

The code behind it customizes how and where the DI framework provides dependencies. The use cases illustrate different ways to use the _provide_ object literal to associate a definition object with a DI token.

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

The `providers` array shows how you might use the different provider-definition keys: `useValue`, `useClass`, `useExisting`, or `useFactory`.

<a id="usevalue"></a>

#### Value providers: `useValue`

The `useValue` key lets you associate a fixed value with a DI token. Use this technique to provide _runtime configuration constants_ such as website base addresses and feature flags. You can also use a value provider in a unit test to provide mock data in place of a production data service.

The `HeroOfTheMonthComponent` example has two value providers.

```ts
{ provide: Hero,  useValue: someHero },
{ provide: TITLE, useValue: 'Hero of the Month' },
```

-   The first provides an existing instance of the `Hero` class to use for the `Hero` token, rather than requiring the injector to create a new instance with `new` or use its own cached instance.

    Here, the token is the class itself.

-   The second specifies a literal string resource to use for the `TITLE` token.

    The `TITLE` provider token is _not_ a class, but is instead a special kind of provider lookup key called an [injection token](dependency-injection-in-action.md#injection-token), represented by an `InjectionToken` instance.

You can use an injection token for any kind of provider but it's particularly helpful when the dependency is a simple value like a string, a number, or a function.

The value of a _value provider_ must be defined before you specify it here. The title string literal is immediately available. The `someHero` variable in this example was set earlier in the file as shown below. You can't use a variable whose value will be defined later.

```ts
const someHero = new Hero(
    42,
    'Magma',
    'Had a great month!',
    '555-555-5555'
);
```

Other types of providers can create their values _lazily_; that is, when they're needed for injection.

<a id="useclass"></a>

#### Class providers: `useClass`

The `useClass` provider key lets you create and return a new instance of the specified class.

You can use this type of provider to substitute an _alternative implementation_ for a common or default class. The alternative implementation could, for example, implement a different strategy, extend the default class, or emulate the behavior of the real class in a test case.

The following code shows two examples in `HeroOfTheMonthComponent`.

```ts
{ provide: HeroService,   useClass: HeroService },
{ provide: LoggerService, useClass: DateLoggerService },
```

The first provider is the _de-sugared_, expanded form of the most typical case in which the class to be created (`HeroService`) is also the provider's dependency injection token. The short form is generally preferred; this long form makes the details explicit.

The second provider substitutes `DateLoggerService` for `LoggerService`. `LoggerService` is already registered at the `AppComponent` level. When this child component requests `LoggerService`, it receives a `DateLoggerService` instance instead.

!!!note ""

    This component and its tree of child components receive `DateLoggerService` instance. Components outside the tree continue to receive the original `LoggerService` instance.

`DateLoggerService` inherits from `LoggerService`; it appends the current date/time to each message:

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

#### Alias providers: `useExisting`

The `useExisting` provider key lets you map one token to another. In effect, the first token is an _alias_ for the service associated with the second token, creating two ways to access the same service object.

```ts
{ provide: MinimalLogger, useExisting: LoggerService },
```

You can use this technique to narrow an API through an aliasing interface. The following example shows an alias introduced for that purpose.

Imagine that `LoggerService` had a large API, much larger than the actual three methods and a property. You might want to shrink that API surface to just the members you actually need. In this example, the `MinimalLogger` [class-interface](#class-interface) reduces the API to two members:

```ts
// Class used as a "narrowing" interface that exposes a minimal logger
// Other members of the actual implementation are invisible
export abstract class MinimalLogger {
    abstract logs: string[];
    abstract logInfo: (msg: string) => void;
}
```

The following example puts `MinimalLogger` to use in a simplified version of `HeroOfTheMonthComponent`.

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

The `HeroOfTheMonthComponent` constructor's `logger` parameter is typed as `MinimalLogger`, so only the `logs` and `logInfo` members are visible in a TypeScript-aware editor.

![MinimalLogger restricted API](minimal-logger-intellisense.png)

Behind the scenes, Angular sets the `logger` parameter to the full service registered under the `LoggingService` token, which happens to be the `DateLoggerService` instance that was [provided above](dependency-injection-in-action.md#useclass).

!!!note ""

    This is illustrated in the following image, which displays the logging date.

    ![DateLoggerService entry](date-logger-entry.png)

<a id="usefactory"></a>

#### Factory providers: `useFactory`

The `useFactory` provider key lets you create a dependency object by calling a factory function, as in the following example.

```ts
{ provide: RUNNERS_UP, useFactory: runnersUpFactory(2), deps: [Hero, HeroService] }
```

The injector provides the dependency value by invoking a factory function, that you provide as the value of the `useFactory` key. Notice that this form of provider has a third key, `deps`, which specifies dependencies for the `useFactory` function.

Use this technique to create a dependency object with a factory function whose inputs are a combination of _injected services_ and _local state_.

The dependency object (returned by the factory function) is typically a class instance, but can be other things as well. In this example, the dependency object is a string of the names of the runners-up to the "Hero of the Month" contest.

In the example, the local state is the number `2`, the number of runners-up that the component should show. The state value is passed as an argument to `runnersUpFactory()`.
The `runnersUpFactory()` returns the _provider factory function_, which can use both the passed-in state value and the injected services `Hero` and `HeroService`.

```ts
export function runnersUpFactory(take: number) {
  return (winner: Hero, heroService: HeroService): string =>
    /* ... */
}
```

The provider factory function (returned by `runnersUpFactory()`) returns the actual dependency object, the string of names.

-   The function takes a winning `Hero` and a `HeroService` as arguments.

    Angular supplies these arguments from injected values identified by the two _tokens_ in the `deps` array.

-   The function returns the string of names, which Angular then injects into the `runnersUp` parameter of `HeroOfTheMonthComponent`

!!!note ""

    The function retrieves candidate heroes from the `HeroService`, takes `2` of them to be the runners-up, and returns their concatenated names. Look at the [live example](https://angular.io/generated/live-examples/dependency-injection-in-action/stackblitz.html) for the full source code.

<a id="tokens"></a>

## Provider token alternatives: class interface and 'InjectionToken'

Angular dependency injection is easiest when the provider token is a class that is also the type of the returned dependency object, or service.

However, a token doesn't have to be a class and even when it is a class, it doesn't have to be the same type as the returned object. That's the subject of the next section.

<a id="class-interface"></a>

### Class interface

The previous _Hero of the Month_ example used the `MinimalLogger` class as the token for a provider of `LoggerService`.

```ts
{ provide: MinimalLogger, useExisting: LoggerService },
```

`MinimalLogger` is an abstract class.

```ts
// Class used as a "narrowing" interface that exposes a minimal logger
// Other members of the actual implementation are invisible
export abstract class MinimalLogger {
    abstract logs: string[];
    abstract logInfo: (msg: string) => void;
}
```

An abstract class is usually a base class that you can extend. In this app, however there is no class that inherits from `MinimalLogger`. The `LoggerService` and the `DateLoggerService` could have inherited from `MinimalLogger`, or they could have implemented it instead, in the manner of an interface. But they did neither. `MinimalLogger` is used only as a dependency injection token.

When you use a class this way, it's called a _class interface_.

As mentioned in [Configuring dependency providers](dependency-injection-providers.md), an interface is not a valid DI token because it is a TypeScript artifact that doesn't exist at run time. Use this abstract class interface to get the strong typing of an interface, and also use it as a provider token in the way you would a normal class.

A class interface should define _only_ the members that its consumers are allowed to call. Such a narrowing interface helps decouple the concrete class from its consumers.

!!!note ""

    Using a class as an interface gives you the characteristics of an interface in a real JavaScript object. To minimize memory cost, however, the class should have _no implementation_. The `MinimalLogger` transpiles to this unoptimized, pre-minified JavaScript for a constructor function.

    ```ts
    var MinimalLogger = (function () {
    	function MinimalLogger() {}
    	return MinimalLogger;
    })();
    exports('MinimalLogger', MinimalLogger);
    ```

    It doesn't have any members. It never grows no matter how many members you add to the class, as long as those members are typed but not implemented.

    Look again at the TypeScript `MinimalLogger` class to confirm that it has no implementation.

<a id="injection-token"></a>

### 'InjectionToken' objects

Dependency objects can be simple values like dates, numbers, and strings, or shapeless objects like arrays and functions.

Such objects don't have application interfaces and therefore aren't well represented by a class. They're better represented by a token that is both unique and symbolic, a JavaScript object that has a friendly name but won't conflict with another token that happens to have the same name.

`InjectionToken` has these characteristics. You encountered them twice in the _Hero of the Month_ example, in the _title_ value provider and in the _runnersUp_ factory provider.

```ts
{ provide: TITLE,         useValue:   'Hero of the Month' },
{ provide: RUNNERS_UP,    useFactory:  runnersUpFactory(2), deps: [Hero, HeroService] }
```

You created the `TITLE` token like this:

```ts
import { InjectionToken } from '@angular/core';

export const TITLE = new InjectionToken<string>('title');
```

The type parameter, while optional, conveys the dependency's type to developers and tooling. The token description is another developer aid.

<a id="di-inheritance"></a>

## Inject into a derived class

Take care when writing a component that inherits from another component. If the base component has injected dependencies, you must re-provide and re-inject them in the derived class and then pass them down to the base class through the constructor.

In this contrived example, `SortedHeroesComponent` inherits from `HeroesBaseComponent` to display a _sorted_ list of heroes.

![Sorted Heroes](sorted-heroes.png)

The `HeroesBaseComponent` can stand on its own. It demands its own instance of `HeroService` to get heroes and displays them in the order they arrive from the database.

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

    ### Keep constructors simple

    Constructors should do little more than initialize variables. This rule makes the component safe to construct under test without fear that it will do something dramatic like talk to the server. That's why you call the `HeroService` from within the `ngOnInit` rather than the constructor.

Users want to see the heroes in alphabetical order. Rather than modify the original component, subclass it and create a `SortedHeroesComponent` that sorts the heroes before presenting them. The `SortedHeroesComponent` lets the base class fetch the heroes.

Unfortunately, Angular cannot inject the `HeroService` directly into the base class. You must provide the `HeroService` again for _this_ component, then pass it down to the base class inside the constructor.

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

Now take notice of the `afterGetHeroes()` method. Your first instinct might have been to create an `ngOnInit` method in `SortedHeroesComponent` and do the sorting there. But Angular calls the _derived_ class's `ngOnInit` _before_ calling the base class's `ngOnInit` so you'd be sorting the heroes array _before they arrived_. That produces a nasty error.

Overriding the base class's `afterGetHeroes()` method solves the problem.

These complications argue for _avoiding component inheritance_.

<a id="forwardref"></a>

## Resolve circular dependencies with a forward class reference (_forwardRef_)

The order of class declaration matters in TypeScript. You can't refer directly to a class until it's been defined.

This isn't usually a problem, especially if you adhere to the recommended _one class per file_ rule. But sometimes circular references are unavoidable. For example, when class 'A' refers to class 'B' and 'B' refers to 'A'. One of them has to be defined first.

The Angular `forwardRef()` function creates an _indirect_ reference that Angular can resolve later.

The _Parent Finder_ sample is full of circular class references that are impossible to break.

You face this dilemma when a class makes _a reference to itself_ as does `AlexComponent` in its `providers` array. The `providers` array is a property of the `@Component()` decorator function which must appear _above_ the class definition.

Break the circularity with `forwardRef`.

```ts
providers: [{ provide: Parent, useExisting: forwardRef(() => AlexComponent) }],
```

## Ссылки

-   [Dependency injection in action](https://angular.io/guide/dependency-injection-in-action)
