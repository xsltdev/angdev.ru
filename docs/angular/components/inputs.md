---
description: "Как компонент принимает данные через входные свойства: значения по умолчанию, преобразования, псевдонимы и двусторонняя привязка."
---

# Приём данных через входные свойства {: #accepting-data-with-input-properties}

:date: 30.09.2026

!!! tip ""

    Этот материал предполагает, что вы уже прочитали [руководство по основам](../essentials/overview.md). Если Angular для вас в новинку, начните с него. Если вы знакомы с другими веб-фреймворками, входные свойства похожи на _props_.

Компоненту часто нужно передать данные снаружи. Список принимаемых данных компонент задаёт **входными свойствами**:

```ts
import {Component, input} from '@angular/core';

@Component(/* ... */)
export class CustomSlider {
  // Declare an input named 'value' with a default value of zero.
  value = input(0);
}
```

После этого к свойству можно сделать привязку в шаблоне:

```html
<custom-slider [value]="50" />
```

Если у входного свойства есть значение по умолчанию, TypeScript выводит тип из этого значения:

```ts
@Component(/* ... */)
export class CustomSlider {
  // TypeScript infers that this input is a number, returning InputSignal<number>.
  value = input(0);
}
```

Тип можно задать явно, передав функции параметр обобщения.

Если входное свойство без значения по умолчанию не задано, его значение — `undefined`:

```ts
@Component(/* ... */)
export class CustomSlider {
  // Produces an InputSignal<number | undefined> because `value` may not be set.
  value = input<number>();
}
```

**Angular фиксирует входные свойства статически на этапе компиляции.** Во время выполнения их нельзя добавить или удалить.

Функция `input` имеет особый смысл для компилятора Angular. **Вызывать `input` можно только в инициализаторах свойств компонента и директивы.**

При наследовании класса компонента **входные свойства наследуются дочерним классом.**

**Имена входных свойств чувствительны к регистру.**

## Чтение входных свойств {: #reading-inputs}

Функция `input` возвращает `InputSignal`. Значение читают вызовом сигнала:

```ts
import {Component, input, computed} from '@angular/core';

@Component(/* ... */)
export class CustomSlider {
  // Declare an input named 'value' with a default value of zero.
  value = input(0);

  // Create a computed expression that reads the value input
  label = computed(() => `The slider's value is ${this.value()}`);
}
```

Сигналы, которые создаёт `input`, доступны только для чтения.

## Обязательные входные свойства {: #required-inputs}

Входное свойство можно сделать обязательным, вызвав `input.required` вместо `input`:

```ts
@Component(/* ... */)
export class CustomSlider {
  // Declare a required input named value. Returns an `InputSignal<number>`.
  value = input.required<number>();
}
```

Angular требует, чтобы обязательные входные свойства _были_ заданы при использовании компонента в шаблоне. Если какое-то из них пропущено, Angular сообщает об ошибке на этапе сборки.

У обязательных входных свойств в параметр обобщения возвращаемого `InputSignal` автоматически не входит `undefined`.

## Настройка входных свойств {: #configuring-inputs}

Вторым аргументом `input` принимает объект настройки, который меняет поведение входного свойства.

### Преобразования входных свойств {: #input-transforms}

Функция `transform` меняет значение входного свойства в момент, когда его задаёт Angular.

```ts
@Component({
  selector: 'custom-slider',
  /*...*/
})
export class CustomSlider {
  label = input('', {transform: trimString});
}

function trimString(value: string | undefined): string {
  return value?.trim() ?? '';
}
```

```html
<custom-slider [label]="systemVolume" />
```

В примере выше при каждом изменении `systemVolume` Angular вызывает `trimString` и записывает результат в `label`.

Чаще всего преобразование нужно, чтобы шаблон мог передать более широкий набор типов, в том числе `null` и `undefined`.

**Функция преобразования должна статически разбираться на этапе сборки.** Её нельзя задавать условно или как результат вычисления выражения.

**Функция преобразования должна быть [чистой](https://en.wikipedia.org/wiki/Pure_function).** Если она опирается на состояние снаружи, поведение становится непредсказуемым.

#### Проверка типов {: #type-checking}

Если задано преобразование, тип параметра функции преобразования определяет, какие значения можно привязать к входному свойству в шаблоне.

```ts
@Component(/* ... */)
export class CustomSlider {
  widthPx = input('', {transform: appendPx});
}

