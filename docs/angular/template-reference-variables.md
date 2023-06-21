# Understanding template variables

Template variables help you use data from one part of a template in another part of the template. Use template variables to perform tasks such as respond to user input or finely tune your application's forms.

A template variable can refer to the following:

-   a DOM element within a template

-   a directive or component

-   a [TemplateRef](api/core/TemplateRef) from an [ng-template](api/core/ng-template)

-   a <a href="https://developer.mozilla.org/en-US/docs/Web/Web_Components" title="MDN: Web Components">web component</a>

<div class="alert is-helpful">

Смотрите <live-example></live-example> для рабочего примера, содержащего фрагменты кода, приведенные в этом руководстве.

</div>

## Prerequisites

-   [Understanding templates](guide/template-overview)

## Syntax

In the template, you use the hash symbol, `#`, to declare a template variable. The following template variable, `#phone`, declares a `phone` variable with the `<input>` element as its value.

<code-example path="template-reference-variables/src/app/app.component.html" region="ref-var" header="src/app/app.component.html"></code-example>

Refer to a template variable anywhere in the component's template. Here, a `<button>` further down the template refers to the `phone` variable.

<code-example path="template-reference-variables/src/app/app.component.html" region="ref-phone" header="src/app/app.component.html"></code-example>.

## Как Angular присваивает значения переменным шаблона

Angular присваивает переменной шаблона значение в зависимости от того, где вы объявили переменную:

-   Если вы объявляете переменную в компоненте, то переменная ссылается на экземпляр компонента.

-   Если вы объявите переменную в стандартном HTML-теге, переменная будет ссылаться на элемент.

-   Если вы объявляете переменную в элементе `<ng-template>`, переменная ссылается на экземпляр `TemplateRef`, который представляет шаблон.

    Дополнительную информацию о `<ng-template>` смотрите в [Как Angular использует синтаксис звездочки, `*`,](guide/structural-directives#asterisk) в [Structural directives](guide/structural-directives).

## Переменная, задающая имя

-   Если переменная указывает имя в правой части, например `#var="ngModel"`, переменная ссылается на директиву или компонент на элементе с соответствующим именем `exportAs`.

<!-- What does the second half of this mean?^^ Can we explain this more fully? Could I see a working example? -kw -->

### Using `NgForm` with template variables

In most cases, Angular sets the template variable's value to the element on which it occurs. In the previous example, `phone` refers to the phone number `<input>`.

The button's click handler passes the `<input>` value to the component's `callPhone()` method.

The `NgForm` directive demonstrates getting a reference to a different value by referencing a directive's `exportAs` name. In the following example, the template variable, `itemForm`, appears three times separated by HTML.

<code-example path="template-reference-variables/src/app/app.component.html" region="ngForm" header="src/app/hero-form.component.html"></code-example>.

Без значения атрибута `ngForm`, ссылочным значением `itemForm` будет [HTMLFormElement](https://developer.mozilla.org/en-US/docs/Web/API/HTMLFormElement), `<form>`.

Если элемент является компонентом Angular, то ссылка без значения атрибута будет автоматически ссылаться на экземпляр компонента. В противном случае ссылка без значения будет ссылаться на элемент DOM, даже если к элементу применены одна или несколько директив.

<!-- What is the train of thought from talking about a form element to the difference between a component and a directive? Why is the component directive conversation relevant here?  -kw I agree -alex -->

## Область видимости шаблонных переменных

Подобно переменным в коде JavaScript или TypeScript, переменные шаблона привязаны к шаблону, который их объявляет.

Аналогично, [структурные директивы](guide/built-in-directives), такие как `*ngIf` и `*ngFor`, или объявления `<ng-template>` создают новую вложенную область видимости шаблона, подобно тому, как операторы потока управления JavaScript, такие как `if` и `for`, создают новые лексические области видимости. Вы не можете получить доступ к переменным шаблона внутри одной из этих структурных директив извне ее границ.

<div class="alert is-helpful">

Определите переменную только один раз в шаблоне, чтобы ее значение во время выполнения оставалось предсказуемым.

</div>

### Accessing in a nested template

An inner template can access template variables that the outer template defines.

In the following example, changing the text in the `<input>` changes the value in the `<span>` because Angular immediately updates changes through the template variable, `ref1`.

<code-example path="template-reference-variables/src/app/app.component.html" region="template-ref-vars-scope1" header="src/app/app.component.html"></code-example>

In this case, the `*ngIf` on `<span>` creates a new template scope, which includes the `ref1` variable from its parent scope.

However, accessing a template variable from a child scope in the parent template doesn't work:

```html <input *ngIf="true" #ref2 type="text" [(ngModel)]="secondExample" />
<span>Value: {{ ref2?.value }}</span>
<!-- doesn't work -->
```

Здесь `ref2` объявлена в дочерней области видимости, созданной `*ngIf`, и недоступна из родительского шаблона.

{@a template-input-variable} {@a template-input-variables}

## Входная переменная шаблона

Входная переменная _шаблона_ - это переменная со значением, которое устанавливается при создании экземпляра этого шаблона. См: [Написание структурных директив](/guide/structural-directives)

Входные переменные шаблона можно увидеть в действии в длинной форме использования `NgFor`:

```html <ul>
  <ng-template ngFor let-hero [ngForOf]="heroes">
    <li>{{hero.name}}
  </ng-template>
</ul>
```

Директива `NgFor` будет инстанцировать этот <ng-шаблон> один раз для каждого героя в массиве `heroes` и установит переменную `hero` для каждого экземпляра соответственно.

При инстанцировании `<ng-шаблона>` может быть передано несколько именованных значений, которые могут быть привязаны к различным входным переменным шаблона. В правой части объявления `let-` входной переменной можно указать, какое значение должно быть использовано для этой переменной.

Например, `NgFor` также предоставляет доступ к `index` каждого героя в массиве:

```html <ul>
  <ng-template ngFor let-hero let-i="index" [ngForOf]="heroes">
    <li>Hero number {{i}}: {{hero.name}}
  </ng-template>
</ul>
```

## Что дальше

[Написание структурных директив](/guide/structural-directives)

@reviewed 2022-05-12
