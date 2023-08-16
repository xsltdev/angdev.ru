# Синтаксис связывания данных

Привязка данных автоматически поддерживает страницу в актуальном состоянии на основе состояния вашего приложения. Вы используете привязку данных для указания таких вещей, как источник изображения, состояние кнопки или данные для конкретного пользователя.

<div class="alert is-helpful">

Смотрите <live-example></live-example> для рабочего примера, содержащего фрагменты кода, приведенные в этом руководстве.

</div>

## Data binding and HTML

Developers can customize HTML by specifying attributes with string values. In the following example, `class`, `src`, and `disabled` modify the `<div>`, `<img>`, and `<button>` elements respectively.

<code-example format="html" language="html">

&lt;div class="special"&gt;Обычный старый HTML&lt;/div&gt; &lt;img src="images/item.png"&gt;
&lt;кнопка отключена&gt;Сохранить&lt;/button&gt;

</code-example>

Используйте привязку данных для управления такими вещами, как состояние кнопки:

<code-example header="src/app/app.component.html" path="binding-syntax/src/app/app/app.component.html" region="disabled-button"></code-example>.

Обратите внимание, что привязка происходит к свойству `disabled` DOM-элемента кнопки, а не к атрибуту. Привязка данных работает со свойствами элементов DOM, компонентов и директив, а не с атрибутами HTML.

<a id="html-attribute-vs-dom-property"></a>

### Атрибуты HTML и свойства DOM

Angular binding различает атрибуты HTML и свойства DOM.

Атрибуты инициализируют свойства DOM, и вы можете настроить их для изменения поведения элемента. Свойства - это характеристики узлов DOM.

-   Некоторые атрибуты HTML имеют соответствие 1:1 со свойствами; например,

      <code-example format="html" hideCopy language="html">

    id

      </code-example>

-   Некоторые атрибуты HTML не имеют соответствующих свойств; например,

      <code-example format="html" hideCopy language="html">

    aria-\*

      </code-example>

-   Некоторые свойства DOM не имеют соответствующих атрибутов; например,

      <code-example format="html" hideCopy language="html">

    textContent

      </code-example>

<div class="alert is-important">

Помните, что атрибуты HTML и свойства DOM - это разные вещи, даже если они имеют одинаковые имена.

</div>

In Angular, the only role of HTML attributes is to initialize element and directive state.

When you write a data binding, you're dealing exclusively with the DOM properties and events of the target object.

#### Example 1: an `<input>`

When the browser renders `<input type="text" value="Sarah">`, it creates a corresponding DOM node with a `value` property and initializes that `value` to "Sarah".

<code-example format="html" language="html">

&lt;input type="text" value="Сара"&gt;

</code-example>

Когда пользователь вводит `Sally` в `<input>`, свойство элемента DOM `value` становится `Sally`. Однако, если посмотреть на HTML-атрибут `value`, используя `input.getAttribute('value')`, можно увидеть, что атрибут остается неизменным &mdash; он возвращает "Sarah".

HTML-атрибут `value` определяет начальное значение; свойство DOM `value` - это текущее значение.

Чтобы увидеть атрибуты в сравнении со свойствами DOM в работающем приложении, смотрите <live-example name="binding-syntax"></live-example> специально для синтаксиса связывания.

#### Пример 2: отключенная кнопка

Свойство `disabled` кнопки по умолчанию равно `false`, поэтому кнопка включена.

Когда вы добавляете атрибут `disabled`, вы инициализируете свойство `disabled` кнопки значением `true`, которое отключает кнопку.

<code-example format="html" language="html">

&lt;button disabled&gt;Кнопка тестирования&lt;/button&gt;

</code-example>

Adding and removing the `disabled` attribute disables and enables the button. However, the value of the attribute is irrelevant, which is why you cannot enable a button by writing `<button disabled="false">Still Disabled</button>`.

To control the state of the button, set the `disabled` property instead.

#### Property and attribute comparison

Though you could technically set the `[attr.disabled]` attribute binding, the values are different in that the property binding must be a boolean value, while its corresponding attribute binding relies on whether the value is `null` or not. Consider the following:

<code-example format="html" language="html">

&lt;input [disabled]="условие ? true : false"&gt; &lt;input [attr.disabled]="условие ? 'disabled' : null"&gt;

</code-example>

В первой строке, использующей свойство `disabled`, используется булево значение. Вторая строка, использующая атрибут disabled, проверяет значение `null`.

Как правило, следует использовать привязку к свойствам, а не к атрибутам, поскольку булево значение легко читается, синтаксис короче, а свойство более эффективно.

Чтобы увидеть пример кнопки `disabled` в работающем приложении, посмотрите <live-example></live-example>. В этом примере показано, как переключить свойство disabled из компонента.

## Типы привязки данных

Angular предоставляет три категории привязки данных в зависимости от направления потока данных:

-   От источника к представлению

-   От представления к источнику

-   В двусторонней последовательности от представления к источнику и от источника к представлению.

| Type | Syntax | Category | |:--- |:--- |:--- |
| Interpolation <br /> Property <br /> Attribute <br /> Class <br /> Style | <code-example> {{expression}} &NewLine;[target]="expression" </code-example> | One-way from data source to view target |

| Event | <code-example> (target)="statement" </code-example> | One-way from view target to data source |

| Two-way | <code-example> [(target)]="expression" </code-example> | Two-way |

Binding types other than interpolation have a target name to the left of the equal sign. The target of a binding is a property or event, which you surround with square bracket \(`[ ]`\) characters, parenthesis \(`( )`\) characters, or both \(`[( )]`\) characters.

The binding punctuation of `[]`, `()`, `[()]`, and the prefix specify the direction of data flow.

-   Используйте `[]` для привязки источника к представлению
-   Используйте `()` для привязки от представления к источнику

-   Используйте `[()]` для двухстороннего связывания в последовательности вид - источник - вид.

Поместите выражение или утверждение справа от знака равенства в двойные кавычки \(`""`\). Для получения дополнительной информации смотрите [Интерполяция](interpolation.md) и [Шаблонные утверждения](template-statements.md).

## Типы и цели связывания

Целью привязки данных может быть свойство, событие или имя атрибута. Каждый открытый член исходной директивы автоматически доступен для связывания в шаблонном выражении или утверждении.

В следующей таблице перечислены цели для различных типов привязки.

| Type | Target | Examples | |:--- |:--- |:--- |
| Property | Element property <br /> Component property <br /> Directive property | `alt`, `src`, `hero`, and `ngClass` in the following: <code-example path="template-syntax/src/app/app.component.html" region="property-binding-syntax-1"></code-example> <!-- For more information, see [Property Binding](property-binding.md). --> |
| Event | Element event <br /> Component event <br /> Directive event | `click`, `deleteRequest`, and `myClick` in the following: <code-example path="template-syntax/src/app/app.component.html" region="event-binding-syntax-1"></code-example> |
| Two-way | Event and property | <code-example path="template-syntax/src/app/app.component.html" region="2-way-binding-syntax-1"></code-example> |
| Attribute | Attribute \(the exception\) | <code-example path="template-syntax/src/app/app.component.html" region="attribute-binding-syntax-1"></code-example> |
| Class | `class` property | <code-example path="template-syntax/src/app/app.component.html" region="class-binding-syntax-1"></code-example> |
| Style | `style` property | <code-example path="template-syntax/src/app/app.component.html" region="style-binding-syntax-1"></code-example> |

<!-- links -->

<!-- external links -->

<!-- end links -->

@ просмотрено 2022-02-28