function appendPx(value: number): string {
  return `${value}px`;
}
```

В примере выше входное свойство `widthPx` принимает `number`, а свойство `InputSignal` возвращает `string`.

#### Встроенные преобразования {: #built-in-transformations}

В Angular есть две встроенные функции преобразования для самых частых случаев: приведение к булеву значению и к числу.

```ts
import {Component, input, booleanAttribute, numberAttribute} from '@angular/core';

@Component(/* ... */)
export class CustomSlider {
  disabled = input(false, {transform: booleanAttribute});
  value = input(0, {transform: numberAttribute});
}
```

`booleanAttribute` повторяет поведение стандартных HTML-[булевых атрибутов](https://developer.mozilla.org/docs/Glossary/Boolean/HTML): само _наличие_ атрибута означает значение «истина». При этом `booleanAttribute` в Angular считает строковый литерал `"false"` булевым `false`.

`numberAttribute` пытается разобрать значение как число и даёт `NaN`, если разбор не удался.

### Псевдонимы входных свойств {: #input-aliases}

Параметр `alias` меняет имя входного свойства в шаблонах.

```ts
@Component(/* ... */)
export class CustomSlider {
  value = input(0, {alias: 'sliderValue'});
}
```

```html
<custom-slider [sliderValue]="50" />
```

На обращение к свойству в коде TypeScript псевдоним не влияет.

Псевдонимы входных свойств лучше не плодить, но они уместны, когда свойство переименовывают и оставляют старое имя, либо когда нужно уйти от столкновения с именем свойства нативного DOM-элемента.

## Модельные входные свойства {: #model-inputs}

**Модельные входные свойства** — особый вид входных свойств: компонент может передать новое значение обратно родительскому компоненту.

Модельное входное свойство объявляют почти так же, как обычное.

В оба вида свойств можно привязать значение снаружи. При этом **в модельное входное свойство может писать сам автор компонента**. Если свойство связано двусторонней привязкой, новое значение уходит в эту привязку.

```ts
@Component(/* ... */)
export class CustomSlider {
  // Define a model input named "value".
  value = model(0);

  increment() {
    // Update the model input with a new value, propagating the value to any bindings.
    this.value.update((oldValue) => oldValue + 10);
  }
}

@Component({
  /* ... */
  // Using the two-way binding syntax means that any changes to the slider's
  // value automatically propagate back to the `volume` signal.
  // Note that this binding uses the signal *instance*, not the signal value.
  template: `<custom-slider [(value)]="volume" />`,
})
export class MediaControls {
  // Create a writable signal for the `volume` local state.
  volume = signal(0);
}
```

В примере `CustomSlider` пишет в своё модельное входное свойство `value`, и значения уходят обратно в сигнал `volume` у `MediaControls`. Привязка держит `value` и `volume` синхронными. Обратите внимание: в привязку передаётся экземпляр сигнала `volume`, а не _значение_ сигнала.

В остальном модельные входные свойства похожи на обычные. Значение читают вызовом функции сигнала, в том числе в [реактивных контекстах](../signals/overview.md#reactive-contexts) вроде `computed` и `effect`.

Подробнее о двусторонней привязке в шаблонах см. [Двусторонняя привязка](../templates/two-way-binding.md).

### Двусторонняя привязка с обычными свойствами {: #two-way-binding-with-plain-properties}

К модельному входному свойству можно привязать обычное свойство JavaScript.

```ts
@Component({
  /* ... */
  // `value` is a model input.
  // The parenthesis-inside-square-brackets syntax (aka "banana-in-a-box") creates a two-way binding
  template: '<custom-slider [(value)]="volume" />',
})
export class MediaControls {
  protected volume = 0;
}
```

В примере `CustomSlider` пишет в модельное входное свойство `value`, и значения уходят обратно в свойство `volume` у `MediaControls`. Привязка держит `value` и `volume` синхронными.

### Неявные события `change` {: #implicit-change-events}

Когда в компоненте или директиве объявлено модельное входное свойство, Angular сам создаёт для него соответствующий [output](outputs.md). Имя output — имя модельного входного свойства с суффиксом `Change`.

```ts
@Directive(/* ... */)
export class CustomCheckbox {
  // This automatically creates an output named "checkedChange".
  // Can be subscribed to using `(checkedChange)="handler()"` in the template.
  checked = model(false);
}
```

Angular порождает это событие изменения каждый раз, когда в модельное входное свойство записывают новое значение методами `set` или `update`.

Подробнее об output см. [Пользовательские события через output](outputs.md).

### Настройка модельных входных свойств {: #customizing-model-inputs}

Модельное входное свойство можно пометить как [обязательное](#required-inputs) или задать ему [псевдоним](#input-aliases) так же, как обычному.

Преобразования входных свойств для модельных входов не поддерживаются.

### Когда нужны модельные входные свойства {: #when-to-use-model-inputs}

Модельные входные свойства нужны, когда компонент должен поддерживать двустороннюю привязку. Обычно это компонент, который меняет значение по действию пользователя. Чаще всего так устроены свои элементы форм: выбор даты, комбинированный список и основное значение такого элемента.

## Выбор имён входных свойств {: #choosing-input-names}

Не выбирайте имена входных свойств, которые совпадают со свойствами DOM-элементов вроде `HTMLElement`. Из-за совпадения непонятно, принадлежит привязанное свойство компоненту или DOM-элементу.

Префиксы, как у селекторов компонентов, входным свойствам не нужны. На одном элементе живёт только один компонент, поэтому нестандартные свойства относятся к нему.

## Объявление входных свойств декоратором `@Input` {: #declaring-inputs-with-the-input-decorator}

!!! tip ""

    Команда Angular рекомендует в новых проектах функцию `input` на сигналах, но исходный API на декораторе `@Input` по-прежнему полностью поддерживается.

Входные свойства компонента можно объявить и декоратором `@Input` на свойстве:

```ts
@Component(/* ... */)
export class CustomSlider {
  @Input() value = 0;
}
```

Привязка в шаблоне одинакова и для входных свойств на сигналах, и для свойств на декораторе:

```html
<custom-slider [value]="50" />
```

### Настройка входных свойств на декораторах {: #customizing-decorator-based-inputs}

Декоратор `@Input` принимает объект настройки, который меняет поведение входного свойства.

#### Обязательные входные свойства {: #required-inputs-decorator}

Параметр `required` требует, чтобы у входного свойства всегда было значение.

```ts
@Component(/* ... */)
export class CustomSlider {
  @Input({required: true}) value = 0;
}
```

Если при использовании компонента пропущено обязательное входное свойство, Angular сообщает об ошибке на этапе сборки.

#### Преобразования входных свойств {: #input-transforms-decorator}

Функция `transform` меняет значение входного свойства в момент, когда его задаёт Angular. Она работает так же, как преобразование у входных свойств на сигналах, описанное выше.

```ts
@Component({
  selector: 'custom-slider',
  ...
})
export class CustomSlider {
  @Input({transform: trimString}) label = '';
}

