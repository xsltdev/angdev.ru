# Схемы для библиотек

Когда вы создаете библиотеку Angular, вы можете предоставить и упаковать ее со схемами, которые интегрируют ее с Angular CLI. С помощью ваших схем ваши пользователи могут использовать `ng add` для установки начальной версии вашей библиотеки,

`ng generate` для создания артефактов, определенных в вашей библиотеке, и `ng update` для адаптации проекта к новой версии вашей библиотеки, которая вносит изменения.

Все три типа схем могут быть частью коллекции, которую вы упаковываете вместе с вашей библиотекой.

Загрузите <live-example downloadOnly>library schematics project</live-example> для получения завершенного примера следующих шагов.

## Создание коллекции схем

Чтобы запустить коллекцию, необходимо создать файлы схем. Следующие шаги показывают, как добавить начальную поддержку без изменения каких-либо файлов проекта.

1.  В корневой папке библиотеки создайте папку `schematics`.
1.  В папке `schematics/` создайте папку `ng-add` для вашей первой схемы.

1.  На корневом уровне папки `schematics` создайте файл `collection.json`.

1.  Отредактируйте файл `collection.json`, чтобы определить начальную схему для вашей коллекции.

    <code-example header="projects/my-lib/schematics/collection.json (Schematics Collection)" path="schematics-for-libraries/projects/my-lib/schematics/collection.1.json"></code-example>.

    -   Путь `$schema` является относительным к схеме коллекции Angular Devkit.

    -   Объект `schematics` описывает именованные схемы, которые являются частью этой коллекции.

    -   Первая запись относится к схеме с именем `ng-add`.

        Она содержит описание и указывает на фабричную функцию, которая вызывается при выполнении схемы.

1.  В файл `package.json` проекта библиотеки добавьте запись "schematics" с путем к файлу схемы.

    Angular CLI использует эту запись для поиска именованных схем в вашей коллекции при выполнении команд.

    <code-example header="projects/my-lib/package.json (Ссылка на коллекцию схем)" path="schematics-for-libraries/projects/my-lib/package.json" region="collection"></code-example>.

Начальная схема, которую вы создали, указывает CLI, где найти схему, поддерживающую команду `ng add`. Теперь вы готовы создать эту схему.

## Обеспечение поддержки установки

Схема для команды `ng add` может улучшить процесс начальной установки для ваших пользователей. Следующие шаги определяют этот тип схемы.

1.  Перейдите в папку `<lib-root>/schematics/ng-add`.

1.  Создайте основной файл `index.ts`.

1.  Откройте `index.ts` и добавьте исходный код для вашей функции фабрики схем.

    <code-example header="projects/my-lib/schematics/ng-add/index.ts (ng-add Rule Factory)" path="schematics-for-libraries/projects/my-lib/schematics/ng-add/index.ts"></code-example>.

Angular CLI автоматически установит последнюю версию библиотеки, а в данном примере мы делаем еще один шаг вперед, добавляя `MyLibModule` в корень приложения. Функция `addRootImport` принимает обратный вызов, который должен вернуть блок кода. Вы можете написать любой код внутри строки, помеченной функцией `code`, а любой внешний символ должен быть обернут функцией `external`, чтобы обеспечить генерацию соответствующих утверждений импорта.

### Определите тип зависимости

Используйте опцию `save` функции `ng-add` для настройки того, должна ли библиотека быть добавлена в `dependencies`, `devDependencies` или вообще не сохраняться в конфигурационном файле проекта `package.json`.

<code-example header="projects/my-lib/package.json (ng-add Reference)" path="schematics-for-libraries/projects/my-lib/package.json" region="ng-add"></code-example>.

Возможными значениями являются:

| Значения | Подробности | | :------------------ | :-------------------------------------- |.

| `false` | Не добавлять пакет в `package.json` |

| `true` | Добавить пакет в зависимости |

| `"dependencies"| | Добавить пакет в зависимости |

| | `"devDependencies"| | Добавить пакет в devDependencies |

## Сборка схем

Чтобы собрать схемы вместе с библиотекой, вы должны настроить библиотеку на сборку схем отдельно, а затем добавить их в пакет. Вы должны собрать схемы _после_ сборки библиотеки, чтобы они были помещены в правильную директорию.

-   Вашей библиотеке необходим пользовательский конфигурационный файл Typescript с инструкциями по компиляции схем в вашу распределенную библиотеку.

-   Чтобы добавить схемы в пакет библиотеки, добавьте скрипты в файл библиотеки `package.json`.

