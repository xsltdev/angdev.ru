---
description: Ниже перечислены ошибки метаданных, с которыми вы можете столкнуться, с пояснениями и предлагаемыми исправлениями
---

# Ошибки метаданных AOT

Ниже перечислены ошибки метаданных, с которыми вы можете столкнуться, с пояснениями и предлагаемыми исправлениями.

[Expression form not supported](#expression-form-not-supported) <br /> [Reference to a local (non-exported) symbol](#reference-to-a-local-symbol) <br />

[Only initialized variables and constants](#only-initialized-variables) <br />

[Reference to a non-exported class](#reference-to-a-non-exported-class) <br />

[Reference to a non-exported function](#reference-to-a-non-exported-function) <br />

[Function calls are not supported](#function-calls-not-supported) <br />

[Destructured variable or constant not supported](#destructured-variable-not-supported) <br />

[Could not resolve type](#could-not-resolve-type) <br />

[Name expected](#name-expected) <br />

[Unsupported enum member name](#unsupported-enum-member-name) <br />

[Tagged template expressions are not supported](#tagged-template-expressions-not-supported) <br />

[Symbol reference expected](#symbol-reference-expected) <br />

<a id="expression-form-not-supported"></a>

## Форма выражения не поддерживается

<div class="alert is-helpful">

Компилятор столкнулся с непонятным выражением при оценке метаданных Angular.\_

</div>

Особенности языка, выходящие за рамки [ограниченного синтаксиса выражения] (guide/aot-compiler#expression-syntax) компилятора, могут вызвать эту ошибку, как показано в следующем примере:

<code-example format="typescript" language="typescript">

// ERROR export class Fooish { &hellip; }
&hellip;

const prop = typeof Fooish; // typeof не является допустимым в метаданных

&hellip;

// скобочная нотация недопустима в метаданных

{ provide: 'token', useValue: { [prop]: 'value' } };

&hellip;

</code-example>

Вы можете использовать `typeof` и скобочную нотацию в обычном коде приложения. Вы просто не можете использовать эти функции в выражениях, определяющих метаданные Angular.

Избежать этой ошибки можно, придерживаясь [ограниченного синтаксиса выражений] (guide/aot-compiler#expression-syntax) компилятора при написании метаданных Angular

и остерегайтесь новых или необычных функций TypeScript.

<a id="reference-to-a-local-symbol"></a>

## Ссылка на локальный (неэкспортированный) символ

<div class="alert is-helpful">

_Ссылка на локальный\(неэкспортируемый\) символ 'имя символа'. Рассмотрите возможность экспорта символа._

</div>

Компилятор столкнулся со ссылкой на локально определенный символ, который либо не экспортирован, либо не инициализирован.

Вот пример проблемы в `provider`.

<code-example format="typescript" language="typescript">

// ERROR let foo: number; // не экспортируется и не инициализируется

&commat;Component({ selector: 'my-component',

template: &hellip; ,

providers: [

{ provide: Foo, useValue: foo }

]

})

export class MyComponent {}

</code-example>

Компилятор генерирует фабрику компонентов, которая включает код поставщика `useValue`, в отдельном модуле. Этот модуль фабрики не может вернуться в исходный модуль, чтобы получить доступ к локальной \(неэкспортируемой\) переменной `foo`.

Вы можете решить проблему, инициализировав `foo`.

<code-example format="typescript" language="typescript">

let foo = 42; // инициализация

</code-example>

Компилятор [свернет](guide/aot-compiler#code-folding) выражение в провайдер, как если бы вы написали это.

<code-example format="typescript" language="typescript">

providers: [ { provide: Foo, useValue: 42 }
]

</code-example>

Альтернативно, вы можете исправить это, экспортируя `foo` с расчетом на то, что `foo` будет присвоено во время выполнения, когда вы действительно будете знать его значение.

<code-example format="typescript" language="typescript">

// КОРРЕКТИРОВАН экспорт let foo: number; // экспортировано

&commat;Component({ selector: 'my-component',

template: &hellip; ,

providers: [

{ provide: Foo, useValue: foo }

]

})

export class MyComponent {}

</code-example>

Добавление `export` часто работает для переменных, на которые ссылаются в метаданных, таких как `providers` и `animations`, потому что компилятор может генерировать _ссылки_ на экспортируемые переменные в этих выражениях. Ему не нужны _значения_ этих переменных.

Добавление `export` не работает, когда компилятору нужно _фактическое значение_ для генерации кода.

Например, это не работает для свойства `template`.

<code-example format="typescript" language="typescript">

// ERROR export let someTemplate: string; // экспортирован, но не инициализирован

&commat;Component({ selector: 'my-component',

template: someTemplate

})

export class MyComponent {}

</code-example>

Компилятору необходимо значение свойства `template` _прямо сейчас_ для создания фабрики компонентов. Одной ссылки на переменную недостаточно.
Префикс объявления с `export` просто выдает новую ошибку, "[`Only initialized variables and constants can be referenced`](#only-initialized-variables)".

<a id="only-initialized-variables"></a>

## Только инициализированные переменные и константы

<div class="alert is-helpful">

На _только_ инициализированные переменные и константы можно ссылаться, потому что значение этой переменной необходимо компилятору шаблона.\_

</div>

Компилятор обнаружил ссылку на экспортируемую переменную или статическое поле, которое не было инициализировано. Для генерации кода ему необходимо значение этой переменной.

Следующий пример пытается установить свойство компонента `template` в значение экспортированной переменной `someTemplate`, которая объявлена, но _не назначена_.

<code-example format="typescript" language="typescript">

// ERROR export let someTemplate: string;

&commat;Component({ selector: 'my-component',

template: someTemplate

})

export class MyComponent {}

</code-example>

Вы также получите эту ошибку, если импортируете `someTemplate` из другого модуля и не инициализируете его там.

<code-example format="typescript" language="typescript">

// ERROR - там тоже нет инициализации import { someTemplate } from './config';

&commat;Component({ selector: 'my-component',

template: someTemplate

})

export class MyComponent {}

</code-example>

Компилятор не может дожидаться времени выполнения, чтобы получить информацию о шаблоне. Он должен статически получить значение переменной `someTemplate` из исходного кода, чтобы сгенерировать фабрику компонентов, которая включает инструкции по созданию элемента на основе шаблона.

Чтобы исправить эту ошибку, укажите начальное значение переменной в предложении инициализатора _в той же строке_.

<code-example format="typescript" language="typescript">

// КОРРЕКТИРОВАННЫЙ экспорт let someTemplate = '&lt;h1&gt;Greetings from Angular&lt;/h1&gt;';

&commat;Component({ selector: 'my-component',

template: someTemplate

})

export class MyComponent {}

</code-example>

<a id="reference-to-a-non-exported-class"></a>

## Ссылка на неэкспортированный класс

<div class="alert is-helpful">

_Ссылка на неэкспортированный класс `<имя класса>`._ _Рассмотрите возможность экспорта класса._

</div>

Метаданные ссылаются на класс, который не был экспортирован.

Например, вы могли определить класс и использовать его в качестве маркера инъекции в массиве провайдеров, но не экспортировать этот класс.

<code-example format="typescript" language="typescript">

// ERROR абстрактный класс MyStrategy { }

&hellip; providers: [

{ provide: MyStrategy, useValue: &hellip; }

]

&hellip;

</code-example>

Angular создает фабрику классов в отдельном модуле, и эта фабрика [может получить доступ только к экспортированным классам](guide/aot-compiler#exported-symbols). Чтобы исправить эту ошибку, экспортируйте ссылающийся класс.

<code-example format="typescript" language="typescript">

// CORRECTED export abstract class MyStrategy { }

&hellip; providers: [

{ provide: MyStrategy, useValue: &hellip; }

]

&hellip;

</code-example>

<a id="reference-to-a-non-exported-function"></a>

## Ссылка на неэкспортированную функцию

<div class="alert is-helpful">

_Метаданные ссылались на функцию, которая не была экспортирована._

</div>

Например, вы могли установить свойство провайдера `useFactory` на локально определенную функцию, которую вы забыли экспортировать.

<code-example format="typescript" language="typescript">

// ERROR function myStrategy() { &hellip; }

&hellip; providers: [

{ provide: MyStrategy, useFactory: myStrategy }

]

&hellip;

</code-example>

Angular создает фабрику классов в отдельном модуле, и эта фабрика [может получить доступ только к экспортированным функциям](guide/aot-compiler#exported-symbols). Чтобы исправить эту ошибку, экспортируйте функцию.

<code-example format="typescript" language="typescript">

// CORRECTED export function myStrategy() { &hellip; }

&hellip; providers: [

{ provide: MyStrategy, useFactory: myStrategy }

]

&hellip;

</code-example>

<a id="function-calls-not-supported"></a>

## Вызовы функций не поддерживаются

<div class="alert is-helpful">

_Вызовы функций не поддерживаются. Подумайте о замене функции или лямбды ссылкой на экспортируемую функцию._

</div>

В настоящее время компилятор не поддерживает [функциональные выражения или лямбда-функции] (guide/aot-compiler#function-expression). Например, вы не можете установить `useFactory` провайдера на анонимную функцию или стрелочную функцию, как это сделано здесь.

<code-example format="typescript" language="typescript">

// ERROR &hellip;
провайдеры: [

{ provide: MyStrategy, useFactory: function() { &hellip; } },

{ provide: OtherStrategy, useFactory: () =&gt; { &hellip; } }

]

&hellip;

</code-example>

Вы также получите эту ошибку, если вызовете функцию или метод в `useValue` провайдера.

<code-example format="typescript" language="typescript">

// ERROR import { calculateValue } from './utilities';

&hellip; providers: [

{ provide: SomeValue, useValue: calculateValue() }

]

&hellip;

</code-example>

Чтобы исправить эту ошибку, экспортируйте функцию из модуля и обратитесь к ней в провайдере `useFactory`.

<code-example format="typescript" language="typescript">

// ИСПРАВЛЕН импорт { calculateValue } из './utilities';

export function myStrategy() { &hellip; } export function otherStrategy() { &hellip; }

export function someValueFactory() {

return calculateValue();

}

&hellip;

провайдеры: [

{ provide: MyStrategy, useFactory: myStrategy }

{ provide: OtherStrategy, useFactory: otherStrategy },

{ { provide: SomeValue, useFactory: someValueFactory }

]

&hellip;

</code-example>

<a id="destructured-variable-not-supported"></a>

## Деструктурированная переменная или константа не поддерживается

<div class="alert is-helpful">

_Ссылка на экспортируемую деструктурированную переменную или константу не поддерживается компилятором шаблонов. Рассмотрите возможность упрощения, чтобы избежать деструктуризации._

</div>

Компилятор не поддерживает ссылки на переменные, назначенные [деструктуризацией](https://www.typescriptlang.org/docs/handbook/variable-declarations.html#destructuring).

Например, вы не можете написать что-то вроде этого:

<code-example format="typescript" language="typescript">

// ERROR import { configuration } from './configuration';

// деструктурированное присвоение foo и bar const {foo, bar} = configuration;

&hellip;

providers: [

{provide: Foo, useValue: foo},

{provide: Bar, useValue: bar},

]

&hellip;

</code-example>

Чтобы исправить эту ошибку, обратитесь к неструктурированным значениям.

<code-example format="typescript" language="typescript">

// ИСПРАВЛЕН импорт { configuration } из './configuration';
&hellip;

провайдеры: [

{provide: Foo, useValue: configuration.foo},

{provide: Bar, useValue: configuration.bar},

]

&hellip;

</code-example>

<a id="could-not-resolve-type"></a>

## Не удалось определить тип

<div class="alert is-helpful">

_Компилятор встретил тип и не может определить, какой модуль экспортирует этот тип._

</div>

Это может произойти, если вы ссылаетесь на окружающий тип. Например, тип `Window` является окружающим типом, объявленным в глобальном файле `.d.ts`.

Вы получите ошибку, если обратитесь к нему в конструкторе компонента, который компилятор должен статически анализировать.

<code-example format="typescript" language="typescript">

// ERROR &commat;Component({ })
export class MyComponent {

constructor (private win: Window) { &hellip; }

}

</code-example>

TypeScript понимает окружающие типы, поэтому вы не импортируете их. Компилятор Angular не понимает тип, который вы пренебрегаете экспортом или импортом.

В данном случае компилятор не понимает, как внедрить что-то с помощью маркера `Window`.

Не ссылайтесь на окружающие типы в выражениях метаданных.

Если вам необходимо ввести экземпляр окружающего типа, вы можете решить эту проблему в четыре шага:

1.  Создайте инъекционный маркер для экземпляра окружающего типа.

1.  Создайте фабричную функцию, которая возвращает этот экземпляр.

1.  Добавьте провайдер `useFactory` к этой заводской функции.

1.  Используйте `@Inject` для инъекции экземпляра.

Вот наглядный пример.

<code-example format="typescript" language="typescript">

// ИСПРАВЛЕН импорт { Inject } из '&commat;angular/core';

export const WINDOW = new InjectionToken('Window'); export function \_window() { return window; }

&commat;Component({ &hellip;

providers: [

{ provide: WINDOW, useFactory: \_window }

]

})

export class MyComponent {

constructor (&commat;Inject(WINDOW) private win: Window) { &hellip; }

}

</code-example>

Тип `Window` в конструкторе больше не является проблемой для компилятора, потому что он использует `@Inject(WINDOW)` для генерации кода инъекции.

Angular делает нечто подобное с маркером `DOCUMENT`, чтобы вы могли внедрить объект `document` браузера\ (или его абстракцию, в зависимости от платформы, на которой работает приложение\).

<code-example format="typescript" language="typescript">

import { Inject } from '&commat;angular/core'; import { DOCUMENT } from '&commat;angular/common';

&commat;Component({ &hellip; }) export class MyComponent {

constructor (&commat;Inject(DOCUMENT) private doc: Document) { &hellip; }

}

</code-example>

<a id="name-expected"></a>

## Имя ожидается

<div class="alert is-helpful">

Компилятор ожидал увидеть имя в выражении, которое он оценивал.\_

</div>

Это может произойти, если вы используете число в качестве имени свойства, как в следующем примере.

<code-example format="typescript" language="typescript">

// ERROR provider: [{ provide: Foo, useValue: { 0: 'test' } }]

</code-example>

Измените имя свойства на нечисловое.

<code-example format="typescript" language="typescript">

// Исправленный провайдер: [{ provide: Foo, useValue: { '0': 'test' } }]

</code-example>

<a id="unsupported-enum-member-name"></a>

## Неподдерживаемое имя члена перечисления

<div class="alert is-helpful">

_Angular не смог определить значение [enum member](https://www.typescriptlang.org/docs/handbook/enums.html), на которое вы ссылались в метаданных._

</div>

Компилятор может понимать простые значения перечислений, но не сложные значения, например, полученные из вычисляемых свойств.

<code-example format="typescript" language="typescript">

// ERROR enum Colors {
Красный = 1,

Белый,

Blue = "Blue".length // вычислено

}

&hellip; providers: [

{ provide: BaseColor, useValue: Colors.White } // ok

{ provide: DangerColor, useValue: Colors.Red } // ok

{ provide: StrongColor, useValue: Colors.Blue } // плохо

]

&hellip;

</code-example>

Избегайте ссылок на перечисления со сложными инициализаторами или вычисляемыми свойствами.

<a id="tagged-template-expressions-not-supported"></a>

## Выражения шаблонов с метками не поддерживаются

<div class="alert is-helpful">

_Тегированные шаблонные выражения не поддерживаются в метаданных._

</div>

Компилятор встретил JavaScript ES2015 [tagged template expression](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Template_literals#Tagged_template_literals), такой как следующий.

<code-example format="typescript" language="typescript">

// ERROR const expression = 'funky';
const raw = String.raw`A tagged template &dollar;{expression} string`;

&hellip;

template: '&lt;div&gt;' + raw + '&lt;/div&gt;'

&hellip;

</code-example>

[`String.raw()`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/String/raw) - это _теговая функция_, встроенная в JavaScript ES2015.

Компилятор AOT не поддерживает выражения шаблонов с метками; избегайте их в выражениях метаданных.

<a id="symbol-reference-expected"></a>

## Ожидается ссылка на символ

<div class="alert is-helpful">

Компилятор ожидал получить ссылку на символ в месте, указанном в сообщении об ошибке.\_

</div>

Эта ошибка может возникнуть, если вы используете выражение в предложении `extends` класса.

<!--todo: Chuck: After reviewing your PR comment I'm still at a loss. See [comment there](https://github.com/angular/angular/pull/17712#discussion_r132025495). -->

<!-- links -->

<!-- external links -->

<!-- end links -->

:date: 28.02.2022
