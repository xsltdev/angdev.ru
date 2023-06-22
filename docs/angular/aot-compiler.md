# Компиляция с опережением времени (AOT)

Приложение Angular состоит в основном из компонентов и их HTML-шаблонов. Поскольку компоненты и шаблоны, предоставляемые Angular, не могут быть поняты браузером напрямую, приложения Angular требуют процесса компиляции перед запуском в браузере.

Компилятор Angular [ahead-of-time (AOT) compiler](guide/glossary#aot) преобразует ваш код Angular HTML и TypeScript в эффективный код JavaScript на этапе сборки _до_ того, как браузер загрузит и запустит этот код. Компиляция вашего приложения в процессе сборки обеспечивает более быстрый рендеринг в браузере.

Это руководство объясняет, как указать метаданные и применить доступные опции компилятора для эффективной компиляции ваших приложений с помощью компилятора AOT.

<div class="alert is-helpful">

[Смотрите, как Алекс Рикабо объясняет компилятор Angular] (https://www.youtube.com/watch?v=anphffaCZrQ) на AngularConnect 2019.

</div>

<a id="why-aot"></a>

Вот несколько причин, по которым вы можете захотеть использовать AOT.

| Reasons | Details | | :-------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Faster rendering | With AOT, the browser downloads a pre-compiled version of the application. The browser loads executable code so it can render the application immediately, without waiting to compile the application first. |
| Fewer asynchronous requests | The compiler _inlines_ external HTML templates and CSS style sheets within the application JavaScript, eliminating separate ajax requests for those source files. |
| Smaller Angular framework download size | There's no need to download the Angular compiler if the application is already compiled. The compiler is roughly half of Angular itself, so omitting it dramatically reduces the application payload. |
| Detect template errors earlier | The AOT compiler detects and reports template binding errors during the build step before users can see them. |
| Better security | AOT compiles HTML templates and components into JavaScript files long before they are served to the client. With no templates to read and no risky client-side HTML or JavaScript evaluation, there are fewer opportunities for injection attacks. |

<a id="обзор"></a>

## Выбор компилятора

Angular предлагает два способа компиляции вашего приложения:

| Angular compile | Details | | | :-------------------- | :------------------------------------------------------------------------------------------------ |.

| Just-in-Time \(JIT\) | Компилирует ваше приложение в браузере во время выполнения. Это было по умолчанию до Angular 8. |

| Ahead-of-Time \(AOT\) | Компилирует ваше приложение и библиотеки во время сборки. Этот вариант используется по умолчанию, начиная с Angular 9. |

Когда вы выполняете CLI-команды [`ng build`](cli/build) \(build only\) или [`ng serve`](cli/serve) \(build and serve locally\), тип компиляции \(JIT или AOT\) зависит от значения свойства `aot` в вашей конфигурации сборки, указанной в `angular.json`. По умолчанию `aot` установлено в `true` для новых приложений CLI.

Дополнительную информацию см. в [CLI command reference](cli) и [Building and serving Angular apps](guide/build).

## Как работает AOT

Компилятор Angular AOT извлекает **метаданные** для интерпретации частей приложения, которыми должен управлять Angular. Вы можете указать метаданные явно в **декораторах**, таких как `@Component()` и `@Input()`, или неявно в объявлениях конструкторов декорированных классов.

Метаданные указывают Angular, как создавать экземпляры классов вашего приложения и взаимодействовать с ними во время выполнения.

В следующем примере объект метаданных `@Component()` и конструктор класса указывают Angular, как создать и отобразить экземпляр `TypicalComponent`.

<code-example format="typescript" language="typescript">

&commat;Component({ selector: 'app-typical',
template: '&lt;div&gt;Типичный компонент для {{data.name}}&lt;/div&gt;'

})

export class TypicalComponent {

&commat;Input() data: TypicalData;

constructor(private someService: SomeService) { &hellip; }

}

</code-example>

Компилятор Angular извлекает метаданные _один раз_ и создает _фабрику_ для `TypicalComponent`. Когда нужно создать экземпляр `TypicalComponent`, Angular вызывает фабрику, которая создает новый визуальный элемент, привязанный к новому экземпляру класса компонента с инжектированной зависимостью.

### Фазы компиляции

Существует три фазы компиляции AOT.

| | Фаза | Детали | | :-- | :--------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |.

| 1 | анализ кода | На этой фазе компилятор TypeScript и _AOT-сборщик_ создают представление исходного текста. Сборщик не пытается интерпретировать метаданные, которые он собирает. Он представляет метаданные как можно лучше и записывает ошибки, когда обнаруживает нарушение синтаксиса метаданных. |

2 | 2 | Генерация кода | На этой фазе `StaticReflector` компилятора интерпретирует метаданные, собранные на фазе 1, выполняет дополнительную проверку метаданных и выдает ошибку, если обнаруживает нарушение ограничений метаданных. |

3 | | Проверка типов шаблонов | На этом необязательном этапе компилятор шаблонов Angular _template compiler_ использует компилятор TypeScript для проверки выражений привязки в шаблонах. Вы можете включить эту фазу явно, установив параметр конфигурации `strictTemplates`; см. [Angular compiler options](guide/angular-compiler-options). |

### Ограничения метаданных

Вы пишете метаданные в _подмножестве_ TypeScript, которое должно соответствовать следующим общим ограничениям:

-   Ограничить [синтаксис выражения](#expression-syntax) поддерживаемым подмножеством JavaScript.

-   Ссылаться на экспортированные символы только после [сворачивания кода](#code-folding)

-   Вызывать только [функции, поддерживаемые](#supported-functions) компилятором.

-   Ввод/вывод и связанные с данными члены класса должны быть общедоступными или защищенными.

Дополнительные рекомендации и инструкции по подготовке приложения к компиляции AOT см. в [Angular: Writing AOT-friendly applications](https://medium.com/sparkles-blog/angular-writing-aot-friendly-applications-7b64c8afbe3f).

<div class="alert is-helpful">

Ошибки при компиляции AOT обычно возникают из-за метаданных, которые не соответствуют требованиям компилятора\(более подробно описано ниже\). Для помощи в понимании и решении этих проблем смотрите [AOT Metadata Errors](guide/aot-metadata-errors).

</div>

### Настройка компиляции AOT

В файле [TypeScript configuration file](guide/typescript-configuration) можно указать опции, управляющие процессом компиляции. Полный список доступных опций см. в [Angular compiler options](guide/angular-compiler-options).

## Фаза 1: Анализ кода

Компилятор TypeScript выполняет часть аналитической работы на первом этапе. Он создает `.d.ts` _файлы определения типов_ с информацией о типах, которая необходима компилятору AOT для генерации кода приложения.

В то же время AOT **коллектор** анализирует метаданные, записанные в декораторах Angular, и выводит информацию о метаданных в файлы **`.metadata.json`**, по одному на файл `.d.ts`.

Вы можете думать о `.metadata.json` как о диаграмме общей структуры метаданных декоратора, представленной в виде [абстрактного синтаксического дерева (AST)] (https://en.wikipedia.org/wiki/Abstract_syntax_tree).

<div class="alert is-helpful">

В [schema.ts](https://github.com/angular/angular/blob/main/packages/compiler-cli/src/metadata/schema.ts) Angular формат JSON описывается как набор интерфейсов TypeScript.

</div>

<a id="expression-syntax"></a>

### Ограничения синтаксиса выражений

Коллектор AOT понимает только подмножество JavaScript. Определяйте объекты метаданных с помощью следующего ограниченного синтаксиса:

| Syntax | Example | | :------------------------ | :---------------------------------------------------------------------- |
| Literal object | `{cherry: true, apple: true, mincemeat: false}` |

| Literal array | `['cherries', 'flour', 'sugar']` |

| Spread in literal array | `['apples', 'flour', ...]` |

| Calls | `bake(ingredients)` |

| New | `new Oven()` |

| Property access | `pie.slice` |

| Array index | `ingredients[0]` |

| Identity reference | `Component` |

| A template string | <code>&grave;pie is \${multiplier} times better than cake&grave;</code> |

| Literal string | `'pi'` |

| Literal number | `3.14153265` |

| Literal boolean | `true` |

| Literal null | `null` |

| Supported prefix operator | `!cake` |

| Supported binary operator | `a+b` |

| Conditional operator | `a ? b : c` |

| Parentheses | `(a+b)` |

Если в выражении используется неподдерживаемый синтаксис, сборщик записывает узел ошибки в файл `.metadata.json`. Позже компилятор сообщает об ошибке, если ему нужна эта часть метаданных для генерации кода приложения.

<div class="alert is-helpful">

Если вы хотите, чтобы `ngc` немедленно сообщал о синтаксических ошибках, а не создавал файл `.metadata.json` с ошибками, установите опцию `strictMetadataEmit` в конфигурационном файле TypeScript.

<code-example format="json" language="json">

"angularCompilerOptions": { &hellip;
"strictMetadataEmit" : true

}

</code-example>

В библиотеках Angular есть эта опция для обеспечения чистоты всех файлов Angular `.metadata.json`, и это лучшая практика - делать то же самое при создании собственных библиотек.

</div>

<a id="function-expression"></a> <a id="arrow-functions"></a>

### Нет стрелочных функций

Компилятор AOT не поддерживает [функциональные выражения](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Operators/function) и [стрелочные функции](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Functions/Arrow_functions), также называемые _лямбда_ функциями.

Рассмотрим следующий декоратор компонента:

<code-example format="typescript" language="typescript">

&commat;Component({ &hellip;
провайдеры: [{ {provide: server, useFactory: () =&gt; new Server()}]]

})

</code-example>

Коллектор AOT не поддерживает функцию стрелки, `() => new Server()`, в выражении метаданных. Вместо функции он генерирует узел ошибки.
Когда компилятор позже интерпретирует этот узел, он сообщает об ошибке, предлагая вам превратить стрелочную функцию в _экспортируемую функцию_.

Вы можете исправить ошибку, преобразовав ее в это выражение:

<code-example format="typescript" language="typescript">

export function serverFactory() { return new Server();
}

&commat;Component({ &hellip;

провайдеры: [{ {provide: server, useFactory: serverFactory}]]

})

</code-example>

В версии 5 и более поздних компилятор автоматически выполняет эту перезапись при эмуляции файла `.js`.

<a id="exported-symbols"></a> <a id="code-folding"></a>

### Свертывание кода

Компилятор может разрешать только ссылки на **_экспортированные_** символы. Однако сборщик может оценить выражение во время сбора и записать результат в `.metadata.json`, а не исходное выражение.

Это позволяет ограниченно использовать неэкспортированные символы в выражениях.

Например, сборщик может оценить выражение `1 + 2 + 3 + 4` и заменить его результатом `10`. Этот процесс называется _складыванием_.

Выражение, которое может быть сокращено таким образом, является _складываемым_.

<a id="var-declaration"></a>

Коллектор может оценивать ссылки на локальные для модуля объявления `const` и инициализированные объявления `var` и `let`, эффективно удаляя их из файла `.metadata.json`.

Рассмотрим следующее определение компонента:

<code-example format="typescript" language="typescript">

const template = '&lt;div&gt;{{hero.name}}&lt;/div&gt;';

&commat;Component({ selector: 'app-hero',

template: template

})

export class HeroComponent {

&commat;Input() hero: Hero;

}

</code-example>

Компилятор не может сослаться на константу `template`, поскольку она не экспортируется. Однако сборщик может включить константу `template` в определение метаданных, вписав ее содержимое.
Эффект будет таким же, как если бы вы написали:

<code-example format="typescript" language="typescript">

&commat;Component({ selector: 'app-hero',
template: '&lt;div&gt;{{hero.name}}&lt;/div&gt;'

})

export class HeroComponent {

&commat;Input() hero: Hero;

}

</code-example>

Больше нет ссылки на `template` и, следовательно, компилятору нечего беспокоить, когда он позже интерпретирует вывод _коллектора_ в `.metadata.json`.

Вы можете пойти дальше, включив константу `template` в другое выражение:

<code-example format="typescript" language="typescript">

const template = '&lt;div&gt;{{hero.name}}&lt;/div&gt;';

&commat;Component({ selector: 'app-hero',

template: template + '&lt;div&gt;{{hero.title}}&lt;/div&gt;'

})

export class HeroComponent {

&commat;Input() hero: Hero;

}

</code-example>

Коллектор сводит это выражение к эквивалентной _сложенной_ строке:

<code-example format="typescript" language="typescript">

'&lt;div&gt;{{hero.name}}&lt;/div&gt;&lt;div&gt;{{hero.title}}&lt;/div&gt;'

</code-example>

#### Складываемый синтаксис

В следующей таблице описано, какие выражения коллектор может складывать, а какие нет:

| Синтаксис | Складываемый | | :------------------------------- | :--------------------------------------- |

| Буквальный объект | да |

| Буквальный массив | да |

| Разброс в литеральном массиве | нет |

| Вызовы | нет |

| Новые | нет |

| Доступ к свойствам | да, если объект является сворачиваемым |

| Индекс массива | да, если цель и индекс складные | |

| Ссылка на идентичность | да, если это ссылка на локаль |

| Шаблон без подстановок | да | |

| Шаблон с подстановками | да, если подстановки складываемые | да.

| Буквальная строка | да |

| Буквальное число | да |

| Буквальное булево | да |

| Буквальный null | да |

| Поддерживается префиксный оператор | да, если операнд является складываемым | да.

| Поддерживается бинарный оператор | да, если и левый, и правый операнды являются складываемыми | да.

| Условный оператор | да, если условие является складываемым | |

| Родительские скобки | да, если выражение является складным | |

Если выражение не складывается, сборщик записывает его в `.metadata.json` в виде [AST](https://en.wikipedia.org/wiki/Abstract*syntax*tree), чтобы компилятор мог его разрешить.

## Фаза 2: генерация кода

Коллектор не пытается понять метаданные, которые он собирает и выводит в `.metadata.json`. Он представляет метаданные как можно лучше и записывает ошибки, когда обнаруживает нарушение синтаксиса метаданных.
Работа компилятора заключается в интерпретации `.metadata.json` на этапе генерации кода.

Компилятор понимает все синтаксические формы, которые поддерживает коллектор, но он может отвергнуть _синтаксически_ корректные метаданные, если _семантика_ нарушает правила компилятора.

### Публичные или защищенные символы

Компилятор может ссылаться только на _экспортируемые символы_.

-   Украшенные члены класса компонента должны быть публичными или защищенными.

    Нельзя сделать свойство `@Input()` приватным.

-   Свойства, связанные с данными, также должны быть публичными или защищенными

<a id="supported-functions"></a>

### Поддерживаемые классы и функции

Сборщик может представлять вызов функции или создание объекта с помощью `new` до тех пор, пока синтаксис корректен. Компилятор, однако, может впоследствии отказаться генерировать вызов _определенной_ функции или создание _определенного_ объекта.

Компилятор может создавать только экземпляры определенных классов, поддерживает только основные декораторы, и поддерживает только вызовы макросов\(функций или статических методов\), которые возвращают выражения.

| Действия компилятора | Подробности | | :------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------- |

| Новые экземпляры | Компилятор разрешает метаданные, создающие экземпляры класса `InjectionToken` из `@angular/core`. |

| Поддерживаемые декораторы | Компилятор поддерживает метаданные только для [декораторов Angular в модуле `@angular/core`](api/core#decorators). |

| Вызовы функций | Фабричные функции должны быть экспортируемыми, именованными функциями. Компилятор AOT не поддерживает лямбда-выражения \("стрелочные функции"\) для фабричных функций. |

<a id="function-calls"></a>

### Вызовы функций и статических методов

Коллектор принимает любую функцию или статический метод, содержащий единственный оператор `return`. Однако компилятор поддерживает только макросы в виде функций или статических методов, которые возвращают _выражение_.

Например, рассмотрим следующую функцию:

<code-example format="typescript" language="typescript">

export function wrapInArray&lt;T&gt;(value: T): T[] { return [value];
}

</code-example>

Вы можете вызвать `wrapInArray` в определении метаданных, потому что он возвращает значение выражения, которое соответствует ограничительному подмножеству JavaScript компилятора.

Вы можете использовать `wrapInArray()` следующим образом:

<code-example format="typescript" language="typescript">

&commat;NgModule({ declarations: wrapInArray(TypicalComponent))
})

export class TypicalModule {}

</code-example>

Компилятор воспринимает это использование так, как если бы вы написали:

<code-example format="typescript" language="typescript">

&commat;NgModule({ declarations: [TypicalComponent]
})

export class TypicalModule {}

</code-example>

Модуль Angular [`RouterModule`](api/router/RouterModule) экспортирует два макростатических метода, `forRoot` и `forChild`, чтобы помочь объявить корневые и дочерние маршруты. Просмотрите [исходный код](https://github.com/angular/angular/blob/main/packages/router/src/router_module.ts#L139 'RouterModule.forRoot source code')
для этих методов, чтобы увидеть, как макросы могут упростить настройку сложных [NgModules](guide/ngmodules).

<a id="metadata-rewriting"></a>

### Переписывание метаданных

Компилятор специально обрабатывает объектные литералы, содержащие поля `useClass`, `useValue`, `useFactory` и `data`, преобразуя выражение, инициализирующее одно из этих полей, в экспортируемую переменную, которая заменяет выражение. Этот процесс переписывания этих выражений снимает все ограничения на то, что может быть в них, потому что

компилятору не нужно знать значение выражения &mdash; ему просто нужно уметь генерировать ссылку на это значение.

Вы можете написать что-то вроде:

<code-example format="typescript" language="typescript">

class TypicalServer {

}

&commat;NgModule({ providers: [{ {provide: SERVER, useFactory: () =&gt; TypicalServer}]]

})

export class TypicalModule {}

</code-example>

Без переписывания это было бы некорректно, поскольку ламбды не поддерживаются, а `TypicalServer` не экспортируется. Чтобы разрешить это, компилятор автоматически переписывает это на что-то вроде:

<code-example format="typescript" language="typescript">

class TypicalServer {

}

export const &theta;0 = () =&gt; new TypicalServer();

&commat;NgModule({ providers: [{ {provide: SERVER, useFactory: &theta;0}]]

})

export class TypicalModule {}

</code-example>

Это позволяет компилятору генерировать ссылку на `θ0` в фабрике без необходимости знать, что содержит значение `θ0`.

Компилятор переписывает файл `.js` во время эмитата. Однако он не переписывает файл `.d.ts`, поэтому TypeScript не распознает его как экспорт.

И он не вмешивается в экспортируемый API модуля ES.

<a id="binding-expression-validation"></a>

## Фаза 3: Проверка типов шаблонов

Одной из наиболее полезных функций компилятора Angular является возможность проверки типов выражений в шаблонах и выявления любых ошибок до того, как они приведут к сбоям во время выполнения. На этапе проверки типов шаблонов компилятор шаблонов Angular использует компилятор TypeScript для проверки выражений привязки в шаблонах.

Включите эту фазу явно, добавив опцию компилятора `"fullTemplateTypeCheck"` в `"angularCompilerOptions"` файла конфигурации TypeScript проекта (см. [Angular Compiler Options](guide/angular-compiler-options)).

Проверка шаблонов выдает сообщения об ошибках, когда в выражении привязки шаблона обнаруживается ошибка типа, подобно тому, как компилятор TypeScript сообщает об ошибках типа в коде в файле `.ts`.

файле.

Например, рассмотрим следующий компонент:

<code-example format="typescript" language="typescript">

&commat;Component({ selector: 'my-component',
template: '{ {person.addresss.street}}'

})

class MyComponent {

person? Person;

}

</code-example>

При этом возникает следующая ошибка:

<code-example format="output" hideCopy language="shell">

my.component.ts.MyComponent.html(1,1): : Свойство 'addresss' не существует для типа 'Person'. Вы имели в виду 'адрес'?

</code-example>

Имя файла, указанное в сообщении об ошибке, `my.component.ts.MyComponent.html`, является синтетическим файлом, созданным компилятором шаблонов, который содержит содержимое шаблона класса `MyComponent`.
Компилятор никогда не записывает этот файл на диск.

Номера строк и столбцов относятся к строке шаблона в аннотации `@Component` класса, в данном случае `MyComponent`.

Если компонент использует `templateUrl` вместо `template`, то ошибки сообщаются в HTML-файл, на который ссылается `templateUrl`, а не в синтетический файл.

Местонахождение ошибки - это начало текстового узла, содержащего интерполяционное выражение с ошибкой. Если ошибка в привязке атрибута, например `[value]="person.address.street"`, то местоположение ошибки - это местоположение атрибута.

является местоположение атрибута, содержащего ошибку.

При проверке используется средство проверки типов TypeScript и опции, предоставляемые компилятору TypeScript, чтобы контролировать степень детализации проверки типов. Например, если указано `strictTypeChecks`, то ошибка

<code-example format="output" hideCopy language="shell">

my.component.ts.MyComponent.html(1,1): : Объект, возможно, 'неопределенный'

</code-example>

сообщается, как и вышеприведенное сообщение об ошибке.

### Сужение типов

Выражение, используемое в директиве `ngIf`, используется для сужения объединений типов в компиляторе шаблонов Angular, точно так же, как это делает выражение `if` в TypeScript.

Например, чтобы избежать ошибки `Object is possibly 'undefined'` в шаблоне выше, измените его так, чтобы он выдавал интерполяцию, только если значение `person` инициализировано, как показано ниже:

<code-example format="typescript" language="typescript">

&commat;Component({ selector: 'my-component',
template: '<span \*ngIf="person"> {{person.address.street}} </span>'

})

class MyComponent {

person?: Person;

}

</code-example>

Использование `*ngIf` позволяет компилятору TypeScript сделать вывод, что `person`, используемый в выражении привязки, никогда не будет `undefined`.

Для получения дополнительной информации о сужении входного типа смотрите [Улучшение проверки типов шаблонов для пользовательских директив](guide/structural-directives#directive-type-checks).

### Оператор утверждения типа non-null

Используйте [оператор утверждения типа non-null](guide/template-expression-operators#non-null-assertion-operator) для подавления ошибки `Object is possibly 'undefined'`, когда неудобно использовать `*ngIf` или когда некоторые ограничения в компоненте гарантируют, что выражение всегда будет non-null при интерполяции выражения связывания.

В следующем примере свойства `person` и `address` всегда установлены вместе, что подразумевает, что `address` всегда будет non-null, если `person` будет non-null. Не существует удобного способа описать это ограничение для TypeScript и компилятора шаблонов, но в примере ошибка подавлена за счет использования `address!.street`.

<code-example format="typescript" language="typescript">

&commat;Component({ selector: 'my-component',
template: '&lt;span \*ngIf="person"&gt; {{person.name}} живет на {{address!.street}} &lt;/span&gt;'

})

class MyComponent {

person? Person;

адрес? Адрес;

setData(person: Person, address: Address) { this.person = person;

this.address = address;

}

}

</code-example>

Оператор утверждения non-null следует использовать осторожно, так как рефакторинг компонента может нарушить это ограничение.

В данном примере рекомендуется включить проверку `address` в `*ngIf`, как показано ниже:

<code-example format="typescript" language="typescript">

&commat;Component({ selector: 'my-component',
template: '&lt;span \*ngIf="person &amp;&amp; address"&gt; {{person.name}} lives on {{address.street}} &lt;/span&gt;'

})

class MyComponent {

person? Person;

адрес? Адрес;

setData(person: Person, address: Address) { this.person = person;

this.address = address;

}

}

</code-example>

<!-- links -->

<!-- external links -->

<!-- end links -->

:date: 28.02.2022