Предположим, что у вас есть библиотечный проект `my-lib` в рабочем пространстве Angular. Чтобы указать библиотеке, как собирать схемы, добавьте файл `tsconfig.schematics.json` рядом со сгенерированным файлом `tsconfig.lib.json`, который настраивает сборку библиотеки.

1.  Отредактируйте файл `tsconfig.schematics.json`, чтобы добавить следующее содержимое.

    <code-example header="projects/my-lib/tsconfig.schematics.json (TypeScript Config)" path="schematics-for-libraries/projects/my-lib/tsconfig.schematics.json"></code-example>.

    | Опции | Детали |

    | :-------- | :--------------------------------------------------------------------------------------------------------------- |

    | `rootDir` | Указывает, что ваша папка `schematics` содержит входные файлы для компиляции. |

    | `outDir` | Указывает папку вывода библиотеки. По умолчанию это папка `dist/my-lib` в корне вашего рабочего пространства. |

1.  Чтобы убедиться, что ваши исходные файлы схем будут скомпилированы в пакет библиотеки, добавьте следующие скрипты в файл `package.json` в корневой папке проекта библиотеки \(`projects/my-lib`\).

    <code-example header="projects/my-lib/package.json (Build Scripts)" path="schematics-for-libraries/projects/my-lib/package.json"></code-example>.

    -   Сценарий `build` компилирует вашу схему, используя пользовательский файл `tsconfig.schematics.json`.

    -   Сценарий `postbuild` копирует файлы схемы после завершения работы сценария `build`.

    -   Сценарии `build` и `postbuild` требуют наличия зависимостей `copyfiles` и `typescript`.

        Чтобы установить эти зависимости, перейдите по пути, указанному в `devDependencies`, и запустите `npm install` перед запуском скриптов.

## Обеспечение поддержки генерации

Вы можете добавить именованную схему в свою коллекцию, которая позволит вашим пользователям использовать команду `ng generate` для создания артефакта, определенного в вашей библиотеке.

Предположим, что ваша библиотека определяет сервис, `my-service`, который требует некоторой настройки. Вы хотите, чтобы ваши пользователи могли создать его с помощью следующей команды CLI.

<code-example format="shell" language="shell">

ng generate my-lib:my-service

</code-example>

Для начала создайте новую подпапку `my-service` в папке `chematics`.

### Настройте новую схему

Когда вы добавляете схему в коллекцию, вы должны указать на нее в схеме коллекции и предоставить конфигурационные файлы для определения опций, которые пользователь может передать команде.

1.  Edit the `schematics/collection.json` file to point to the new schematic subfolder, and include a pointer to a schema file that specifies inputs for the new schematic.

    <code-example header="projects/my-lib/schematics/collection.json (Schematics Collection)" path="schematics-for-libraries/projects/my-lib/schematics/collection.json"></code-example>

1.  Go to the `<lib-root>/schematics/my-service` folder.
1.  Create a `schema.json` file and define the available options for the schematic.

    <code-example header="projects/my-lib/schematics/my-service/schema.json (Schematic JSON Schema)" path="schematics-for-libraries/projects/my-lib/schematics/my-service/schema.json"></code-example>

    -   _id_: A unique ID for the schema in the collection.
    -   _title_: A human-readable description of the schema.
    -   _type_: A descriptor for the type provided by the properties.
    -   _properties_: An object that defines the available options for the schematic.

    Each option associates key with a type, description, and optional alias.
    The type defines the shape of the value you expect, and the description is displayed when the user requests usage help for your schematic.

    See the workspace schema for additional customizations for schematic options.

1.  Create a `schema.ts` file and define an interface that stores the values of the options defined in the `schema.json` file.

    <code-example header="projects/my-lib/schematics/my-service/schema.ts (Schematic Interface)" path="schematics-for-libraries/projects/my-lib/schematics/my-service/schema.ts"></code-example>

    | Options | Details                                                                                                                                     |
    | :------ | :------------------------------------------------------------------------------------------------------------------------------------------ |
    | name    | The name you want to provide for the created service.                                                                                       |
    | path    | Overrides the path provided to the schematic. The default path value is based on the current working directory.                             |
    | project | Provides a specific project to run the schematic on. In the schematic, you can provide a default if the option is not provided by the user. |

### Добавить файлы шаблонов

Чтобы добавить артефакты в проект, вашей схеме нужны собственные файлы шаблонов. Шаблоны схем поддерживают специальный синтаксис для выполнения кода и подстановки переменных.

