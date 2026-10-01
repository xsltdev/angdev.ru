---
description: "Привязка связывает шаблон компонента с его данными и обновляет отрисовку, когда эти данные меняются."
---

# Привязка динамического текста, свойств и атрибутов {: #binding-dynamic-text-properties-and-attributes}

:date: 30.09.2026

В Angular **привязка** создаёт динамическую связь между шаблоном компонента и его данными. Благодаря этой связи изменения данных компонента автоматически обновляют отрисованный шаблон.

## Динамический текст через интерполяцию {: #render-dynamic-text-with-text-interpolation}

Динамический текст в шаблоне привязывают двойными фигурными скобками: Angular берёт на себя выражение внутри и следит, чтобы оно обновлялось правильно. Это называется **интерполяцией текста**.

```ts
@Component({
  template: `
    <p>Your color preference is {{ theme }}.</p>
  `,
  ...
})
export class App {
  theme = 'dark';
}
```

В этом примере при отрисовке фрагмента на странице Angular заменит `{{ theme }}` на `dark`.

```html
<!-- Rendered Output -->
<p>Your color preference is dark.</p>
```

Привязки, которые меняются со временем, должны читать значения из [сигналов](../signals/overview.md). Angular отслеживает сигналы, прочитанные в шаблоне, и обновляет отрисованную страницу, когда значения этих сигналов меняются.

```ts
@Component({
  template: `
    <!-- Does not necessarily update when `welcomeMessage` changes. -->
    <p>{{ welcomeMessage }}</p>

    <p>Your color preference is {{ theme() }}.</p> <!-- Always updates when the value of the `theme` signal changes. -->
  `
  ...
})
export class App {
  welcomeMessage = "Welcome, enjoy this app that we built for you";
  theme = signal('dark');
}
```

Подробнее — в [руководстве по сигналам](../signals/overview.md).

Если продолжить пример с темой: после загрузки страницы пользователь нажимает кнопку, которая обновляет сигнал `theme` до `'light'`, и страница обновляется так:

```html
<!-- Rendered Output -->
<p>Your color preference is light.</p>
```

Интерполяцию текста можно использовать везде, где в HTML обычно пишут текст.

Все значения выражений приводятся к строке. Объекты и массивы преобразуются методом `toString` значения.

## Привязка динамических свойств и атрибутов {: #binding-dynamic-properties-and-attributes}

Angular умеет привязывать динамические значения к свойствам объектов и атрибутам HTML через квадратные скобки.

Привязка работает со свойствами экземпляра DOM элемента HTML, экземпляра [компонента](../components/anatomy-of-components.md) или экземпляра [директивы](../directives/overview.md).

### Свойства нативных элементов {: #native-element-properties}

У каждого элемента HTML есть соответствующее представление в DOM. Например, каждому элементу `<button>` соответствует экземпляр `HTMLButtonElement`. В Angular привязка свойства записывает значение прямо в это представление элемента в DOM.

```html
<!-- Bind the `disabled` property on the button element's DOM object -->
<button [disabled]="isFormValid()">Save</button>
```

В этом примере при каждом изменении `isFormValid` Angular автоматически выставляет свойство `disabled` экземпляра `HTMLButtonElement`.

### Свойства компонентов и директив {: #component-and-directive-properties}

Если элемент — компонент Angular, той же записью в квадратных скобках привязка свойства задаёт входные свойства компонента.

```html
<!-- Bind the `value` property on the `MyListbox` component instance. -->
<my-listbox [value]="mySelection()" />
```

В этом примере при каждом изменении `mySelection` Angular автоматически выставляет свойство `value` экземпляра `MyListbox`.

Так же привязываются и свойства директив.

```html
<!-- Bind to the `ngSrc` property of the `NgOptimizedImage` directive  -->
<img [ngSrc]="profilePhotoUrl()" alt="The current user's profile photo" />
```

### Атрибуты {: #attributes}

Если нужно задать атрибут HTML, у которого нет соответствующего свойства DOM, например атрибут SVG, его привязывают к элементу шаблона с префиксом `attr.`.

```html
<!-- Bind the `role` attribute on the `<ul>` element to the component's `listRole` property. -->
<ul [attr.role]="listRole()">
```

В этом примере при каждом изменении `listRole` Angular автоматически задаёт атрибут `role` элемента `<ul>`, вызывая `setAttribute`.

Если значение привязки атрибута равно `null`, Angular удаляет атрибут вызовом `removeAttribute`.

### Интерполяция текста в свойствах и атрибутах {: #text-interpolation-in-properties-and-attributes}

Интерполяцию текста можно использовать и в свойствах, и в атрибутах: вместо квадратных скобок вокруг имени свойства или атрибута ставят двойные фигурные. При таком синтаксисе Angular считает присваивание привязкой свойства.

```html
<!-- Binds a value to the `alt` property of the image element's DOM object. -->
<img src="profile-photo.jpg" alt="Profile photo of {{ firstName() }}" />
```

## Привязки CSS-классов и CSS-свойств {: #css-class-and-style-property-bindings}

Для привязки CSS-классов и CSS-свойств к элементам у Angular есть дополнительные возможности.

### CSS-классы {: #css-classes}

