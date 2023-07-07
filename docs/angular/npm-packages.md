# Зависимости npm рабочего пространства

Angular Framework, Angular CLI и компоненты, используемые в приложениях Angular, упакованы как [npm-пакеты](https://docs.npmjs.com/getting-started/what-is-npm 'Что такое npm?') и распространяются с помощью [npm-регистра](https://docs.npmjs.com).

Вы можете загрузить и установить эти пакеты npm с помощью клиента [npm CLI](https://docs.npmjs.com/cli/install), который устанавливается вместе с приложением [Node.js®](https://nodejs.org 'Nodejs.org') и запускается как приложение. По умолчанию Angular CLI использует клиент npm.

В качестве альтернативы вы можете использовать [yarn client](https://yarnpkg.com) для загрузки и установки пакетов npm.

<div class="alert is-helpful">

Информацию о необходимых версиях и установке `Node.js` и `npm` смотрите в [Local Environment Setup](guide/setup-local 'Setting up for Local Development').

Если на вашей машине уже запущены проекты, использующие другие версии Node.js и npm, воспользуйтесь [nvm](https://github.com/creationix/nvm) для управления несколькими версиями Node.js и npm.

</div>

## `package.json`.

И `npm`, и `yarn` устанавливают пакеты, которые определены в файле [`package.json`](https://docs.npmjs.com/files/package.json).

Команда CLI `ng new` создает файл `package.json` при создании нового рабочего пространства. Этот `package.json` используется всеми проектами в рабочем пространстве, включая начальный проект приложения, который создается CLI при создании рабочего пространства.

Изначально этот `package.json` включает _стартовый набор пакетов_, некоторые из которых требуются Angular, а другие поддерживают общие сценарии приложений. Вы добавляете пакеты в `package.json` по мере развития вашего приложения.

Вы можете даже удалить некоторые из них.

В `package.json` организованы две группы пакетов:

| Пакеты | Подробности | |:--- |:--- |:--- |.

| [Зависимости](guide/npm-packages#dependencies) | Необходимые для _запуска_ приложения. |

| [DevDependencies](guide/npm-packages#dev-dependencies) | Необходимы только для _разработки_ и _сборки_ приложений. |

<div class="alert is-helpful">

**LIBRARY DEVELOPERS**: <br /> By default, the CLI command [`ng generate library`](cli/generate) creates a `package.json` for the new library.
That `package.json` is used when publishing the library to npm.

For more information, see the CLI wiki page [Library Support](guide/creating-libraries).

</div>

<a id="dependencies"></a>

## Зависимости

Пакеты, перечисленные в разделе `dependencies` файла `package.json`, необходимы для _запуска_ приложений.

Раздел `dependencies` в `package.json` содержит:

| Пакеты | Подробности | |:--- |:--- |:--- |

| [Angular packages](#angular-packages) | Ядро Angular и дополнительные модули; их имена пакетов начинаются с `@angular` |

| [Support packages](#support-packages) | Сторонние библиотеки, которые должны присутствовать для работы приложений Angular |

| [Polyfill packages](#polyfills) | Полифиллы заполняют пробелы в реализации JavaScript в браузере |.

Чтобы добавить новую зависимость, используйте команду [`ng add`](cli/add).

<a id="angular-packages"></a>

### Пакеты Angular

Следующие пакеты Angular включены в качестве зависимостей в файл по умолчанию `package.json` для нового рабочего пространства Angular. Полный список пакетов Angular см. в [API reference](api?type=package).

| Package name | Details | |:--- |:--- |
| [`@angular/animations`](api/animations) | Angular's animations library makes it easy to define and apply animation effects such as page and list transitions. For more information, see the [Animations guide](guide/animations). |
| [`@angular/common`](api/common) | The commonly-needed services, pipes, and directives provided by the Angular team. The [`HttpClientModule`](api/common/http/HttpClientModule) is also here, in the [`@angular/common/http`](api/common/http) subfolder. For more information, see the [HttpClient guide](guide/understanding-communicating-with-http). |
| `@angular/compiler` | Angular's template compiler. It understands templates and can convert them to code that makes the application run and render. Typically you don't interact with the compiler directly; rather, you use it indirectly using `platform-browser-dynamic` when JIT compiling in the browser. For more information, see the [Ahead-of-time Compilation guide](guide/aot-compiler). |
| [`@angular/core`](api/core) | Critical runtime parts of the framework that are needed by every application. Includes all metadata decorators, `Component`, `Directive`, dependency injection, and the component lifecycle hooks. |
| [`@angular/forms`](api/forms) | Support for both [template-driven](guide/forms) and [reactive forms](guide/reactive-forms). For information about choosing the best forms approach for your app, see [Introduction to forms](guide/forms-overview). |
| [`@angular/platform-browser`](api/platform-browser) | Everything DOM and browser related, especially the pieces that help render into the DOM. This package also includes the `bootstrapModuleFactory()` method for bootstrapping applications for production builds that pre-compile with [AOT](guide/aot-compiler). |
| [`@angular/platform-browser-dynamic`](api/platform-browser-dynamic) | Includes [providers](api/core/Provider) and methods to compile and run the application on the client using the [JIT compiler](guide/aot-compiler). |
| [`@angular/router`](api/router) | The router module navigates among your application pages when the browser URL changes. For more information, see [Routing and Navigation](guide/router). |

<a id="support-packages"></a>

### Пакеты поддержки

Следующие пакеты поддержки включены в качестве зависимостей в файл по умолчанию `package.json` для нового рабочего пространства Angular.

| Имя пакета | Подробности | |:--- |:--- |:--- |

| [`rxjs`](https://github.com/ReactiveX/rxjs) | Многие API Angular возвращают [_observables_](guide/glossary#observable). RxJS является реализацией предложенной спецификации [Observables](https://github.com/tc39/proposal-observable), которая в настоящее время находится на рассмотрении комитета [TC39](https://www.ecma-international.org/memento/tc39.htm), определяющего стандарты для языка JavaScript. |

| [`zone.js`](https://github.com/angular/zone.js) | Angular полагается на zone.js для запуска процессов обнаружения изменений Angular, когда собственные операции JavaScript вызывают события. Zone.js является реализацией [спецификации](https://gist.github.com/mhevery/63fdcdf7c65886051d55), которая в настоящее время находится на рассмотрении комитета [TC39](https://www.ecma-international.org/memento/tc39.htm), определяющего стандарты для языка JavaScript. |

<a id="polyfills"></a>

### Пакеты полифиллов

Во многих браузерах отсутствует встроенная поддержка некоторых функций в последних стандартах HTML, которые необходимы Angular. [_Полифиллы_](<https://en.wikipedia.org/wiki/Polyfill_(программирование)>) могут эмулировать недостающие возможности.

В руководстве [Browser Support](guide/browser-support) объясняется, каким браузерам нужны полифиллы и как их можно добавить.

<a id="dev-dependencies"></a>

## DevDependencies

Пакеты, перечисленные в секции `devDependencies` файла `package.json`, помогают вам разрабатывать приложение на вашей локальной машине. Вы не развертываете их вместе с производственным приложением.

Чтобы добавить новую `devDependency`, используйте одну из следующих команд:

<code-example format="shell" language="shell">

npm install --save-dev &lt;package-name&gt;

</code-example>

<code-example format="shell" language="shell">

yarn add --dev &lt;package-name&gt;

</code-example>

Следующие `devDependencies` предоставляются в файле по умолчанию `package.json` для нового рабочего пространства Angular.

| Package name | Details | |:--- |:--- |
| [`@angular-devkit/build-angular`](https://github.com/angular/angular-cli) | The Angular build tools. |
| [`@angular/cli`](https://github.com/angular/angular-cli) | The Angular CLI tools. |
| `@angular/compiler-cli` | The Angular compiler, which is invoked by the Angular CLI's `ng build` and `ng serve` commands. |
| `@types/... ` | TypeScript definition files for 3rd party libraries such as Jasmine and Node.js. |
| `jasmine/... ` | Packages to support the [Jasmine](https://jasmine.github.io) test library. |
| `karma/... ` | Packages to support the [karma](https://www.npmjs.com/package/karma) test runner. |
| [`typescript`](https://www.npmjs.com/package/typescript) | The TypeScript language server, including the _tsc_ TypeScript compiler. |

## Связанная информация

Информацию о том, как Angular CLI работает с пакетами, можно найти в следующих руководствах:

| Темы | Подробности | |:--- |:--- |:--- |

| [Сборка и обслуживание](guide/build) | Как пакеты собираются вместе для создания сборки разработки |

| [Развертывание](guide/deployment) | Как пакеты объединяются для создания производственной сборки |

<!-- links -->

<!-- external links -->

<!-- end links -->

@ просмотрено 2022-02-28
