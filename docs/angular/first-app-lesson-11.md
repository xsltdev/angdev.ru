# Урок 11 - Интеграция страницы подробностей в приложение

Этот урок демонстрирует, как подключить страницу подробностей к вашему приложению.

**Затраты времени:** ожидайте, что на выполнение этого урока вы потратите около 20 минут.

## Перед началом

Этот урок начинается с кода из предыдущего урока, поэтому вы можете:

-   Использовать код, созданный в Уроке 10, в своей интегрированной среде разработки (IDE).

-   Начните с примера кода из предыдущего урока. Выберите <live-example name="first-app-lesson-10"></live-example> из Урока 10, где вы можете:

    -   Использовать _живой пример_ в StackBlitz, где интерфейс StackBlitz является вашей IDE.

    -   Использовать _download пример_ и открыть его в вашей IDE.

Если вы не просмотрели введение, посетите [Введение в Angular tutorial](first-app.md), чтобы убедиться, что у вас есть все необходимое для завершения этого урока.

Если у вас возникнут трудности во время этого урока, вы можете просмотреть готовый код для этого урока в <live-example></live-example> для этого урока.

## После завершения

По окончании этого урока ваше приложение будет поддерживать маршрутизацию на страницу подробностей.

## Концептуальный предварительный просмотр маршрутизации с параметрами маршрута

В предыдущем уроке вы добавили маршрутизацию в ваше приложение, а в этом уроке вы расширите типы маршрутизации, которые поддерживает ваше приложение. Каждое местоположение жилья имеет определенные детали, которые должны отображаться, когда пользователь переходит на страницу подробностей для этого элемента. Для достижения этой цели вам потребуется использовать параметры маршрута.

Параметры маршрута позволяют включать динамическую информацию в URL-адрес маршрута. Чтобы определить, на какое жилье кликнул пользователь, вы будете использовать свойство `id` типа `HousingLocation`.

## Шаги урока

Выполните эти шаги над кодом приложения в вашей IDE.

### Шаг 1 - Создайте новую службу для вашего приложения.

В уроке 10 вы добавили второй маршрут в `src/app/routes.ts`, этот маршрут включает специальный сегмент, который идентифицирует параметр маршрута, `id`:

    <code-example format="javascript" language="javascript">
     'details/:id'
    </code-example>

В этом случае `:id` является динамическим и будет изменяться в зависимости от того, как маршрут запрашивается кодом.

1.  В `src/app/housing-location/housing-location.component.ts` добавьте тег якоря к элементу `section` и включите директиву `routerLink`:

    <code-example header="Add anchor with a routerLink directive to housing-location.component.ts" path="first-app-lesson-11/src/app/housing-location/housing-location.component.ts" region="add-router-link"></code-example>.

    Директива `routerLink` позволяет маршрутизатору Angular создавать динамические ссылки в приложении. Значение, присваиваемое директиве `routerLink`, представляет собой массив с двумя элементами: статической частью пути и динамическими данными.

    Чтобы routerLink работал в шаблоне, добавьте импорт RouterLink и RouterOutlet на уровне файла из '@angular/router', затем обновите массив импорта компонентов, чтобы включить в него RouterLink и RouterOutlet.

1.  На этом этапе вы можете убедиться, что маршрутизация работает в вашем приложении. В браузере обновите домашнюю страницу и нажмите кнопку "Узнать больше", чтобы узнать местоположение жилья.

<section class="lightbox">
 <img alt="details page displaying the text 'details works!'" src="generated/images/guide/faa/homes-app-lesson-11-step-1.png">
</section>

### Шаг 2 - Получение параметров маршрута

На этом шаге вы получите параметры маршрута в `DetailsComponent`. В настоящее время приложение отображает `details works!`, далее вы обновите код для отображения значения `id`, переданного с помощью параметров маршрута.

1.  В `src/app/details/details.component.ts` обновите шаблон, чтобы импортировать функции, классы и сервисы, которые вам нужно будет использовать в `DetailsComponent`:

    <code-example header="Update file level imports" path="first-app-lesson-11/src/app/details/details.component.ts" region="import-resources-for-details"></code-example>.

1.  Обновите свойство `template` декоратора `@Component` для отображения значения `housingLocationId`:

<code-example format="javascript" language="javascript">
   template: `&lt;p&gt;details works! {{ housingLocationId }}&lt;/p&gt;`,
</code-example>

