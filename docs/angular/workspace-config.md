# Конфигурация рабочего пространства Angular

Файл `angular.json` на корневом уровне рабочего пространства Angular [workspace](glossary.md#workspace) предоставляет настройки по умолчанию для всего рабочего пространства и конкретного проекта. Они используются для инструментов сборки и разработки, предоставляемых Angular CLI. Значения путей, указанные в конфигурации, относятся к корневому каталогу рабочего пространства.

## Общая структура JSON

На верхнем уровне `angular.json` несколько свойств конфигурируют рабочее пространство, а раздел `projects` содержит остальные параметры конфигурации для каждого проекта. Вы можете переопределить параметры по умолчанию Angular CLI, установленные на уровне рабочего пространства, через параметры по умолчанию, установленные на уровне проекта.

Вы также можете отменить значения по умолчанию, установленные на уровне проекта, используя командную строку.

Следующие свойства, расположенные на верхнем уровне файла, настраивают рабочее пространство.

| Свойства | Подробности | |:--- |:--- |:--- |
| `version` | Версия конфигурационного файла. |

| `newProjectRoot` | Путь, где создаются новые проекты. Абсолютный или относительный к каталогу рабочей области. |

| | `cli` | Набор опций, настраивающих [Angular CLI](https://angular.io/cli). См. раздел [Angular CLI configuration options](#cli-configuration-options). |

| `schematics` | Набор [schematics](glossary.md#schematic), которые настраивают параметры по умолчанию подкоманды `ng generate` для данного рабочего пространства. См. раздел [Generation schematics](#schematics). |

| `projects` | Содержит подраздел для каждой библиотеки или приложения в рабочем пространстве, с опциями конфигурации для каждого проекта. |

Первоначальное приложение, которое вы создаете с помощью команды `ng new app_name`, находится в списке "projects":

<code-example language="json">

"projects": { "app_name": {
&hellip;

}

&hellip;

}

</code-example>

Когда вы создаете проект библиотеки с помощью `ng generate library`, проект библиотеки также добавляется в раздел `projects`.

<div class="alert is-helpful">

**NOTE**: <br /> The `projects` section of the configuration file does not correspond exactly to the workspace file structure.

-   The initial application created by `ng new` is at the top level of the workspace file structure

-   Other applications and libraries go into a `projects` directory in the workspace

For more information, see [Workspace and project file structure](file-structure.md).

</div>

<a id="cli-configuration-options"></a>

## Параметры конфигурации Angular CLI

Следующие свойства конфигурации представляют собой набор опций, которые настраивают Angular CLI.

| Свойство | Детали | Тип значения | | |:--- |:--- |:--- |:--- |:---.
| `analytics` | Поделиться анонимными [данными об использовании](https://angular.io/cli/analytics) с командой Angular Team. | `boolean` &verbar; `ci` | `cache`.

| `cache` | Управление [постоянным дисковым кэшем](https://angular.io/cli/cache), используемым [Angular CLI Builders](cli-builder.md). | [Опции кэша](#cache-options)|.

| `schematicCollections`| Список коллекций схем по умолчанию для использования. | `string[]` |

| `packageManager` | Предпочтительный инструмент менеджера пакетов для использования. | `npm` &verbar; `cnpm` &verbar; `pnpm` &verbar;`yarn` |

| `warnings` | Управление предупреждениями консоли, специфичными для Angular CLI. | [Warnings options](#warnings-options) | [Warnings options](#warnings-options).

### Опции кэша

| Свойство | Подробности | Тип значения | Значение по умолчанию | | |:--- | :--- |:--- |:--- |:--- |:---.
| `enabled` | Настройка того, включено ли кэширование дисков. | `boolean` | `true` |.

| `environment` | Настройте, в каком окружении включено дисковое кэширование. | `local` &verbar; `ci` &verbar; `all` | `local` | `local`.

| `path` | Каталог, используемый для хранения результатов кэширования. | `string` | `.angular/cache` |.

### Параметры предупреждений

| Свойство | Детали | Тип значения | Значение по умолчанию | |:--- |:--- |:--- |:--- |:--- |:--- |:---.

| `versionMismatch` | Показывать предупреждение, когда глобальная версия Angular CLI новее локальной. | `boolean` | `true` |.

## Параметры конфигурации проекта

Следующие свойства конфигурации верхнего уровня доступны для каждого проекта в разделе `projects:<имя_проекта>`.

<code-example language="json">

"my-app": { "root": "",
"sourceRoot": "src",

"projectType": "application",

"prefix": "app",

"schematics": {},

"архитектор": {}

}

</code-example>

| Свойство | Детали | |:--- |:--- |:--- |
| `root` | Корневой каталог для файлов этого проекта, относительно каталога рабочего пространства. Пустой для начального приложения, которое находится на верхнем уровне рабочего пространства. |

| | `sourceRoot` | Корневой каталог для исходных файлов проекта. |

| | `projectType` | Одно из "приложение" или "библиотека" Приложение может запускаться самостоятельно в браузере, а библиотека - нет. |

| | `prefix` | Строка, которую Angular добавляет к создаваемым селекторам. Может быть настроена для идентификации приложения или области возможностей. |

| | `schematics` | Набор схем, которые настраивают опции по умолчанию подкоманды `ng generate` для этого проекта. См. раздел [Generation schematics](#schematics)|.

| `architect` | Конфигурация по умолчанию для целей конструктора Architect для этого проекта. |

<a id="schematics"></a>

## Схемы генерации

Angular generation [schematics](glossary.md#schematic) - это инструкции по модификации проекта путем добавления файлов или изменения существующих файлов. Отдельные схемы для стандартных подкоманд Angular CLI `ng generate` собраны в пакете `@schematics/angular`.

Укажите имя схемы для подкоманды в формате `schematic-package:schematic-name`;

например, схема для генерации компонента - `@schematics/angular:component`.

JSON-схемы для схем по умолчанию, используемых Angular CLI для создания проектов и частей проектов, собраны в пакете [`@schematics/angular`](https://github.com/angular/angular-cli/blob/main/packages/schematics/angular/application/schema.json). Схема описывает опции, доступные Angular CLI для каждой из подкоманд `ng generate`, как показано в выводе `--help`.

Поля, указанные в схеме, соответствуют допустимым значениям аргументов и значениям по умолчанию для опций подкоманд Angular CLI. Вы можете обновить файл схемы рабочего пространства, чтобы установить другое значение по умолчанию для опции подкоманды.

<a id="architect"></a>

## Параметры конфигурации инструмента проекта

Architect - это инструмент, который используется в Angular CLI для выполнения сложных задач, таких как компиляция и запуск тестов. Architect - это оболочка, которая запускает указанный [builder](glossary.md#builder) для выполнения заданной задачи в соответствии с конфигурацией [target](glossary.md#target).

Вы можете определить и настроить новые конструкторы и цели для расширения Angular CLI.

Смотрите [Angular CLI Builders](cli-builder.md).

<a id="default-build-targets"></a>

### Строители и цели архитекторов по умолчанию

Angular определяет конструкторы по умолчанию для использования с определенными командами или с общей командой `ng run`. JSON-схемы, определяющие опции и значения по умолчанию для каждого из этих дефолтных конструкторов, собраны в пакете [`@angular-devkit/build-angular`](https://github.com/angular/angular-cli/blob/main/packages/angular_devkit/build_angular/builders.json).

Схемы определяют опции для следующих конструкторов.

<!-- vale Angular.Google_WordListWarnings = NO -->

-   [app-shell](https://github.com/angular/angular-cli/blob/main/packages/angular_devkit/build_angular/src/builders/app-shell/schema.json)
-   [browser](https://github.com/angular/angular-cli/blob/main/packages/angular_devkit/build_angular/src/builders/browser/schema.json)

-   [dev-server](https://github.com/angular/angular-cli/blob/main/packages/angular_devkit/build_angular/src/builders/dev-server/schema.json)

-   [extract-i18n](https://github.com/angular/angular-cli/blob/main/packages/angular_devkit/build_angular/src/builders/extract-i18n/schema.json)

-   [karma](https://github.com/angular/angular-cli/blob/main/packages/angular_devkit/build_angular/src/builders/karma/schema.json)

-   [сервер](https://github.com/angular/angular-cli/blob/main/packages/angular_devkit/build_angular/src/builders/server/schema.json)

<!-- vale Angular.Google_WordListWarnings = YES -->

### Настройка целей конструктора

Раздел `architect` в файле `angular.json` содержит набор целей Architect. Многие из целей соответствуют командам Angular CLI, которые их запускают.

Некоторые дополнительные предопределенные цели могут быть запущены с помощью команды `ng run`, и вы можете определить свои собственные цели.

Каждый объект цели определяет `builder` для этой цели, который является пакетом npm для инструмента, запускаемого Architect. Каждая цель также имеет раздел `options`, в котором настраиваются параметры по умолчанию для цели, и раздел `configurations`, в котором называются и указываются альтернативные конфигурации для цели.

Смотрите пример в [Build target](#build-target) ниже.

<code-example language="json">

"architect": { "build": {},
"serve": {},

"e2e" : {},

"test": {},

"lint": {},

"extract-i18n": {},

"server": {},

"app-shell": {}

}

</code-example>

| Sections | Details | |:--- |:--- |
| `architect/build` | Configures defaults for options of the `ng build` command. See the [Build target](#build-target) section for more information. |
| `architect/serve` | Overrides build defaults and supplies extra serve defaults for the `ng serve` command. Besides the options available for the `ng build` command, it adds options related to serving the application. |
| `architect/e2e` | Overrides build-option defaults for building end-to-end testing applications using the `ng e2e` command. |
| `architect/test` | Overrides build-option defaults for test builds and supplies extra test-running defaults for the `ng test` command. |
| `architect/lint` | Configures defaults for options of the `ng lint` command, which performs code analysis on project source files. |
| `architect/extract-i18n` | Configures defaults for options of the `ng extract-i18n` command, which extracts marked message strings from source code and outputs translation files. |
| `architect/server` | Configures defaults for creating a Universal application with server-side rendering, using the `ng run <project>:server` command. |
| `architect/app-shell` | Configures defaults for creating an application shell for a progressive web application \(PWA\), using the `ng run <project>:app-shell` command. |

В целом, параметры, для которых можно настроить значения по умолчанию, соответствуют параметрам команд, перечисленным в [Angular CLI reference page](https://angular.io/cli) для каждой команды.

<div class="alert is-helpful">

**NOTE**: <br /> All options in the configuration file must use [camelCase](glossary.md#case-conventions), rather than dash-case.

</div>

<a id="build-target"></a>

## Цель сборки

Раздел `architect/build` задает значения по умолчанию для опций команды `ng build`. Он имеет следующие свойства верхнего уровня.

| PROPERTY | Details | |:--- |:--- |
| `builder` | The npm package for the build tool used to create this target. The default builder for an application \(`ng build myApp`\) is `@angular-devkit/build-angular:browser`, which uses the [webpack](https://webpack.js.org) package bundler. <div class="alert is-helpful"> **NOTE**: A different builder is used for building a library \(`ng build myLib`\). </div> |
| `options` | This section contains default build target options, used when no named alternative configuration is specified. See the [Default build targets](#default-build-targets) section. |
| `configurations`| This section defines and names alternative configurations for different intended destinations. It contains a section for each named configuration, which sets the default options for that intended environment. See the [Alternate build configurations](#build-configs) section. |

<a id="build-configs"></a>

### Альтернативные конфигурации сборки

Angular CLI поставляется с двумя конфигурациями сборки: `production` и `development`. По умолчанию команда `ng build` использует конфигурацию `production`, которая применяет несколько оптимизаций сборки, включая:

-   Пакетирование файлов

-   Минимизация лишних пробельных символов

-   Удаление комментариев и мертвого кода

-   Переписывание кода для использования коротких, искаженных имен, также известное как минификация.

Вы можете определить и назвать дополнительные альтернативные конфигурации \(такие как `stage`, для instance\), соответствующие вашему процессу разработки. Примерами различных конфигураций сборки являются `stable`, `archive` и `next`, используемые самим Angular.io, а также отдельные конфигурации, специфичные для локализации, необходимые для создания локализованных версий приложения.

Подробнее см. в [Интернационализация (i18n)][aioguidei18ncommonmerge].

Вы можете выбрать альтернативную конфигурацию, передав ее имя во флаге командной строки `--configuration`.

Вы также можете передать более одного имени конфигурации в виде списка, разделенного запятыми. Например, чтобы применить конфигурации сборки `stage` и `fr`, используйте команду `ng build --configuration stage,fr`.
В этом случае команда анализирует именованные конфигурации слева направо.

Если несколько конфигураций изменяют одну и ту же настройку, то последнее установленное значение является окончательным.

В данном примере, если обе конфигурации `stage` и `fr` задают выходной путь, будет использовано значение в `fr`.

<a id="build-props"></a>

### Дополнительные опции сборки и тестирования

Настраиваемые опции для сборки по умолчанию или целевой сборки в целом соответствуют опциям, доступным для команд [`ng build`](https://angular.io/cli/build), [`ng serve`](https://angular.io/cli/serve) и [`ng test`](https://angular.io/cli/test). Подробнее об этих опциях и их возможных значениях смотрите в [Angular CLI Reference](https://angular.io/cli).

Некоторые дополнительные опции могут быть установлены только через конфигурационный файл, либо путем прямого редактирования, либо с помощью команды [`ng config`](https://angular.io/cli/config).

| Options properties | Details | |:--- |:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `assets` | An object containing paths to static assets to add to the global context of the project. The default paths point to the project's icon file and its `assets` directory. See more in the [Assets configuration](#asset-config) section. |
| `styles` | An array of style files to add to the global context of the project. Angular CLI supports CSS imports and all major CSS preprocessors: [sass/scss](https://sass-lang.com) and [less](https://lesscss.org). See more in the [Styles and scripts configuration](#style-script-config) section. |
| `stylePreprocessorOptions` | An object containing option-value pairs to pass to style preprocessors. See more in the [Styles and scripts configuration](#style-script-config) section. |
| `scripts` | An object containing JavaScript script files to add to the global context of the project. The scripts are loaded exactly as if you had added them in a `<script>` tag inside `index.html`. See more in the [Styles and scripts configuration](#style-script-config) section. |
| `budgets` | Default size-budget type and thresholds for all or parts of your application. You can configure the builder to report a warning or an error when the output reaches or exceeds a threshold size. See [Configure size budgets](build.md#configure-size-budgets). \(Not available in `test` section.\) |
| `fileReplacements` | An object containing files and their compile-time replacements. See more in [Configure target-specific file replacements](build.md#configure-target-specific-file-replacements). |
`index` | Configures the generation of the application's HTML index. See more in [Index configuration](#index-config). \(Only available in `browser` section.\) | |

<a id="complex-config"></a>

## Значения сложной конфигурации

Опции `assets`, `index`, `styles` и `scripts` могут иметь либо простые строковые значения пути, либо объектные значения с определенными полями. Опции `sourceMap` и `optimization` могут быть установлены в простое булево значение с командным флагом. Им также можно придать сложное значение с помощью конфигурационного файла.

В следующих разделах более подробно описано, как эти сложные значения используются в каждом конкретном случае.

<a id="asset-config"></a>

### Конфигурация активов

Каждая конфигурация цели `build` может включать массив `assets`, в котором перечислены файлы или папки, которые вы хотите скопировать как есть при сборке проекта. По умолчанию копируются директория `src/assets/` и `src/favicon.ico`.

<code-example language="json">

"assets": [ "src/assets",
[ "src/favicon.ico"

]

</code-example>

<!-- vale off -->

Чтобы исключить актив, вы можете удалить его из конфигурации активов.

Вы можете дополнительно настроить активы для копирования, указав их как объекты, а не как простые пути относительно корня рабочей области. Объект спецификации актива может иметь следующие поля.

| Поля | Подробности | |:--- |:--- |:--- |

| `glob` | A [node-glob](https://github.com/isaacs/node-glob/blob/master/README.md) using `input` as base directory. |

| `input` | Путь относительно корня рабочей области. |

| | `output` | Путь относительно `outDir`\ (по умолчанию `dist/project-name`\). Из-за проблем с безопасностью, Angular CLI никогда не записывает файлы за пределами пути вывода проекта. |

| | `ignore` | Список глобусов для исключения. |

| | `followSymlinks` | Разрешить шаблонам glob следовать за каталогами симлинков. Это позволяет искать в подкаталогах симлинка. По умолчанию `false`. |

Например, пути активов по умолчанию могут быть представлены более подробно с помощью следующих объектов.

<!-- vale on -->

<code-example language="json">

"assets": [ {
"glob": "\*_/_",

    "input": "src/assets/",

    "output": "/assets/"

},

{

    "glob": "favicon.ico",

    "input": "src/",

    "output": "/"

}

]

</code-example>

Вы можете использовать эту расширенную конфигурацию для копирования активов извне вашего проекта. Например, следующая конфигурация копирует активы из пакета узла:

<code-example language="json">

"assets": [ {
"glob": "\*_/_",

    "input": "./node_modules/some-package/images",

    "output": "/some-package/"

}

]

</code-example>

<!-- vale Angular.Google_Will = NO -->

Содержимое `node_modules/some-package/images/` будет доступно в `dist/some-package/`.

<!-- vale Angular.Google_Will = YES -->

В следующем примере поле `ignore` используется для исключения копирования в сборку определенных файлов из каталога assets:

<code-example language="json">

"assets": [ {
"glob": "\*_/_",

    "input": "src/assets/",

    "ignore": ["**/*.svg"],

    "output": "/assets/"

}

]

</code-example>

<a id="style-script-config"></a>

### Конфигурация стилей и скриптов

Запись массива для опций `styles` и `scripts` может быть простой строкой пути или объектом, указывающим на дополнительный файл точки входа. При сборке ассоциированный билдер загружает этот файл и его зависимости как отдельный пакет.

С помощью объекта конфигурации вы можете задать имя пакета для точки входа, используя поле `bundleName`.

По умолчанию пакет инжектируется, но вы можете установить `inject` в `false`, чтобы исключить инжектирование пакета. Например, следующие значения объектов создают и называют пакет, содержащий стили и скрипты, и исключают его из инъекции:

<code-example language="json">

"styles": [ {
"input": "src/external-module/styles.scss",

    "inject": false,

    "bundleName": "external-module"

}

],

"scripts": [

{

    "input": "src/external-module/main.js",

    "inject": false,

    "bundleName": "external-module"

}

]

</code-example>

Вы можете смешивать простые и сложные ссылки на файлы для стилей и скриптов.

<code-example language="json">

"styles": [ "src/styles.css",
"src/more-styles.css",

{ "input": "src/lazy-style.scss", "ввод": false }

{ "input": "src/pre-rename-style.scss", "bundleName": "renamed-style" }

]

</code-example>

<a id="style-preprocessor"></a>

#### Опции препроцессора стилей

В Sass вы можете использовать функцию `includePaths` как для компонентных, так и для глобальных стилей. Это позволяет добавлять дополнительные базовые пути, которые проверяются при импорте.

Чтобы добавить пути, используйте опцию `stylePreprocessorOptions`:

<code-example language="json">

"stylePreprocessorOptions": { "includePaths": [
"src/style-paths"

]

}

</code-example>

Файлы в этом каталоге, такие как `src/style-paths/_variables.scss`, могут быть импортированы из любой точки вашего проекта без необходимости указания относительного пути:

<code-example language="typescript">

// src/app/app.component.scss // Относительный путь работает
&commat;import '../style-paths/variables';

// Но теперь это тоже работает

&commat;import 'variables';

</code-example>

<div class="alert is-helpful">

**NOTE**: <br /> You also need to add any styles or scripts to the `test` builder if you need them for unit tests.
See also [Using runtime-global libraries inside your application](using-libraries.md#using-runtime-global-libraries-inside-your-app).

</div>

### Конфигурация оптимизации

Опция `optimization` сборщика браузеров может быть как булевым значением, так и объектом для более тонкой настройки. Эта опция включает различные оптимизации вывода сборки, в том числе:

<!-- vale Angular.Angular_Spelling = NO-->

-   Минификация скриптов и стилей
-   Смена деревьев

-   Устранение "мертвого кода

-   Инкрустация критических CSS

-   Инкрустация шрифтов

<!-- vale Angular.Angular_Spelling = YES-->

Several options can be used to fine-tune the optimization of an application.

| Options | Details | Value type | Default value | |:--- |:--- |:--- |:--- |

| `scripts` | Enables optimization of the scripts output. | `boolean` | `true` |

| `styles` | Enables optimization of the styles output. | `boolean` &verbar; [Styles optimization options](#styles-optimization-options) | `true` |

| `fonts` | Enables optimization for fonts. <div class="alert is-helpful"> **NOTE**: <br /> This requires internet access. </div> | `boolean` &verbar; [Fonts optimization options](#fonts-optimization-options) | `true` |

#### Styles optimization options

<!-- vale Angular.Angular_Spelling = NO -->

| Параметры | Подробности | Тип значения | Значение по умолчанию | | |:--- |:--- |:--- |:--- |:--- |:--- |:---.
| `minify` | Минифицировать определения CSS, удаляя лишние пробелы и комментарии, объединяя идентификаторы и сворачивая значения. | `` boolean` |  ``true``.

| `inlineCritical` | Извлечение и инлайнирование критических CSS определений для улучшения [First Contentful Paint](https://web.dev/first-contentful-paint). | `boolean` | `true` | |

#### Опции оптимизации шрифтов

| Options | Details | Value type | Default value | |:--- |:--- |:--- |:--- |
| `inline` | Reduce [render blocking requests](https://web.dev/render-blocking-resources) by inlining external Google Fonts and Adobe Fonts CSS definitions in the application's HTML index file. <div class="alert is-helpful"> **NOTE**: <br /> This requires internet access. </div> | `boolean` | `true` |

<!-- vale Angular.Angular_Spelling = YES -->

Вы можете задать значение, подобное следующему, чтобы применить оптимизацию к одному или другому параметру:

<code-example language="json">

"оптимизация": { "скрипты": true,
"styles": {

    "minify": true,

    "inlineCritical": true

},

"шрифты": true

}

</code-example>

<div class="alert is-helpful">

Для [Universal](glossary.md#universal) вы можете уменьшить код, отображаемый в HTML-странице, установив оптимизацию стилей на `true`.

</div>

### Конфигурация карты источников

Опция `sourceMap` конструктора браузера может быть либо булевым значением, либо объектом для более тонкой настройки конфигурации для управления исходными картами приложения.

| Опции | Детали | Тип значения | Значение по умолчанию | |:--- |:--- |:--- |:--- |:--- |:--- |:---.

| `scripts` | Выводить карты источников для всех скриптов. | `булево` | `истина` | `истина`.

| `styles` | Вывод исходных карт для всех стилей. | | `boolean` | `true` |.

| `vendor` | Разрешить исходные карты пакетов поставщиков. | | `boolean` | `false` | `false`.

| `hidden` | Выводить исходные карты, используемые для инструментов отчетности об ошибках. | `boolean` | `false` | `hidden`.

В примере ниже показано, как переключать одно или несколько значений для настройки вывода карт источников:

<code-example language="json">

"sourceMap": { "scripts": true,
"стили": false,

"hidden": true,

"vendor": true

}

</code-example>

<div class="alert is-helpful">

При использовании скрытых карт источников на карты источников не ссылаются в пакете. Это полезно, если карты источников нужны только для отображения трассировки стека ошибок в инструментах отчетности об ошибках. Скрытые карты источников не отображают ваши карты источников в инструментах разработчика браузера.

</div>

<a id="index-config"></a>

### Конфигурация индекса

Настраивает генерацию HTML-индекса приложения.

Параметр `index` может быть как строкой, так и объектом для более тонкой настройки.

При передаче значения в виде String для сгенерированного файла будет использовано имя файла по указанному пути, который будет создан в корне настроенного пути вывода приложения.

#### Параметры индекса

| Опции | Детали | Тип значения | Значение по умолчанию | | |:--- |:--- |:--- |:--- |:--- |:--- |:---.

| `input` | Путь к файлу, который будет использоваться для генерируемого приложением HTML-индекса. | `string` | | |

| `output` | Путь к выходному файлу HTML-индекса приложения. Будет использован полный путь и будет считаться относительным к настроенному пути вывода приложения. | `string` | `index.html` | `index.html`.

<!-- links -->

[aioguidei18ncommonmerge]: guide/i18n-common-merge 'Common Internationalization task #6: Merge translations into the application | Angular'

<!-- external links -->

<!-- end links -->

@ просмотрено 2022-02-28
