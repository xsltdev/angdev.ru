---
description: "Создание динамических данных и работа с ними."
---

# Сигналы {: #signals}

:date: 30.09.2026

Создание динамических данных и работа с ними.

В Angular состояние создают и держат в _сигналах_. Сигнал — лёгкая обёртка над значением.

Локальное состояние кладут в сигнал функцией `signal`:

```ts
import {signal} from '@angular/core';

// Create a signal with the `signal` function.
const firstName = signal('Morgan');

// Read a signal value by calling it— signals are functions.
console.log(firstName());

// Change the value of this signal by calling its `set` method with a new value.
firstName.set('Jaime');

// You can also use the `update` method to change the value
// based on the previous value.
firstName.update((name) => name.toUpperCase());
```

Angular следит, где сигналы читают и когда их обновляют. По этим сведениям фреймворк делает дополнительную работу, например обновляет DOM новым состоянием. Способность реагировать на изменение сигналов во времени называется _реактивностью_.

## Вычисляемые выражения {: #computed-expressions}

`computed` — сигнал, значение которого считается по другим сигналам.

```ts
import {signal, computed} from '@angular/core';

const firstName = signal('Morgan');
const firstNameCapitalized = computed(() => firstName().toUpperCase());

console.log(firstNameCapitalized()); // MORGAN
```

Вычисляемый сигнал `computed` только для чтения: у него нет методов `set` и `update`. Значение меняется само, когда меняется любой сигнал, который он читает:

```ts
import {signal, computed} from '@angular/core';

const firstName = signal('Morgan');
const firstNameCapitalized = computed(() => firstName().toUpperCase());
console.log(firstNameCapitalized()); // MORGAN

firstName.set('Jaime');
console.log(firstNameCapitalized()); // JAIME
```

## Сигналы в компонентах {: #using-signals-in-components}

В компонентах состояние создают и ведут через `signal` и `computed`:

```ts
@Component({
  /* ... */
})
export class UserProfile {
  isTrial = signal(false);
  isTrialExpired = signal(false);
  showTrialDuration = computed(() => this.isTrial() && !this.isTrialExpired());

  activateTrial() {
    this.isTrial.set(true);
  }
}
```

!!! tip ""

    Подробнее о сигналах Angular — в [подробном руководстве по сигналам](../signals/overview.md).

## Следующий шаг {: #next-step}

Динамические данные уже можно объявлять и менять. Дальше — как вывести их в шаблоне.

-   [Динамические интерфейсы на шаблонах](templates.md)
-   [Подробное руководство по сигналам](../signals/overview.md)


---

Источник: [https://angular.dev/essentials/signals](https://angular.dev/essentials/signals)
