---
description: "Связанный сигнал хранит записываемое состояние, которое само обновляется вместе с другим состоянием."
---

# Зависимое состояние через `linkedSignal` {: #dependent-state-with-linkedsignal}

:date: 30.09.2026

Функцией `signal` в коде Angular держат состояние. Иногда оно зависит от какого-то _другого_ состояния. Например, компонент, в котором пользователь выбирает способ доставки заказа:

```ts
@Component({
  /* ... */
})
export class ShippingMethodPicker {
  shippingOptions: Signal<ShippingMethod[]> = getShippingOptions();

  // Select the first shipping option by default.
  selectedOption = signal(this.shippingOptions()[0]);

  changeShipping(newOptionIndex: number) {
    this.selectedOption.set(this.shippingOptions()[newOptionIndex]);
  }
}
```

В этом примере `selectedOption` по умолчанию равен первому варианту и меняется, если пользователь выбирает другой. Но `shippingOptions` — тоже сигнал, и его значение может измениться. Когда `shippingOptions` меняется, в `selectedOption` может остаться значение, которого среди вариантов уже нет.

**Функция `linkedSignal` создаёт сигнал для состояния, которое по сути _связано_ с другим состоянием.** В том же примере `linkedSignal` заменяет `signal`:

```ts
@Component({
  /* ... */
})
export class ShippingMethodPicker {
  shippingOptions: Signal<ShippingMethod[]> = getShippingOptions();

  // Initialize selectedOption to the first shipping option.
  selectedOption = linkedSignal(() => this.shippingOptions()[0]);

  changeShipping(index: number) {
    this.selectedOption.set(this.shippingOptions()[index]);
  }
}
```

`linkedSignal` устроен похоже на `signal`, с одним отличием: вместо значения по умолчанию передают _функцию вычисления_, как в `computed`. Когда результат вычисления меняется, значение `linkedSignal` становится этим результатом. Так у `linkedSignal` остаётся допустимое значение.

Ниже видно, как значение `linkedSignal` меняется вместе со связанным состоянием:

```ts
const shippingOptions = signal(['Ground', 'Air', 'Sea']);
const selectedOption = linkedSignal(() => shippingOptions()[0]);
console.log(selectedOption()); // 'Ground'

selectedOption.set(shippingOptions()[2]);
console.log(selectedOption()); // 'Sea'

shippingOptions.set(['Email', 'Will Call', 'Postal service']);
console.log(selectedOption()); // 'Email'
```

## Учёт предыдущего состояния {: #accounting-for-previous-state}

Иногда вычислению `linkedSignal` нужно предыдущее значение самого `linkedSignal`.

В примере выше при изменении `shippingOptions` сигнал `selectedOption` каждый раз возвращается к первому варианту. Выбор пользователя можно сохранить, если выбранный вариант всё ещё есть в списке. Для этого `linkedSignal` создают с отдельными _источником_ и _вычислением_:

```ts
interface ShippingMethod {
  id: number;
  name: string;
}

@Component({
  /* ... */
})
export class ShippingMethodPicker {
  constructor() {
    this.changeShipping(2);
    this.changeShippingOptions();
    console.log(this.selectedOption()); // {"id":2,"name":"Postal Service"}
  }

  shippingOptions = signal<ShippingMethod[]>([
    {id: 0, name: 'Ground'},
    {id: 1, name: 'Air'},
    {id: 2, name: 'Sea'},
  ]);

  selectedOption = linkedSignal<ShippingMethod[], ShippingMethod>({
    // `selectedOption` is set to the `computation` result whenever this `source` changes.
    source: this.shippingOptions,
    computation: (newOptions, previous) => {
      // If the newOptions contain the previously selected option, preserve that selection.
      // Otherwise, default to the first option.
      return newOptions.find((opt) => opt.id === previous?.value.id) ?? newOptions[0];
    },
  });

  changeShipping(index: number) {
    this.selectedOption.set(this.shippingOptions()[index]);
  }

  changeShippingOptions() {
    this.shippingOptions.set([
      {id: 0, name: 'Email'},
      {id: 1, name: 'Sea'},
      {id: 2, name: 'Postal Service'},
    ]);
  }
}
```

