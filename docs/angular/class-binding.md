# Привязка классов и стилей

Используйте привязки классов и стилей для добавления и удаления имен классов CSS из атрибута `class` элемента и для динамической установки стилей.

## Предварительные условия

-   [Property binding](guide/property-binding)

## Привязка к одному CSS `class`.

Чтобы создать привязку к одному классу, введите следующее:

`[class.sale]="onSale"`.

Angular добавляет класс, когда связанное выражение `onSale` истинно, и удаляет класс, когда выражение ложно&mdash; за исключением `undefined`. Дополнительную информацию смотрите в [делегирование стилей](guide/style-precedence#styling-delegation).

## Привязка к нескольким классам CSS

Чтобы привязать несколько классов, введите следующее:

`[class]="classExpression"`.

Выражение может быть одним из:

-   Строка имен классов, ограниченная пробелами.

-   Объект с именами классов в качестве ключей и истинными или ложными выражениями в качестве значений.

-   Массив имен классов.

При использовании объектного формата Angular добавляет класс, только если его связанное значение истинно.

<div class="alert is-important">

При использовании любого объектоподобного выражения &mdash; такого как `object`, `Array`, `Map` или `Set` &mdash; идентификатор объекта должен измениться, чтобы Angular обновил список классов. Обновление свойства без изменения идентичности объекта не имеет эффекта.

</div>

If there are multiple bindings to the same class name, Angular uses [styling precedence](guide/style-precedence) to determine which binding to use.

The following table summarizes class binding syntax.

| Binding Type | Syntax | Input Type | Example Input Values | |:--- |:--- |:--- |:--- |

| Single class binding | `[class.sale]="onSale"` | <code>boolean &verbar; undefined &verbar; null</code> | `true`, `false` |

| Multi-class binding | `[class]="classExpression"` | `string` | `"my-class-1 my-class-2 my-class-3"` |

| Multi-class binding | `[class]="classExpression"` | <code>Record&lt;string, boolean &verbar; undefined &verbar; null&gt;</code> | `{foo: true, bar: false}` |

| Multi-class binding | `[class]="classExpression"` | <code>Array&lt;string&gt;</code> | `['foo', 'bar']` |

## Binding to a single style

To create a single style binding, use the prefix `style` followed by a dot and the name of the CSS style.

For example, to set the `width` style, type the following: `[style.width]="width"`

Angular sets the property to the value of the bound expression, which is usually a string. Optionally, you can add a unit extension like `em` or `%`, which requires a number type.

1. Чтобы написать стиль в тире, введите следующее:

    <code-example language="html">&lt;nav [style.background-color]="expression"&gt;&lt;/nav&gt;</code-example>.

2. Чтобы написать стиль в camelCase, введите следующее:

    <code-example language="html">&lt;nav [style.backgroundColor]="expression"&gt;&lt;/nav&gt;</code-example>.

## Привязка к нескольким стилям

Чтобы переключить несколько стилей, привяжитесь к атрибуту `[style]`&mdash; например, `[style]="styleExpression"`. Выражение `styleExpression` может быть одним из:

-   Строковый список стилей, например, `ширина: 100px; высота: 100px; background-color: cornflowerblue;`.

-   Объект с именами стилей в качестве ключей и значениями стилей в качестве значений, например `{width: '100px', height: '100px', backgroundColor: 'cornflowerblue'}`.

Обратите внимание, что привязка массива к `[style]` не поддерживается.

<div class="alert is-important">

При привязке `[style]` к выражению объекта, идентификатор объекта должен измениться, чтобы Angular обновил список классов. Обновление свойства без изменения идентичности объекта не имеет эффекта.

</div>

### Пример связывания в одном и нескольких стилях

<code-example path="attribute-binding/src/app/single-and-multiple-style-binding.component.ts" header="nav-bar.component.ts"></code-example>

If there are multiple bindings to the same style attribute, Angular uses [styling precedence](guide/style-precedence) to determine which binding to use.

The following table summarizes style binding syntax.

| Binding Type | Syntax | Input Type | Example Input Values | |:--- |:--- |:--- |:--- |

| Single style binding | `[style.width]="width"` | <code>string &verbar; undefined &verbar; null</code> | `"100px"` |

| Single style binding with units | `[style.width.px]="width"` | <code>number &verbar; undefined &verbar; null</code> | `100` |

| Multi-style binding | `[style]="styleExpression"` | `string` | `"width: 100px; height: 100px"` |

| Multi-style binding | `[style]="styleExpression"` | <code>Record&lt;string, string &verbar; undefined &verbar; null&gt;</code> | `{width: '100px', height: '100px'}` |

{@a styling-precedence}

## Styling precedence

A single HTML element can have its CSS class list and style values bound to multiple sources (for example, host bindings from multiple directives).

## What’s next

-   [Component styles](/guide/component-styles)

-   [Введение в анимации Angular](/guide/animations)

:date: 9.05.2022