function trimString(value: string | undefined) {
  return value?.trim() ?? '';
}
```

#### Псевдонимы входных свойств {: #input-aliases-decorator}

Параметр `alias` меняет имя входного свойства в шаблонах.

```ts
@Component(/* ... */)
export class CustomSlider {
  @Input({alias: 'sliderValue'}) value = 0;
}
```

```html
<custom-slider [sliderValue]="50" />
```

Декоратор `@Input` принимает псевдоним и первым аргументом, вместо объекта настройки.

Псевдонимы работают так же, как у входных свойств на сигналах, описанных выше.

### Входные свойства с геттером и сеттером {: #inputs-with-getters-and-setters}

У входных свойств на декораторе входным может быть свойство с геттером и сеттером:

```ts
export class CustomSlider {
  @Input()
  get value(): number {
    return this.internalValue;
  }

  set value(newValue: number) {
    this.internalValue = newValue;
  }

  private internalValue = 0;
}
```

Можно сделать входное свойство _только для записи_, оставив публичным один сеттер:

```ts
export class CustomSlider {
  @Input()
  set value(newValue: number) {
    this.internalValue = newValue;
  }

  private internalValue = 0;
}
```

**По возможности предпочитайте преобразования входных свойств геттерам и сеттерам.**

Не делайте геттеры и сеттеры сложными или дорогими. Angular может вызвать сеттер входного свойства несколько раз, и если сеттер делает тяжёлую работу, например меняет DOM, это бьёт по производительности.

## Входные свойства в декораторе `@Component` {: #specify-inputs-in-the-component-decorator}

Помимо декоратора `@Input`, входные свойства можно перечислить в свойстве `inputs` декоратора `@Component`. Это удобно, когда компонент наследует свойство базового класса:

```ts
// `CustomSlider` inherits the `disabled` property from `BaseSlider`.
@Component({
  ...,
  inputs: ['disabled'],
})
export class CustomSlider extends BaseSlider { }
```

Псевдоним в списке `inputs` задают после двоеточия в строке:

```ts
// `CustomSlider` inherits the `disabled` property from `BaseSlider`.
@Component({
  ...,
  inputs: ['disabled: sliderDisabled'],
})
export class CustomSlider extends BaseSlider { }
```

---

Источник: [https://angular.dev/guide/components/inputs](https://angular.dev/guide/components/inputs)
