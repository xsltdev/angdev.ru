---
description: "Двусторонняя привязка одновременно передаёт значение в элемент и возвращает его изменения обратно."
---

# Двусторонняя привязка {: #two-way-binding}

:date: 30.09.2026

**Двусторонняя привязка** — краткая запись, которая одновременно передаёт значение в элемент и даёт этому элементу вернуть изменения обратно через ту же привязку.

## Синтаксис {: #syntax}

Синтаксис двусторонней привязки — сочетание квадратных и круглых скобок, `[()]`. Он объединяет синтаксис привязки свойства `[]` и синтаксис привязки события `()`. В сообществе Angular эту запись неформально называют «банан в коробке».

## Двусторонняя привязка с элементами форм {: #two-way-binding-with-form-controls}

Двустороннюю привязку часто используют, чтобы данные компонента оставались согласованными с элементом формы, пока пользователь с ним работает. Например, когда пользователь заполняет текстовое поле, должно обновляться состояние компонента.

В примере ниже значение `firstName` на странице обновляется динамически:

```ts
import {Component} from '@angular/core';
import {FormsModule} from '@angular/forms';

@Component({
  imports: [FormsModule],
  template: `
    <main>
      <h2>Hello {{ firstName }}!</h2>
      <input type="text" [(ngModel)]="firstName" />
    </main>
  `,
})
export class App {
  firstName = 'Ada';
}
```

Чтобы использовать двустороннюю привязку с нативными элементами форм, нужно:

1.  Импортировать `FormsModule` из `@angular/forms`
1.  Использовать директиву `ngModel` с синтаксисом двусторонней привязки (например, `[(ngModel)]`)
1.  Присвоить ей состояние, которое нужно обновлять (например, `firstName`)

После этой настройки Angular следит, чтобы любые изменения в текстовом поле правильно отражались в состоянии компонента.

Подробнее о [`NgModel`](https://angular.dev/api/forms/NgModel) — в официальной документации.

## Двусторонняя привязка между компонентами {: #two-way-binding-between-components}

Двусторонняя привязка между родительским и дочерним компонентом требует больше настройки, чем у элементов формы.

В примере ниже `App` задаёт начальное состояние счётчика, а логика обновления и отрисовки интерфейса счётчика в основном живёт в дочернем компоненте `Counter`.

```ts
import {Component} from '@angular/core';
import {Counter} from './counter';

@Component({
  selector: 'app-root',
  imports: [Counter],
  template: `
    <main>
      <h1>Counter: {{ initialCount }}</h1>
      <app-counter [(count)]="initialCount"></app-counter>
    </main>
  `,
})
export class App {
  initialCount = 18;
}
```

```ts
import {Component, model} from '@angular/core';

@Component({
  selector: 'app-counter',
  template: `
    <button (click)="updateCount(-1)">-</button>
    <span>{{ count() }}</span>
    <button (click)="updateCount(+1)">+</button>
  `,
})
export class Counter {
  count = model<number>(0);

  updateCount(amount: number): void {
    this.count.update((currentCount) => currentCount + amount);
  }
}
```

### Как включить двустороннюю привязку между компонентами {: #enabling-two-way-binding-between-components}

Если разобрать пример до сути, каждой двусторонней привязке между компонентами нужно следующее.

Дочерний компонент должен содержать свойство `model`.

Упрощённый пример:

```ts
import {Component, model} from '@angular/core';

@Component({
  /* Omitted for brevity */
})
export class Counter {
  count = model<number>(0);

  updateCount(amount: number): void {
    this.count.update((currentCount) => currentCount + amount);
  }
}
```

Родительский компонент должен:

1.  Обернуть имя свойства `model` в синтаксис двусторонней привязки.
1.  Присвоить свойству `model` свойство или сигнал.

Упрощённый пример:

```ts
import {Component} from '@angular/core';
import {Counter} from './counter';

@Component({
  selector: 'app-root',
  imports: [Counter],
  template: `
    <main>
      <app-counter [(count)]="initialCount"></app-counter>
    </main>
  `,
})
export class App {
  initialCount = 18;
}
```


---

Источник: [https://angular.dev/guide/templates/two-way-binding](https://angular.dev/guide/templates/two-way-binding)
