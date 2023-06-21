# Синтаксис шаблонов

В Angular _шаблон_ - это фрагмент HTML. Используйте специальный синтаксис в шаблоне, чтобы использовать многие возможности Angular.

## Предварительные условия

Прежде чем изучать синтаксис шаблонов, вы должны быть знакомы со следующим:

-   [Концепции Angular] (руководство/архитектура)

-   JavaScript

-   HTML

-   CSS

<!--todo: Do we still need the following section? It seems more relevant to those coming from AngularJS, which is now 7 versions ago. -->

<!-- You may be familiar with the component/template duality from your experience with model-view-controller (MVC) or model-view-viewmodel (MVVM). In Angular, the component plays the part of the controller/viewmodel, and the template represents the view. -->

Каждый шаблон Angular в вашем приложении - это раздел HTML для включения в состав страницы, которую отображает браузер. Шаблон Angular HTML отображает представление или пользовательский интерфейс в браузере, как и обычный HTML, но с гораздо большей функциональностью.

Когда вы создаете приложение Angular с помощью Angular CLI, файл `app.component.html` является шаблоном по умолчанию, содержащим заполнитель HTML.

Руководства по синтаксису шаблонов показывают, как управлять UX/UI путем координации данных между классом и шаблоном.

<div class="is-helpful alert">

В большинстве руководств по синтаксису шаблонов есть специальные рабочие примеры приложений, которые демонстрируют отдельные темы каждого руководства. Чтобы увидеть, как все они работают вместе в одном приложении, смотрите полный <live-example title="Template Syntax Live Code"></live-example>.

</div>

## Расширьте возможности вашего HTML

Расширьте словарь HTML ваших приложений с помощью специального синтаксиса Angular в ваших шаблонах. Например, Angular помогает вам динамически получать и устанавливать значения DOM \(Document Object Model\) с помощью таких функций, как встроенные функции шаблонов, переменные, прослушивание событий и привязка данных.

Почти весь синтаксис HTML является допустимым синтаксисом шаблона. Однако, поскольку шаблон Angular является частью общей веб-страницы, а не всей страницей, вам не нужно включать такие элементы, как `<html>`, `<body>` или `<base>`, а можно сосредоточиться исключительно на той части страницы, которую вы разрабатываете.

<div class="alert is-important">

Чтобы исключить риск атак внедрения сценариев, Angular не поддерживает элемент `<script>` в шаблонах. Angular игнорирует тег `<script>` и выводит предупреждение в консоль браузера.
Для получения дополнительной информации см. страницу [Security](guide/security).

</div>

## Подробнее о синтаксисе шаблонов

Возможно, вас также заинтересует следующее:

| Topics | Details | |:--- |:--- |
| [Interpolation](guide/interpolation) | Learn how to use interpolation and expressions in HTML. |
| [Template statements](guide/template-statements) | Respond to events in your templates. |
| [Binding syntax](guide/binding-syntax) | Use binding to coordinate values in your application. |
| [Property binding](guide/property-binding) | Set properties of target elements or directive `@Input()` decorators. |
| [Attribute, class, and style bindings](guide/attribute-binding) | Set the value of attributes, classes, and styles. |
| [Event binding](guide/event-binding) | Listen for events and your HTML. |
| [Two-way binding](guide/two-way-binding) | Share data between a class and its template. |
| [Built-in directives](guide/built-in-directives) | Listen to and modify the behavior and layout of HTML. |
| [Template reference variables](guide/template-reference-variables) | Use special variables to reference a DOM element within a template. |
| [Inputs and Outputs](guide/inputs-outputs) | Share data between the parent context and child directives or components |
| [Template expression operators](guide/template-expression-operators) | Learn about the pipe operator \(<code>&verbar;</code>\), and protect against `null` or `undefined` values in your HTML. |
| [SVG in templates](guide/svg-in-templates) | Dynamically generate interactive graphics. |

<!-- links -->

<!-- external links -->

<!-- end links -->

@ просмотрено 2022-02-28
