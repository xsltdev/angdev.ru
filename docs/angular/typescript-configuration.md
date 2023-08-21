---
description: TypeScript - основной язык для разработки приложений Angular. Он представляет собой надмножество JavaScript с поддержкой безопасности типов и инструментальных средств во время проектирования
---

# Конфигурация TypeScript

:date: 24.10.2022

TypeScript - основной язык для разработки приложений Angular. Он представляет собой надмножество JavaScript с поддержкой безопасности типов и инструментальных средств во время проектирования.

Браузеры не могут выполнять TypeScript напрямую. Typescript должен быть "транспилирован" в JavaScript с помощью компилятора _tsc_, что требует определенной настройки.

На этой странице рассматриваются некоторые аспекты конфигурации TypeScript и среды TypeScript которые важны для разработчиков Angular, включая подробности о следующих файлах:

| Файлы                                                 | Подробности                          |
| :---------------------------------------------------- | :----------------------------------- |
| [tsconfig.json](typescript-configuration.md#tsconfig) | Конфигурация компилятора TypeScript. |
| [typings](typescript-configuration.md#typings)        | Файлы декларации языка TypesScript.  |

## Конфигурационные файлы {#tsconfig}

Данное рабочее пространство Angular содержит несколько конфигурационных файлов TypeScript. В корневом файле `tsconfig.json` задаются базовые опции TypeScript и компилятора Angular, которые наследуются всеми проектами в рабочем пространстве.

!!!note ""

    Информацию о том, какие опции доступны для компилятора Angular, см. в руководстве [Angular compiler options](angular-compiler-options.md).

В TypeScript и Angular имеется широкий набор опций, которые можно использовать для настройки функций проверки типов и генерируемого вывода. Более подробную информацию см. в разделе [Наследование конфигурации с помощью extends](https://www.typescriptlang.org/docs/handbook/tsconfig-json.html#configuration-inheritance-with-extends) документации по TypeScript.

!!!note ""

    Более подробную информацию о конфигурационных файлах TypeScript см. в официальном руководстве [TypeScript handbook](https://www.typescriptlang.org/docs/handbook/tsconfig-json.html). Подробнее о наследовании конфигурации см. в разделе [Наследование конфигурации с помощью extends](https://www.typescriptlang.org/docs/handbook/tsconfig-json.html#configuration-inheritance-with-extends).

Начальный `tsconfig.json` для рабочего пространства Angular обычно выглядит следующим образом.

```json
/* To learn more about this file see: https://angular.io/guide/typescript-configuration. */
{
    "compileOnSave": false,
    "compilerOptions": {
        "baseUrl": "./",
        "forceConsistentCasingInFileNames": true,
        "strict": true,
        "noImplicitOverride": true,
        "noPropertyAccessFromIndexSignature": true,
        "noImplicitReturns": true,
        "noFallthroughCasesInSwitch": true,
        "sourceMap": true,
        "declaration": false,
        "downlevelIteration": true,
        "experimentalDecorators": true,
        "moduleResolution": "node",
        "importHelpers": true,
        "target": "ES2022",
        "module": "ES2022",
        "useDefineForClassFields": false,
        "lib": ["ES2022", "dom"]
    },
    "angularCompilerOptions": {
        "enableI18nLegacyMessageIdFormat": false,
        "strictInjectionParameters": true,
        "strictInputAccessModifiers": true,
        "strictTemplates": true
    }
}
```

### `noImplicitAny` и `suppressImplicitAnyIndexErrors` {#noImplicitAny}

Разработчики TypeScript расходятся во мнениях относительно того, каким должен быть флаг `noImplicitAny` - `true` или `false`. Правильного ответа нет, и флаг можно изменить позже. Но ваш выбор сейчас может иметь значение в больших проектах, поэтому он заслуживает обсуждения.

Если флаг `noImplicitAny` установлен в значение `false` (по умолчанию), и если компилятор не может вывести тип переменной на основании того, как она используется, то он молча присваивает ей тип `any`. Именно это и подразумевается под _implicit `any`_.

Если флаг `noImplicitAny` установлен `true` и компилятор TypeScript не может определить тип, он все равно генерирует JavaScript-файлы, но при этом **сообщает об ошибке**. Многие опытные разработчики предпочитают использовать эту более строгую настройку, поскольку проверка типов позволяет выявить больше непреднамеренных ошибок во время компиляции.

Вы можете установить тип переменной `any`, даже если флаг `noImplicitAny` равен `true`.

Когда флаг `noImplicitAny` установлен `true`, вы также можете получить _имплицитные индексные ошибки_. Большинство разработчиков считают, что _эти ошибки_ скорее раздражают, чем помогают. Подавить их можно с помощью следующего дополнительного флага:

```json
"suppressImplicitAnyIndexErrors": true
```

!!!note ""

    Подробнее о том, как конфигурация TypeScript влияет на компиляцию, см. в разделах [Angular Compiler Options](angular-compiler-options.md) и [Template Type Checking](template-typecheck.md).

## Типизации TypeScript {#typings}

Многие библиотеки JavaScript, такие как jQuery, библиотека тестирования Jasmine и Angular, расширяют среду JavaScript функциями и синтаксисом, которые компилятор TypeScript не распознает как родные. Когда компилятор не распознает что-либо, он сообщает об ошибке.

Используйте [файлы определения типов TypeScript](https://www.typescriptlang.org/docs/handbook/writing-declaration-files.html) &mdash; `d.ts` файлы &mdash;, чтобы сообщить компилятору о загружаемых библиотеках.

Редакторы, поддерживающие TypeScript, используют эти же файлы определений для отображения информации о типах библиотечных функций.

Многие библиотеки включают файлы определений в свои пакеты npm, где их могут найти как компилятор TypeScript, так и редакторы. Angular является одной из таких библиотек. Папка `node_modules/@angular/core/` любого приложения Angular содержит несколько файлов `d.ts`, которые описывают части Angular.

!!!note ""

    Для получения файлов _typings_ для пакетов библиотек, включающих файлы `d.ts`, ничего делать не нужно. Пакеты Angular уже включают их в себя.

### `lib`

TypeScript включает в себя набор файлов деклараций по умолчанию. Эти файлы содержат декларации окружения для различных распространенных конструкций JavaScript, присутствующих в средах выполнения JavaScript и DOM.

Более подробную информацию можно найти в разделе [lib](https://www.typescriptlang.org/tsconfig#lib) руководства по TypeScript.

### Устанавливаемые файлы типизации

Многие библиотеки &mdash; среди них jQuery, Jasmine и Lodash &mdash; _не_ включают файлы `d.ts` в свои npm-пакеты. К счастью, либо их авторы, либо участники сообщества создали отдельные файлы `d.ts` для этих библиотек и опубликовали их в известных местах.

Вы можете установить эти типизации с помощью `npm`, используя [`@types/*` scoped package](https://www.typescriptlang.org/docs/handbook/declaration-files/consumption.html).

Какие файлы объявления окружения в `@types/*` включаются автоматически, определяется опцией [`types` компилятора TypeScript](https://www.typescriptlang.org/tsconfig#types). Angular CLI генерирует файл `tsconfig.app.json`, который используется для сборки приложения, в котором опция компилятора `types` установлена в значение `[]`, чтобы отключить автоматическое включение деклараций из `@types/*`. Аналогично, для тестирования используется файл `tsconfig.spec.json`, в котором установлено значение `"types": ["jasmine"]`, чтобы разрешить использование в тестах деклараций окружения Jasmine.

После установки деклараций `@types/*` необходимо обновить файлы `tsconfig.app.json` и `tsconfig.spec.json` для добавления вновь установленных деклараций в список `types`. Если декларации предназначены только для тестирования, то следует обновить только файл `tsconfig.spec.json`.

Например, для установки типизаций для `chai` необходимо выполнить команду `npm install @types/chai --save-dev`, а затем обновить файл `tsconfig.spec.json` для добавления `"chai"` в список `types`.

### `target` {#target}

По умолчанию в качестве целевого используется `ES2022`. Для управления синтаксисом ECMA используйте конфигурационный файл [Browserslist](https://github.com/browserslist/browserslist). Более подробную информацию можно найти в руководстве [configuring browser compatibility](build.md#configuring-browser-compatibility).

## Ссылки

-   [TypeScript configuration](https://angular.io/guide/typescript-configuration)