Привязка CSS-класса условно добавляет или снимает класс с элемента в зависимости от того, [истинно или ложно](https://developer.mozilla.org/en-US/docs/Glossary/Truthy) привязанное значение.

```html
<!-- When `isExpanded` is truthy, add the `expanded` CSS class. -->
<ul [class.expanded]="isExpanded()">
```

Можно привязаться и напрямую к свойству `class`. Angular принимает три вида значений:

| Описание значения `class` | Тип TypeScript |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------- |
| Строка с одним или несколькими CSS-классами через пробел | `string` |
| Массив строк с CSS-классами | `string[]` |
| Объект, где имя каждого свойства — имя CSS-класса, а соответствующее значение по истинности решает, применяется ли этот класс к элементу | `Record<string, any>` |

```ts
@Component({
  template: `
    <ul [class]="listClasses"> ... </ul>
    <section [class]="sectionClasses()"> ... </section>
    <button [class]="buttonClasses()"> ... </button>
  `,
  ...
})
export class UserProfile {
  listClasses = 'full-width outlined';
  sectionClasses = signal(['expandable', 'elevated']);
  buttonClasses = signal({
    highlighted: true,
    embiggened: false,
  });
}
```

Пример выше отрисовывает такой DOM:

```html
<ul class="full-width outlined"> ... </ul>
<section class="expandable elevated"> ... </section>
<button class="highlighted"> ... </button>
```

Angular игнорирует строковые значения, которые не являются допустимыми именами CSS-классов.

Если одновременно заданы статические CSS-классы, прямая привязка `class` и привязка отдельных классов, Angular собирает все эти классы в отрисованном результате.

```ts
@Component({
  template: `<ul class="list" [class]="listType()" [class.expanded]="isExpanded()"> ...`,
  ...
})
export class Listbox {
  listType = signal('box');
  isExpanded = signal(true);
}
```

В примере выше Angular отрисовывает элемент `ul` со всеми тремя CSS-классами.

```html
<ul class="list box expanded">
```

Angular не гарантирует конкретный порядок CSS-классов на отрисованных элементах.

Когда `class` привязан к массиву или объекту, Angular сравнивает предыдущее значение с текущим оператором тройного равенства (`===`). Чтобы Angular применил обновления, при изменении этих значений нужно создавать новый экземпляр объекта или массива.

Если у элемента несколько привязок одного и того же CSS-класса, Angular разрешает столкновения по своему порядку приоритета стилей.

!!! info ""

    Привязки классов не поддерживают имена классов через пробел в одном ключе. Они также не поддерживают мутации объектов: ссылка привязки остаётся той же. Если нужно одно или другое, используйте директиву [ngClass](https://angular.dev/api/common/NgClass).

### CSS-свойства {: #css-style-properties}

CSS-свойства тоже можно привязывать прямо на элементе.

```html
<!-- Set the CSS `display` property based on the `isExpanded` property. -->
<section [style.display]="isExpanded() ? 'block' : 'none'">
```

Для CSS-свойств, которые принимают единицы, можно указать единицу измерения.

```html
<!-- Set the CSS `height` property to a pixel value based on the `sectionHeightInPixels` property. -->
<section [style.height.px]="sectionHeightInPixels()">
```

Несколько значений стиля можно задать одной привязкой. Angular принимает такие виды значений:

| Описание значения `style` | Тип TypeScript |
| ------------------------------------------------------------------------------------------------------------------------- | --------------------- |
| Строка с нулём или более объявлений CSS, например `"display: flex; margin: 8px"`. | `string` |
| Объект, где имя каждого свойства — имя CSS-свойства, а соответствующее значение — значение этого CSS-свойства. | `Record<string, any>` |

```ts
@Component({
  template: `
    <ul [style]="listStyles()"> ... </ul>
    <section [style]="sectionStyles()"> ... </section>
  `,
  ...
})
export class UserProfile {
  listStyles = signal('display: flex; padding: 8px');
  sectionStyles = signal({
    border: '1px solid black',
    'font-weight': 'bold',
  });
}
```

Пример выше отрисовывает такой DOM.

```html
<ul style="display: flex; padding: 8px"> ... </ul>
<section style="border: 1px solid black; font-weight: bold"> ... </section>
```

Когда `style` привязан к объекту, Angular сравнивает предыдущее значение с текущим оператором тройного равенства (`===`). Чтобы Angular применил обновления, при изменении этих значений нужно создавать новый экземпляр объекта.

Если у элемента несколько привязок одного и того же свойства стиля, Angular разрешает столкновения по своему порядку приоритета стилей.

## Атрибуты ARIA {: #aria-attributes}

Angular поддерживает привязку строковых значений к атрибутам ARIA.

```html
<button type="button" [aria-label]="actionLabel()">
  {{ actionLabel() }}
</button>
```

Angular записывает строковое значение в атрибут `aria-label` элемента и удаляет его, когда привязанное значение равно `null`.

Некоторые возможности ARIA открывают свойства DOM или входы директив, которые принимают структурированные значения (например, ссылки на элементы). В таких случаях используйте обычную привязку свойства. Примеры и дополнительные пояснения — в [руководстве по доступности](https://angular.dev/best-practices/a11y#aria-attributes-and-properties).


---

Источник: [https://angular.dev/guide/templates/binding](https://angular.dev/guide/templates/binding)
