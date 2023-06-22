# Создание библиотек

На этой странице представлен концептуальный обзор того, как создавать и публиковать новые библиотеки для расширения функциональности Angular.

Если вы обнаружили, что вам нужно решить одну и ту же проблему в нескольких приложениях\(или вы хотите поделиться своим решением с другими разработчиками\), у вас есть кандидат на создание библиотеки. Простым примером может быть кнопка, отправляющая пользователей на сайт вашей компании, которая будет включена во все приложения, создаваемые вашей компанией.

## Начало работы

Используйте Angular CLI для создания нового скелета библиотеки в новом рабочем пространстве с помощью следующих команд.

<code-example format="shell" language="shell">

ng new my-workspace --no-create-application cd my-workspace
ng generate library my-lib

</code-example>

<div class="callout is-important">

<header>Naming your library</header>

Вы должны быть очень внимательны при выборе имени вашей библиотеки, если вы хотите опубликовать ее позже в публичном реестре пакетов, таком как npm. Смотрите [Публикация вашей библиотеки] (guide/creating-libraries#publishing-your-library).

Избегайте использования имен с префиксом `ng-`, например `ng-library`. Префикс `ng-` - это зарезервированное ключевое слово, используемое в фреймворке Angular и его библиотеках.

Префикс `ngx-` предпочтительнее в качестве соглашения, используемого для обозначения того, что библиотека подходит для использования с Angular.

Он также является отличным указанием для потребителей реестра для различения библиотек различных фреймворков JavaScript.

</div>

Команда `ng generate` создает папку `projects/my-lib` в вашем рабочем пространстве, которая содержит компонент и сервис внутри NgModule.

<div class="alert is-helpful">

Подробнее о том, как структурируется библиотечный проект, читайте в разделе [Файлы библиотечных проектов](guide/file-structure#library-project-files) руководства [Структура файлов проекта](guide/file-structure).

Используйте модель monorepo, чтобы использовать одно и то же рабочее пространство для нескольких проектов. См. раздел [Настройка рабочего пространства для нескольких проектов](guide/file-structure#multiple-projects).

</div>

Когда вы создаете новую библиотеку, файл конфигурации рабочего пространства, `angular.json`, обновляется проектом типа `library`.

<code-example format="json">

"projects": { &hellip;
"my-lib": {

"root": "projects/my-lib",

"sourceRoot": "projects/my-lib/src",

"projectType": "library",

"prefix": "lib",

"architect": {

"build": {

"builder": "&commat;angular-devkit/build-angular:ng-packagr",

&hellip;

</code-example>

Сборка, тестирование и линтинг проекта с помощью команд CLI:

<code-example format="shell" language="shell">

ng build my-lib --configuration development ng test my-lib
ng lint my-lib

</code-example>

Обратите внимание, что настроенный сборщик для проекта отличается от сборщика по умолчанию для проектов приложений. Этот конструктор, помимо прочего, гарантирует, что библиотека всегда собирается с помощью [AOT-компилятора](guide/aot-compiler).

Чтобы сделать код библиотеки многократно используемым, необходимо определить для него публичный API. Этот "пользовательский уровень" определяет, что доступно потребителям вашей библиотеки.

Пользователь вашей библиотеки должен иметь доступ к публичной функциональности\(такой как NgModules, провайдеры услуг и общие полезные функции\) через единый путь импорта.

Публичный API для вашей библиотеки хранится в файле `public-api.ts` в папке вашей библиотеки. Все, что экспортируется из этого файла, становится общедоступным, когда ваша библиотека импортируется в приложение.

Используйте NgModule для демонстрации сервисов и компонентов.

Ваша библиотека должна поставлять документацию\(обычно файл README\) для установки и обслуживания.

## Рефакторинг частей приложения в библиотеку

Чтобы сделать ваше решение многоразовым, вам нужно настроить его так, чтобы оно не зависело от кода, специфичного для приложения. Вот некоторые моменты, которые следует учитывать при переносе функциональности приложения в библиотеку.

-   Такие объявления, как компоненты и трубы, должны быть разработаны как без состояния, то есть они не зависят от внешних переменных и не изменяют их.
    Если вы полагаетесь на состояние, вам необходимо оценить каждый случай и решить, является ли это состоянием приложения или состоянием, которым будет управлять библиотека.

-   Любые наблюдаемые переменные, на которые компоненты подписываются внутри, должны быть очищены и утилизированы в течение жизненного цикла этих компонентов.

-   Компоненты должны раскрывать свое взаимодействие через входы для предоставления контекста и выходы для передачи событий другим компонентам.

-   Проверьте все внутренние зависимости.

    -   Для пользовательских классов или интерфейсов, используемых в компонентах или сервисе, проверьте, не зависят ли они от дополнительных классов или интерфейсов, которые также должны быть перенесены.

    -   Аналогично, если код вашей библиотеки зависит от сервиса, этот сервис необходимо перенести.

    -   Если код вашей библиотеки или ее шаблоны зависят от других библиотек\(таких как Angular Material, например\), вы должны настроить вашу библиотеку с учетом этих зависимостей.

-   Подумайте о том, как вы предоставляете услуги клиентским приложениям.

    -   Сервисы должны объявлять своих собственных провайдеров, а не объявлять провайдеров в NgModule или компоненте.

        Объявление провайдера делает этот сервис _три-шатаемым_.

        Такая практика позволяет компилятору не включать сервис в пакет, если он никогда не будет внедрен в приложение, импортирующее библиотеку.

        Подробнее об этом см. в [Tree-shakable providers](guide/architecture-services#providing-services).

    -   Если вы регистрируете глобальных провайдеров услуг или совместно используете провайдеров в нескольких NgModules, используйте шаблоны проектирования [`forRoot()` и `forChild()`](guide/singleton-services), предоставляемые [RouterModule](api/router/RouterModule).

    -   Если ваша библиотека предоставляет дополнительные услуги, которые могут использоваться не всеми клиентскими приложениями, поддерживайте надлежащее встряхивание дерева для этого случая, используя шаблон проектирования [lightweight token](guide/lightweight-injection-tokens)

<a id="integrating-with-the-cli"></a>

## Интеграция с CLI с помощью схем генерации кода

Библиотека обычно включает _повторно используемый код_, определяющий компоненты, сервисы и другие артефакты Angular \(трубы, директивы\), которые вы импортируете в проект. Библиотека упаковывается в пакет npm для публикации и совместного использования.

Этот пакет также может включать [схемы](guide/glossary#schematic), которые содержат инструкции по генерации или преобразованию кода непосредственно в вашем проекте, подобно тому, как CLI создает общий новый компонент с помощью `ng generate component`.

Схема, которая упакована с библиотекой, может, например, предоставить Angular CLI информацию, необходимую для создания компонента, который конфигурирует и использует определенную функцию или набор функций, определенных в этой библиотеке.

Примером может служить [Angular Material's navigation schematic](https://material.angular.io/guide/schematics#navigation-schematic), который конфигурирует [BreakpointObserver](https://material.angular.io/cdk/layout/overview#breakpointobserver) CDK и использует его с компонентами Material's [MatSideNav](https://material.angular.io/components/sidenav/overview) и [MatToolbar](https://material.angular.io/components/toolbar/overview).

Создайте и включите следующие виды схем:

-   Включите схему установки, чтобы `ng add` мог добавить вашу библиотеку в проект.

-   Включите схему генерации в вашу библиотеку, чтобы `ng generate` мог поместить ваши определенные артефакты\(компоненты, сервисы, тесты\) в проект

-   Включите схему обновления, чтобы `ng update` мог обновлять зависимости вашей библиотеки и обеспечивать миграции для изменений в новых релизах.

То, что вы включите в свою библиотеку, зависит от вашей задачи. Например, вы можете определить схему для создания выпадающего списка, который предварительно заполняется консервированными данными, чтобы показать, как добавить его в приложение.
Если вам нужен выпадающий список, который каждый раз будет содержать разные передаваемые значения, ваша библиотека может определить схему для его создания с заданной конфигурацией.

Разработчики могли бы затем использовать `ng generate` для конфигурирования экземпляра для своего приложения.

Предположим, вы хотите прочитать файл конфигурации и затем сгенерировать форму на основе этой конфигурации. Если эта форма нуждается в дополнительной настройке разработчиком, использующим вашу библиотеку, она может лучше всего работать в виде схемы.

Однако если форма всегда будет одной и той же и не будет нуждаться в особой настройке разработчиками, то можно создать динамический компонент, который принимает конфигурацию и генерирует форму.

В общем, чем сложнее настройка, тем полезнее схематический подход.

Для получения дополнительной информации смотрите [Schematics Overview](guide/schematics) и [Schematics for Libraries](guide/schematics-for-libraries).

## Публикация вашей библиотеки

Используйте Angular CLI и менеджер пакетов npm для создания и публикации вашей библиотеки в виде пакета npm.

Angular CLI использует инструмент под названием [ng-packagr](https://github.com/ng-packagr/ng-packagr/blob/master/README.md) для создания пакетов из вашего скомпилированного кода, которые могут быть опубликованы в npm. Смотрите [Создание библиотек с помощью Ivy](guide/creating-libraries#ivy-libraries) для получения информации о форматах распространения, поддерживаемых `ng-packagr`, и руководства о том, как

выбрать правильный формат для вашей библиотеки.

Вы всегда должны собирать библиотеки для распространения, используя конфигурацию `production`. Это гарантирует, что сгенерированный вывод использует соответствующие оптимизации и правильный формат пакета для npm.

<code-example format="shell" language="shell">

ng build my-lib cd dist/my-lib
npm опубликовать

</code-example>

<a id="lib-assets"></a>

## Управление активами в библиотеке

В вашу библиотеку Angular дистрибутив может включать дополнительные активы, такие как тематические файлы, Sass-миксины или документацию\(например, журнал изменений\). Для получения дополнительной информации [копируйте активы в вашу библиотеку как часть сборки](https://github.com/ng-packagr/ng-packagr/blob/master/docs/copy-assets.md) и [встраивайте активы в стили компонентов](https://github.com/ng-packagr/ng-packagr/blob/master/docs/embed-assets-css.md).

<div class="alert is-important">

При включении дополнительных активов, таких как миксины Sass или предварительно скомпилированные CSS. Вам нужно добавить их вручную в условный ["exports"](guide/angular-package-format/#exports) в `package.json` основной точки входа.

`ng-packagr` объединит написанные вручную `"exports"` с автоматически сгенерированными, позволяя авторам библиотек настраивать дополнительные подпути экспорта или пользовательские условия.

<code-example language="json">

"exports": { ".": {
"sass": "./\_index.scss",

},

"./theming": {

"sass": "./\_theming.scss".

},

"./prebuilt-themes/indigo-pink.css": {

"style": "./prebuilt-themes/indigo-pink.css".

}

}

</code-example>

Вышеприведенное является выдержкой из [@angular/material](https://unpkg.com/browse/@angular/material/package.json) дистрибутива.

</div>

## Одноранговые зависимости

Библиотеки Angular должны перечислять любые `@angular/*` зависимости, от которых зависит библиотека, как одноранговые зависимости. Это гарантирует, что когда модули запрашивают Angular, все они получают один и тот же модуль.

Если библиотека перечислит `@angular/core` в `dependencies` вместо `peerDependencies`, она может получить вместо него другой модуль Angular, что приведет к поломке вашего приложения.

## Использование собственной библиотеки в приложениях

Вам не обязательно публиковать свою библиотеку в менеджере пакетов npm, чтобы использовать ее в том же рабочем пространстве, но вы должны сначала собрать ее.

Чтобы использовать собственную библиотеку в приложении:

-   Соберите библиотеку.

    Вы не можете использовать библиотеку до того, как она собрана.

      <code-example format="shell" language="shell">

    ng build my-lib

    </code-example>.

-   В своих приложениях импортируйте из библиотеки по имени:

      <code-example format="typescript" language="typescript">

    import { myExport } from 'my-lib';

      </code-example>

### Сборка и восстановление вашей библиотеки

Шаг сборки важен, если вы не опубликовали свою библиотеку как пакет npm и затем не установили пакет обратно в свое приложение из npm. Например, если вы клонируете свой git-репозиторий и запустите `npm install`, ваш редактор покажет, что импорт `my-lib` отсутствует, если вы еще не собрали библиотеку.

<div class="alert is-helpful">

Когда вы импортируете что-то из библиотеки в приложение Angular, Angular ищет соответствие между именем библиотеки и местом на диске. Когда вы устанавливаете пакет библиотеки, сопоставление находится в папке `node_modules`.
Когда вы создаете свою собственную библиотеку, она должна найти отображение в ваших путях `tsconfig`.

Генерация библиотеки с помощью Angular CLI автоматически добавляет ее путь в файл `tsconfig`. Angular CLI использует пути `tsconfig`, чтобы указать системе сборки, где найти библиотеку.

Для получения дополнительной информации смотрите [Path mapping overview](https://www.typescriptlang.org/docs/handbook/module-resolution.html#path-mapping).

</div>

Если вы обнаружили, что изменения в вашей библиотеке не отражаются в вашем приложении, вероятно, ваше приложение использует старую сборку библиотеки.

Вы можете пересобирать библиотеку каждый раз, когда вносите в нее изменения, но этот дополнительный шаг требует времени. Функциональность _Incremental Builds_ улучшает опыт разработки библиотеки.

Каждый раз, когда файл изменяется, выполняется частичная сборка, в которую попадают измененные файлы.

Инкрементные сборки могут быть запущены как фоновый процесс в вашей среде разработки. Чтобы воспользоваться этой функцией, добавьте флаг `--watch` к команде сборки:

<code-example format="shell" language="shell">

ng build my-lib --watch

</code-example>

<div class="alert is-important">

The CLI `build` command uses a different builder and invokes a different build tool for libraries than it does for applications.

-   The build system for applications, `@angular-devkit/build-angular`, is based on `webpack`, and is included in all new Angular CLI projects
-   The build system for libraries is based on `ng-packagr`.
    It is only added to your dependencies when you add a library using `ng generate library my-lib`.

The two build systems support different things, and even where they support the same things, they do those things differently. This means that the TypeScript source can result in different JavaScript code in a built library than it would in a built application.

For this reason, an application that depends on a library should only use TypeScript path mappings that point to the _built library_. TypeScript path mappings should _not_ point to the library source `.ts` files.

</div>

<a id="ivy-libraries"></a>

## Publishing libraries

There are two distribution formats to use when publishing a library:

| Distribution formats | Details | | :-------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Partial-Ivy \(recommended\) | Contains portable code that can be consumed by Ivy applications built with any version of Angular from v12 onwards. |
| Full-Ivy | Contains private Angular Ivy instructions, which are not guaranteed to work across different versions of Angular. This format requires that the library and application are built with the _exact_ same version of Angular. This format is useful for environments where all library and application code is built directly from source. |

For publishing to npm use the partial-Ivy format as it is stable between patch versions of Angular.

Avoid compiling libraries with full-Ivy code if you are publishing to npm because the generated Ivy instructions are not part of Angular's public API, and so might change between patch versions.

## Ensuring library version compatibility

The Angular version used to build an application should always be the same or greater than the Angular versions used to build any of its dependent libraries. For example, if you had a library using Angular version 13, the application that depends on that library should use Angular version 13 or later.
Angular does not support using an earlier version for the application.

If you intend to publish your library to npm, compile with partial-Ivy code by setting `"compilationMode": "partial"` in `tsconfig.prod.json`. This partial format is stable between different versions of Angular, so is safe to publish to npm.
Code with this format is processed during the application build using the same version of the Angular compiler, ensuring that the application and all of its libraries use a single version of Angular.

Avoid compiling libraries with full-Ivy code if you are publishing to npm because the generated Ivy instructions are not part of Angular's public API, and so might change between patch versions.

If you've never published a package in npm before, you must create a user account. Read more in [Publishing npm Packages](https://docs.npmjs.com/getting-started/publishing-npm-packages).

## Consuming partial-Ivy code outside the Angular CLI

An application installs many Angular libraries from npm into its `node_modules` directory. However, the code in these libraries cannot be bundled directly along with the built application as it is not fully compiled.
To finish compilation, use the Angular linker.

For applications that don't use the Angular CLI, the linker is available as a [Babel](https://babeljs.io) plugin. The plugin is to be imported from `@angular/compiler-cli/linker/babel`.

The Angular linker Babel plugin supports build caching, meaning that libraries only need to be processed by the linker a single time, regardless of other npm operations.

Example of integrating the plugin into a custom [Webpack](https://webpack.js.org) build by registering the linker as a [Babel](https://babeljs.io) plugin using [babel-loader](https://webpack.js.org/loaders/babel-loader/#options).

<code-example header="webpack.config.mjs" path="angular-linker-plugin/webpack.config.mjs" region="webpack-config"></code-example>

<div class="alert is-helpful">

The Angular CLI integrates the linker plugin automatically, so if consumers of your library are using the CLI, they can install Ivy-native libraries from npm without any additional configuration.

</div>

<!-- links -->

<!-- external links -->

<!-- end links -->

:date: 28.02.2022
