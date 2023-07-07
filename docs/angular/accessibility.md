# Доступность в Angular

Интернетом пользуются самые разные люди, в том числе те, кто страдает нарушениями зрения или двигательных функций. Существует множество вспомогательных технологий, которые значительно облегчают этим группам людей взаимодействие с веб-приложениями.

Кроме того, разработка приложения для обеспечения его доступности в целом улучшает пользовательский опыт для всех пользователей.

Подробный обзор вопросов и методов разработки доступных приложений см. в разделе [Accessibility](https://developers.google.com/web/fundamentals/accessibility/#what_is_accessibility) раздела [Web Fundamentals](https://developers.google.com/web/fundamentals) Google.

На этой странице обсуждаются лучшие практики проектирования приложений Angular, которые хорошо работают для всех пользователей, включая тех, кто использует вспомогательные технологии.

<div class="alert is-helpful">

Пример приложения, которое описывается на этой странице, см. в <live-example></live-example>.

</div>

## Атрибуты доступности

Создание доступного веб-опыта часто включает установку [Accessible Rich Internet Applications \(ARIA\) attributes](https://developers.google.com/web/fundamentals/accessibility/semantics-aria) для обеспечения семантического смысла там, где он может отсутствовать. Используйте синтаксис шаблона [привязка атрибутов](guide/attribute-binding) для управления значениями атрибутов, связанных с доступностью.

При привязке к атрибутам ARIA в Angular вы должны использовать префикс `attr.`. Спецификация ARIA зависит именно от атрибутов HTML, а не от свойств элементов DOM.

<code-example format="html" language="html">

&lt;!-- Используйте attr. при привязке к ARIA-атрибуту --&gt; &lt;button [attr.aria-label]="myActionLabel"&gt;&hellip;&lt;/button&gt;

</code-example>

<div class="alert is-helpful">

**NOTE** <br /> Этот синтаксис необходим только для _привязок_ атрибутов.
Статические атрибуты ARIA не требуют дополнительного синтаксиса.

<code-example format="html" language="html">

&lt;!-- Статические атрибуты ARIA не требуют дополнительного синтаксиса --&gt; &lt;button aria-label="Сохранить документ"&gt;&hellip;&lt;/button&gt;

</code-example>

</div>

<div class="alert is-helpful">

По соглашению, атрибуты HTML используют имена в нижнем регистре \(`tabindex`\), в то время как свойства используют имена в camelCase \(`tabIndex`\).

Подробнее о разнице между атрибутами и свойствами см. в руководстве [Binding syntax](guide/binding-syntax#html-attribute-vs-dom-property).

</div>

## Angular UI components

The [Angular Material](https://material.angular.io) library, which is maintained by the Angular team, is a suite of reusable UI components that aims to be fully accessible. The [Component Development Kit (CDK)](https://material.angular.io/cdk/categories) includes the `a11y` package that provides tools to support various areas of accessibility.

For example:

-   `LiveAnnouncer` is used to announce messages for screen-reader users using an `aria-live` region.

    See the W3C documentation for more information on [aria-live regions](https://www.w3.org/WAI/PF/aria-1.1/states_and_properties#aria-live).

-   The `cdkTrapFocus` directive traps Tab-key focus within an element.

    Use it to create accessible experience for components such as modal dialogs, where focus must be constrained.

For full details of these and other tools, see the [Angular CDK accessibility overview](https://material.angular.io/cdk/a11y/overview).

### Augmenting native elements

Native HTML elements capture several standard interaction patterns that are important to accessibility. When authoring Angular components, you should re-use these native elements directly when possible, rather than re-implementing well-supported behaviors.

For example, instead of creating a custom element for a new variety of button, create a component that uses an attribute selector with a native `<button>` element. Чаще всего это относится к `<button>` и `<a>`, но может быть использовано и со многими другими типами элементов.

Вы можете увидеть примеры этого паттерна в Angular Material: [`MatButton`](https://github.com/angular/components/blob/50d3f29b6dc717b512dbd0234ce76f4ab7e9762a/src/material/button/button.ts#L67-L69), [`MatTabNav`](https://github.com/angular/components/blob/50d3f29b6dc717b512dbd0234ce76f4ab7e9762a/src/material/tabs/tab-nav-bar/tab-nav-bar.ts#L139), и [`MatTable`](https://github.com/angular/components/blob/50d3f29b6dc717b512dbd0234ce76f4ab7e9762a/src/material/table/table.ts#L22).

### Using containers for native elements

Sometimes using the appropriate native element requires a container element. For example, the native `<input>` element cannot have children, so any custom text entry components need to wrap an `<input>` with extra elements.

By just including `<input>` in your custom component's template, it's impossible for your component's users to set arbitrary properties and attributes to the `<input>` element.

Instead, create a container component that uses content projection to include the native control in the component's API.

You can see [`MatFormField`](https://material.angular.io/components/form-field/overview) as an example of this pattern.

## Case study: Building a custom progress bar

The following example shows how to make a progress bar accessible by using host binding to control accessibility-related attributes.

-   The component defines an accessibility-enabled element with both the standard HTML attribute `role`, and ARIA attributes.

    The ARIA attribute `aria-valuenow` is bound to the user's input.

    <code-example header="src/app/progress-bar.component.ts" path="accessibility/src/app/progress-bar.component.ts" region="progressbar-component"></code-example>

-   In the template, the `aria-label` attribute ensures that the control is accessible to screen readers.

    <code-example header="src/app/app.component.html" path="accessibility/src/app/app.component.html" region="template"></code-example>

## Маршрутизация

### Управление фокусом после навигации

Отслеживание и управление [focus](https://developers.google.com/web/fundamentals/accessibility/focus) в пользовательском интерфейсе является важным моментом при проектировании доступности. При использовании маршрутизации Angular вы должны решить, куда перейдет фокус страницы после навигации.

Чтобы не полагаться исключительно на визуальные подсказки, необходимо убедиться, что код маршрутизации обновляет фокус после навигации страницы. Используйте событие `NavigationEnd` из службы `Router`, чтобы знать, когда нужно обновить фокус.

Следующий пример показывает, как найти и сфокусировать заголовок основного содержимого в DOM после навигации.

<code-example format="typescript" language="typescript">

router.events.pipe(filter(e =&gt; e instanceof NavigationEnd)).subscribe(() =&gt; { const mainHeader = document.querySelector('&num;main-content-header')
if (mainHeader) {

mainHeader.focus();

}

});

</code-example>

В реальном приложении элемент, на котором фокусируется внимание, зависит от конкретной структуры и расположения приложения. Сфокусированный элемент должен располагать пользователя к немедленному переходу к основному содержимому, которое только что было направлено в поле зрения.
Вы должны избегать ситуаций, когда фокус возвращается к элементу `body` после изменения маршрута.

### Идентификация активных ссылок

CSS-классы, применяемые к активным элементам `RouterLink`, такие как `RouterLinkActive`, обеспечивают визуальную подсказку для идентификации активной ссылки. К сожалению, визуальная подсказка не помогает слепым или слабовидящим пользователям.

Применение атрибута `aria-current` к элементу может помочь определить активную ссылку.

Для получения дополнительной информации смотрите [Mozilla Developer Network \(MDN\) aria-current](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Attributes/aria-current)).

Директива `RouterLinkActive` предоставляет вход `ariaCurrentWhenActive`, который устанавливает `aria-current` в указанное значение, когда ссылка становится активной.

Следующий пример показывает, как применить класс `active-page` к активным ссылкам, а также установить их атрибут `aria-current` в значение `"page"`, когда они становятся активными:

```html <nav>
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

<!-- vale Angular.Angular_Spelling = NO -->

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

<!-- vale Angular.Angular_Spelling = YES -->

Книги

<!-- vale Angular.Google_Quotes = NO -->

-   "Веб для всех: Проектирование доступного пользовательского опыта", Сара Хортон и Уитни Кесенбери
-   "Паттерны инклюзивного дизайна", Хейдон Пикеринг

<!-- vale Angular.Google_Quotes = YES -->

<!-- links -->

<!-- external links -->

<!-- end links -->

:date: 28.02.2022