1.  Создайте папку `files/` внутри папки `schematics/my-service/`.

1.  Создайте файл с именем `__name@dasherize__.service.ts.template`, определяющий шаблон, который будет использоваться для генерации файлов.

    Этот шаблон будет генерировать сервис, который уже имеет Angular's `HttpClient`, инжектированный в его конструктор.

    <code-example lang="typescript" header="projects/my-lib/schematics/my-service/files/__name@dasherize__.service.ts.template (Шаблон схемы)">.

    import { Injectable } from '&commat;angular/core';

    import { HttpClient } from '&commat;angular/common/http';

    &commat;Injectable({

    providedIn: 'root'

    })

    export class &lt;%= classify(name) %&gt;Service {

    constructor(private http: HttpClient) { }

    }

    </code-example>

    -   Методы `classify` и `dasherize` являются вспомогательными функциями, которые ваша схема использует для преобразования исходного шаблона и имени файла.

    -   Имя `name` предоставляется как свойство из вашей фабричной функции.

        Это то же самое `имя`, которое вы определили в схеме.

### Добавьте фабричную функцию

Теперь, когда у вас есть инфраструктура, вы можете определить главную функцию, которая выполняет необходимые вам изменения в проекте пользователя.

Фреймворк Schematics предоставляет систему шаблонизации файлов, которая поддерживает шаблоны путей и содержимого. Система работает с заполнителями, определенными внутри файлов или путей, загруженных во входное `дерево`.

Она заполняет их, используя значения, переданные в `Rule`.

