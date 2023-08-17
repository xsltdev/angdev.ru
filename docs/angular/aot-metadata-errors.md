---
description: Ниже перечислены ошибки метаданных, с которыми вы можете столкнуться, с пояснениями и предлагаемыми исправлениями
---

# Ошибки метаданных AOT

:date: 28.02.2022

Ниже перечислены ошибки метаданных, с которыми вы можете столкнуться, с пояснениями и предлагаемыми исправлениями.

## Форма выражения не поддерживается {#expression-form-not-supported}

!!!note ""

    Компилятор столкнулся с непонятным выражением при оценке метаданных Angular.

Особенности языка, выходящие за рамки [ограниченного синтаксиса выражения](aot-compiler.md#expression-syntax) компилятора, могут вызвать эту ошибку, как показано в следующем примере:

```ts
// ERROR
export class Fooish { … }
…
const prop = typeof Fooish; // typeof is not valid in metadata
  …
  // bracket notation is not valid in metadata
  { provide: 'token', useValue: { [prop]: 'value' } };
  …
```

Вы можете использовать `typeof` и скобочную нотацию в обычном коде приложения. Вы просто не можете использовать эти функции в выражениях, определяющих метаданные Angular.

Избежать этой ошибки можно, придерживаясь [ограниченного синтаксиса выражений](aot-compiler.md#expression-syntax) компилятора при написании метаданных Angular

и остерегайтесь новых или необычных функций TypeScript.

## Ссылка на локальный (неэкспортированный) символ {#reference-to-a-local-symbol}

!!!note ""

    _Ссылка на локальный (неэкспортируемый) символ 'имя символа'. Рассмотрите возможность экспорта символа._

Компилятор столкнулся со ссылкой на локально определенный символ, который либо не экспортирован, либо не инициализирован.

Вот пример проблемы в `provider`.

```ts
// ERROR
let foo: number; // neither exported nor initialized

@Component({
  selector: 'my-component',
  template: … ,
  providers: [
    { provide: Foo, useValue: foo }
  ]
})
export class MyComponent {}
```

Компилятор генерирует фабрику компонентов, которая включает код поставщика `useValue`, в отдельном модуле. Этот модуль фабрики не может вернуться в исходный модуль, чтобы получить доступ к локальной (неэкспортируемой) переменной `foo`.

Вы можете решить проблему, инициализировав `foo`.

```ts
let foo = 42; // initialized
```

Компилятор [свернет](aot-compiler.md#code-folding) выражение в провайдер, как если бы вы написали это.

```ts
providers: [{ provide: Foo, useValue: 42 }];
```

Альтернативно, вы можете исправить это, экспортируя `foo` с расчетом на то, что `foo` будет присвоено во время выполнения, когда вы действительно будете знать его значение.

```ts
// CORRECTED
export let foo: number; // exported

@Component({
  selector: 'my-component',
  template: … ,
  providers: [
    { provide: Foo, useValue: foo }
  ]
})
export class MyComponent {}
```

Добавление `export` часто работает для переменных, на которые ссылаются в метаданных, таких как `providers` и `animations`, потому что компилятор может генерировать _ссылки_ на экспортируемые переменные в этих выражениях. Ему не нужны _значения_ этих переменных.

Добавление `export` не работает, когда компилятору нужно _фактическое значение_ для генерации кода.

Например, это не работает для свойства `template`.

```ts
// ERROR
export let someTemplate: string; // exported but not initialized

@Component({
    selector: 'my-component',
    template: someTemplate,
})
export class MyComponent {}
```

Компилятору необходимо значение свойства `template` _прямо сейчас_ для создания фабрики компонентов. Одной ссылки на переменную недостаточно.
Префикс объявления с `export` просто выдает новую ошибку, "[`Only initialized variables and constants can be referenced`](#only-initialized-variables)".

## Только инициализированные переменные и константы {#only-initialized-variables}

!!!note ""

    На _только_ инициализированные переменные и константы можно ссылаться, потому что значение этой переменной необходимо компилятору шаблона.

Компилятор обнаружил ссылку на экспортируемую переменную или статическое поле, которое не было инициализировано. Для генерации кода ему необходимо значение этой переменной.

Следующий пример пытается установить свойство компонента `template` в значение экспортированной переменной `someTemplate`, которая объявлена, но _не назначена_.

```ts
// ERROR
export let someTemplate: string;

@Component({
    selector: 'my-component',
    template: someTemplate,
})
export class MyComponent {}
```

Вы также получите эту ошибку, если импортируете `someTemplate` из другого модуля и не инициализируете его там.

```ts
// ERROR - not initialized there either
import { someTemplate } from './config';

@Component({
    selector: 'my-component',
    template: someTemplate,
})
export class MyComponent {}
```

Компилятор не может дожидаться времени выполнения, чтобы получить информацию о шаблоне. Он должен статически получить значение переменной `someTemplate` из исходного кода, чтобы сгенерировать фабрику компонентов, которая включает инструкции по созданию элемента на основе шаблона.

Чтобы исправить эту ошибку, укажите начальное значение переменной в предложении инициализатора _в той же строке_.

```ts
// CORRECTED
export let someTemplate = '<h1>Greetings from Angular</h1>';

@Component({
    selector: 'my-component',
    template: someTemplate,
})
export class MyComponent {}
```

## Ссылка на неэкспортированный класс {#reference-to-a-non-exported-class}

!!!note ""

    _Ссылка на неэкспортированный класс `<имя класса>`. Рассмотрите возможность экспорта класса._

Метаданные ссылаются на класс, который не был экспортирован.

Например, вы могли определить класс и использовать его в качестве маркера инъекции в массиве провайдеров, но не экспортировать этот класс.

```ts
// ERROR
abstract class MyStrategy { }

  // …
  providers: [
    { provide: MyStrategy, useValue: … }
  ]
  // …
```

Angular создает фабрику классов в отдельном модуле, и эта фабрика [может получить доступ только к экспортированным классам](aot-compiler.md#exported-symbols). Чтобы исправить эту ошибку, экспортируйте ссылающийся класс.

```ts
// CORRECTED
export abstract class MyStrategy { }

  …
  providers: [
    { provide: MyStrategy, useValue: … }
  ]
  …
```

## Ссылка на неэкспортированную функцию {#reference-to-a-non-exported-function}

!!!note ""

    _Метаданные ссылались на функцию, которая не была экспортирована._

Например, вы могли установить свойство провайдера `useFactory` на локально определенную функцию, которую вы забыли экспортировать.

```ts
// ERROR
function myStrategy() { … }

  …
  providers: [
    { provide: MyStrategy, useFactory: myStrategy }
  ]
  …
```

Angular создает фабрику классов в отдельном модуле, и эта фабрика [может получить доступ только к экспортированным функциям](aot-compiler.md#exported-symbols). Чтобы исправить эту ошибку, экспортируйте функцию.

```ts
// CORRECTED
export function myStrategy() { … }

  …
  providers: [
    { provide: MyStrategy, useFactory: myStrategy }
  ]
  …
```

## Вызовы функций не поддерживаются {#function-calls-not-supported}

!!!note ""

    _Вызовы функций не поддерживаются. Подумайте о замене функции или лямбды ссылкой на экспортируемую функцию._

В настоящее время компилятор не поддерживает [функциональные выражения или лямбда-функции](aot-compiler.md#function-expression). Например, вы не можете установить `useFactory` провайдера на анонимную функцию или стрелочную функцию, как это сделано здесь.

```ts
// ERROR
  …
  providers: [
    { provide: MyStrategy, useFactory: function() { … } },
    { provide: OtherStrategy, useFactory: () => { … } }
  ]
  …
```

Вы также получите эту ошибку, если вызовете функцию или метод в `useValue` провайдера.

```ts
// ERROR
import { calculateValue } from './utilities';

  …
  providers: [
    { provide: SomeValue, useValue: calculateValue() }
  ]
  …
```

Чтобы исправить эту ошибку, экспортируйте функцию из модуля и обратитесь к ней в провайдере `useFactory`.

```ts
// CORRECTED
import { calculateValue } from './utilities';

export function myStrategy() { … }
export function otherStrategy() { … }
export function someValueFactory() {
  return calculateValue();
}
  …
  providers: [
    { provide: MyStrategy, useFactory: myStrategy },
    { provide: OtherStrategy, useFactory: otherStrategy },
    { provide: SomeValue, useFactory: someValueFactory }
  ]
  …
```

## Деструктурированная переменная или константа не поддерживается {#destructured-variable-not-supported}

!!!note ""

    _Ссылка на экспортируемую деструктурированную переменную или константу не поддерживается компилятором шаблонов. Рассмотрите возможность упрощения, чтобы избежать деструктуризации._

Компилятор не поддерживает ссылки на переменные, назначенные [деструктуризацией](https://www.typescriptlang.org/docs/handbook/variable-declarations.html#destructuring).

Например, вы не можете написать что-то вроде этого:

```ts
// ERROR
import { configuration } from './configuration';

// destructured assignment to foo and bar
const {foo, bar} = configuration;
  …
  providers: [
    {provide: Foo, useValue: foo},
    {provide: Bar, useValue: bar},
  ]
  …
```

Чтобы исправить эту ошибку, обратитесь к неструктурированным значениям.

```ts
// CORRECTED
import { configuration } from './configuration';
  …
  providers: [
    {provide: Foo, useValue: configuration.foo},
    {provide: Bar, useValue: configuration.bar},
  ]
  …
```

## Не удалось определить тип {#could-not-resolve-type}

!!!note ""

    _Компилятор встретил тип и не может определить, какой модуль экспортирует этот тип._

Это может произойти, если вы ссылаетесь на окружающий тип. Например, тип `Window` является окружающим типом, объявленным в глобальном файле `.d.ts`.

Вы получите ошибку, если обратитесь к нему в конструкторе компонента, который компилятор должен статически анализировать.

```ts
// ERROR
@Component({ })
export class MyComponent {
  constructor (private win: Window) { … }
}
```

TypeScript понимает окружающие типы, поэтому вы не импортируете их. Компилятор Angular не понимает тип, который вы пренебрегаете экспортом или импортом.

В данном случае компилятор не понимает, как внедрить что-то с помощью маркера `Window`.

Не ссылайтесь на окружающие типы в выражениях метаданных.

Если вам необходимо ввести экземпляр окружающего типа, вы можете решить эту проблему в четыре шага:

1.  Создайте инъекционный маркер для экземпляра окружающего типа.

2.  Создайте фабричную функцию, которая возвращает этот экземпляр.

3.  Добавьте провайдер `useFactory` к этой заводской функции.

4.  Используйте `@Inject` для инъекции экземпляра.

Вот наглядный пример.

```ts
// CORRECTED
import { Inject } from '@angular/core';

export const WINDOW = new InjectionToken('Window');
export function _window() { return window; }

@Component({
  …
  providers: [
    { provide: WINDOW, useFactory: _window }
  ]
})
export class MyComponent {
  constructor (@Inject(WINDOW) private win: Window) { … }
}
```

Тип `Window` в конструкторе больше не является проблемой для компилятора, потому что он использует `@Inject(WINDOW)` для генерации кода инъекции.

Angular делает нечто подобное с маркером `DOCUMENT`, чтобы вы могли внедрить объект `document` браузера (или его абстракцию, в зависимости от платформы, на которой работает приложение).

```ts
import { Inject }   from '@angular/core';
import { DOCUMENT } from '@angular/common';

@Component({ … })
export class MyComponent {
  constructor (@Inject(DOCUMENT) private doc: Document) { … }
}
```

## Имя ожидается {#name-expected}

!!!note ""

    Компилятор ожидал увидеть имя в выражении, которое он оценивал.

Это может произойти, если вы используете число в качестве имени свойства, как в следующем примере.

```ts
// ERROR
provider: [{ provide: Foo, useValue: { 0: 'test' } }];
```

Измените имя свойства на нечисловое.

```ts
// CORRECTED
provider: [{ provide: Foo, useValue: { '0': 'test' } }];
```

## Неподдерживаемое имя члена перечисления {#unsupported-enum-member-name}

!!!note ""

    _Angular не смог определить значение [enum member](https://www.typescriptlang.org/docs/handbook/enums.html), на которое вы ссылались в метаданных._

Компилятор может понимать простые значения перечислений, но не сложные значения, например, полученные из вычисляемых свойств.

```ts
// ERROR
enum Colors {
    Red = 1,
    White,
    Blue = 'Blue'.length, // computed
}

// …
providers: [
    { provide: BaseColor, useValue: Colors.White }, // ok
    { provide: DangerColor, useValue: Colors.Red }, // ok
    { provide: StrongColor, useValue: Colors.Blue }, // bad
];
// …
```

Избегайте ссылок на перечисления со сложными инициализаторами или вычисляемыми свойствами.

## Выражения шаблонов с метками не поддерживаются {#tagged-template-expressions-not-supported}

!!!note ""

    _Тегированные шаблонные выражения не поддерживаются в метаданных._

Компилятор встретил JavaScript ES2015 [tagged template expression](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Template_literals#Tagged_template_literals), такой как следующий.

```ts
// ERROR
const expression = 'funky';
const raw = String.raw`A tagged template ${expression} string`;
// …
template: '<div>' + raw + '</div>';
// …
```

[`String.raw()`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/String/raw) - это _теговая функция_, встроенная в JavaScript ES2015.

Компилятор AOT не поддерживает выражения шаблонов с метками; избегайте их в выражениях метаданных.

## Ожидается ссылка на символ {#symbol-reference-expected}

!!!note ""

    Компилятор ожидал получить ссылку на символ в месте, указанном в сообщении об ошибке.

Эта ошибка может возникнуть, если вы используете выражение в предложении `extends` класса.

## Ссылки

-   [AOT metadata errors](https://angular.io/guide/aot-metadata-errors)
