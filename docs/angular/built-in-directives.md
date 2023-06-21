# Встроенные директивы

Директивы - это классы, которые добавляют дополнительное поведение к элементам в ваших приложениях Angular.

Используйте встроенные директивы Angular для управления формами, списками, стилями и тем, что видят пользователи.

<div class="alert is-helpful">

Смотрите <live-example></live-example> для рабочего примера, содержащего фрагменты кода, приведенные в этом руководстве.

</div>

Ниже перечислены различные типы директив Angular:

| Типы директив | Подробности | |:--- |:--- |:--- |

| [Components](guide/component-overview) | Используется с шаблоном. Этот тип директив является наиболее распространенным. |

| [Директивы атрибутов](guide/built-in-directives#built-in-attribute-directives) | Изменяют внешний вид или поведение элемента, компонента или другой директивы. |

| [Структурные директивы](guide/built-in-directives#built-in-structural-directives) | Изменяют компоновку DOM путем добавления и удаления элементов DOM. |

Это руководство охватывает встроенные [атрибутивные директивы](guide/built-in-directives#built-in-attribute-directives) и [структурные директивы](guide/built-in-directives#built-in-structural-directives).

<a id="attribute-directives"></a>

## Встроенные директивы атрибутов

Директивы атрибутов слушают и изменяют поведение других элементов HTML, атрибутов, свойств и компонентов.

Многие модули NgModule, такие как [`RouterModule`](guide/router 'Routing and Navigation') и [`FormsModule`](guide/forms 'Forms') определяют свои собственные директивы атрибутов. Наиболее распространенными директивами атрибутов являются следующие:

| Общие директивы | Подробности | |:--- |:--- |:--- |

| [`NgClass`](guide/built-in-directives#ngClass) | Добавляет и удаляет набор классов CSS. |

| [`NgStyle`](guide/built-in-directives#ngstyle) | Добавляет и удаляет набор стилей HTML. |

| [`NgModel`](guide/built-in-directives#ngModel) | Добавляет двустороннюю привязку данных к элементу HTML-формы. |

<div class="alert is-helpful">

Встроенные директивы используют только общедоступные API. Они не имеют специального доступа к каким-либо частным API, к которым не могут обращаться другие директивы.

</div>

<a id="ngClass"></a>

## Добавление и удаление классов с помощью `NgClass`

Добавьте или удалите несколько классов CSS одновременно с помощью `ngClass`.

<div class="alert is-helpful">

Чтобы добавить или удалить _один_ класс, используйте [class binding](guide/class-binding), а не `NgClass`.

</div>

### Using `NgClass` with an expression

On the element you'd like to style, add `[ngClass]` and set it equal to an expression. In this case, `isSpecial` is a boolean set to `true` in `app.component.ts`.

Because `isSpecial` is true, `ngClass` applies the class of `special` to the `<div>`.

<code-example header="src/app/app.component.html" path="built-in-directives/src/app/app/app.component.html" region="special-div"></code-example>

### Использование `NgClass` с методом

1.  Чтобы использовать `NgClass` с методом, добавьте метод в класс компонента.

    В следующем примере `setCurrentClasses()` устанавливает свойство `currentClasses` с объектом, который добавляет или удаляет три класса на основе состояния `true` или `false` трех других свойств компонента.

    Каждый ключ объекта - это имя класса CSS.

    Если ключ имеет значение `true`, `ngClass` добавляет класс.

    Если ключ равен `false`, то `ngClass` удаляет класс.

    <code-example header="src/app/app.component.ts" path="built-in-directives/src/app/app/app.component.ts" region="setClasses"></code-example>

1.  В шаблоне добавьте привязку свойства `ngClass` к `currentClasses` для установки классов элемента:

    <code-example header="src/app/app.component.html" path="built-in-directives/src/app/app/app.component.html" region="NgClass-1"></code-example>.

Для этого случая использования Angular применяет классы при инициализации и в случае изменений. Полный пример вызывает `setCurrentClasses()` изначально с `ngOnInit()` и когда зависимые свойства изменяются по нажатию кнопки.

Эти шаги не являются необходимыми для реализации `ngClass`.

Для получения дополнительной информации смотрите <live-example></live-example> `app.component.ts` и `app.component.html`.

<a id="ngstyle"></a>

## Установка встроенных стилей с помощью `NgStyle`

Используйте `NgStyle` для установки нескольких встроенных стилей одновременно, основываясь на состоянии компонента.

1.  Чтобы использовать `NgStyle`, добавьте метод в класс компонента.

    В следующем примере `setCurrentStyles()` устанавливает свойство `currentStyles` с объектом, определяющим три стиля, основываясь на состоянии трех других свойств компонента.

    <code-example header="src/app/app.component.ts" path="built-in-directives/src/app/app/app.component.ts" region="setStyles"></code-example>.

1.  Чтобы установить стили элемента, добавьте свойство `ngStyle`, связывающее `currentStyles`.

    <code-example header="src/app/app.component.html" path="built-in-directives/src/app/app/app.component.html" region="NgStyle-2"></code-example>.

Для этого случая использования Angular применяет стили при инициализации и в случае изменений. Для этого в полном примере вызывается `setCurrentStyles()` изначально с `ngOnInit()` и при изменении зависимых свойств по нажатию кнопки.

Однако эти шаги не являются необходимыми для самостоятельной реализации `ngStyle`.

Смотрите <live-example></live-example> `app.component.ts` и `app.component.html` для этой дополнительной реализации.

<a id="ngModel"></a>

## Displaying and updating properties with `ngModel`

Use the `NgModel` directive to display a data property and update that property when the user makes changes.

1.  Import `FormsModule` and add it to the NgModule's `imports` list.

    <code-example header="src/app/app.module.ts (FormsModule import)" path="built-in-directives/src/app/app.module.ts" region="import-forms-module"></code-example>

1.  Add an `[(ngModel)]` binding on an HTML `<form>` element and set it equal to the property, here `name`.

    <code-example header="src/app/app.component.html (NgModel example)" path="built-in-directives/src/app/app.component.html" region="NgModel-1"></code-example>

    This `[(ngModel)]` syntax can only set a data-bound property.

To customize your configuration, write the expanded form, which separates the property and event binding. Use [property binding](guide/property-binding) to set the property and [event binding](guide/event-binding) to respond to changes.

The following example changes the `<input>` value to uppercase:

<code-example header="src/app/app.component.html" path="built-in-directives/src/app/app/app.component.html" region="uppercase"></code-example>.

Вот все варианты в действии, включая версию в верхнем регистре:

<div class="lightbox">

<img alt="NgModel variations" src="generated/images/guide/built-in-directives/ng-model-anim.gif">

</div>

### `NgModel` и аксессоры значений

Директива `NgModel` работает для элемента, поддерживаемого [ControlValueAccessor](api/forms/ControlValueAccessor). Angular предоставляет _аксессоры значений_ для всех основных элементов HTML-форм.

Для получения дополнительной информации смотрите [Forms](guide/forms).

Чтобы применить `[(ngModel)]` к встроенному элементу, не являющемуся формой, или стороннему пользовательскому компоненту, необходимо написать аксессор значения. Для получения дополнительной информации смотрите документацию API по [DefaultValueAccessor](api/forms/DefaultValueAccessor).

<div class="alert is-helpful">

Когда вы пишете компонент Angular, вам не нужен аксессор значения или `NgModel`, если вы называете свойства значения и события в соответствии с [синтаксисом двустороннего связывания Angular] (guide/two-way-binding#how-two-way-binding-works).

</div>

<a id="structural-directives"></a>

## Встроенные структурные директивы

Структурные директивы отвечают за верстку HTML. Они формируют или изменяют структуру DOM, как правило, путем добавления, удаления и манипулирования элементами, к которым они прикреплены.

В этом разделе представлены наиболее распространенные встроенные структурные директивы:

| Общие встроенные структурные директивы | Подробности | | |:--- |:--- |:---.

| [`NgIf`](guide/built-in-directives#ngIf) | Условно создает или удаляет вложенные представления из шаблона. |

| [`NgFor`](guide/built-in-directives#ngFor) | Повторяет узел для каждого элемента в списке. |

| | [`NgSwitch`](guide/built-in-directives#ngSwitch) | Набор директив, переключающих между альтернативными представлениями. |

Для получения дополнительной информации смотрите [Structural Directives](guide/structural-directives).

<a id="ngIf"></a>

## Добавление или удаление элемента с помощью `NgIf`

Добавьте или удалите элемент, применив директиву `NgIf` к главному элементу.

Когда `NgIf` имеет значение `false`, Angular удаляет элемент и его потомков из DOM. Затем Angular утилизирует их компоненты, освобождая память и ресурсы.

Чтобы добавить или удалить элемент, привяжите `*ngIf` к выражению условия, например `isActive` в следующем примере.

<code-example header="src/app/app.component.html" path="built-in-directives/src/app/app.component.html" region="NgIf-1"></code-example>

When the `isActive` expression returns a truthy value, `NgIf` adds the `ItemDetailComponent` to the DOM. When the expression is falsy, `NgIf` removes the `ItemDetailComponent` from the DOM and disposes of the component and all of its subcomponents.

For more information on `NgIf` and `NgIfElse`, see the [NgIf API documentation](api/common/NgIf).

### Guarding against `null`

By default, `NgIf` prevents display of an element bound to a null value.

To use `NgIf` to guard a `<div>`, add `*ngIf="yourProperty"` to the `<div>`. In the following example, the `currentCustomer` name appears because there is a `currentCustomer`.

<code-example header="src/app/app.component.html" path="built-in-directives/src/app/app.component.html" region="NgIf-2"></code-example>

However, if the property is `null`, Angular does not display the `<div>`. In this example, Angular does not display the `nullCustomer` because it is `null`.

<code-example header="src/app/app.component.html" path="built-in-directives/src/app/app/app.component.html" region="NgIf-2b"></code-example>.

<a id="ngFor"></a>

## Вывод списка элементов с помощью `NgFor`

Используйте директиву `NgFor` для представления списка элементов.

1.  Определите блок HTML, который определяет, как Angular отображает отдельный элемент.

1.  Чтобы перечислить элементы, назначьте сокращение `let item of items` для `*ngFor`.

<code-example header="src/app/app.component.html" path="built-in-directives/src/app/app/app.component.html" region="NgFor-1"></code-example>.

Строка `"let item of items"` инструктирует Angular делать следующее:

-   Хранить каждый элемент массива `items` в локальной циклической переменной `item`.

-   Сделать каждый элемент доступным в шаблоне HTML для каждой итерации.

-   Перевести `пусть элемент items` в `<ng-шаблон>` вокруг основного элемента.

-   Повторять `<ng-шаблон>` для каждого `пункта` в списке.

Для получения дополнительной информации смотрите раздел [Structural directive shorthand](guide/structural-directives#shorthand) раздела [Structural directives](guide/structural-directives).

### Повторение компонентного представления

Чтобы повторить элемент компонента, примените `*ngFor` к селектору. В следующем примере селектором является `<app-item-detail>`.

<code-example header="src/app/app.component.html" path="built-in-directives/src/app/app/app.component.html" region="NgFor-2"></code-example>.

Ссылайтесь на входную переменную шаблона, такую как `item`, в следующих местах:

-   В главном элементе `ngFor`.

-   В потомках главного элемента для доступа к свойствам элемента.

Следующий пример сначала ссылается на `item` в интерполяции, а затем передает привязку к свойству `item` компонента `<app-item-detail>`.

<code-example header="src/app/app.component.html" path="built-in-directives/src/app/app/app.component.html" region="NgFor-1-2"></code-example>.

Для получения дополнительной информации о входных переменных шаблона смотрите [Сокращение структурных директив](guide/structural-directives#shorthand).

### Получение `index` из `*ngFor`.

Получите `index` из `*ngFor` во входной переменной шаблона и используйте его в шаблоне.

В `*ngFor` добавьте точку с запятой и `let i=index` к сокращению. Следующий пример получает `index` в переменную с именем `i` и отображает его вместе с именем элемента.

<code-example header="src/app/app.component.html" path="built-in-directives/src/app/app/app.component.html" region="NgFor-3"></code-example>.

Свойство index контекста директивы `NgFor` возвращает нулевой индекс элемента в каждой итерации.

Angular переводит эту инструкцию в `<ng-template>` вокруг основного элемента, затем использует этот шаблон несколько раз для создания нового набора элементов и привязок для каждого `item`.

в списке.

Более подробную информацию о сокращении см. в руководстве [Structural Directives](guide/structural-directives#shorthand).

## Повторение элементов при истинности условия

Чтобы повторить блок HTML, когда определенное условие истинно, поместите `*ngIf` в контейнерный элемент, который обертывает элемент `*ngFor`.

Дополнительную информацию смотрите в разделе [одна структурная директива на элемент](guide/structural-directives#one-per-element).

<a id="ngfor-with-trackby"></a>

### Отслеживание элементов с `*ngFor` `trackBy`

Сократите количество обращений вашего приложения к серверу, отслеживая изменения в списке элементов. С помощью свойства `*ngFor` `trackBy`, Angular может изменять и перерисовывать только те элементы, которые изменились, вместо того, чтобы перезагружать весь список элементов.

1.  Добавьте в компонент метод, возвращающий значение, которое должен отслеживать `NgFor`.

    В данном примере значением для отслеживания является `id` элемента.

    Если браузер уже отобразил `id`, Angular отслеживает его и не запрашивает сервер повторно для получения того же `id`.

    <code-example header="src/app/app.component.ts" path="built-in-directives/src/app/app/app.component.ts" region="trackByItems"></code-example>.

1.  В сокращенном выражении установите `trackBy` на метод `trackByItems()`.

    <code-example header="src/app/app.component.html" path="built-in-directives/src/app/app/app.component.html" region="trackBy"></code-example>

**Изменение id** создает новые элементы с новыми `item.id`. В следующей иллюстрации эффекта `trackBy`, **Reset items** создает новые элементы с теми же `item.id`.

-   При отсутствии `trackBy` обе кнопки вызывают полную замену элементов DOM.

-   При использовании `trackBy` только изменение `id` вызывает замену элемента.

<div class="lightbox">

<img alt="Animation of trackBy" src="generated/images/guide/built-in-directives/ngfor-trackby.gif">

</div>

<a id="ngcontainer"></a>

## Размещение директивы без элемента DOM

Angular `<ng-container>` - это группирующий элемент, который не вмешивается в стили или макет, потому что Angular не помещает его в DOM.

Используйте `<ng-container>`, когда нет отдельного элемента для размещения директивы.

Вот условный параграф с использованием `<ng-container>`.

<code-example header="src/app/app.component.html (ngif-ngcontainer)" path="structural-directives/src/app/app.component.html" region="ngif-ngcontainer"></code-example>

<div class="lightbox">

<img alt="ngcontainer paragraph with proper style" src="generated/images/guide/structural-directives/good-paragraph.png">

</div>

1.  Import the `ngModel` directive from `FormsModule`.

1.  Add `FormsModule` to the imports section of the relevant Angular module.

1.  To conditionally exclude an `<option>`, wrap the `<option>` in an `<ng-container>`.

    <code-example header="src/app/app.component.html (select-ngcontainer)" path="structural-directives/src/app/app.component.html" region="select-ngcontainer"></code-example>

    <div class="lightbox">

    <img alt="ngcontainer options work properly" src="generated/images/guide/structural-directives/select-ngcontainer-anim.gif">

    </div>

<a id="ngSwitch"></a>

## Переключение случаев с помощью `NgSwitch`

Как и оператор JavaScript `switch`, `NgSwitch` отображает один элемент из нескольких возможных элементов, основываясь на условии переключения. Angular помещает в DOM только выбранный элемент.

<!--todo: API Flagged -->

`NgSwitch` - это набор из трех директив:

| Директивы `NgSwitch` | Подробности | | |:--- |:--- |.

| `NgSwitch` | Атрибутивная директива, которая изменяет поведение сопутствующих директив. |

| | `NgSwitchCase` | Структурная директива, которая добавляет свой элемент в DOM, когда его связанное значение равно значению switch и удаляет его связанное значение, когда оно не равно значению switch. |

| `NgSwitchDefault` | Структурная директива, которая добавляет свой элемент в DOM, когда нет выбранного `NgSwitchCase`. |

1.  On an element, such as a `<div>`, add `[ngSwitch]` bound to an expression that returns the switch value, such as `feature`.
    Though the `feature` value in this example is a string, the switch value can be of any type.

1.  Bind to `*ngSwitchCase` and `*ngSwitchDefault` on the elements for the cases.

    <code-example header="src/app/app.component.html" path="built-in-directives/src/app/app.component.html" region="NgSwitch"></code-example>

1.  In the parent component, define `currentItem`, to use it in the `[ngSwitch]` expression.

    <code-example header="src/app/app.component.ts" path="built-in-directives/src/app/app.component.ts" region="item"></code-example>

1.  In each child component, add an `item` [input property](guide/inputs-outputs#input 'Input property') which is bound to the `currentItem` of the parent component.

    The following two snippets show the parent component and one of the child components.

    The other child components are identical to `StoutItemComponent`.

    <code-example header="In each child component, here StoutItemComponent" path="built-in-directives/src/app/item-switch.component.ts" region="input"></code-example>

    <div class="lightbox">

    <img alt="Animation of NgSwitch" src="generated/images/guide/built-in-directives/ngswitch.gif">

    </div>

Switch directives also work with built-in HTML elements and web components. For example, you could replace the `<app-best-item>` switch case with a `<div>` as follows.

<code-example header="src/app/app.component.html" path="built-in-directives/src/app/app/app.component.html" region="NgSwitch-div"></code-example>

## Что дальше

Информацию о том, как создавать свои собственные пользовательские директивы, смотрите в [Attribute Directives](guide/attribute-directives) и [Structural Directives](guide/structural-directives).

<!-- links -->

<!-- external links -->

<!-- end links -->

@ просмотрено 2022-02-28
