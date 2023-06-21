# Связывание свойств

Привязка свойств в Angular помогает задавать значения для свойств HTML-элементов или директив. Используйте привязку свойств для таких задач, как переключение функций кнопки, программная установка путей и обмен значениями между компонентами.

<div class="alert is-helpful">

Смотрите <live-example></live-example> для рабочего примера, содержащего фрагменты кода, приведенные в этом руководстве.

</div>

## Предварительные условия

-   [Основы компонентов](guide/architecture-components)

-   [Основы шаблонов](guide/glossary#template)

-   [Синтаксис связывания](guide/binding-syntax)

## Понимание потока данных

Привязка свойств перемещает значение в одном направлении, из свойства компонента в свойство целевого элемента.

<div class="alert is-helpful">

Для получения дополнительной информации о прослушивании событий смотрите [Event binding](guide/event-binding).

</div>

Чтобы прочитать свойство целевого элемента или вызвать один из его методов, см. справку API для [ViewChild](api/core/ViewChild) и [ContentChild](api/core/ContentChild).

## Привязка к свойству

Чтобы привязать свойство элемента, заключите его в квадратные скобки, `[]`, что идентифицирует свойство как целевое.

Целевое свойство - это свойство DOM, которому вы хотите присвоить значение.

Чтобы присвоить значение целевому свойству `src` элемента image, введите следующий код:

<code-example path="property-binding/src/app/app.component.html" region="property-binding" header="src/app/app.component.html"></code-example>

In most cases, the target name is the name of a property, even when it appears to be the name of an attribute.

In this example, `src` is the name of the `<img>` element property.

<!-- vale Angular.Google_WordListSuggestions = NO -->

Скобки `[]` заставляют Angular оценивать правую часть присваивания как динамическое выражение.

<!-- vale Angular.Google_WordListSuggestions = NO -->

Без скобок Angular рассматривает правую часть как строковый литерал и устанавливает свойству это статическое значение.

Чтобы присвоить свойству строку, введите следующий код:

<code-example path="property-binding/src/app/app.component.html" region="no-evaluation" header="src/app.component.html"></code-example>

Omitting the brackets renders the string `parentItem`, not the value of `parentItem`.

## Setting an element property to a component property value

To bind the `src` property of an `<img>` element to a component's property, place `src` in square brackets followed by an equal sign and then the property.

Using the property `itemImageUrl`, type the following code:

<code-example path="property-binding/src/app/app.component.html" region="property-binding" header="src/app/app.component.html"></code-example>.

Объявите свойство `itemImageUrl` в классе, в данном случае `AppComponent`.

<code-example path="property-binding/src/app/app.component.ts" region="item-image" header="src/app/app.component.ts"></code-example>

{@a colspan}

#### `colspan` и `colSpan`.

Часто возникает путаница между атрибутом `colspan` и свойством `colSpan`. Обратите внимание, что эти два имени отличаются всего одной буквой.

Чтобы использовать связывание свойств с помощью `colSpan`, введите следующее:

<code-example path="attribute-binding/src/app/app.component.html" region="colSpan" header="src/app/app.component.html"></code-example>.

Чтобы отключить кнопку, пока свойство `isUnchanged` компонента равно `true`, введите следующее:

<code-example path="property-binding/src/app/app.component.html" region="disabled-button" header="src/app/app.component.html"></code-example>.

Чтобы установить свойство директивы, введите следующее:

<code-example path="property-binding/src/app/app.component.html" region="class-binding" header="src/app/app.component.html"></code-example>.

Чтобы установить свойство model пользовательского компонента для связи родительского и дочернего компонентов друг с другом, введите следующее:

<code-example path="property-binding/src/app/app.component.html" region="model-property-binding" header="src/app/app.component.html"></code-example>

## Переключение свойств кнопки

<!-- vale Angular.Google_WordListSuggestions = NO -->

Чтобы использовать булево значение для отключения функций кнопки, привяжите DOM-атрибут `disabled` к булеву свойству класса.

<!-- vale Angular.Google_WordListSuggestions = YES -->

<code-example path="property-binding/src/app/app.component.html" region="disabled-button" header="src/app/app.component.html"></code-example>.

Поскольку значение свойства `isUnchanged` в `AppComponent` равно `true`, Angular отключает кнопку.

<code-example path="property-binding/src/app/app.component.ts" region="boolean" header="src/app/app.component.ts"></code-example>

## Что дальше

-   [Лучшие практики связывания свойств](guide/property-binding-best-practices)

-   [Привязка событий](guide/event-binding)

-   [Интерполяция текста](guide/interpolation)

-   [Привязка классов и стилей](guide/class-binding)

-   [Привязка атрибутов](guide/attribute-binding)

@ просмотрено 2022-04-14
