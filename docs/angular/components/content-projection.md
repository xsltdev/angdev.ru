---
description: "Как передать в компонент внешнее содержимое через ng-content и разложить его по нескольким местам."
---

# Проекция содержимого через ng-content {: #content-projection-with-ng-content}

:date: 30.09.2026

!!! tip ""

    Этот материал предполагает, что вы уже прочитали [руководство по основам](../essentials/overview.md). Если Angular для вас в новинку, начните с него.

Часто нужен компонент-контейнер под разное содержимое. Например, своя карточка:

```ts
@Component({
  selector: 'custom-card',
  template: '<div class="card-shadow"> <!-- card content goes here --> </div>',
})
export class CustomCard {
  /* ... */
}
```

**Элемент `<ng-content>` ставят туда, куда должно попасть содержимое**:

```ts
@Component({
  selector: 'custom-card',
  template: '<div class="card-shadow"> <ng-content/> </div>',
})
export class CustomCard {
  /* ... */
}
```

!!! tip ""

    `<ng-content>` похож на [нативный элемент `<slot>`](https://developer.mozilla.org/docs/Web/HTML/Element/slot), но добавляет возможности, специфичные для Angular.

Если у компонента есть `<ng-content>`, дочерние узлы элемента-хоста отрисовываются, то есть **проецируются**, на место этого `<ng-content>`:

```ts
// Component source
@Component({
  selector: 'custom-card',
  template: `
    <div class="card-shadow">
      <ng-content />
    </div>
  `,
})
export class CustomCard {
  /* ... */
}
```

```html
<!-- Using the component -->
<custom-card>
  <p>This is the projected content</p>
</custom-card>
```

```html
<!-- The rendered DOM -->
<custom-card>
  <div class="card-shadow">
    <p>This is the projected content</p>
  </div>
</custom-card>
```

Дочерние узлы, переданные таким образом, Angular называет **содержимым** компонента. Это не то же самое, что **представление**: представление — элементы, заданные в шаблоне компонента.

**Элемент `<ng-content>` — не компонент и не DOM-элемент.** Это особый заполнитель: он говорит Angular, куда отрисовать содержимое. Компилятор обрабатывает все элементы `<ng-content>` на этапе сборки. Во время выполнения `<ng-content>` нельзя вставить, удалить или изменить. К `<ng-content>` нельзя добавить директивы, стили или произвольные атрибуты.

!!! warning ""

    Не включайте `<ng-content>` условно через `@if`, `@for` или `@switch`. Angular всегда создаёт экземпляр и DOM-узлы для содержимого, которое попадает в заполнитель `<ng-content>`, даже если этот заполнитель скрыт. Условная отрисовка содержимого компонента описана в [Фрагменты шаблона](https://angular.dev/api/core/ng-template).

## Несколько мест для содержимого {: #multiple-content-placeholders}

Angular умеет раскладывать разные элементы по разным заполнителям `<ng-content>` по CSS-селектору. Продолжая пример с карточкой, заголовок и тело можно развести атрибутом `select`:

```ts
@Component({
  selector: 'card-title',
  template: `<ng-content>card-title</ng-content>`,
})
export class CardTitle {}

@Component({
  selector: 'card-body',
  template: `<ng-content>card-body</ng-content>`,
})
export class CardBody {}
```

```ts
<!-- Component template -->
@Component({
  selector: 'custom-card',
  template: `
  <div class="card-shadow">
    <ng-content select="card-title" />
    <div class="card-divider"></div>
    <ng-content select="card-body" />
  </div>
  `,
})
export class CustomCard {}
```

```ts
<!-- Using the component -->
@Component({
  selector: 'app-root',
  imports: [CustomCard, CardTitle, CardBody],
  template: `
    <custom-card>
      <card-title>Hello</card-title>
      <card-body>Welcome to the example</card-body>
    </custom-card>
`,
})
export class App {}
```

```html
<!-- Rendered DOM -->
<custom-card>
  <div class="card-shadow">
    <card-title>Hello</card-title>
    <div class="card-divider"></div>
    <card-body>Welcome to the example</card-body>
  </div>
</custom-card>
```

Заполнитель `<ng-content>` принимает те же CSS-селекторы, что и [селекторы компонентов](selectors.md).

Если есть один или несколько заполнителей `<ng-content>` с атрибутом `select` и один `<ng-content>` без `select`, последний забирает все элементы, которые не совпали ни с одним `select`:

```html
<!-- Component template -->
<div class="card-shadow">
  <ng-content select="card-title" />
  <div class="card-divider"></div>
  <!-- capture anything except "card-title" -->
  <ng-content />
</div>
```

```html
<!-- Using the component -->
<custom-card>
  <card-title>Hello</card-title>
  <img src="..." />
  <p>Welcome to the example</p>
</custom-card>
```

```html
<!-- Rendered DOM -->
<custom-card>
  <div class="card-shadow">
    <card-title>Hello</card-title>
    <div class="card-divider"></div>
    <img src="..." />
    <p>Welcome to the example</p>
  </div>
</custom-card>
```

Если у компонента нет заполнителя `<ng-content>` без атрибута `select`, элементы, которые не совпали ни с одним заполнителем, в DOM не попадают.

## Запасное содержимое {: #fallback-content}

Если у заполнителя `<ng-content>` нет подходящего дочернего содержимого, Angular может показать _запасное содержимое_. Его задают дочерними узлами самого элемента `<ng-content>`.

```html
<!-- Component template -->
<div class="card-shadow">
  <ng-content select="card-title">Default Title</ng-content>
  <div class="card-divider"></div>
  <ng-content select="card-body">Default Body</ng-content>
</div>
```

```html
<!-- Using the component -->
<custom-card>
  <card-title>Hello</card-title>
  <!-- No card-body provided -->
</custom-card>
```

```html
<!-- Rendered DOM -->
<custom-card>
  <div class="card-shadow">
    <card-title>Hello</card-title>
    <div class="card-divider"></div>
    Default Body
  </div>
</custom-card>
```

## Псевдоним содержимого для проекции {: #aliasing-content-for-projection}

Специальный атрибут `ngProjectAs` задаёт элементу CSS-селектор. Когда элемент с `ngProjectAs` сверяют с заполнителем `<ng-content>`, Angular сравнивает значение `ngProjectAs`, а не сам элемент:

```html
<!-- Component template -->
<div class="card-shadow">
  <ng-content select="card-title" />
  <div class="card-divider"></div>
  <ng-content />
</div>
```

```html
<!-- Using the component -->
<custom-card>
  <h3 ngProjectAs="card-title">Hello</h3>

  <p>Welcome to the example</p>
</custom-card>
```

```html
<!-- Rendered DOM -->
<custom-card>
  <div class="card-shadow">
    <h3>Hello</h3>
    <div class="card-divider"></div>
    <p>Welcome to the example</p>
  </div>
</custom-card>
```

`ngProjectAs` принимает только статические значения и не привязывается к динамическим выражениям.

## Ограничения {: #caveats}

### Проецируемое содержимое живёт в представлении родителя {: #projected-content-lives-in-the-parents-view}

Проецируемое содержимое _отрисовывается_ внутри принимающего компонента, но принадлежит тому компоненту, который его объявил. Angular ведёт его как часть представления родителя, и из этого следуют два побочных эффекта.

**Обнаружение изменений.** Проецируемое содержимое проверяется, когда обнаружение изменений запускает _родитель_. Если принимающий компонент использует `OnPush`, Angular может пропустить проверку его собственного шаблона, но не пропустит проецируемое содержимое: оно принадлежит родителю.

```html
<!-- Parent template (default change detection) -->
<onpush-wrapper>
  <!-- Still checked on every parent cycle, OnPush doesn't help here -->
  <expensive-component />
</onpush-wrapper>
```

**Инъекция зависимостей.** Проецируемое содержимое получает зависимости из инжектора родителя, а не из `viewProviders` принимающего компонента. Подробнее в [Провайдеры и viewProviders](../di/hierarchical-dependency-injection.md).

### Не все библиотечные компоненты принимают проецируемых потомков {: #some-library-components-dont-support-projected-children}

Некоторые компоненты — меню, вкладки, списки — ищут потомков через `ContentChildren` и сами настраивают поведение: навигацию с клавиатуры, фокус, атрибуты ARIA. Они написаны в расчёте на то, что потомки принадлежат им напрямую, поэтому проекция чужого содержимого внутрь ломает это поведение неочевидным образом.

Например, если обернуть элементы `<mat-menu-item>` лишним слоем и спроецировать их в `<mat-menu>`, навигация с клавиатуры и поддержка экранных дикторов могут молча сломаться. Запрос по-прежнему находит пункты, но внутренняя настройка, которая делает их интерактивными, может работать неправильно, когда пункты приходят из другого контекста представления.

Если библиотечный компонент сам управляет поведением потомков, сначала загляните в его документацию: проекция содержимого может быть не предусмотрена.

---

Источник: [https://angular.dev/guide/components/content-projection](https://angular.dev/guide/components/content-projection)
