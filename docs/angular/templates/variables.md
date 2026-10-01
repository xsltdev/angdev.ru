---
description: "В шаблонах два вида объявлений переменных: локальные переменные шаблона и ссылочные переменные шаблона."
---

# Переменные в шаблонах {: #variables-in-templates}

:date: 30.09.2026

В шаблонах Angular два вида объявлений переменных: локальные переменные шаблона и ссылочные переменные шаблона.

!!! tip ""

    В этом руководстве «шаблон» — не весь HTML-файл шаблона. Речь только о конкретной конструкции или выражении шаблона внутри файла.

## Локальные переменные шаблона через `@let` {: #local-template-variables-with-let}

Синтаксис `@let` в Angular позволяет объявить локальную переменную и переиспользовать её в шаблоне — по аналогии с [синтаксисом `let` в JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/let).

### Использование `@let` {: #using-let}

Через `@let` объявляют переменную, значение которой берётся из результата выражения шаблона. Angular сам поддерживает значение переменной в соответствии с этим выражением, как и у [привязок](binding.md).

```html
@let name = user.name;
@let greeting = 'Hello, ' + name;
@let data = data$ | async;
@let pi = 3.14159;
@let coordinates = {x: 50, y: 100};
@let longExpression =
  'Lorem ipsum dolor sit amet, consectetur adipiscing elit ' +
  'sed do eiusmod tempor incididunt ut labore et dolore magna ' +
  'Ut enim ad minim veniam...';
```

Каждый блок `@let` объявляет ровно одну переменную. Несколько переменных в одном блоке через запятую объявить нельзя.

### Обращение к значению `@let` {: #referencing-the-value-of-let}

После объявления переменной через `@let` её можно переиспользовать в том же шаблоне:

```html
@let user = user$ | async;

@if (user) {
  <h1>Hello, {{ user.name }}</h1>
  <user-avatar [photo]="user.photo" />

  <ul>
    @for (snack of user.favoriteSnacks; track snack.id) {
      <li>{{ snack.name }}</li>
    }
  </ul>

  <button (click)="update(user)">Update profile</button>
}
```

### Присваиваемость {: #assignability}

Главное отличие `@let` от `let` в JavaScript: после объявления `@let` нельзя переприсвоить. При этом Angular сам поддерживает значение переменной в соответствии с заданным выражением.

```html
@let value = 1;

<!-- Invalid - This does not work! -->
<button (click)="value = value + 1">Increment the value</button>
```

### Область видимости переменной {: #variable-scope}

Объявления `@let` видны в текущем представлении и у его потомков. Angular создаёт новое представление на границах компонентов и там, где шаблон может содержать динамическое содержимое: блоки управления потоком, блоки `@defer` или структурные директивы.

Объявления `@let` не всплывают, поэтому родительские представления и соседи **не могут** к ним обратиться:

```html
@let topLevel = value;

<div>
  @let insideDiv = value;
</div>

<!-- Valid -->
{{ topLevel }}
<!-- Valid -->
{{ insideDiv }}

@if (condition) {
  <!-- Valid -->
  {{ topLevel + insideDiv }}

  @let nested = value;

  @if (condition) {
    <!-- Valid -->
    {{ topLevel + insideDiv + nested }}
  }
}

<!-- Error, not hoisted from @if -->
{{ nested }}
```

### Полный синтаксис {: #full-syntax}

Формально синтаксис `@let` задаётся так:

-   Ключевое слово `@let`.
-   Затем один или несколько пробельных символов, без перевода строки.
-   Затем допустимое имя JavaScript и ноль или более пробельных символов.
-   Затем символ `=` и ноль или более пробельных символов.
-   Затем выражение Angular, которое может занимать несколько строк.
-   Завершается символом `;`.

## Ссылочные переменные шаблона {: #template-reference-variables}

Ссылочные переменные шаблона позволяют объявить переменную, которая ссылается на значение элемента в шаблоне.

Ссылочная переменная шаблона может указывать на:

