---
description: "Синтаксис шаблонов Angular для динамических интерфейсов."
---

# Шаблоны {: #templates}

:date: 30.09.2026

Синтаксис шаблонов Angular для динамических интерфейсов.

Шаблон компонента — это не только статический HTML. Он берёт данные из класса компонента и вешает обработчики действий пользователя.

## Динамический текст {: #showing-dynamic-text}

В Angular _привязка_ связывает шаблон компонента с его данными. Когда данные меняются, отрисованный шаблон обновляется сам.

Динамический текст в шаблоне выводят привязкой в двойных фигурных скобках:

```ts
@Component({
  selector: 'user-profile',
  template: `<h1>Profile for {{ userName() }}</h1>`,
})
export class UserProfile {
  userName = signal('pro_programmer_123');
}
```

Когда Angular отрисует компонент, на странице будет:

```html
<h1>Profile for pro_programmer_123</h1>
```

Angular сам поддерживает привязку в актуальном состоянии, когда меняется значение сигнала. Если в примере выше обновить сигнал `userName`:

```ts
this.userName.set('cool_coder_789');
```

Страница обновится и покажет новое значение:

```html
<h1>Profile for cool_coder_789</h1>
```

## Динамические свойства и атрибуты {: #setting-dynamic-properties-and-attributes}

Динамическое значение попадает в свойство DOM через квадратные скобки:

```ts
@Component({
  /*...*/
  // Set the `disabled` property of the button based on the value of `isValidUserId`.
  template: `<button [disabled]="!isValidUserId()">Save changes</button>`,
})
export class UserProfile {
  isValidUserId = signal(false);
}
```

К HTML-_атрибуту_ привязываются так же, если перед именем поставить `attr.`:

```html
<!-- Bind the `role` attribute on the `<ul>` element to value of `listRole`. -->
<ul [attr.role]="listRole()"></ul>
```

Когда привязанное значение меняется, Angular сам обновляет свойства и атрибуты DOM.

## Действия пользователя {: #handling-user-interaction}

Слушатель события вешают на элемент шаблона круглыми скобками:

```ts
@Component({
  /*...*/
  // Add an 'click' event handler that calls the `cancelSubscription` method.
  template: `<button (click)="cancelSubscription()">Cancel subscription</button>`,
})
export class UserProfile {
  /* ... */

  cancelSubscription() {
    /* Your event handling code goes here. */
  }
}
```

Чтобы передать слушателю объект [события](https://developer.mozilla.org/docs/Web/API/Event), в вызове функции используют встроенную переменную `$event`:

```ts
@Component({
  /*...*/
  // Add an 'click' event handler that calls the `cancelSubscription` method.
  template: `<button (click)="cancelSubscription($event)">Cancel subscription</button>`,
})
export class UserProfile {
  /* ... */

  cancelSubscription(event: Event) {
    /* Your event handling code goes here. */
  }
}
```

## Управление потоком: `@if` и `@for` {: #control-flow-with-if-and-for}

Части шаблона показывают и скрывают по условию блоком `@if`:

```html
<h1>User profile</h1>

@if (isAdmin()) {
  <h2>Admin settings</h2>
  <!-- ... -->
}
```

У блока `@if` есть необязательная ветка `@else`:

```html
<h1>User profile</h1>

@if (isAdmin()) {
  <h2>Admin settings</h2>
  <!-- ... -->
} @else {
  <h2>User settings</h2>
  <!-- ... -->
}
```

Фрагмент шаблона повторяют блоком `@for`:

```html
<h1>User profile</h1>

<ul class="user-badge-list">
  @for (badge of badges(); track badge.id) {
    <li class="user-badge">{{ badge.name }}</li>
  }
</ul>
```

Ключевое слово `track` из примера выше связывает данные с элементами DOM, которые создаёт `@for`. Подробнее — [_Зачем нужен track в блоках @for?_](../templates/control-flow.md#why-is-track-in-for-blocks-important).

!!! tip ""

    Подробнее о шаблонах Angular — в [подробном руководстве по шаблонам](../templates/overview.md).

## Следующий шаг {: #next-step}

Динамические данные и шаблоны уже в приложении. Дальше — как усилить шаблоны: скрывать и показывать элементы по условию, проходить по ним циклом и не только.

-   [Формы с сигналами](signal-forms.md)
-   [Подробное руководство по шаблонам](../templates/overview.md)


---

Источник: [https://angular.dev/essentials/templates](https://angular.dev/essentials/templates)