В `linkedSignal` можно передать не одну функцию вычисления, а объект с отдельными свойствами `source` и `computation`.

`source` может быть любым сигналом, например `computed` или входом `input` компонента. `linkedSignal` меняет значение, когда меняется `source` или любой сигнал, к которому обратились в `computation`, и записывает результат переданного `computation`.

`computation` — функция. Она получает новое значение `source` и объект `previous`. У `previous` два свойства. `previous.source` — прежнее значение `source`, `previous.value` — прежнее значение `linkedSignal`. По этим прежним значениям решают, каким будет новый результат вычисления.

!!! tip ""

    С параметром `previous` аргументы обобщённого типа у `linkedSignal` указывают явно. Первый обобщённый тип — это тип `source`, второй — тип результата `computation`.

## Своё сравнение на равенство {: #custom-equality-comparison}

Как и у любого другого сигнала, у `linkedSignal` можно задать свою функцию равенства. По ней зависимости ниже по графу решают, изменилось ли значение `linkedSignal`, то есть результат вычисления:

```ts
const activeUser = signal({id: 123, name: 'Morgan', isAdmin: true});

const activeUserEditCopy = linkedSignal(() => activeUser(), {
  // Consider the user as the same if it's the same `id`.
  equal: (a, b) => a.id === b.id,
});

// Or, if separating `source` and `computation`
const activeUserEditCopy = linkedSignal({
  source: activeUser,
  computation: (user) => user,
  equal: (a, b) => a.id === b.id,
});
```

## Настройка операции `set` {: #customizing-the-set-operation}

Иногда `set` и `update` у `linkedSignal` должны записывать значение обратно в источник состояния, а не менять сам `linkedSignal`. Такое поведение задают функцией `set` в параметрах.

Своя функция `set` получает два аргумента:

1.  Новое значение, которое записывают.
2.  Функцию `rawSet`. Её вызов обновляет внутреннее состояние `linkedSignal` напрямую — так же, как поведение по умолчанию.

!!! info ""

    Через `rawSet` значение `linkedSignal` обновляют напрямую. Это нужно, чтобы не запускать вычисление: например, оно дорогое, а результат уже известен.

### Запись обратно в исходный сигнал {: #writing-back-to-a-source-signal}

Возьмём компонент, который показывает температуру в градусах Фаренгейта и даёт её редактировать, а источником состояния держит сигнал в градусах Цельсия:

```ts
const tempC = signal(0);
const tempF = linkedSignal(() => (tempC() * 9) / 5 + 32, {
  set: (valF) => tempC.set(((valF - 32) * 5) / 9),
});

console.log(tempF()); // 32

// Setting Fahrenheit updates Celsius, which reactively updates Fahrenheit
tempF.set(212);
console.log(tempC()); // 100
console.log(tempF()); // 212
```

### Обновление свойства внутри родительского объекта {: #updating-a-property-inside-a-parent-object}

Другой частый случай — обновить одно свойство внутри родительского объекта. Родитель хранится в сигнале, а связь ведёт к вложенному свойству:

```ts
interface Order {
  id: number;
  shippingMethod: string;
}

const order = signal<Order>({
  id: 42,
  shippingMethod: 'Ground',
});

const shippingMethod = linkedSignal(() => order().shippingMethod, {
  set: (newMethod) => {
    // Perform an immutable update to write the change back to the order
    order.update((currentOrder) => ({
      ...currentOrder,
      shippingMethod: newMethod,
    }));
  },
});

console.log(shippingMethod()); // 'Ground'

// Updating the shippingMethod updates the parent order object
shippingMethod.set('Air');
console.log(order()); // { id: 42, shippingMethod: 'Air' }
console.log(shippingMethod()); // 'Air'
```


---

Источник: [https://angular.dev/guide/signals/linked-signal](https://angular.dev/guide/signals/linked-signal)
