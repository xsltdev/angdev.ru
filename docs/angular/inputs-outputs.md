# Совместное использование данных между дочерними и родительскими директивами и компонентами

Распространенным паттерном в Angular является обмен данными между родительским компонентом и одним или несколькими дочерними компонентами. Реализуйте этот паттерн с помощью декораторов `@Input()` и `@Output()`.

<div class="alert is-helpful">

Смотрите <live-example></live-example> для рабочего примера, содержащего фрагменты кода, приведенные в этом руководстве.

</div>

Рассмотрим следующую иерархию:

<code-example format="html" language="html">

&lt;parent-component&gt; &lt;child-component&gt;&lt;/child-component&gt;
&lt;/parent-component&gt;

</code-example>

Компонент `<родительский компонент>` служит контекстом для компонента `<детский компонент>`.

`@Input()` и `@Output()` дают дочернему компоненту возможность общаться со своим родительским компонентом. `@Input()` позволяет родительскому компоненту обновлять данные в дочернем компоненте.

И наоборот, `@Output()` позволяет дочернему компоненту отправлять данные в родительский компонент.

<a id="input"></a>

## Отправка данных в дочерний компонент

Декоратор `@Input()` в дочернем компоненте или директиве означает, что свойство может получать свое значение от родительского компонента.

<div class="lightbox">

<img alt="Input data flow diagram of data flowing from parent to child" src="generated/images/guide/inputs-outputs/input.svg">

</div>

Чтобы использовать `@Input()`, вы должны настроить родительский и дочерний компоненты.

### Настройка дочернего компонента

Чтобы использовать декоратор `@Input()` в классе дочернего компонента, сначала импортируйте `Input`, а затем украсьте свойство с помощью `@Input()`, как показано в следующем примере.

<code-example header="src/app/item-detail/item-detail.component.ts" path="inputs-outputs/src/app/item-detail/item-detail.component.ts" region="use-input"></code-example>

In this case, `@Input()` decorates the property <code class="no-auto-link">item</code>, which has a type of `string`, however, `@Input()` properties can have any type, such as `number`, `string`, `boolean`, or `object`. The value for `item` comes from the parent component.

Next, in the child component template, add the following:

<code-example header="src/app/item-detail/item-detail.component.html" path="inputs-outputs/src/app/item-detail/item-detail.component.html" region="property-in-template"></code-example>.

### Настройка родительского компонента

Следующим шагом будет привязка свойства в шаблоне родительского компонента. В данном примере шаблоном родительского компонента является `app.component.html`.

1.  Используйте селектор дочернего компонента, здесь `<app-item-detail>`, как директиву в шаблоне родительского компонента.

1.  Используйте [property binding](guide/property-binding) для привязки свойства `item` в дочернем компоненте к свойству `currentItem` родительского компонента.

    <code-example header="src/app/app.component.html" path="inputs-outputs/src/app/app/app.component.html" region="input-parent"></code-example>.

1.  В классе родительского компонента определите значение для `currentItem`:

    <code-example header="src/app/app.component.ts" path="inputs-outputs/src/app/app/app.component.ts" region="parent-property"></code-example>.

С помощью `@Input()`, Angular передает значение `currentItem` дочернему элементу, так что `item` отображается как `Television`.

На следующей диаграмме показана эта структура:

<div class="lightbox">

<img alt="Property binding diagram of the target, item, in square brackets set to the source, currentItem, on the right of an equal sign" src="generated/images/guide/inputs-outputs/input-diagram-target-source.svg">

</div>

Цель в квадратных скобках, `[]`, - это свойство, которое вы украшаете с помощью `@Input()` в дочернем компоненте. Источник привязки, часть справа от знака равенства, - это данные, которые родительский компонент передает вложенному компоненту.

### Наблюдение за изменениями `@Input()`.