Подробности об этих структурах данных и синтаксисе см. в [Schematics README](https://github.com/angular/angular-cli/blob/main/packages/angular_devkit/schematics/README.md).

1.  Создайте основной файл `index.ts` и добавьте в него исходный код для функции фабрики схем.
1.  Сначала импортируйте определения схем, которые вам понадобятся.

    Фреймворк Schematics предлагает множество вспомогательных функций для создания и использования правил при выполнении схемы.

    <code-example header="projects/my-lib/schematics/my-service/index.ts (Imports)" path="schematics-for-libraries/projects/my-lib/schematics/my-service/index.ts" region="schematics-imports"></code-example>.

1.  Импортируйте определенный интерфейс схемы, который предоставляет информацию о типе для опций вашей схемы.

    <code-example header="projects/my-lib/schematics/my-service/index.ts (Schema Import)" path="schematics-for-libraries/projects/my-lib/schematics/my-service/index.ts" region="schema-imports"></code-example>.

1.  Чтобы построить схему генерации, начните с пустой фабрики правил.

    <code-example header="projects/my-lib/schematics/my-service/index.ts (Initial Rule)" path="schematics-for-libraries/projects/my-lib/schematics/my-service/index.1.ts" region="factory"></code-example>.

Эта фабрика правил возвращает дерево без изменений. Опции - это значения опций, переданные командой `ng generate`.

## Определите правило генерации

Теперь у вас есть основа для создания кода, который фактически изменяет приложение пользователя, чтобы настроить его на работу с сервисом, определенным в вашей библиотеке.

Рабочая область Angular, куда пользователь установил вашу библиотеку, содержит несколько проектов\(приложения и библиотеки\). Пользователь может указать проект в командной строке или использовать его по умолчанию.

В любом случае, ваш код должен определить конкретный проект, к которому применяется эта схема, чтобы вы могли получить информацию из конфигурации проекта.

Сделайте это с помощью объекта `Tree`, который передается в функцию factory. Методы `Tree` дают вам доступ к полному дереву файлов в вашей рабочей области, позволяя вам читать и записывать файлы во время выполнения схемы.

### Получение конфигурации проекта

1.  Чтобы определить проект назначения, используйте метод `workspaces.readWorkspace` для чтения содержимого файла конфигурации рабочего пространства, `angular.json`.

    Чтобы использовать `workspaces.readWorkspace`, необходимо создать `workspaces.WorkspaceHost` из `Tree`.

    Добавьте следующий код в вашу фабричную функцию.

    <code-example header="projects/my-lib/schematics/my-service/index.ts (Schema Import)" path="schematics-for-libraries/projects/my-lib/schematics/my-service/index.ts" region="workspace"></code-example>.

    Обязательно проверьте, что контекст существует, и выбросьте соответствующую ошибку.

1.  Теперь, когда у вас есть имя проекта, используйте его для получения информации о конфигурации, специфичной для проекта.

    <code-example header="projects/my-lib/schematics/my-service/index.ts (Project)" path="schematics-for-libraries/projects/my-lib/schematics/my-service/index.ts" region="project-info"></code-example>.

    Объект `workspace.projects` содержит всю специфическую для проекта информацию о конфигурации.

1.  Параметр `options.path` определяет, куда будут перемещены файлы шаблона схемы после применения схемы.

    Опция `path` в схеме схемы по умолчанию заменяется на текущий рабочий каталог.

    Если `path` не определен, используйте `sourceRoot` из конфигурации проекта вместе с `projectType`.

    <code-example header="projects/my-lib/schematics/my-service/index.ts (Информация о проекте)" path="schematics-for-libraries/projects/my-lib/schematics/my-service/index.ts" region="path"></code-example>.

### Определите правило

Правило `Rule` может использовать внешние файлы шаблонов, преобразовывать их и возвращать другой объект `Rule` с преобразованным шаблоном. Используйте шаблонизацию для создания любых пользовательских файлов, необходимых для вашей схемы.

1.  Add the following code to your factory function.

    <code-example header="projects/my-lib/schematics/my-service/index.ts (Template transform)" path="schematics-for-libraries/projects/my-lib/schematics/my-service/index.ts" region="template"></code-example>

    | Methods            | Details                                                                                                                                                                                                                                          |
    | :----------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `apply()`          | Applies multiple rules to a source and returns the transformed source. It takes 2 arguments, a source and an array of rules.                                                                                                                     |
    | `url()`            | Reads source files from your filesystem, relative to the schematic.                                                                                                                                                                              |
    | `applyTemplates()` | Receives an argument of methods and properties you want make available to the schematic template and the schematic filenames. It returns a `Rule`. This is where you define the `classify()` and `dasherize()` methods, and the `name` property. |
    | `classify()`       | Takes a value and returns the value in title case. For example, if the provided name is `my service`, it is returned as `MyService`.                                                                                                             |
    | `dasherize()`      | Takes a value and returns the value in dashed and lowercase. For example, if the provided name is MyService, it is returned as `my-service`.                                                                                                     |
    | `move()`           | Moves the provided source files to their destination when the schematic is applied.                                                                                                                                                              |

1.  Finally, the rule factory must return a rule.

    <code-example header="projects/my-lib/schematics/my-service/index.ts (Chain Rule)" path="schematics-for-libraries/projects/my-lib/schematics/my-service/index.ts" region="chain"></code-example>

    The `chain()` method lets you combine multiple rules into a single rule, so that you can perform multiple operations in a single schematic.
    Here you are only merging the template rules with any code executed by the schematic.

Смотрите полный пример следующей схемы функции правила.

<code-example header="projects/my-lib/schematics/my-service/index.ts" path="schematics-for-libraries/projects/my-lib/schematics/my-service/index.ts"></code-example>.

Для получения дополнительной информации о правилах и методах утилиты смотрите [Provided Rules](https://github.com/angular/angular-cli/tree/main/packages/angular_devkit/schematics#provided-rules).

## Запуск схемы вашей библиотеки

После сборки библиотеки и схем вы можете установить коллекцию схем для запуска в вашем проекте. Следующие шаги показывают, как сгенерировать сервис, используя схему, которую вы создали ранее.

### Создайте библиотеку и схемы

В корне рабочей области выполните команду `ng build` для вашей библиотеки.

<code-example format="shell" language="shell">

ng build my-lib

</code-example>

Затем вы переходите в каталог библиотеки для создания схемы

<code-example format="shell" language="shell">

cd projects/my-lib npm run build

</code-example>

### Свяжите библиотеку

Ваша библиотека и схемы упакованы и помещены в папку `dist/my-lib` в корне вашего рабочего пространства. Чтобы запустить схему, вам нужно связать библиотеку в папке `node_modules`.

Из корня рабочей области выполните команду `npm link`, указав путь к вашей распространяемой библиотеке.

<code-example format="shell" language="shell">

npm link dist/my-lib

</code-example>

### Запустите схему

Теперь, когда библиотека установлена, запустите схему с помощью команды `ng generate`.

<code-example format="shell" language="shell">

ng generate my-lib:my-service --name my-data

</code-example>

В консоли вы видите, что схема была запущена и файл `my-data.service.ts` был создан в папке вашего приложения.

<code-example language="shell" hideCopy>

CREATE src/app/my-data.service.ts (208 байт)

</code-example>

<!-- links -->

<!-- external links -->

<!-- end links -->

:date: 28.02.2022
