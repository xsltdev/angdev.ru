# Проекция содержимого

В этой теме описывается, как использовать проекцию содержимого для создания гибких, многократно используемых компонентов.

<div class="alert is-helpful">

Для просмотра или загрузки кода примера, использованного в этой теме, см. <live-example></live-example>.

</div>

Проекция содержимого - это шаблон, в котором вы вставляете, или _проектируете_, содержимое, которое хотите использовать, внутрь другого компонента. Например, у вас может быть компонент `Card`, который принимает содержимое, предоставленное другим компонентом.

В следующих разделах описываются общие реализации проекции содержимого в Angular, включая:

| Проекция контента | Подробности | |:--- |:--- |:---.

| [Single-slot content projection](#single-slot) | При этом типе проекции контента компонент принимает контент из одного источника. |

| [Multi-slot content projection](#multi-slot) | В этом сценарии компонент принимает содержимое из нескольких источников. |

| | [Условная проекция контента](#conditional) | Компоненты, использующие условную проекцию контента, отображают контент только при выполнении определенных условий. |

<a id="single-slot"></a>

## Однослотовая проекция контента

Самой основной формой проекции контента является _однослотовая проекция контента_. Однослотовая проекция содержимого относится к созданию компонента, в который вы можете спроецировать один компонент.

Чтобы создать компонент, использующий однослотовую проекцию содержимого, выполните следующие действия:

1.  [Создать компонент] (guide/component-overview#creating-a-component).

1.  В шаблоне компонента добавьте элемент `<ng-content>` в то место, где должно отображаться проецируемое содержимое.

Например, следующий компонент использует элемент `<ng-content>` для отображения сообщения.

<code-example header="content-projection/src/app/zippy-basic/zippy-basic.component.ts" path="content-projection/src/app/zippy-basic/zippy-basic.component.ts"></code-example>.

С установленным элементом `<ng-content>` пользователи этого компонента теперь могут проецировать свое собственное сообщение в компонент. Например:

<code-example header="content-projection/src/app/app.component.html" path="content-projection/src/app/app.component.html" region="single-slot"></code-example>

<div class="alert is-helpful">

Элемент `<ng-content>` - это заполнитель, который не создает реального элемента DOM. Пользовательские атрибуты, применяемые к `<ng-content>`, игнорируются.

</div>

<a id="multi-slot"></a>

## Проекция содержимого на несколько слотов

Компонент может иметь несколько слотов. Каждый слот может определять CSS-селектор, который определяет, какое содержимое попадает в этот слот.

Этот шаблон называется _проекция содержимого на несколько слотов_.

При использовании этого шаблона вы должны указать, где должно отображаться проецируемое содержимое.

Для этого используется атрибут `select` в `<ng-content>`.

Чтобы создать компонент, использующий многослотовую проекцию содержимого, выполните следующие действия:

1.  [Создать компонент](guide/component-overview#creating-a-component).

1.  В шаблоне компонента добавьте элемент `<ng-content>`, в котором должно отображаться проецируемое содержимое.

1.  Добавьте атрибут `select` к элементам `<ng-content>`.

    Angular поддерживает [selectors](https://developer.mozilla.org/docs/Web/CSS/CSS_Selectors) для любой комбинации имени тега, атрибута, CSS-класса и псевдокласса `:not`.

    Например, следующий компонент использует два элемента `<ng-content>`.

    <code-example header="content-projection/src/app/zippy-multislot/zippy-multislot.component.ts" path="content-projection/src/app/zippy-multislot/zippy-multislot.component.ts"></code-example>.

Содержимое, использующее атрибут `question`, проецируется в элемент `<ng-content>` с атрибутом `select=[question]`.

<code-example header="content-projection/src/app/app.component.html" path="content-projection/src/app/app.component.html" region="multi-slot"></code-example>.

<div class="callout is-helpful">

<header>ng-content without a select attribute</header>

Если ваш компонент включает элемент `<ng-content>` без атрибута `select`, этот экземпляр получает все спроецированные компоненты, которые не соответствуют ни одному из других элементов `<ng-content>`.

В предыдущем примере только второй элемент `<ng-content>` определяет атрибут `select`. В результате первый элемент `<ng-content>` получает любое другое содержимое, проецируемое в компонент.

</div>

<a id="conditional"></a>

## Условное проецирование содержимого

Если ваш компонент должен _условно_ отображать содержимое или отображать его несколько раз, вы должны настроить этот компонент на прием элемента `<ng-template>`, который содержит содержимое, которое вы хотите условно отобразить.

Использование элемента `<ng-content>` в этих случаях не рекомендуется, потому что когда потребитель компонента предоставляет содержимое, это содержимое _всегда_ инициализируется, даже если компонент не определяет элемент `<ng-content>` или если этот элемент `<ng-content>` находится внутри оператора `ngIf`.

С помощью элемента `<ng-template>` вы можете заставить свой компонент явно выводить содержимое на основе любого условия, сколько угодно раз. Angular не будет инициализировать содержимое элемента `<ng-template>` до тех пор, пока этот элемент не будет явно отрисован.

Следующие шаги демонстрируют типичную реализацию условного проецирования содержимого с использованием `<ng-template>`.

1.  [Create a component](guide/component-overview#creating-a-component).
1.  In the component that accepts an `<ng-template>` element, use an `<ng-container>` element to render that template, such as:

    <code-example header="content-projection/src/app/example-zippy.template.html" path="content-projection/src/app/example-zippy.template.html" region="ng-container"></code-example>

    This example uses the `ngTemplateOutlet` directive to render a given `<ng-template>` element, which you will define in a later step.
    You can apply an `ngTemplateOutlet` directive to any type of element.
    This example assigns the directive to an `<ng-container>` element because the component does not need to render a real DOM element.

1.  Wrap the `<ng-container>` element in another element, such as a `div` element, and apply your conditional logic.

    <code-example header="content-projection/src/app/example-zippy.template.html" path="content-projection/src/app/example-zippy.template.html" region="ngif"></code-example>

1.  In the template where you want to project content, wrap the projected content in an `<ng-template>` element, such as:

    <code-example header="content-projection/src/app/app.component.html"  region="ng-template" path="content-projection/src/app/app.component.html"></code-example>

    The `<ng-template>` element defines a block of content that a component can render based on its own logic.
    A component can get a reference to this template content, or `TemplateRef`, by using either the `@ContentChild` or `@ContentChildren` decorators.
    The preceding example creates a custom directive, `appExampleZippyContent`, as an API to mark the `<ng-template>` for the component's content.
    With the `TemplateRef`, the component can render the referenced content by using either the `ngTemplateOutlet` directive, or with the `ViewContainerRef` method `createEmbeddedView()`.

1.  [Create an attribute directive](guide/attribute-directives#building-an-attribute-directive) with a selector that matches the custom attribute for your template.
    In this directive, inject a `TemplateRef` instance.

    <code-example header="content-projection/src/app/example-zippy.component.ts" path="content-projection/src/app/example-zippy.component.ts" region="zippycontentdirective"></code-example>

    In the previous step, you added an `<ng-template>` element with a custom attribute, `appExampleZippyContent`.
    This code provides the logic that Angular will use when it encounters that custom attribute.
    In this case, that logic instructs Angular to instantiate a template reference.

1.  In the component you want to project content into, use `@ContentChild` to get the template of the projected content.

    <code-example header="content-projection/src/app/example-zippy.component.ts" path="content-projection/src/app/example-zippy.component.ts" region="contentchild"></code-example>

    Prior to this step, your application has a component that instantiates a template when certain conditions are met.
    You've also created a directive that provides a reference to that template.
    In this last step, the `@ContentChild` decorator instructs Angular to instantiate the template in the designated component.

    <div class="alert is-helpful">

    In the case of multi-slot content projection, use `@ContentChildren` to get a `QueryList` of projected elements.

    </div>

<a id="ngprojectas"></a>

## Проецирование содержимого в более сложных средах

Как описано в [Многослотовое проецирование содержимого](#multi-slot), вы обычно используете либо атрибут, либо элемент, либо CSS-класс, либо некоторую комбинацию всех трех для определения места проецирования содержимого. Например, в следующем шаблоне HTML тег абзаца использует пользовательский атрибут `question` для проецирования содержимого в компонент `app-zippy-multislot`.

<code-example header="content-projection/src/app/app.component.html" path="content-projection/src/app/app.component.html" region="multi-slot"></code-example>.

В некоторых случаях вы можете захотеть спроецировать содержимое как другой элемент. Например, содержимое, которое вы хотите спроецировать, может быть дочерним элементом другого элемента.

Для этого используется атрибут `ngProjectAs`.

Например, рассмотрим следующий фрагмент HTML:

<code-example header="content-projection/src/app/app.component.html" path="content-projection/src/app/app.component.html" region="ngprojectas"></code-example>.

В этом примере используется атрибут `<ng-container>` для имитации проецирования компонента в более сложную структуру.

<div class="callout is-helpful">

<header>Reminder</header>

Элемент `ng-container` - это логическая конструкция, которая используется для группировки других элементов DOM; однако сам `ng-container` не отображается в дереве DOM.

</div>

В данном примере содержимое, которое мы хотим спроецировать, находится внутри другого элемента. Чтобы спроецировать это содержимое, шаблон использует атрибут `ngProjectAs`.
С помощью `ngProjectAs` весь элемент `<ng-container>` проецируется в компонент с помощью селектора `[question]`.

<!-- links -->

<!-- external links -->

<!-- end links -->

@ просмотрено 2022-02-28
