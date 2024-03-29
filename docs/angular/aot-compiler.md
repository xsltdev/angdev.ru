---
description: Это руководство объясняет, как указать метаданные и применить доступные опции компилятора для эффективной компиляции ваших приложений с помощью компилятора AOT
---

# Компиляция с опережением времени (AOT)

Приложение Angular состоит в основном из компонентов и их HTML-шаблонов. Поскольку компоненты и шаблоны, предоставляемые Angular, не могут быть поняты браузером напрямую, приложения Angular требуют процесса компиляции перед запуском в браузере.

Компилятор Angular [ahead-of-time (AOT) compiler](glossary.md#aot) преобразует ваш код Angular HTML и TypeScript в эффективный код JavaScript на этапе сборки _до_ того, как браузер загрузит и запустит этот код. Компиляция вашего приложения в процессе сборки обеспечивает более быстрый рендеринг в браузере.

Это руководство объясняет, как указать метаданные и применить доступные опции компилятора для эффективной компиляции ваших приложений с помощью компилятора AOT.

!!!note ""

    [Смотрите, как Алекс Рикабо объясняет компилятор Angular](https://www.youtube.com/watch?v=anphffaCZrQ) на AngularConnect 2019.

Вот несколько причин, по которым вы можете захотеть использовать AOT.

| Причины                                    | Подробности                                                                                                                                                                                                                                              |
| :----------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Более быстрый рендеринг                    | При использовании AOT браузер загружает предварительно скомпилированную версию приложения. Браузер загружает исполняемый код и может сразу же отрисовать приложение, не дожидаясь его компиляции.                                                        |
| Меньше асинхронных запросов                | Компилятор _включает_ внешние HTML-шаблоны и таблицы стилей CSS в JavaScript приложения, устраняя отдельные ajax-запросы к этим исходным файлам.                                                                                                         |
| Меньший размер загрузки фреймворка Angular | Нет необходимости загружать компилятор Angular, если приложение уже скомпилировано. Компилятор составляет примерно половину самого Angular, поэтому его отказ от загрузки значительно уменьшает полезную нагрузку на приложение.                         |
| Более раннее обнаружение ошибок шаблонов   | Компилятор AOT обнаруживает и сообщает об ошибках привязки шаблонов на этапе сборки до того, как их увидят пользователи.                                                                                                                                 |
| Повышение безопасности                     | AOT компилирует HTML-шаблоны и компоненты в файлы JavaScript задолго до того, как они будут переданы клиенту. Отсутствие необходимости читать шаблоны и рискованной оценки HTML или JavaScript на стороне клиента снижает вероятность инъекционных атак. |

## Выбор компилятора {: #choosing-a-compiler}

Angular предлагает два способа компиляции вашего приложения:

| Angular compile     | Details                                                                                                                |
| :------------------ | :--------------------------------------------------------------------------------------------------------------------- |
| Just-in-Time (JIT)  | Компилирует ваше приложение в браузере во время выполнения. Это было по умолчанию до Angular 8.                        |
| Ahead-of-Time (AOT) | Компилирует ваше приложение и библиотеки во время сборки. Этот вариант используется по умолчанию, начиная с Angular 9. |

Когда вы выполняете CLI-команды [`ng build`](https://angular.io/cli/build) (build only) или [`ng serve`](https://angular.io/cli/serve) (build and serve locally), тип компиляции (JIT или AOT) зависит от значения свойства `aot` в вашей конфигурации сборки, указанной в `angular.json`. По умолчанию `aot` установлено в `true` для новых приложений CLI.

Дополнительную информацию см. в [CLI command reference](https://angular.io/cli) и [Building and serving Angular apps](build.md).

## Как работает AOT

Компилятор Angular AOT извлекает **метаданные** для интерпретации частей приложения, которыми должен управлять Angular. Вы можете указать метаданные явно в **декораторах**, таких как `@Component()` и `@Input()`, или неявно в объявлениях конструкторов декорированных классов.

Метаданные указывают Angular, как создавать экземпляры классов вашего приложения и взаимодействовать с ними во время выполнения.

В следующем примере объект метаданных `@Component()` и конструктор класса указывают Angular, как создать и отобразить экземпляр `TypicalComponent`.

```ts
@Component({
  selector: 'app-typical',
  template: '<div>A typical component for {{data.name}}</div>'
})
export class TypicalComponent {
  @Input() data: TypicalData;
  constructor(private someService: SomeService) { … }
}
```

Компилятор Angular извлекает метаданные _один раз_ и создает _фабрику_ для `TypicalComponent`. Когда нужно создать экземпляр `TypicalComponent`, Angular вызывает фабрику, которая создает новый визуальный элемент, привязанный к новому экземпляру класса компонента с инжектированной зависимостью.

### Фазы компиляции

Существует три фазы компиляции AOT.

|     | Фаза                    | Детали                                                                                                                                                                                                                                                                                                      |
| :-- | :---------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | анализ кода             | На этой фазе компилятор TypeScript и _AOT-сборщик_ создают представление исходного текста. Сборщик не пытается интерпретировать метаданные, которые он собирает. Он представляет метаданные как можно лучше и записывает ошибки, когда обнаруживает нарушение синтаксиса метаданных.                        |
| 2   | Генерация кода          | На этой фазе `StaticReflector` компилятора интерпретирует метаданные, собранные на фазе 1, выполняет дополнительную проверку метаданных и выдает ошибку, если обнаруживает нарушение ограничений метаданных.                                                                                                |
| 3   | Проверка типов шаблонов | На этом необязательном этапе компилятор шаблонов Angular _template compiler_ использует компилятор TypeScript для проверки выражений привязки в шаблонах. Вы можете включить эту фазу явно, установив параметр конфигурации `strictTemplates`; см. [Angular compiler options](angular-compiler-options.md). |

### Ограничения метаданных

Вы пишете метаданные в _подмножестве_ TypeScript, которое должно соответствовать следующим общим ограничениям:

-   Ограничить [синтаксис выражения](#expression-syntax) поддерживаемым подмножеством JavaScript.
-   Ссылаться на экспортированные символы только после [сворачивания кода](#code-folding)
-   Вызывать только [функции, поддерживаемые](#supported-functions) компилятором.
-   Ввод/вывод и связанные с данными члены класса должны быть общедоступными или защищенными.

Дополнительные рекомендации и инструкции по подготовке приложения к компиляции AOT см. в [Angular: Writing AOT-friendly applications](https://medium.com/sparkles-blog/angular-writing-aot-friendly-applications-7b64c8afbe3f).

!!!note ""

    Ошибки при компиляции AOT обычно возникают из-за метаданных, которые не соответствуют требованиям компилятора (более подробно описано ниже). Для помощи в понимании и решении этих проблем смотрите [AOT Metadata Errors](aot-metadata-errors.md).

### Настройка компиляции AOT

В файле [TypeScript configuration file](typescript-configuration.md) можно указать опции, управляющие процессом компиляции. Полный список доступных опций см. в [Angular compiler options](angular-compiler-options.md).

## Фаза 1: Анализ кода

Компилятор TypeScript выполняет часть аналитической работы на первом этапе. Он создает `.d.ts` _файлы определения типов_ с информацией о типах, которая необходима компилятору AOT для генерации кода приложения.

В то же время AOT **коллектор** анализирует метаданные, записанные в декораторах Angular, и выводит информацию о метаданных в файлы **`.metadata.json`**, по одному на файл `.d.ts`.

Вы можете думать о `.metadata.json` как о диаграмме общей структуры метаданных декоратора, представленной в виде [абстрактного синтаксического дерева (AST)](https://ru.wikipedia.org/wiki/%D0%90%D0%B1%D1%81%D1%82%D1%80%D0%B0%D0%BA%D1%82%D0%BD%D0%BE%D0%B5_%D1%81%D0%B8%D0%BD%D1%82%D0%B0%D0%BA%D1%81%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%BE%D0%B5_%D0%B4%D0%B5%D1%80%D0%B5%D0%B2%D0%BE).

!!!note ""

    В [schema.ts](https://github.com/angular/angular/blob/main/packages/compiler-cli/src/metadata/schema.ts) Angular формат JSON описывается как набор интерфейсов TypeScript.

### Ограничения синтаксиса выражений {: #expression-syntax}

Коллектор AOT понимает только подмножество JavaScript. Определяйте объекты метаданных с помощью следующего ограниченного синтаксиса:

| Syntax                    | Example                                                                 |
| :------------------------ | :---------------------------------------------------------------------- |
| Literal object            | `{cherry: true, apple: true, mincemeat: false}`                         |
| Literal array             | `['cherries', 'flour', 'sugar']`                                        |
| Spread in literal array   | `['apples', 'flour', ...]`                                              |
| Calls                     | `bake(ingredients)`                                                     |
| New                       | `new Oven()`                                                            |
| Property access           | `pie.slice`                                                             |
| Array index               | `ingredients[0]`                                                        |
| Identity reference        | `Component`                                                             |
| A template string         | <code>&grave;pie is \${multiplier} times better than cake&grave;</code> |
| Literal string            | `'pi'`                                                                  |
| Literal number            | `3.14153265`                                                            |
| Literal boolean           | `true`                                                                  |
| Literal null              | `null`                                                                  |
| Supported prefix operator | `!cake`                                                                 |
| Supported binary operator | `a+b`                                                                   |
| Conditional operator      | `a ? b : c`                                                             |
| Parentheses               | `(a+b)`                                                                 |

Если в выражении используется неподдерживаемый синтаксис, сборщик записывает узел ошибки в файл `.metadata.json`. Позже компилятор сообщает об ошибке, если ему нужна эта часть метаданных для генерации кода приложения.

!!!note ""

    Если вы хотите, чтобы `ngc` немедленно сообщал о синтаксических ошибках, а не создавал файл `.metadata.json` с ошибками, установите опцию `strictMetadataEmit` в конфигурационном файле TypeScript.

    ```json
    "angularCompilerOptions": {
    …
    "strictMetadataEmit" : true
    }
    ```

    В библиотеках Angular есть эта опция для обеспечения чистоты всех файлов Angular `.metadata.json`, и это лучшая практика — делать то же самое при создании собственных библиотек.

### Нет стрелочных функций {: #function-expression}

Компилятор AOT не поддерживает [функциональные выражения](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Operators/function) и [стрелочные функции](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Functions/Arrow_functions), также называемые _лямбда_ функциями.

Рассмотрим следующий декоратор компонента:

```ts
@Component({
  …
  providers: [{provide: server, useFactory: () => new Server()}]
})
```

Коллектор AOT не поддерживает функцию стрелки, `() => new Server()`, в выражении метаданных. Вместо функции он генерирует узел ошибки.

Когда компилятор позже интерпретирует этот узел, он сообщает об ошибке, предлагая вам превратить стрелочную функцию в _экспортируемую функцию_.

Вы можете исправить ошибку, преобразовав ее в это выражение:

```ts
export function serverFactory() {
  return new Server();
}

@Component({
  …
  providers: [{provide: server, useFactory: serverFactory}]
})
```

В версии 5 и более поздних компилятор автоматически выполняет эту перезапись при эмуляции файла `.js`.

### Сворачивание кода {: #code-folding}

Компилятор может разрешать только ссылки на **_экспортированные_** символы. Однако сборщик может оценить выражение во время сбора и записать результат в `.metadata.json`, а не исходное выражение.

Это позволяет ограниченно использовать неэкспортированные символы в выражениях.

Например, сборщик может оценить выражение `1 + 2 + 3 + 4` и заменить его результатом `10`. Этот процесс называется _сворачиванием_.

Выражение, которое может быть сокращено таким образом, является _сворачиваемым_.

Коллектор может оценивать ссылки на локальные для модуля объявления `const` и инициализированные объявления `var` и `let`, эффективно удаляя их из файла `.metadata.json`.

Рассмотрим следующее определение компонента:

```ts
const template = '<div>{{hero.name}}</div>';

@Component({
    selector: 'app-hero',
    template: template,
})
export class HeroComponent {
    @Input() hero: Hero;
}
```

Компилятор не может сослаться на константу `template`, поскольку она не экспортируется. Однако сборщик может включить константу `template` в определение метаданных, вписав ее содержимое.
Эффект будет таким же, как если бы вы написали:

```ts
@Component({
    selector: 'app-hero',
    template: '<div>{{hero.name}}</div>',
})
export class HeroComponent {
    @Input() hero: Hero;
}
```

Больше нет ссылки на `template` и, следовательно, компилятору нечего беспокоить, когда он позже интерпретирует вывод _коллектора_ в `.metadata.json`.

Вы можете пойти дальше, включив константу `template` в другое выражение:

```ts
const template = '<div>{{hero.name}}</div>';

@Component({
    selector: 'app-hero',
    template: template + '<div>{{hero.title}}</div>',
})
export class HeroComponent {
    @Input() hero: Hero;
}
```

Коллектор сводит это выражение к эквивалентной _сёрнутой_ строке:

```ts
'<div>{{hero.name}}</div><div>{{hero.title}}</div>';
```

#### Свёртываемый синтаксис

В следующей таблице описано, какие выражения коллектор может сворачивать, а какие нет:

| Синтаксис                          | Сворачивается                                               |
| :--------------------------------- | :---------------------------------------------------------- |
| Буквальный объект                  | да                                                          |
| Буквальный массив                  | да                                                          |
| Spread в литеральном массиве       | нет                                                         |
| Вызовы                             | нет                                                         |
| Новые                              | нет                                                         |
| Доступ к свойствам                 | да, если объект является сворачиваемым                      |
| Индекс массива                     | да, если цель и индекс сворачиваемые                        |
| Ссылка на идентичность             | да, если это ссылка на локаль                               |
| Шаблон без подстановок             | да                                                          |
| Шаблон с подстановками             | да, если подстановки сворачиваемые                          |
| Буквальная строка                  | да                                                          |
| Буквальное число                   | да                                                          |
| Буквальное булево                  | да                                                          |
| Буквальный null                    | да                                                          |
| Поддерживается префиксный оператор | да, если операнд является сворачиваемым                     |
| Поддерживается бинарный оператор   | да, если и левый, и правый операнды являются сворачиваемыми |
| Условный оператор                  | да, если условие является сворачиваемым                     |
| Родительские скобки                | да, если выражение является сворачиваемм                    |

Если выражение не сворачивается, сборщик записывает его в `.metadata.json` в виде [AST](https://ru.wikipedia.org/wiki/%D0%90%D0%B1%D1%81%D1%82%D1%80%D0%B0%D0%BA%D1%82%D0%BD%D0%BE%D0%B5_%D1%81%D0%B8%D0%BD%D1%82%D0%B0%D0%BA%D1%81%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%BE%D0%B5_%D0%B4%D0%B5%D1%80%D0%B5%D0%B2%D0%BE), чтобы компилятор мог его разрешить.

## Фаза 2: генерация кода

Коллектор не пытается понять метаданные, которые он собирает и выводит в `.metadata.json`. Он представляет метаданные как можно лучше и записывает ошибки, когда обнаруживает нарушение синтаксиса метаданных.
Работа компилятора заключается в интерпретации `.metadata.json` на этапе генерации кода.

Компилятор понимает все синтаксические формы, которые поддерживает коллектор, но он может отвергнуть _синтаксически_ корректные метаданные, если _семантика_ нарушает правила компилятора.

### Публичные или защищенные символы

Компилятор может ссылаться только на _экспортируемые символы_.

-   Декорарованные члены класса компонента должны быть публичными или защищенными.

    Нельзя сделать свойство `@Input()` приватным.

-   Свойства, связанные с данными, также должны быть публичными или защищенными

### Поддерживаемые классы и функции {#supported-functions}

Сборщик может представлять вызов функции или создание объекта с помощью `new` до тех пор, пока синтаксис корректен. Компилятор, однако, может впоследствии отказаться генерировать вызов _определенной_ функции или создание _определенного_ объекта.

Компилятор может создавать только экземпляры определенных классов, поддерживает только основные декораторы, и поддерживает только вызовы макросов (функций или статических методов), которые возвращают выражения.

| Действия компилятора      | Подробности                                                                                                                                                          |
| :------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Новые экземпляры          | Компилятор разрешает метаданные, создающие экземпляры класса `InjectionToken` из `@angular/core`.                                                                    |
| Поддерживаемые декораторы | Компилятор поддерживает метаданные только для декораторов Angular в модуле `@angular/core`.                                                                          |
| Вызовы функций            | Фабричные функции должны быть экспортируемыми, именованными функциями. Компилятор AOT не поддерживает лямбда-выражения ("стрелочные функции") для фабричных функций. |

### Вызовы функций и статических методов {#function-calls}

Коллектор принимает любую функцию или статический метод, содержащий единственный оператор `return`. Однако компилятор поддерживает только макросы в виде функций или статических методов, которые возвращают _выражение_.

Например, рассмотрим следующую функцию:

```ts
export function wrapInArray<T>(value: T): T[] {
    return [value];
}
```

Вы можете вызвать `wrapInArray` в определении метаданных, потому что он возвращает значение выражения, которое соответствует ограничительному подмножеству JavaScript компилятора.

Вы можете использовать `wrapInArray()` следующим образом:

```ts
@NgModule({ declarations: wrapInArray(TypicalComponent) })
export class TypicalModule {}
```

Компилятор воспринимает это использование так, как если бы вы написали:

```ts
@NgModule({ declarations: [TypicalComponent] })
export class TypicalModule {}
```

Модуль Angular [`RouterModule`](https://angular.io/api/router/RouterModule) экспортирует два макростатических метода, `forRoot` и `forChild`, чтобы помочь объявить корневые и дочерние маршруты. Просмотрите [исходный код](https://github.com/angular/angular/blob/main/packages/router/src/router_module.ts#L139 'RouterModule.forRoot source code') для этих методов, чтобы увидеть, как макросы могут упростить настройку сложных [NgModules](ngmodules.md).

### Переписывание метаданных {#metadata-rewriting}

Компилятор специально обрабатывает объектные литералы, содержащие поля `useClass`, `useValue`, `useFactory` и `data`, преобразуя выражение, инициализирующее одно из этих полей, в экспортируемую переменную, которая заменяет выражение. Этот процесс переписывания этих выражений снимает все ограничения на то, что может быть в них, потому что

компилятору не нужно знать значение выражения &mdash; ему просто нужно уметь генерировать ссылку на это значение.

Вы можете написать что-то вроде:

```ts
class TypicalServer {}

@NgModule({
    providers: [
        {
            provide: SERVER,
            useFactory: () => TypicalServer,
        },
    ],
})
export class TypicalModule {}
```

Без переписывания это было бы некорректно, поскольку ламбды не поддерживаются, а `TypicalServer` не экспортируется. Чтобы разрешить это, компилятор автоматически переписывает это на что-то вроде:

```ts
class TypicalServer {}

export const θ0 = () => new TypicalServer();

@NgModule({
    providers: [{ provide: SERVER, useFactory: θ0 }],
})
export class TypicalModule {}
```

Это позволяет компилятору генерировать ссылку на `θ0` в фабрике без необходимости знать, что содержит значение `θ0`.

Компилятор переписывает файл `.js` во время эмитата. Однако он не переписывает файл `.d.ts`, поэтому TypeScript не распознает его как экспорт.

И он не вмешивается в экспортируемый API модуля ES.

## Фаза 3: Проверка типов шаблонов {#binding-expression-validation}

Одной из наиболее полезных функций компилятора Angular является возможность проверки типов выражений в шаблонах и выявления любых ошибок до того, как они приведут к сбоям во время выполнения. На этапе проверки типов шаблонов компилятор шаблонов Angular использует компилятор TypeScript для проверки выражений привязки в шаблонах.

Включите эту фазу явно, добавив опцию компилятора `"fullTemplateTypeCheck"` в `"angularCompilerOptions"` файла конфигурации TypeScript проекта (см. [Angular Compiler Options](angular-compiler-options.md)).

Проверка шаблонов выдает сообщения об ошибках, когда в выражении привязки шаблона обнаруживается ошибка типа, подобно тому, как компилятор TypeScript сообщает об ошибках типа в коде в файле `.ts`.

Например, рассмотрим следующий компонент:

```ts
@Component({
    selector: 'my-component',
    template: '{{person.addresss.street}}',
})
class MyComponent {
    person?: Person;
}
```

При этом возникает следующая ошибка:

```
my.component.ts.MyComponent.html(1,1): : Property 'addresss' does not exist on type 'Person'. Did you mean 'address'?
```

Имя файла, указанное в сообщении об ошибке, `my.component.ts.MyComponent.html`, является синтетическим файлом, созданным компилятором шаблонов, который содержит содержимое шаблона класса `MyComponent`. Компилятор никогда не записывает этот файл на диск.

Номера строк и столбцов относятся к строке шаблона в аннотации `@Component` класса, в данном случае `MyComponent`.

Если компонент использует `templateUrl` вместо `template`, то ошибки сообщаются в HTML-файл, на который ссылается `templateUrl`, а не в синтетический файл.

Местонахождение ошибки — это начало текстового узла, содержащего интерполяционное выражение с ошибкой. Если ошибка в привязке атрибута, например `[value]="person.address.street"`, то местоположение ошибки — это местоположение атрибута, содержащего ошибку.

При проверке используется средство проверки типов TypeScript и опции, предоставляемые компилятору TypeScript, чтобы контролировать степень детализации проверки типов. Например, если указано `strictTypeChecks`, то ошибка

```
my.component.ts.MyComponent.html(1,1): : Object is possibly 'undefined'
```

сообщается, как и вышеприведенное сообщение об ошибке.

### Сужение типов

Выражение, используемое в директиве `ngIf`, используется для сужения объединений типов в компиляторе шаблонов Angular, точно так же, как это делает выражение `if` в TypeScript.

Например, чтобы избежать ошибки `Object is possibly 'undefined'` в шаблоне выше, измените его так, чтобы он выдавал интерполяцию, только если значение `person` инициализировано, как показано ниже:

```ts
@Component({
    selector: 'my-component',
    template: ' {{person.address.street}} ',
})
class MyComponent {
    person?: Person;
}
```

Использование `*ngIf` позволяет компилятору TypeScript сделать вывод, что `person`, используемый в выражении привязки, никогда не будет `undefined`.

Для получения дополнительной информации о сужении входного типа смотрите [Улучшение проверки типов шаблонов для пользовательских директив](structural-directives.md#directive-type-checks).

### Оператор утверждения типа non-null

Используйте оператор утверждения типа non-null для подавления ошибки `Object is possibly 'undefined'`, когда неудобно использовать `*ngIf` или когда некоторые ограничения в компоненте гарантируют, что выражение всегда будет non-null при интерполяции выражения связывания.

В следующем примере свойства `person` и `address` всегда установлены вместе, что подразумевает, что `address` всегда будет non-null, если `person` будет non-null. Не существует удобного способа описать это ограничение для TypeScript и компилятора шаблонов, но в примере ошибка подавлена за счет использования `address!.street`.

```ts
@Component({
    selector: 'my-component',
    template:
        '<span *ngIf="person"> {{person.name}} lives on {{address!.street}} </span>',
})
class MyComponent {
    person?: Person;
    address?: Address;

    setData(person: Person, address: Address) {
        this.person = person;
        this.address = address;
    }
}
```

Оператор утверждения non-null следует использовать осторожно, так как рефакторинг компонента может нарушить это ограничение.

В данном примере рекомендуется включить проверку `address` в `*ngIf`, как показано ниже:

```ts
@Component({
    selector: 'my-component',
    template:
        '<span *ngIf="person && address"> {{person.name}} lives on {{address.street}} </span>',
})
class MyComponent {
    person?: Person;
    address?: Address;

    setData(person: Person, address: Address) {
        this.person = person;
        this.address = address;
    }
}
```

## Ссылки

-   [Ahead-of-time (AOT) compilation](https://angular.io/guide/aot-compiler)