Чтобы следить за изменениями свойства `@Input()`, используйте `OnChanges`, один из [хуков жизненного цикла Angular](guide/lifecycle-hooks). Более подробную информацию и примеры смотрите в разделе [`OnChanges`](guide/lifecycle-hooks#onchanges) руководства [Lifecycle Hooks](guide/lifecycle-hooks).

<a id="output"></a>

## Отправка данных в родительский компонент

Декоратор `@Output()` в дочернем компоненте или директиве позволяет передавать данные от дочернего компонента к родительскому.

<div class="lightbox">

<img alt="Output diagram of the data flow going from child to parent" src="generated/images/guide/inputs-outputs/output.svg">

</div>

`@Output()` marks a property in a child component as a doorway through which data can travel from the child to the parent.

The child component uses the `@Output()` property to raise an event to notify the parent of the change. To raise an event, an `@Output()` must have the type of `EventEmitter`, which is a class in `@angular/core` that you use to emit custom events.

The following example shows how to set up an `@Output()` in a child component that pushes data from an HTML `<input>` to an array in the parent component.

To use `@Output()`, you must configure the parent and child.

### Configuring the child component

The following example features an `<input>` where a user can enter a value and click a `<button>` that raises an event. The `EventEmitter` then relays the data to the parent component.

1.  Импортируйте `Output` и `EventEmitter` в класс дочернего компонента:

    <code-example format="javascript" language="javascript">.

    import { Output, EventEmitter } from '&commat;angular/core';

    </code-example>.

1.  В классе компонента украсьте свойство `@Output()`.

    Следующий пример `newItemEvent` `@Output()` имеет тип `EventEmitter`, что означает, что это событие.

    <code-example header="src/app/item-output/item-output.component.ts" path="inputs-outputs/src/app/item-output/item-output.component.ts" region="item-output"></code-example>.

    Различные части предыдущей декларации выглядят следующим образом:

    | Части декларации | Детали |

    |:--- |:--- |

    | `@Output()` | Функция-декоратор, помечающая свойство как способ передачи данных от дочернего компонента к родительскому. |

    | | `newItemEvent` | Имя `@Output()`. |

    | | `EventEmitter<string>` | Тип `@Output()`. |

    | | `new EventEmitter<string>()` | Сообщает Angular о создании нового эмиттера события и о том, что данные, которые он эмитирует, имеют тип string. |

    Для получения дополнительной информации о `EventEmitter` смотрите документацию [EventEmitter API documentation](api/core/EventEmitter).

1.  Create an `addNewItem()` method in the same component class:

    <code-example header="src/app/item-output/item-output.component.ts" path="inputs-outputs/src/app/item-output/item-output.component.ts" region="item-output-class"></code-example>

    The `addNewItem()` function uses the `@Output()`, `newItemEvent`, to raise an event with the value the user types into the `<input>`.

### Configuring the child's template

The child's template has two controls. The first is an HTML `<input>` with a [template reference variable](guide/template-reference-variables), `#newItem`, where the user types in an item name.
The `value` property of the `#newItem` variable stores what the user types into the `<input>`.

<code-example header="src/app/item-output/item-output.component.html" path="inputs-outputs/src/app/item-output/item-output.component.html" region="child-output"></code-example>

The second element is a `<button>` with a `click` [event binding](guide/event-binding).

The `(click)` event is bound to the `addNewItem()` method in the child component class. The `addNewItem()` method takes as its argument the value of the `#newItem.value` property.

### Configuring the parent component

The `AppComponent` in this example features a list of `items` in an array and a method for adding more items to the array.

<code-example header="src/app/app.component.ts" path="inputs-outputs/src/app/app.component.ts" region="add-new-item"></code-example>

The `addItem()` method takes an argument in the form of a string and then adds that string to the `items` array.

### Configuring the parent's template

1.  In the parent's template, bind the parent's method to the child's event.

1.  Put the child selector, here `<app-item-output>`, within the parent component's template, `app.component.html`.

    <code-example header="src/app/app.component.html" path="inputs-outputs/src/app/app.component.html" region="output-parent"></code-example>

    The event binding, `(newItemEvent)='addItem($event)'`, connects the event in the child, `newItemEvent`, to the method in the parent, `addItem()`.

    The `$event` contains the data that the user types into the `<input>` in the child template UI.

    To see the `@Output()` working, add the following to the parent's template:

    <code-example format="html" language="html">

    &lt;ul&gt;

    &lt;li \*ngFor="let item of items"&gt;{{item}}&lt;/li&gt;

    &lt;/ul&gt;

    </code-example>

    The `*ngFor` iterates over the items in the `items` array.

    When you enter a value in the child's `<input>` and click the button, the child emits the event and the parent's `addItem()` method pushes the value to the `items` array and new item renders in the list.

## Using `@Input()` and `@Output()` together

Use `@Input()` and `@Output()` on the same child component as follows:

<code-example header="src/app/app.component.html" path="inputs-outputs/src/app/app/app.component.html" region="together"></code-example>.

Цель, `item`, которая является свойством `@Input()` в классе дочернего компонента, получает свое значение из свойства родителя, `currentItem`. Когда вы нажимаете кнопку delete, дочерний компонент вызывает событие `deleteRequest`, которое является аргументом для родительского метода `crossOffItem()`.

На следующей схеме показаны различные части `@Input()` и `@Output()` на дочернем компоненте `<app-input-output>`.

<div class="lightbox">

<img alt="Diagram of an input target and an output target each bound to a source." src="generated/images/guide/inputs-outputs/input-output-diagram.svg">

</div>

Дочерний селектор - `<app-input-output>`, при этом `item` и `deleteRequest` являются свойствами `@Input()` и `@Output()` в классе дочернего компонента. Свойство `currentItem` и метод `crossOffItem()` находятся в классе родительского компонента.

Чтобы объединить привязки свойств и событий с помощью синтаксиса "банана в коробке", `[()]`, смотрите [Двусторонняя привязка](guide/two-way-binding).

<!-- links -->

<!-- external links -->

<!-- end links -->

:date: 28.02.2022
