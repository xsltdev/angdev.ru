---
description: "Сигналы детально отслеживают, где и как в приложении используется состояние, чтобы фреймворк точечно обновлял отрисовку."
---

# Сигналы Angular {: #angular-signals}

:date: 30.09.2026

Сигналы Angular детально отслеживают, где и как в приложении используется состояние, и за счёт этого фреймворк оптимизирует обновление отрисовки.

!!! tip ""

    Перед этим подробным руководством загляните в [основы сигналов](../essentials/signals.md).

## Что такое сигналы? {: #what-are-signals}

**Сигнал** — обёртка над значением. Когда значение меняется, сигнал уведомляет тех, кто его читает. В сигнале может лежать что угодно: от примитива до сложной структуры данных.

Значение читают вызовом геттера: так Angular отслеживает, где сигнал используется.

Сигнал бывает _записываемым_ или _только для чтения_.

### Записываемые сигналы {: #writable-signals}

У записываемого сигнала есть API, которым значение меняют напрямую. Такой сигнал создают функцией `signal`, передав начальное значение:

```ts
const count = signal(0);

// Signals are getter functions - calling them reads their value.
console.log('The count is: ' + count());
```

Значение меняют напрямую через `.set()`:

```ts
count.set(3);
```

или считают новое из предыдущего через `.update()`:

```ts
// Increment the count by 1.
count.update((value) => value + 1);
```

Тип записываемого сигнала — `WritableSignal`.

#### Записываемый сигнал только для чтения {: #converting-writable-signals-to-readonly}

У `WritableSignal` есть метод `asReadonly()`. Он возвращает версию сигнала только для чтения. Так значение отдают потребителям и не дают менять его напрямую:

```ts
@Service()
export class CounterState {
  // Private writable state
  private readonly _count = signal(0);

  readonly count = this._count.asReadonly(); // public readonly

  increment() {
    this._count.update((v) => v + 1);
  }
}

@Component({/* ... */})
export class AwesomeCounter {
  state = inject(CounterState);

  count = this.state.count; // can read but not modify

  increment() {
    this.state.increment();
  }
}
```

Сигнал только для чтения повторяет изменения исходного записываемого сигнала, но методы `set()` и `update()` его не меняют.

!!! warning ""

    У сигнала только для чтения **нет** встроенной защиты от глубокого изменения значения.

### Вычисляемые сигналы {: #computed-signals}

**Вычисляемые сигналы** доступны только для чтения: их значение выводится из других сигналов. Такой сигнал задают функцией `computed` и функцией вычисления:

```ts
const count: WritableSignal<number> = signal(0);
const doubleCount: Signal<number> = computed(() => count() * 2);
```

Сигнал `doubleCount` зависит от `count`. Когда `count` обновляется, Angular знает, что `doubleCount` тоже пора обновить.

#### Вычисляемые сигналы ленивы и кэшируют результат {: #computed-signals-are-both-lazily-evaluated-and-memoized}

Функция вычисления `doubleCount` не запускается, пока `doubleCount` не прочитают в первый раз. Результат кэшируется. Повторное чтение возвращает кэш и ничего не пересчитывает.

Если затем изменить `count`, Angular считает кэш `doubleCount` недействительным. Следующее чтение посчитает новое значение.

Поэтому в вычисляемом сигнале можно спокойно делать дорогие вычисления, например фильтровать массивы.

#### Вычисляемый сигнал нельзя записывать {: #computed-signals-are-not-writable-signals}

В вычисляемый сигнал нельзя записать значение напрямую. Вызов

```ts
doubleCount.set(3);
```

не компилируется: `doubleCount` — не `WritableSignal`.

#### Зависимости вычисляемого сигнала динамические {: #computed-signal-dependencies-are-dynamic}

Отслеживаются только сигналы, которые действительно прочитали во время вычисления. В этом `computed` сигнал `count` читается, только если сигнал `showCount` истинен:

```ts
const showCount = signal(false);
const count = signal(0);
const conditionalCount = computed(() => {
  if (showCount()) {
    return `The count is ${count()}.`;
  } else {
    return 'Nothing to see here!';
  }
});
```

Если при чтении `conditionalCount` сигнал `showCount` равен `false`, возвращается сообщение «Nothing to see here!», а сигнал `count` _не_ читается. Поэтому последующее изменение `count` _не_ пересчитает `conditionalCount`.

Если установить `showCount` в `true` и снова прочитать `conditionalCount`, вычисление выполнится заново, пойдёт по ветке с истинным `showCount` и вернёт сообщение со значением `count`. После этого изменение `count` сбросит кэш `conditionalCount`.

Зависимость во время вычисления можно не только добавить, но и убрать. Если позже вернуть `showCount` в `false`, `count` перестанет быть зависимостью `conditionalCount`.

## Реактивные контексты {: #reactive-contexts}

**Реактивный контекст** — состояние среды выполнения, в котором Angular следит за чтением сигналов и строит зависимость. Код, который читает сигнал, — _потребитель_, а читаемый сигнал — _производитель_.

Angular автоматически входит в реактивный контекст, когда:

-   выполняется обратный вызов `effect` или `afterRenderEffect`;
-   вычисляется сигнал `computed`;
-   вычисляется `linkedSignal`;
-   вычисляется функция `params` или загрузчик `resource`;
-   рендерится шаблон компонента, включая привязки [свойства хоста](../components/host-elements.md#binding-to-the-host-element).

Во время этих операций Angular создаёт _живую_ связь. Если отслеживаемый сигнал изменится, Angular со временем снова выполнит потребителя.

### Проверка реактивного контекста {: #asserts-the-reactive-context}

Вспомогательная функция `assertNotInReactiveContext` проверяет, что код выполняется не внутри реактивного контекста. Передайте ссылку на вызывающую функцию: если проверка не пройдёт, сообщение об ошибке укажет на нужную точку входа API. Такое сообщение понятнее общей ошибки реактивного контекста и сразу показывает, что исправлять.

```ts
import {assertNotInReactiveContext} from '@angular/core';

function subscribeToEvents() {
  assertNotInReactiveContext(subscribeToEvents);
  // Safe to proceed - subscription logic here
}
```

### Чтение без отслеживания зависимостей {: #reading-without-tracking-dependencies}

Иногда код внутри реактивной функции вроде `computed` или `effect` читает сигналы, но зависимость от них создавать не нужно.

Допустим, при смене `currentUser` нужно записать в журнал значение `counter`. Можно создать `effect`, который читает оба сигнала:

```ts
effect(() => {
  console.log(`User set to ${currentUser()} and the counter is ${counter()}`);
});
```

Сообщение появится, когда изменится _любой_ из сигналов `currentUser` и `counter`. Если эффект должен срабатывать только при смене `currentUser`, чтение `counter` побочное: изменение `counter` не должно давать новую запись.

Чтобы чтение не отслеживалось, геттер вызывают через `untracked`:

```ts
effect(() => {
  console.log(`User set to ${currentUser()} and the counter is ${untracked(counter)}`);
});
```

`untracked` также нужен, когда эффект вызывает внешний код, который не должен становиться зависимостью:

```ts
effect(() => {
  const user = currentUser();
  untracked(() => {
    // If the `loggingService` reads signals, they won't be counted as
    // dependencies of this effect.
    this.loggingService.log(`User set to ${user}`);
  });
});
```

### Реактивный контекст и асинхронные операции {: #reactive-context-and-async-operations}

Реактивный контекст действует только в синхронном коде. Чтение сигнала после асинхронной границы зависимостью не станет.

```ts
effect(async () => {
  const data = await fetchUserData();
  // Reactive context is lost here - theme() won't be tracked
  console.log(`User: ${data.name}, Theme: ${theme()}`);
});
```

Чтобы чтение отслеживалось, сигнал читают до `await`. Это касается и аргументов ожидаемой функции: они вычисляются синхронно.

```ts
effect(async () => {
  const currentTheme = theme(); // Read before await
  const data = await fetchUserData();
  console.log(`User: ${data.name}, Theme: ${currentTheme}`);
});
```

```ts
effect(async () => {
  // Also works: signal is read before await (as function argument)
  await renderContent(docContent());
});
```

## Сложные вычисления {: #advanced-derivations}

`computed` закрывает простые вычисления только для чтения. Иногда нужно записываемое состояние, которое зависит от других сигналов. Подробнее — в руководстве [Зависимое состояние через `linkedSignal`](linked-signal.md).

Все API сигналов синхронны: `signal`, `computed`, `input` и остальные. Приложению часто нужны данные, которые появляются асинхронно. `Resource` встраивает такие данные в код на сигналах и оставляет синхронный доступ к результату. Подробнее — в руководстве [Асинхронная реактивность через ресурсы](resource.md).

## Побочные эффекты для нереактивных API {: #executing-side-effects-on-non-reactive-apis}

На смену состояния лучше отвечать синхронным или асинхронным вычислением. Этого хватает не всегда: иногда на изменение сигнала нужно ответить через API, который сам по себе не реактивен. Для таких случаев берите `effect` или `afterRenderEffect`. Подробнее — в руководстве [Побочные эффекты для нереактивных API](effect.md).

## Чтение сигналов в компонентах `OnPush` {: #reading-signals-in-onpush-components}

Если сигнал читают в шаблоне компонента со стратегией `OnPush`, Angular записывает его в зависимости этого компонента. Когда значение меняется, Angular автоматически [помечает](https://angular.dev/api/core/ChangeDetectorRef#markForCheck) компонент, и тот обновится при следующем обнаружении изменений. Подробнее о компонентах `OnPush` — в руководстве [Пропуск поддеревьев компонентов](https://angular.dev/best-practices/skipping-subtrees).

## Дополнительные темы {: #advanced-topics}

### Функции равенства сигнала {: #signal-equality-functions}

При создании сигнала можно передать функцию равенства. Она проверяет, отличается ли новое значение от предыдущего.

```ts
import isEqual from 'lodash/isEqual';

const data = signal(['test'], {equal: isEqual});

// Even though this is a different array instance, the deep equality
// function will consider the values to be equal, and the signal won't
// trigger any updates.
data.set(['test']);
```

Функцию равенства принимают и записываемые, и вычисляемые сигналы.

!!! tip ""

    По умолчанию сигналы сравнивают значения по ссылке (сравнение [`Object.is()`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Object/is)).

### Проверка типа сигнала {: #type-checking-signals}

Функция `isSignal` проверяет, является ли значение сигналом `Signal`:

```ts
const count = signal(0);
const doubled = computed(() => count() * 2);

isSignal(count); // true
isSignal(doubled); // true
isSignal(42); // false
```

Проверить, что сигнал именно записываемый, можно через `isWritableSignal`:

```ts
const count = signal(0);
const doubled = computed(() => count() * 2);

isWritableSignal(count); // true
isWritableSignal(doubled); // false
```

## Сигналы вместе с RxJS {: #using-signals-with-rxjs}

Как сигналы стыкуются с RxJS, разобрано в руководстве [Совместимость RxJS с сигналами Angular](https://angular.dev/ecosystem/rxjs-interop).


---

Источник: [https://angular.dev/guide/signals](https://angular.dev/guide/signals)
