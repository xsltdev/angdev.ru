---
description: С первых дней своего существования Angular Router всегда был тесно связан с NgModules. Поэтому при переходе на автономные компоненты возникает один вопрос — Как будут работать маршрутизация и ленивая загрузка без NgModules? В этой главе мы дадим ответы, а также покажем, почему маршрутизатор станет более важным для Dependency Injection
---

# API для маршрутизации и ленивой загрузки

<big>С первых дней своего существования Angular Router всегда был тесно связан с NgModules. Поэтому при переходе на автономные компоненты возникает один вопрос: Как будут работать маршрутизация и ленивая загрузка без NgModules? В этой главе мы дадим ответы, а также покажем, почему маршрутизатор станет более важным для Dependency Injection.</big>

!!!note "Исходный код"

    **Исходный код** для примеров, используемых здесь, можно найти в виде традиционного [Angular CLI workspace](https://github.com/manfredsteyer/standalone-example-cli) и в виде [Nx workspace](https://github.com/manfredsteyer/standalone-example-nx), который использует библиотеки в качестве замены NgModules.

## Предоставление конфигурации маршрутизации {#leanpub-auto-providing-the-routing-configuration}

При загрузке отдельного компонента мы можем предоставить сервисы для корневой области видимости. Это сервисы, которые вы использовали в вашем `AppModule`. Тем временем Router предоставляет функцию `provideRouter`, которая возвращает всех провайдеров, которых нам нужно зарегистрировать здесь:

```ts title="main.ts"
import { importProvidersFrom } from '@angular/core';
import { bootstrapApplication } from '@angular/platform-browser';
import {
    PreloadAllModules,
    provideRouter,
    withDebugTracing,
    withPreloading,
    withRouterConfig,
} from '@angular/router';

import { APP_ROUTES } from './app/app.routes';
/* ... */

bootstrapApplication(AppComponent, {
    providers: [
        importProvidersFrom(HttpClientModule),
        provideRouter(
            APP_ROUTES,
            withPreloading(PreloadAllModules),
            withDebugTracing()
        ),

        /* ... */

        importProvidersFrom(TicketsModule),
        provideAnimations(),
        importProvidersFrom(LayoutModule),
    ],
});
```

Функция `provideRouter` принимает не только корневые маршруты, но и реализацию дополнительных возможностей маршрутизатора. Эти возможности передаются с помощью функций, имеющих шаблон именования `withXYZ`, например `withPreloading` или `withDebugTracing`. Так как функции могут быть легко перелицованы, это дизайнерское решение делает весь маршрутизатор более перелицованным.

> Вместе с рассмотренными функциями команда Angular также вводит шаблон именования, которому должны следовать авторы библиотек. Таким образом, при добавлении новой библиотеки нам просто нужно обратить внимание на `provideXYZ` и некоторые необязательные функции `withXYZ`.

Поскольку в настоящее время не все библиотеки поставляются с функцией `provideXYZ`, Angular поставляется с промежуточной функцией `importProvidersFrom`. Она позволяет получить все провайдеры, определенные в существующих `NgModules`, и, следовательно, является ключом для их использования в автономных компонентах.

Я уверен, что использование `importProvidersFrom` со временем достигнет пика, так как все больше и больше библиотек будут предоставлять функции для непосредственной настройки своих провайдеров. Например, в NGRX недавно появились функции `provideStore` и `provideEffects`.

## Использование директив маршрутизатора {#leanpub-auto-using-router-directives}

После настройки маршрутов нам также необходимо определить место, где Router будет отображать активированный компонент и ссылки для переключения между ними. Чтобы получить необходимые для этого директивы, вы можете напрямую импортировать модуль RouterModule в свой отдельный компонент. Однако лучшей альтернативой будет просто импортировать нужные вам директивы:

```ts
@Component({
    standalone: true,
    selector: 'app-root',
    imports: [
        // Just import the RouterModule:
        // RouterModule,

        // Better: Just import what you need:
        RouterOutlet,
        RouterLinkWithHref, // Angular 14
        // RouterLink // Angular 15+

        NavbarComponent,
        SidebarComponent,
    ],
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css'],
})
export class AppComponent {
    /* ... */
}
```

Можно импортировать только действительно необходимые директивы, поскольку маршрутизатор предоставляет их в виде автономных директив. Обратите внимание, что в Angular 14 директива `RouterLinkWithHref` необходима, если вы используете `routerLink` с `a`-тегом; во всех остальных случаях вы должны импортировать `RouterLink` вместо нее. Поскольку это немного запутывает, команда Angular Team рефакторизовала это для Angular 15: начиная с этой версии, `RouterLink` используется во всех случаях.

В большинстве случаев нам не нужно беспокоиться об этом, когда IDE начнут предоставлять автоимпорты для автономных компонентов.

## Ленивая загрузка с автономными компонентами {#leanpub-auto-lazy-loading-with-standalone-components}

Раньше ленивый маршрут указывал на `NgModule` с дочерними маршрутами. Поскольку больше нет `NgModules`, `loadChildren` теперь может напрямую указывать на конфигурацию ленивой маршрутизации:

```ts title="app.routes.ts"
import { Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';

export const APP_ROUTES: Routes = [
    {
        path: '',
        pathMatch: 'full',
        redirectTo: 'home',
    },
    {
        path: 'home',
        component: HomeComponent,
    },

    // Option 1: Lazy Loading another Routing Config
    {
        path: 'flight-booking',
        loadChildren: () =>
            import('./booking/flight-booking.routes').then(
                (m) => m.FLIGHT_BOOKING_ROUTES
            ),
    },

    // Option 2: Directly Lazy Loading a Standalone Component
    {
        path: 'next-flight',
        loadComponent: () =>
            import(
                './next-flight/next-flight.component'
            ).then((m) => m.NextFlightComponent),
    },
    /* ... */
];
```

Это устраняет непрямую связь через `NgModule` и делает наш код более явным. В качестве альтернативы ленивый маршрут может напрямую указывать на отдельный компонент. Для этого используется показанное выше свойство `loadComponent`.

Я ожидаю, что большинство команд предпочтут первый вариант, потому что обычно приложению требуется ленивая загрузка нескольких маршрутов, которые идут вместе.

## Инжекторы среды: Сервисы для конкретных маршрутов {#leanpub-auto-environment-injectors-services-for-specific-routes}

С `NgModule` каждый ленивый модуль представлял новый инжектор и, следовательно, новую область инжекции. Эта область использовалась для предоставления сервисов, необходимых только соответствующему ленивому модулю.

Чтобы покрыть такие случаи использования, Router теперь позволяет вводить провайдеров для каждого маршрута. Эти сервисы могут использоваться как самим маршрутом, так и его дочерними маршрутами:

```ts title="booking/flight-booking.routes.ts"
export const FLIGHT_BOOKING_ROUTES: Routes = [
    {
        path: '',
        component: FlightBookingComponent,
        providers: [provideBookingDomain(config)],
        children: [
            {
                path: '',
                pathMatch: 'full',
                redirectTo: 'flight-search',
            },
            {
                path: 'flight-search',
                component: FlightSearchComponent,
            },
            {
                path: 'passenger-search',
                component: PassengerSearchComponent,
            },
            {
                path: 'flight-edit/:id',
                component: FlightEditComponent,
            },
        ],
    },
];
```

Как показано здесь, мы можем предоставлять услуги для нескольких маршрутов, группируя их в дочерние маршруты. В этих случаях используется родительский маршрут без компонентов с пустым путем (`path: ''`). Этот паттерн уже много лет используется для назначения гвардейцев группе маршрутов.

Технически, добавление массива `providers` в конфигурацию маршрутизатора вводит новый инжектор на уровне маршрута. Такой инжектор называется Environment Injector и заменяет собой концепцию прежних (Ng)Module Injectors. Корневой инжектор и инжектор платформы также являются инжекторами окружения.

Интересно, что это также избавляет ленивую загрузку от необходимости вводить дополнительные области инъекций. Раньше каждый **ленивый** `NgModule` вводил новую область инжекции, а **неленивый** `NgModule` никогда этого не делал. Теперь ленивая загрузка сама по себе не влияет на диапазоны. Вместо этого, теперь вы определяете новые области, добавляя массив `providers` к вашим маршрутам, **независимо** от того, является ли маршрут ленивым или нет.

Команда Angular рекомендует использовать этот массив провайдеров с осторожностью и **предпочитать** `providedIn: 'root'` вместо него. Как уже упоминалось в предыдущей главе, `providedIn: 'root'` также позволяет ленивую загрузку. Если вы просто используете сервисы, предоставленные с помощью `providedIn: 'root'`, в ленивых частях вашего приложения, они будут загружаться только вместе с ними.

Однако есть одна ситуация, когда `providedIn: 'root'` не работает, и поэтому показанный массив провайдеров необходим, а именно, если вам нужно передать конфигурацию библиотеке. Я уже показал это в примере выше, передав объект конфигурации моей пользовательской `provideBookingDomain`. В следующем разделе приводится более подробный пример с использованием NGRX.

## Настройка NGRX и Feature Slices {#leanpub-auto-setting-up-ngrx-and-feature-slices}

Чтобы проиллюстрировать использование библиотек, принятых для автономных компонентов с ленивой загрузкой, давайте посмотрим, как настроить NGRX. Начнем с предоставления необходимых глобальных сервисов:

```ts
import { bootstrapApplication } from '@angular/platform-browser';

import { provideStore } from '@ngrx/store';
import { provideEffects } from '@ngrx/effects';
import { provideStoreDevtools } from '@ngrx/store-devtools';

import { reducer } from './app/+state';

/* ... */

bootstrapApplication(AppComponent, {
    providers: [
        importProvidersFrom(HttpClientModule),
        provideRouter(
            APP_ROUTES,
            withPreloading(PreloadAllModules),
            withDebugTracing()
        ),

        // Setup NGRX:
        provideStore(reducer),
        provideEffects([]),
        provideStoreDevtools(),

        importProvidersFrom(TicketsModule),
        provideAnimations(),
        importProvidersFrom(LayoutModule),
    ],
});
```

Для этого мы используем функции `provideStore`, `provideEffects` и `provideStoreDevtools`, которыми NGRX комплектуется с версии `14.3`.

Чтобы позволить "ленивым" частям приложения иметь свои собственные срезы функций, мы вызываем `provideState` и `provideEffects` в соответствующей конфигурации маршрутизации:

```ts
import { provideEffects } from '@ngrx/effects';
import { provideState } from '@ngrx/store';

export const FLIGHT_BOOKING_ROUTES: Routes = [
    {
        path: '',
        component: FlightBookingComponent,
        providers: [
            provideState(bookingFeature),
            provideEffects([BookingEffects]),
        ],
        children: [
            {
                path: 'flight-search',
                component: FlightSearchComponent,
            },
            {
                path: 'passenger-search',
                component: PassengerSearchComponent,
            },
            {
                path: 'flight-edit/:id',
                component: FlightEditComponent,
            },
        ],
    },
];
```

В то время как `provideStore` устанавливает хранилище на корневом уровне, `provideState` устанавливает дополнительные фрагменты функций. Для этого вы можете предоставить функцию или просто имя ветки с редуктором. Интересно, что функция `provideEffects` используется не только на корневом уровне, но и на уровне ленивых частей. Таким образом, она предоставляет начальные эффекты, а также эффекты, необходимые для данного фрагмента функции.

## Настройка окружения: ENVIRONMENT_INITIALIZER {#leanpub-auto-setting-up-your-environment-environmentinitializer}

Некоторые библиотеки использовали конструктор ленивого `NgModule` для своей инициализации. Для дальнейшей поддержки этого подхода без `NgModule` существует концепция `ENVIRONMENT_INITIALIZER`:

```ts
export const FLIGHT_BOOKING_ROUTES: Routes = [
    {
        path: '',
        component: FlightBookingComponent,
        providers: [
            importProvidersFrom(
                StoreModule.forFeature(bookingFeature)
            ),
            importProvidersFrom(
                EffectsModule.forFeature([BookingEffects])
            ),
            {
                provide: ENVIRONMENT_INITIALIZER,
                multi: true,
                useValue: () => inject(InitService).init(),
            },
        ],
        children: [
            /* ... */
        ],
    },
];
```

По сути, `ENVIRONMENT_INITIALIZER` предоставляет функцию, выполняемую при инициализации инжектора окружения. Флаг `multi: true` уже указывает на то, что вы можете иметь несколько таких инициализаторов в одной области видимости.

## Привязки компонентного ввода {#leanpub-auto-component-input-bindings}

Маршрутизатор также получил несколько приятных дополнений. Например, теперь ему можно поручить передавать параметры маршрутизации непосредственно на входы соответствующего компонента. Например, если маршрут вызывается с `;q=Graz`, маршрутизатор присваивает значение `Graz` входу с именем `q`:

```ts
@Input ( ) q = '' ;
```

Получение значений параметров через сервис `ActivatedRoute` больше не требуется. Такое поведение применяется к параметрам в объекте `data`, в строке запроса, а также к матричным параметрам, которые обычно используются в Angular. В случае конфликта также применяется такой порядок, например, если значение присутствует, то оно берется из объекта `data`, в противном случае проверяется строка запроса, а затем параметры матрицы. Чтобы не нарушать существующий код, эта опция должна быть явно активирована. Для этого при вызове `provideRouter` используется функция `withComponentInputBinding`:

```ts
provideRouter(
  APP_ROUTES,
  withComponentInputBinding()
),
```

Кроме того, у маршрутизатора теперь есть свойство `lastSuccessfulNavigation`, которое предоставляет информацию о текущем маршруте:

```ts
router = inject(Router);
/* … */
console.log(
    'lastSuccessfullNavigation',
    this.router.lastSuccessfulNavigation
);
```

## Заключение {#leanpub-auto-conclusion-2}

Усовершенствованный API маршрутизатора устраняет ненужные перенаправления для ленивой загрузки: Вместо того чтобы указывать на ленивый NgModule, конфигурация маршрутизации теперь напрямую указывает на другую конфигурацию ленивой маршрутизации. Провайдеры, которые мы раньше регистрировали в ленивых NgModules, например, провайдеры для среза функций, напрямую добавляются в соответствующий маршрут и могут быть использованы в каждом дочернем маршруте.
