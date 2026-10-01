---
description: "Как устроен элемент-хост компонента и как привязать к нему свойства, атрибуты, стили и события."
---

# Элементы-хосты компонентов {: #component-host-elements}

:date: 30.09.2026

!!! tip ""

    Этот материал предполагает, что вы уже прочитали [руководство по основам](../essentials/overview.md). Если Angular для вас в новинку, начните с него.

Angular создаёт экземпляр компонента для каждого HTML-элемента, который совпал с селектором компонента. DOM-элемент, совпавший с селектором, — это **элемент-хост** компонента. Содержимое шаблона отрисовывается внутри элемента-хоста.

```ts
// Component source
@Component({
  selector: 'profile-photo',
  template: `<img src="profile-photo.jpg" alt="Your profile photo" />`,
})
export class ProfilePhoto {}
```

```html
<!-- Using the component -->
<h3>Your profile photo</h3>
<profile-photo />
<button>Upload a new profile photo</button>
```

```html
<!-- Rendered DOM -->
<h3>Your profile photo</h3>
<profile-photo>
  <img src="profile-photo.jpg" alt="Your profile photo" />
</profile-photo>
<button>Upload a new profile photo</button>
```

В примере выше `<profile-photo>` — элемент-хост компонента `ProfilePhoto`.

## Привязка к элементу-хосту {: #binding-to-the-host-element}

Компонент может привязать к своему элементу-хосту свойства, атрибуты, стили и события. Это те же привязки, что и у элементов внутри шаблона, только задаются они свойством `host` в декораторе `@Component`:

```ts
@Component({
  ...,
  host: {
    'role': 'slider',
    '[attr.aria-valuenow]': 'value',
    '[class.active]': 'isActive()',
    '[style.background]' : `hasError() ? 'red' : 'green'`,
    '[tabIndex]': 'disabled ? -1 : 0',
    '(keydown)': 'updateValue($event)',
  },
})
export class CustomSlider {
  value: number = 0;
  disabled: boolean = false;
  isActive = signal(false);
  hasError = signal(false);
  updateValue(event: KeyboardEvent) { /* ... */ }

  /* ... */
}
```

!!! info ""

    К имени события можно добавить глобальную цель: `document:`, `window:` или `body:`.

!!! info ""

    Имена клавиш вроде `'(keydown.enter)'` сравниваются с `KeyboardEvent.key` и зависят от раскладки и языка ввода. Чтобы попасть в физическую клавишу независимо от раскладки, используйте модификатор `code`, например `'(keydown.code.Enter)'`. Подробнее в разделе [Модификаторы клавиш](../templates/event-listeners.md#using-key-modifiers).

## Декораторы `@HostBinding` и `@HostListener` {: #the-hostbinding-and-hostlistener-decorators}

К элементу-хосту можно привязаться и декораторами `@HostBinding` и `@HostListener` на членах класса.

`@HostBinding` привязывает свойства и атрибуты хоста к свойствам и геттерам:

```ts
@Component({/* ... */})
export class CustomSlider {
  @HostBinding('attr.aria-valuenow')
  value: number = 0;

  @HostBinding('tabIndex')
  get tabIndex() {
    return this.disabled ? -1 : 0;
  }

  /* ... */
}
```

`@HostListener` вешает обработчик события на элемент-хост. Декоратор принимает имя события и необязательный массив аргументов:

```ts
export class CustomSlider {
  @HostListener('keydown', ['$event'])
  updateValue(event: KeyboardEvent) {
    /* ... */
  }
}
```

!!! danger "Предпочитайте свойство `host` декораторам"

    **Всегда предпочитайте свойство `host` декораторам `@HostBinding` и `@HostListener`.** Эти декораторы оставлены только для обратной совместимости.

## Конфликты привязок {: #binding-collisions}

В шаблоне на элемент экземпляра компонента можно повесить свои привязки. Компонент _тоже_ может задать привязки хоста к тем же свойствам или атрибутам.

```ts
@Component({
  ...,
  host: {
    'role': 'presentation',
    '[id]': 'id',
  }
})
export class ProfilePhoto { /* ... */ }
```

```html
<profile-photo role="group" [id]="otherId" />
```

Какое значение победит, решают такие правила:

-   Если оба значения статические, побеждает привязка экземпляра.
-   Если одно значение статическое, а другое динамическое, побеждает динамическое.
-   Если оба значения динамические, побеждает привязка хоста компонента.

## Стили через пользовательские свойства CSS {: #styling-with-css-custom-properties}

Стили компонента часто настраивают через [пользовательские свойства CSS](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_cascading_variables/Using_CSS_custom_properties). На элемент-хост их задают [привязкой стиля](../templates/binding.md#css-style-properties).

```ts
@Component({
  /* ... */
  host: {
    '[style.--my-background]': 'color()',
  },
})
export class MyComponent {
  color = signal('lightgreen');
}
```

В примере пользовательское свойство CSS `--my-background` привязано к сигналу `color`. Значение свойства обновляется само, когда меняется сигнал `color`. Это затрагивает текущий компонент и всех потомков, которые опираются на это свойство.

### Пользовательские свойства на дочерних компонентах {: #setting-custom-properties-on-children-components}

Пользовательские свойства CSS можно задать и на элементе-хосте дочернего компонента той же [привязкой стиля](../templates/binding.md#css-style-properties).

```ts
@Component({
  selector: 'my-component',
  template: `<my-child [style.--my-background]="color()" />`,
})
export class MyComponent {
  color = signal('lightgreen');
}
```

## Чтение атрибутов элемента-хоста {: #injecting-host-element-attributes}

Компоненты и директивы читают статические атрибуты своего элемента-хоста через `HostAttributeToken` и функцию [`inject`](https://angular.dev/api/core/inject).

```ts
import { Component, HostAttributeToken, inject } from '@angular/core';

@Component({
  selector: 'app-button',
  ...,
})
export class Button {
  variation = inject(new HostAttributeToken('variation'));
}
```

```html
<app-button variation="primary">Click me</app-button>
```

!!! tip ""

    `HostAttributeToken` выбрасывает ошибку, если атрибут отсутствует, кроме случая, когда инъекция помечена как необязательная.

---

Источник: [https://angular.dev/guide/components/host-elements](https://angular.dev/guide/components/host-elements)
