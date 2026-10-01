---
description: Этот урок демонстрирует, как подключить страницу подробностей к вашему приложению
---

# Урок 11: Интеграция страницы подробностей в приложение

Этот урок демонстрирует, как подключить страницу подробностей к вашему приложению.

**Затраты времени:** ожидайте, что на выполнение этого урока вы потратите около 20 минут.

## Перед началом

Этот урок начинается с кода из предыдущего урока, поэтому вы можете:

-   Использовать код, созданный в Уроке 10, в своей интегрированной среде разработки (IDE).

-   Начните с примера кода из предыдущего урока. Выберите код из Урока 10, где вы можете:

    -   Использовать [живой пример](https://angular.io/generated/live-examples/first-app-lesson-10/stackblitz.html) в StackBlitz, где интерфейс StackBlitz является вашей IDE.

    -   Использовать [download пример](https://angular.io/generated/zips/first-app-lesson-10/first-app-lesson-10.zip) и открыть его в вашей IDE.

Если вы не просмотрели введение, посетите [Введение в Angular tutorial](first-app.md), чтобы убедиться, что у вас есть все необходимое для завершения этого урока.

Если у вас возникнут трудности во время этого урока, вы можете просмотреть [готовый код](https://angular.io/generated/live-examples/first-app-lesson-11/stackblitz.html) для этого урока.

## После завершения

По окончании этого урока ваше приложение будет поддерживать маршрутизацию на страницу подробностей.

## Концептуальный предварительный просмотр маршрутизации с параметрами маршрута

В предыдущем уроке вы добавили маршрутизацию в ваше приложение, а в этом уроке вы расширите типы маршрутизации, которые поддерживает ваше приложение. Каждое местоположение жилья имеет определенные детали, которые должны отображаться, когда пользователь переходит на страницу подробностей для этого элемента. Для достижения этой цели вам потребуется использовать параметры маршрута.

Параметры маршрута позволяют включать динамическую информацию в URL-адрес маршрута. Чтобы определить, на какое жилье кликнул пользователь, вы будете использовать свойство `id` типа `HousingLocation`.

## Шаги урока

Выполните эти шаги над кодом приложения в вашей IDE.

### Шаг 1 — Создайте новую службу для вашего приложения

В уроке 10 вы добавили второй маршрут в `src/app/routes.ts`, этот маршрут включает специальный сегмент, который идентифицирует параметр маршрута, `id`:

```js
'details/:id';

```

В этом случае `:id` является динамическим и будет изменяться в зависимости от того, как маршрут запрашивается кодом.

1.  В `src/app/housing-location/housing-location.component.ts` добавьте тег якоря к элементу `section` и включите директиву `routerLink`:

    ```ts
    template: `
    <section class="listing">
    	<img class="listing-photo" [src]="housingLocation.photo" alt="Exterior photo of {{housingLocation.name}}">
    	<h2 class="listing-heading">{{ housingLocation.name }}</h2>
    	<p class="listing-location">{{ housingLocation.city}}, {{housingLocation.state }}</p>
    	<a [routerLink]="['/details', housingLocation.id]">Learn More</a>
    </section>
    `,
    ```

    Директива `routerLink` позволяет маршрутизатору Angular создавать динамические ссылки в приложении. Значение, присваиваемое директиве `routerLink`, представляет собой массив с двумя элементами: статической частью пути и динамическими данными.

    Чтобы routerLink работал в шаблоне, добавьте импорт RouterLink и RouterOutlet на уровне файла из '@angular/router', затем обновите массив импорта компонентов, чтобы включить в него RouterLink и RouterOutlet.

2.  На этом этапе вы можете убедиться, что маршрутизация работает в вашем приложении. В браузере обновите домашнюю страницу и нажмите кнопку "Узнать больше", чтобы узнать местоположение жилья.

    ![details page displaying the text 'details works!'](homes-app-lesson-11-step-1.png)

### Шаг 2 — Получение параметров маршрута

На этом шаге вы получите параметры маршрута в `DetailsComponent`. В настоящее время приложение отображает `details works!`, далее вы обновите код для отображения значения `id`, переданного с помощью параметров маршрута.

1.  В `src/app/details/details.component.ts` обновите шаблон, чтобы импортировать функции, классы и сервисы, которые вам нужно будет использовать в `DetailsComponent`:

    ```ts
    import { Component, inject } from '@angular/core';
    import { CommonModule } from '@angular/common';
    import { ActivatedRoute } from '@angular/router';
    import { HousingService } from '../housing.service';
    import { HousingLocation } from '../housinglocation';
    ```

2.  Обновите свойство `template` декоратора `@Component` для отображения значения `housingLocationId`:

    ```js
    template: `<p>details works! {{ housingLocationId }}</p>`,
    ```

3.  Обновите тело `DetailsComponent` следующим кодом:

    ```js
    export class DetailsComponent {
        route: ActivatedRoute = inject(ActivatedRoute);
        housingLocationId = -1;
        constructor() {
            this.housingLocationId = Number(
                this.route.snapshot.params['id']
            );
        }
    }
    ```

    Этот код предоставляет `DetailsComponent` доступ к функции маршрутизатора `ActivatedRoute`, которая позволяет получить доступ к данным о текущем маршруте. В конструкторе код преобразует параметр id из маршрута в число.

4.  Сохраните все изменения.

5.  В браузере щелкните по одной из ссылок "Узнать больше" на местоположение жилья и убедитесь, что числовое значение, отображаемое на странице, совпадает со свойством `id` для этого места в данных.

### Шаг 3 — Настройка компонента `DetailComponent`

Теперь, когда маршрутизация работает должным образом в приложении, самое время обновить шаблон компонента `DetailsComponent` для отображения конкретных данных, представленных местоположением жилья для параметра маршрута.

Для доступа к данным вы добавите вызов к `HousingService`.

1.  Обновите код шаблона, чтобы он соответствовал следующему коду:

    ```ts
    template: `
    <article>
    	<img class="listing-photo" [src]="housingLocation?.photo"
    	alt="Exterior photo of {{housingLocation?.name}}"/>
    	<section class="listing-description">
    	<h2 class="listing-heading">{{housingLocation?.name}}</h2>
    	<p class="listing-location">{{housingLocation?.city}}, {{housingLocation?.state}}</p>
    	</section>
    	<section class="listing-features">
    	<h2 class="section-heading">About this housing location</h2>
    	<ul>
    		<li>Units available: {{housingLocation?.availableUnits}}</li>
    		<li>Does this location have wifi: {{housingLocation?.wifi}}</li>
    		<li>Does this location have laundry: {{housingLocation?.laundry}}</li>
    	</ul>
    	</section>
    </article>
    `,
    ```

    Обратите внимание, что доступ к свойствам `housingLocation` осуществляется с помощью необязательного оператора цепочки `?`. Это гарантирует, что если значение `housingLocation` будет равно null или неопределено, приложение не упадет.

2.  Обновите тело класса `DetailsComponent`, чтобы оно соответствовало следующему коду:

    ```ts
    export class DetailsComponent {
        route: ActivatedRoute = inject(ActivatedRoute);
        housingService = inject(HousingService);
        housingLocation: HousingLocation | undefined;

        constructor() {
            const housingLocationId = Number(
                this.route.snapshot.params['id']
            );
            this.housingLocation = this.housingService.getHousingLocationById(
                housingLocationId
            );
        }
    }
    ```

    Теперь компонент имеет код для отображения правильной информации в зависимости от выбранного местоположения жилья. Теперь конструктор включает вызов `HousingService` для передачи параметра route в качестве аргумента функции сервиса `getHousingLocationById`.

3.  Скопируйте следующие стили в файл `src/app/details/details.component.css`:

    ```css
    .listing-photo {
        height: 600px;
        width: 50%;
        object-fit: cover;
        border-radius: 30px;
        float: right;
    }

    .listing-heading {
        font-size: 48pt;
        font-weight: bold;
        margin-bottom: 15px;
    }

    .listing-location::before {
        content: url('/assets/location-pin.svg') / '';
    }

    .listing-location {
        font-size: 24pt;
        margin-bottom: 15px;
    }

    .listing-features > .section-heading {
        color: var(--secondary-color);
        font-size: 24pt;
        margin-bottom: 15px;
    }

    .listing-features {
        margin-bottom: 20px;
    }

    .listing-features li {
        font-size: 14pt;
    }

    li {
        list-style-type: none;
    }

    .listing-apply .section-heading {
        font-size: 18pt;
        margin-bottom: 15px;
    }

    label,
    input {
        display: block;
    }
    label {
        color: var(--secondary-color);
        font-weight: bold;
        text-transform: uppercase;
        font-size: 12pt;
    }
    input {
        font-size: 16pt;
        margin-bottom: 15px;
        padding: 10px;
        width: 400px;
        border-top: none;
        border-right: none;
        border-left: none;
        border-bottom: solid 0.3px;
    }
    @media (max-width: 1024px) {
        .listing-photo {
            width: 100%;
            height: 400px;
        }
    }
    ```

4.  Сохраните изменения.

5.  В браузере обновите страницу и подтвердите, что при нажатии на ссылку "Узнать больше" для данного жилья на странице подробностей отображается правильная информация, основанная на данных для выбранного элемента.

    ![Страница подробной информации о доме](homes-app-lesson-11-step-3.png)

### Шаг 4 — Добавление навигации в `HomeComponent`

В предыдущем уроке вы обновили шаблон `AppComponent`, чтобы включить в него `routerLink`. Добавление этого кода обновило ваше приложение, чтобы включить навигацию обратно к `Домашнему компоненту` при нажатии на логотип.

1.  Убедитесь, что ваш код соответствует следующему:

    ```ts
    template: `
    <main>
    	<a [routerLink]="['/']">
    	<header class="brand-name">
    		<img class="brand-logo" src="/assets/logo.svg" alt="logo" aria-hidden="true">
    	</header>
    	</a>
    	<section class="content">
    	<router-outlet></router-outlet>
    	</section>
    </main>
    `,
    ```

    Возможно, ваш код уже актуален, но для уверенности подтвердите его.

## Обзор урока

В этом уроке вы обновили свое приложение, чтобы:

-   использовать параметры маршрута для передачи данных в маршрут

-   использовать директиву `routerLink` для использования динамических данных при создании маршрута

-   использовать параметр маршрута для получения данных из `HousingService` для отображения информации о местоположении жилья.

До сих пор это была отличная работа.

Если у вас возникли трудности с этим уроком, вы можете просмотреть [готовый код](https://angular.io/generated/live-examples/first-app-lesson-11/stackblitz.html).

## Следующие шаги

-   [Урок 12 — Добавление форм в ваше приложение Angular](first-app-lesson-12.md)

## Дополнительная информация

Для получения дополнительной информации о темах, рассмотренных в этом уроке, посетите:

-   [Параметры маршрута](router.md#accessing-query-parameters-and-fragments)
-   [Обзор маршрутизации в Angular](routing-overview.md)
-   [Общие задачи маршрутизации](router.md)
-   [Дополнительный оператор цепочки](https://developer.mozilla.org/ru/docs/Web/JavaScript/Reference/Operators/Optional_chaining)

## Ссылки

-   [Lesson 11 — Integrate details page into application](https://angular.io/tutorial/first-app/first-app-lesson-11)