1.  Обновите тело `DetailsComponent` следующим кодом:

    <code-example format="javascript" language="javascript">

        export class DetailsComponent {

            маршрут: ActivatedRoute = inject(ActivatedRoute);

            housingLocationId = -1;

            constructor() {

                this.housingLocationId = Number(this.route.snapshot.params['id']);

            }

        }

    </code-example>

    Этот код предоставляет `DetailsComponent` доступ к функции маршрутизатора `ActivatedRoute`, которая позволяет получить доступ к данным о текущем маршруте. В конструкторе код преобразует параметр id из маршрута в число.

1.  Сохраните все изменения.

1.  В браузере щелкните по одной из ссылок "Узнать больше" на местоположение жилья и убедитесь, что числовое значение, отображаемое на странице, совпадает со свойством `id` для этого места в данных.

### Шаг 3 - Настройка компонента `DetailComponent`.

Теперь, когда маршрутизация работает должным образом в приложении, самое время обновить шаблон компонента `DetailsComponent` для отображения конкретных данных, представленных местоположением жилья для параметра маршрута.

Для доступа к данным вы добавите вызов к `HousingService`.

1.  Обновите код шаблона, чтобы он соответствовал следующему коду:

    <code-example header="Update the DetailsComponent template in src/app/details/details.component.ts" path="first-app-lesson-11/src/app/details/details.component.ts" region="update-details-template"></code-example>.

    Обратите внимание, что доступ к свойствам `housingLocation` осуществляется с помощью необязательного оператора цепочки `?`. Это гарантирует, что если значение `housingLocation` будет равно null или неопределено, приложение не упадет.

1.  Обновите тело класса `DetailsComponent`, чтобы оно соответствовало следующему коду:

    <code-example header="Update the DetailsComponent class in src/app/details/details.component.ts" path="first-app-lesson-11/src/app/details/details.component.ts" region="get-housing-details"></code-example>.

    Теперь компонент имеет код для отображения правильной информации в зависимости от выбранного местоположения жилья. Теперь конструктор включает вызов `HousingService` для передачи параметра route в качестве аргумента функции сервиса `getHousingLocationById`.

1.  Скопируйте следующие стили в файл `src/app/details/details.component.css`:

    <code-example header="Add styles for the DetailsComponent" path="first-app-lesson-11/src/app/details/details.component.css" region="add-details-styles"></code-example>.

1.  Сохраните изменения.

1.  В браузере обновите страницу и подтвердите, что при нажатии на ссылку "Узнать больше" для данного жилья на странице подробностей отображается правильная информация, основанная на данных для выбранного элемента.

    <section class="lightbox">

    <img alt="Страница подробной информации о доме" src="generated/images/guide/faa/homes-app-lesson-11-step-3.png">

    </section>

### Шаг 4 - Добавление навигации в `HomeComponent`.

В предыдущем уроке вы обновили шаблон `AppComponent`, чтобы включить в него `routerLink`. Добавление этого кода обновило ваше приложение, чтобы включить навигацию обратно к `Домашнему компоненту` при нажатии на логотип.

1.  Убедитесь, что ваш код соответствует следующему:

    <code-example header="Add routerLink to AppComponent" path="first-app-lesson-11/src/app/app.component.ts" region="add-router-link-to-header"></code-example>.

    Возможно, ваш код уже актуален, но для уверенности подтвердите его.

## Обзор урока

В этом уроке вы обновили свое приложение, чтобы:

-   использовать параметры маршрута для передачи данных в маршрут

-   использовать директиву `routerLink` для использования динамических данных при создании маршрута

-   использовать параметр маршрута для получения данных из `HousingService` для отображения информации о местоположении жилья.

До сих пор это была отличная работа.

Если у вас возникли трудности с этим уроком, вы можете просмотреть готовый код в <live-example></live-example>.

## Следующие шаги

-   [Урок 12 - Добавление форм в ваше приложение Angular](first-app-lesson-12.md)

## Дополнительная информация

Для получения дополнительной информации о темах, рассмотренных в этом уроке, посетите:

<!-- vale Angular.Google_WordListSuggestions = NO -->

-   [Параметры маршрута](router.md#accessing-query-parameters-and-fragments)
-   [Обзор маршрутизации в Angular](routing-overview.md)

-   [Общие задачи маршрутизации](router.md)

-   [Дополнительный оператор цепочки](https://developer.mozilla.org/ru/docs/Web/JavaScript/Reference/Operators/Optional_chaining)
