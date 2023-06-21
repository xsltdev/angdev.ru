# Связывание атрибутов

Привязка атрибутов в Angular позволяет задавать значения атрибутов напрямую. С помощью привязки атрибутов можно улучшить доступность, динамически изменять стиль приложения и управлять несколькими классами или стилями CSS одновременно.

<div class="alert is-helpful">

Смотрите <live-example></live-example> для рабочего примера, содержащего фрагменты кода, приведенные в этом руководстве.

</div>

## Предварительные условия

-   [Property Binding](guide/property-binding)

## Синтаксис

Синтаксис связывания атрибутов похож на [property binding](guide/property-binding), но вместо свойства элемента в скобках перед именем атрибута ставится префикс `attr`, за которым следует точка. Затем вы задаете значение атрибута с помощью выражения, которое преобразуется в строку.

<code-example format="html" language="html">

&lt;p [attr.attribute-you-are-targeting]="expression"&gt;&lt;/p&gt;

</code-example>

<div class="alert is-helpful">

Когда выражение разрешается в `null` или `undefined`, Angular полностью удаляет атрибут.

</div>

## Привязка атрибутов ARIA

Одним из основных вариантов использования привязки атрибутов является установка атрибутов ARIA.

Для привязки к атрибуту ARIA введите следующее:

<code-example header="src/app/app.component.html" path="attribute-binding/src/app/app.component.html" region="attrib-binding-aria"></code-example>

<a id="colspan"></a>

## Привязка к `colspan`

Другим распространенным случаем использования привязки атрибутов является атрибут `colspan` в таблицах. Привязка к атрибуту `colspan` помогает вам поддерживать программную динамику ваших таблиц. В зависимости от количества данных, которыми ваше приложение заполняет таблицу, количество столбцов, которые охватывает строка, может меняться.

Чтобы использовать привязку атрибута `<td>` к атрибуту `colspan`, выполните следующие действия.

1. Укажите атрибут `colspan`, используя следующий синтаксис: `[attr.colspan]`.

1. Установите `[attr.colspan]` равным выражению.

В следующем примере вы связываете атрибут `colspan` с выражением `1 + 1`.

<code-example header="src/app/app.component.html" path="attribute-binding/src/app/app/app.component.html" region="colspan"></code-example>.

Эта привязка заставляет `<tr>` охватывать две колонки.

<div class="alert is-helpful">

Иногда существуют различия между названием свойства и атрибута.

`colspan` является атрибутом `<td>`, а `colSpan` с заглавной "S" - свойством. При использовании привязки к атрибутам используйте `colspan` со строчной буквой "s".

Подробнее о том, как привязать свойство `colSpan`, смотрите в разделе [`colspan` и `colSpan`](guide/property-binding#colspan) раздела [Property Binding](guide/property-binding).

</div>

## Что дальше

-   [Class & Style Binding](guide/class-binding)
