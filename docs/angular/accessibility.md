# Доступность в Angular

:date: 28.02.2022

Интернетом пользуются самые разные люди, в том числе те, кто страдает нарушениями зрения или двигательных функций. Существует множество вспомогательных технологий, которые значительно облегчают этим группам людей взаимодействие с веб-приложениями.

Кроме того, разработка приложения для обеспечения его доступности в целом улучшает пользовательский опыт для всех пользователей.

Подробный обзор вопросов и методов разработки доступных приложений см. в разделе [Accessibility](https://developers.google.com/web/fundamentals/accessibility/#what_is_accessibility) раздела [Web Fundamentals](https://developers.google.com/web/fundamentals) Google.

На этой странице обсуждаются лучшие практики проектирования приложений Angular, которые хорошо работают для всех пользователей, включая тех, кто использует вспомогательные технологии.

!!!note ""

    Пример приложения, которое описывается на этой странице, см. в [примере](https://angular.io/generated/live-examples/accessibility/stackblitz.html).

## Атрибуты доступности

Создание доступного веб-опыта часто включает установку [Accessible Rich Internet Applications (ARIA) attributes](https://developers.google.com/web/fundamentals/accessibility/semantics-aria) для обеспечения семантического смысла там, где он может отсутствовать. Используйте синтаксис шаблона [привязка атрибутов](attribute-binding.md) для управления значениями атрибутов, связанных с доступностью.

При привязке к атрибутам ARIA в Angular вы должны использовать префикс `attr`. Спецификация ARIA зависит именно от атрибутов HTML, а не от свойств элементов DOM.

```html
<!-- Use attr. when binding to an ARIA attribute -->
<button [attr.aria-label]="myActionLabel">…</button>
```

!!!note ""

    Этот синтаксис необходим только для _привязок_ атрибутов. Статические атрибуты ARIA не требуют дополнительного синтаксиса.

    ```html
    <!-- Static ARIA attributes require no extra syntax -->
    <button aria-label="Save document">…</button>
    ```

!!!note ""

    По соглашению, атрибуты HTML используют имена в нижнем регистре (`tabindex`), в то время как свойства используют имена в camelCase (`tabIndex`).

    Подробнее о разнице между атрибутами и свойствами см. в руководстве [Binding syntax](binding-syntax.md#html-attribute-vs-dom-property).

## Компоненты пользовательского интерфейса Angular

Библиотека [Angular Material](https://material.angular.io), которая поддерживается командой Angular, представляет собой набор многократно используемых компонентов пользовательского интерфейса, целью которых является обеспечение полной доступности. В состав [Component Development Kit (CDK)](https://material.angular.io/cdk/categories) входит пакет `a11y`, который предоставляет инструменты для поддержки различных областей доступности.

Например:

-   `LiveAnnouncer` используется для объявления сообщений для пользователей считывающих экранов, использующих область `aria-live`.

    Более подробную информацию о [aria-live regions](https://www.w3.org/WAI/PF/aria-1.1/states_and_properties#aria-live) смотрите в документации W3C.

-   Директива `cdkTrapFocus` отлавливает фокус клавиши Tab внутри элемента.

    Используйте ее для создания доступного опыта для таких компонентов, как модальные диалоги, где фокус должен быть ограничен.

Подробную информацию об этих и других инструментах см. в [Angular CDK accessibility overview](https://material.angular.io/cdk/a11y/overview).

### Расширение нативных элементов

Родные элементы HTML отражают несколько стандартных моделей взаимодействия, которые важны для доступности. При создании компонентов Angular следует по возможности использовать эти родные элементы напрямую, а не переделывать хорошо поддерживаемые модели поведения.

Например, вместо того чтобы создавать собственный элемент для новой разновидности кнопки, создайте компонент, который использует селектор атрибутов с родным элементом `button`. Чаще всего это относится к `button` и `a`, но может быть использовано и со многими другими типами элементов.

Вы можете увидеть примеры этого паттерна в Angular Material: [`MatButton`](https://github.com/angular/components/blob/50d3f29b6dc717b512dbd0234ce76f4ab7e9762a/src/material/button/button.ts#L67-L69), [`MatTabNav`](https://github.com/angular/components/blob/50d3f29b6dc717b512dbd0234ce76f4ab7e9762a/src/material/tabs/tab-nav-bar/tab-nav-bar.ts#L139), и [`MatTable`](https://github.com/angular/components/blob/50d3f29b6dc717b512dbd0234ce76f4ab7e9762a/src/material/table/table.ts#L22).

### Использование контейнеров для собственных элементов

Иногда для использования соответствующего собственного элемента требуется элемент-контейнер. Например, родной элемент `input` не может иметь дочерних элементов, поэтому любые пользовательские компоненты ввода текста должны обернуть `input` дополнительными элементами.

Просто включив `input` в шаблон вашего пользовательского компонента, пользователи компонента не смогут задать произвольные свойства и атрибуты элементу `input`.

Вместо этого создайте компонент-контейнер, который использует проекцию содержимого для включения собственного элемента управления в API компонента.

Примером такого паттерна может служить [`MatFormField`](https://material.angular.io/components/form-field/overview).

## Тематическое исследование: Создание пользовательского индикатора выполнения

Следующий пример показывает, как сделать прогресс-бар доступным, используя привязку к хосту для управления атрибутами, связанными с доступностью.

-   Компонент определяет элемент `accessibility-enabled` со стандартным HTML атрибутом `role` и ARIA атрибутами.

    ARIA-атрибут `aria-valuenow` привязывается к вводу пользователя.

    ```ts
    import { Component, Input } from '@angular/core';

    /**
     * Example progressbar component.
     */
    @Component({
        selector: 'app-example-progressbar',
        template:
            '<div class="bar" [style.width.%]="value"></div>',
        styleUrls: ['./progress-bar.component.css'],
        host: {
            // Sets the role for this component to "progressbar"
            role: 'progressbar',

            // Sets the minimum and maximum values for the progressbar role.
            'aria-valuemin': '0',
            'aria-valuemax': '100',

            // Binding that updates the current value of the progressbar.
            '[attr.aria-valuenow]': 'value',
        },
    })
    export class ExampleProgressbarComponent {
        /** Current value of the progressbar. */
        @Input() value = 0;
    }
    ```

-   В шаблоне атрибут `aria-label` гарантирует, что элемент управления доступен для чтения с экрана.

    ```html
    <label>
        Enter an example progress value
        <input
            type="number"
            min="0"
            max="100"
            [value]="progress"
            (input)="setProgress($event)"
        />
    </label>

    <!-- The user of the progressbar sets an aria-label to communicate what the progress means. -->
    <app-example-progressbar
        [value]="progress"
        aria-label="Example of a progress bar"
    >
    </app-example-progressbar>
    ```

## Маршрутизация

### Управление фокусом после навигации

Отслеживание и управление [focus](https://developers.google.com/web/fundamentals/accessibility/focus) в пользовательском интерфейсе является важным моментом при проектировании доступности. При использовании маршрутизации Angular вы должны решить, куда перейдет фокус страницы после навигации.

Чтобы не полагаться исключительно на визуальные подсказки, необходимо убедиться, что код маршрутизации обновляет фокус после навигации страницы. Используйте событие `NavigationEnd` из службы `Router`, чтобы знать, когда нужно обновить фокус.

Следующий пример показывает, как найти и сфокусировать заголовок основного содержимого в DOM после навигации.

```ts
router.events
    .pipe(filter((e) => e instanceof NavigationEnd))
    .subscribe(() => {
        const mainHeader = document.querySelector(
            '#main-content-header'
        );
        if (mainHeader) {
            mainHeader.focus();
        }
    });
```

В реальном приложении элемент, на котором фокусируется внимание, зависит от конкретной структуры и расположения приложения. Сфокусированный элемент должен располагать пользователя к немедленному переходу к основному содержимому, которое только что было направлено в поле зрения.
Вы должны избегать ситуаций, когда фокус возвращается к элементу `body` после изменения маршрута.

### Идентификация активных ссылок

CSS-классы, применяемые к активным элементам `RouterLink`, такие как `RouterLinkActive`, обеспечивают визуальную подсказку для идентификации активной ссылки. К сожалению, визуальная подсказка не помогает слепым или слабовидящим пользователям.

Применение атрибута `aria-current` к элементу может помочь определить активную ссылку.

Для получения дополнительной информации смотрите [Mozilla Developer Network (MDN) aria-current](https://developer.mozilla.org/docs/Web/Accessibility/ARIA/Attributes/aria-current)).

Директива `RouterLinkActive` предоставляет вход `ariaCurrentWhenActive`, который устанавливает `aria-current` в указанное значение, когда ссылка становится активной.

Следующий пример показывает, как применить класс `active-page` к активным ссылкам, а также установить их атрибут `aria-current` в значение `"page"`, когда они становятся активными:

```html
<nav>
    <a
        routerLink="home"
        routerLinkActive="active-page"
        ariaCurrentWhenActive="page"
    >
        Home
    </a>
    <a
        routerLink="about"
        routerLinkActive="active-page"
        ariaCurrentWhenActive="page"
    >
        About
    </a>
    <a
        routerLink="shop"
        routerLinkActive="active-page"
        ariaCurrentWhenActive="page"
    >
        Shop
    </a>
</nav>
```

## Дополнительная информация

-   [Accessibility - Google Web Fundamentals](https://developers.google.com/web/fundamentals/accessibility)
-   [Спецификация ARIA и практика разработки](https://www.w3.org/TR/wai-aria)
-   [Material Design - Accessibility](https://material.io/design/usability/accessibility.html)
-   [Smashing Magazine](https://www.smashingmagazine.com/search/?q=accessibility)
-   [Inclusive Components](https://inclusive-components.design)
-   [Accessibility Resources and Code Examples](https://dequeuniversity.com/resources)
-   [W3C - Web Accessibility Initiative](https://www.w3.org/WAI/people-use-web)
-   [Rob Dodson A11ycasts](https://www.youtube.com/watch?v=HtTyRajRuyY)
-   [Angular ESLint](https://github.com/angular-eslint/angular-eslint#functionality) предоставляет правила линтинга, которые помогут вам убедиться, что ваш код соответствует стандартам доступности.

Книги

-   "Веб для всех: Проектирование доступного пользовательского опыта", Сара Хортон и Уитни Кесенбери
-   "Паттерны инклюзивного дизайна", Хейдон Пикеринг