-   элемент DOM внутри шаблона (включая [пользовательские элементы](https://developer.mozilla.org/en-US/docs/Web/API/Web_components/Using_custom_elements))
-   компонент или директиву Angular
-   [TemplateRef](https://angular.dev/api/core/TemplateRef) из [ng-template](https://angular.dev/api/core/ng-template)

Через ссылочные переменные шаблона можно прочитать сведения из одной части шаблона в другой части того же шаблона.

### Объявление ссылочной переменной шаблона {: #declaring-a-template-reference-variable}

Переменную на элементе шаблона объявляют атрибутом, который начинается с символа решётки (`#`) и имени переменной.

```html
<!-- Create a template reference variable named "taskInput", referring to the HTMLInputElement. -->
<input #taskInput placeholder="Enter task name" />
```

### Присваивание значений ссылочным переменным шаблона {: #assigning-values-to-template-reference-variables}

Angular присваивает переменным шаблона значение по элементу, на котором переменная объявлена.

Если переменная объявлена на компоненте Angular, она ссылается на экземпляр компонента.

```html
<!-- The `startDate` variable is assigned the instance of `MyDatepicker`. -->
<my-datepicker #startDate />
```

Если переменная объявлена на элементе `<ng-template>`, она ссылается на экземпляр TemplateRef, который представляет шаблон. Подробнее — в разделе [Как Angular использует синтаксис звёздочки, \*](../directives/structural-directives.md#structural-directive-shorthand) статьи [Структурные директивы](../directives/structural-directives.md).

```html
<!-- The `myFragment` variable is assigned the `TemplateRef` instance corresponding to this template fragment. -->
<ng-template #myFragment>
  <p>This is a template fragment</p>
</ng-template>
```

Если переменная объявлена на любом другом отображаемом элементе, она ссылается на экземпляр `HTMLElement`.

```html
<!-- The "taskInput" variable refers to the HTMLInputElement instance. -->
<input #taskInput placeholder="Enter task name" />
```

#### Ссылка на директиву Angular {: #assigning-a-reference-to-an-angular-directive}

У директив Angular может быть свойство `exportAs`: оно задаёт имя, по которому на директиву ссылаются в шаблоне.

```ts
@Directive({
  selector: '[dropZone]',
  exportAs: 'dropZone',
})
export class DropZone {
  /* ... */
}
```

Когда переменная шаблона объявлена на элементе, ей можно присвоить экземпляр директивы, указав это имя `exportAs`:

```html
<!-- The `firstZone` variable refers to the `DropZone` directive instance. -->
<section dropZone #firstZone="dropZone">...</section>
```

На директиву без имени `exportAs` сослаться нельзя.

### Ссылочные переменные шаблона и запросы {: #using-template-reference-variables-with-queries}

Помимо чтения значений из другой части того же шаблона, таким объявлением переменной можно «пометить» элемент для [запросов компонентов и директив](https://angular.dev/guide/components/queries).

Чтобы запросить конкретный элемент шаблона, объявите на нём переменную шаблона и затем ищите элемент по имени этой переменной.

```html
<input #description value="Original description" />
```

```ts
@Component({
  /* ... */,
  template: `<input #description value="Original description">`,
})
export class AppComponent {
  // Query for the input element based on the template variable name.
  @ViewChild('description') input: ElementRef | undefined;
}
```

Подробнее о запросах — в статье [Ссылки на дочерние элементы через запросы](https://angular.dev/guide/components/queries).

### Область видимости переменной шаблона {: #template-variable-scope}

Как и переменные в коде JavaScript или TypeScript, переменные шаблона видны в том шаблоне, который их объявляет.

Так же [блоки управления потоком](control-flow.md) вроде `@if` и `@for`, [структурные директивы](../directives/structural-directives.md) и объявления `<ng-template>` создают новую вложенную область шаблона — подобно тому, как операторы `if` и `for` в JavaScript создают новые лексические области. К переменным шаблона внутри такой вложенной области снаружи не обратиться.

!!! tip ""

    Объявляйте переменную в шаблоне только один раз, чтобы значение во время выполнения оставалось предсказуемым.

#### Доступ во вложенном шаблоне {: #accessing-in-a-nested-template}

Внутренний шаблон может обращаться к переменным шаблона, которые объявил внешний.

В примере ниже изменение текста в `<input>` меняет значение в ``, потому что Angular сразу проводит изменения через переменную шаблона `ref1`.

```html
<input #ref1 type="text" [(ngModel)]="firstExample" />

@if (true) {
  <span>Value: {{ ref1.value }}</span>
}
```

В этом случае блок `@if` создаёт новую область шаблона, в которую входит переменная `ref1` из родительской области.

Обратиться к переменной шаблона из дочерней области в родительском шаблоне нельзя:

```html
@if (true) {
  <input #ref2 type="text" [(ngModel)]="secondExample" />
}

<span>Value: {{ ref2?.value }}</span>
```

Здесь `ref2` объявлена в дочерней области, которую создал `@if`, и из родительского шаблона недоступна.


---

Источник: [https://angular.dev/guide/templates/variables](https://angular.dev/guide/templates/variables)
