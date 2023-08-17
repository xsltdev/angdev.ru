---
description: Когда вы создаете библиотеку Angular, вы можете предоставить и упаковать ее со схемами, которые интегрируют ее с Angular CLI
---

# Схемы для библиотек

:date: 28.02.2022

Когда вы создаете библиотеку Angular, вы можете предоставить и упаковать ее со схемами, которые интегрируют ее с Angular CLI. С помощью ваших схем ваши пользователи могут использовать `ng add` для установки начальной версии вашей библиотеки,

`ng generate` для создания артефактов, определенных в вашей библиотеке, и `ng update` для адаптации проекта к новой версии вашей библиотеки, которая вносит изменения.

Все три типа схем могут быть частью коллекции, которую вы упаковываете вместе с вашей библиотекой.

Загрузите [library schematics project](https://angular.io/generated/zips/schematics-for-libraries/schematics-for-libraries.zip) для получения завершенного примера следующих шагов.

## Создание коллекции схем

Чтобы запустить коллекцию, необходимо создать файлы схем. Следующие шаги показывают, как добавить начальную поддержку без изменения каких-либо файлов проекта.

1.  В корневой папке библиотеки создайте папку `schematics`.
2.  В папке `schematics/` создайте папку `ng-add` для вашей первой схемы.

3.  На корневом уровне папки `schematics` создайте файл `collection.json`.

4.  Отредактируйте файл `collection.json`, чтобы определить начальную схему для вашей коллекции.

    ```json
    {
        "$schema": "../../../node_modules/@angular-devkit/schematics/collection-schema.json",
        "schematics": {
            "ng-add": {
                "description": "Add my library to the project.",
                "factory": "./ng-add/index#ngAdd",
                "schema": "./ng-add/schema.json"
            }
        }
    }
    ```

    -   Путь `$schema` является относительным к схеме коллекции Angular Devkit.

    -   Объект `schematics` описывает именованные схемы, которые являются частью этой коллекции.

    -   Первая запись относится к схеме с именем `ng-add`.

        Она содержит описание и указывает на фабричную функцию, которая вызывается при выполнении схемы.

5.  В файл `package.json` проекта библиотеки добавьте запись "schematics" с путем к файлу схемы.

    Angular CLI использует эту запись для поиска именованных схем в вашей коллекции при выполнении команд.

    ```json
    {
        "name": "my-lib",
        "version": "0.0.1",
        "schematics": "./schematics/collection.json"
    }
    ```

Начальная схема, которую вы создали, указывает CLI, где найти схему, поддерживающую команду `ng add`. Теперь вы готовы создать эту схему.

## Обеспечение поддержки установки

Схема для команды `ng add` может улучшить процесс начальной установки для ваших пользователей. Следующие шаги определяют этот тип схемы.

1.  Перейдите в папку `<lib-root>/schematics/ng-add`.

2.  Создайте основной файл `index.ts`.

3.  Откройте `index.ts` и добавьте исходный код для вашей функции фабрики схем.

    ```ts
    import { Rule } from '@angular-devkit/schematics';
    import { addRootImport } from '@schematics/angular/utility';
    import { Schema } from './schema';

    export function ngAdd(options: Schema): Rule {
        // Add an import `MyLibModule` from `my-lib` to the root of the user's project.
        return addRootImport(
            options.project,
            ({ code, external }) =>
                code`${external('MyLibModule', 'my-lib')}`
        );
    }
    ```

Angular CLI автоматически установит последнюю версию библиотеки, а в данном примере мы делаем еще один шаг вперед, добавляя `MyLibModule` в корень приложения. Функция `addRootImport` принимает обратный вызов, который должен вернуть блок кода. Вы можете написать любой код внутри строки, помеченной функцией `code`, а любой внешний символ должен быть обернут функцией `external`, чтобы обеспечить генерацию соответствующих утверждений импорта.

### Определите тип зависимости

Используйте опцию `save` функции `ng-add` для настройки того, должна ли библиотека быть добавлена в `dependencies`, `devDependencies` или вообще не сохраняться в конфигурационном файле проекта `package.json`.

```json
"ng-add": {
  "save": "devDependencies"
},
```

Возможными значениями являются:

| Значения            | Подробности                         |
| :------------------ | :---------------------------------- |
| `false`             | Не добавлять пакет в `package.json` |
| `true`              | Добавить пакет в зависимости        |
| `"dependencies"`    | Добавить пакет в зависимости        |
| `"devDependencies"` | Добавить пакет в devDependencies    |

## Сборка схем

Чтобы собрать схемы вместе с библиотекой, вы должны настроить библиотеку на сборку схем отдельно, а затем добавить их в пакет. Вы должны собрать схемы _после_ сборки библиотеки, чтобы они были помещены в правильную директорию.

-   Вашей библиотеке необходим пользовательский конфигурационный файл Typescript с инструкциями по компиляции схем в вашу распределенную библиотеку.

-   Чтобы добавить схемы в пакет библиотеки, добавьте скрипты в файл библиотеки `package.json`.

Предположим, что у вас есть библиотечный проект `my-lib` в рабочем пространстве Angular. Чтобы указать библиотеке, как собирать схемы, добавьте файл `tsconfig.schematics.json` рядом со сгенерированным файлом `tsconfig.lib.json`, который настраивает сборку библиотеки.

1.  Отредактируйте файл `tsconfig.schematics.json`, чтобы добавить следующее содержимое.

    ```json
    {
        "compilerOptions": {
            "baseUrl": ".",
            "lib": ["es2018", "dom"],
            "declaration": true,
            "module": "commonjs",
            "moduleResolution": "node",
            "noEmitOnError": true,
            "noFallthroughCasesInSwitch": true,
            "noImplicitAny": true,
            "noImplicitThis": true,
            "noUnusedParameters": true,
            "noUnusedLocals": true,
            "rootDir": "schematics",
            "outDir": "../../dist/my-lib/schematics",
            "skipDefaultLibCheck": true,
            "skipLibCheck": true,
            "sourceMap": true,
            "strictNullChecks": true,
            "target": "es6",
            "types": ["jasmine", "node"]
        },
        "include": ["schematics/**/*"],
        "exclude": ["schematics/*/files/**/*"]
    }
    ```

    | Опции     | Детали                                                                                                        |
    | :-------- | :------------------------------------------------------------------------------------------------------------ |
    | `rootDir` | Указывает, что ваша папка `schematics` содержит входные файлы для компиляции.                                 |
    | `outDir`  | Указывает папку вывода библиотеки. По умолчанию это папка `dist/my-lib` в корне вашего рабочего пространства. |

2.  Чтобы убедиться, что ваши исходные файлы схем будут скомпилированы в пакет библиотеки, добавьте следующие скрипты в файл `package.json` в корневой папке проекта библиотеки (`projects/my-lib`).

    ```json
    {
        "name": "my-lib",
        "version": "0.0.1",
        "scripts": {
            "build": "tsc -p tsconfig.schematics.json",
            "postbuild": "copyfiles schematics/*/schema.json schematics/*/files/** schematics/collection.json ../../dist/my-lib/"
        },
        "peerDependencies": {
            "@angular/common": "^16.1.0",
            "@angular/core": "^16.1.0"
        },
        "schematics": "./schematics/collection.json",
        "ng-add": {
            "save": "devDependencies"
        },
        "devDependencies": {
            "copyfiles": "file:../../node_modules/copyfiles",
            "typescript": "file:../../node_modules/typescript"
        }
    }
    ```

    -   Сценарий `build` компилирует вашу схему, используя пользовательский файл `tsconfig.schematics.json`.

    -   Сценарий `postbuild` копирует файлы схемы после завершения работы сценария `build`.

    -   Сценарии `build` и `postbuild` требуют наличия зависимостей `copyfiles` и `typescript`.

        Чтобы установить эти зависимости, перейдите по пути, указанному в `devDependencies`, и запустите `npm install` перед запуском скриптов.

## Обеспечение поддержки генерации

Вы можете добавить именованную схему в свою коллекцию, которая позволит вашим пользователям использовать команду `ng generate` для создания артефакта, определенного в вашей библиотеке.

Предположим, что ваша библиотека определяет сервис, `my-service`, который требует некоторой настройки. Вы хотите, чтобы ваши пользователи могли создать его с помощью следующей команды CLI.

```shell
ng generate my-lib:my-service
```

Для начала создайте новую подпапку `my-service` в папке `chematics`.

### Настройте новую схему

Когда вы добавляете схему в коллекцию, вы должны указать на нее в схеме коллекции и предоставить конфигурационные файлы для определения опций, которые пользователь может передать команде.

1.  Отредактируйте файл `schematics/collection.json` так, чтобы он указывал на новую подпапку схем, и включите в него указатель на файл схемы, задающий входные данные для новой схемы.

    ```json
    {
        "$schema": "../../../node_modules/@angular-devkit/schematics/collection-schema.json",
        "schematics": {
            "ng-add": {
                "description": "Add my library to the project.",
                "factory": "./ng-add/index#ngAdd",
                "schema": "./ng-add/schema.json"
            },
            "my-service": {
                "description": "Generate a service in the project.",
                "factory": "./my-service/index#myService",
                "schema": "./my-service/schema.json"
            }
        }
    }
    ```

2.  Перейдите в папку `<lib-root>/schematics/my-service`.
3.  Создайте файл `chema.json` и определите доступные опции для схемы.

    ```json
    {
        "$schema": "http://json-schema.org/schema",
        "$id": "SchematicsMyService",
        "title": "My Service Schema",
        "type": "object",
        "properties": {
            "name": {
                "description": "The name of the service.",
                "type": "string"
            },
            "path": {
                "type": "string",
                "format": "path",
                "description": "The path to create the service.",
                "visible": false
            },
            "project": {
                "type": "string",
                "description": "The name of the project.",
                "$default": {
                    "$source": "projectName"
                }
            }
        },
        "required": ["name"]
    }
    ```

    -   _id_: Уникальный идентификатор схемы в коллекции.
    -   _title_: Человекочитаемое описание схемы.
    -   _type_: Дескриптор для типа, предоставляемого свойствами.
    -   _properties_: Объект, определяющий доступные опции для схемы.

    Каждая опция связывает ключ с типом, описанием и необязательным псевдонимом.
    Тип определяет форму ожидаемого значения, а описание отображается при запросе пользователем помощи по использованию схемы.

    Дополнительные настройки опций схемы см. в схеме рабочего пространства.

4.  Создайте файл `schema.ts` и определите интерфейс, хранящий значения опций, определенных в файле `schema.json`.

    ```ts
    export interface Schema {
        // The name of the service.
        name: string;

        // The path to create the service.
        path?: string;

        // The name of the project.
        project?: string;
    }
    ```

    | Опции     | Детали                                                                                                                                 |
    | :-------- | :------------------------------------------------------------------------------------------------------------------------------------- |
    | `name`    | Имя, которое вы хотите дать создаваемому сервису.                                                                                      |
    | `path`    | Переопределяет путь, указанный к схеме. Значение пути по умолчанию основано на текущем рабочем каталоге.                               |
    | `project` | Указывает конкретный проект для запуска схемы. В схеме можно указать значение по умолчанию, если опция не предоставлена пользователем. |

### Добавить файлы шаблонов

Чтобы добавить артефакты в проект, вашей схеме нужны собственные файлы шаблонов. Шаблоны схем поддерживают специальный синтаксис для выполнения кода и подстановки переменных.

1.  Создайте папку `files/` внутри папки `schematics/my-service/`.

2.  Создайте файл с именем `__name@dasherize__.service.ts.template`, определяющий шаблон, который будет использоваться для генерации файлов.

    Этот шаблон будет генерировать сервис, который уже имеет Angular's `HttpClient`, инжектированный в его конструктор.

    ```ts
    import { Injectable } from '@angular/core';
    import { HttpClient } from '@angular/common/http';

    @Injectable({
    	providedIn: 'root'
    })

    export class <%= classify(name) %>Service {
    	constructor(private http: HttpClient) { }
    }
    ```

    -   Методы `classify` и `dasherize` являются вспомогательными функциями, которые ваша схема использует для преобразования исходного шаблона и имени файла.

    -   Имя `name` предоставляется как свойство из вашей фабричной функции.

        Это то же самое `имя`, которое вы определили в схеме.

### Добавьте фабричную функцию

Теперь, когда у вас есть инфраструктура, вы можете определить главную функцию, которая выполняет необходимые вам изменения в проекте пользователя.

Фреймворк Schematics предоставляет систему шаблонизации файлов, которая поддерживает шаблоны путей и содержимого. Система работает с заполнителями, определенными внутри файлов или путей, загруженных во входное `дерево`.

Она заполняет их, используя значения, переданные в `Rule`.

Подробности об этих структурах данных и синтаксисе см. в [Schematics README](https://github.com/angular/angular-cli/blob/main/packages/angular_devkit/schematics/README.md).

1.  Создайте основной файл `index.ts` и добавьте в него исходный код для функции фабрики схем.
2.  Сначала импортируйте определения схем, которые вам понадобятся.

    Фреймворк Schematics предлагает множество вспомогательных функций для создания и использования правил при выполнении схемы.

    ```ts
    import {
        Rule,
        Tree,
        SchematicsException,
        apply,
        url,
        applyTemplates,
        move,
        chain,
        mergeWith,
    } from '@angular-devkit/schematics';

    import {
        strings,
        normalize,
        virtualFs,
        workspaces,
    } from '@angular-devkit/core';
    ```

3.  Импортируйте определенный интерфейс схемы, который предоставляет информацию о типе для опций вашей схемы.

    ```ts
    import {
        Rule,
        Tree,
        SchematicsException,
        apply,
        url,
        applyTemplates,
        move,
        chain,
        mergeWith,
    } from '@angular-devkit/schematics';

    import {
        strings,
        normalize,
        virtualFs,
        workspaces,
    } from '@angular-devkit/core';

    import { Schema as MyServiceSchema } from './schema';
    ```

4.  Чтобы построить схему генерации, начните с пустой фабрики правил.

    ```ts
    export function myService(
        options: MyServiceSchema
    ): Rule {
        return (tree: Tree) => tree;
    }
    ```

Эта фабрика правил возвращает дерево без изменений. Опции - это значения опций, переданные командой `ng generate`.

## Определите правило генерации

Теперь у вас есть основа для создания кода, который фактически изменяет приложение пользователя, чтобы настроить его на работу с сервисом, определенным в вашей библиотеке.

Рабочая область Angular, куда пользователь установил вашу библиотеку, содержит несколько проектов (приложения и библиотеки). Пользователь может указать проект в командной строке или использовать его по умолчанию.

В любом случае, ваш код должен определить конкретный проект, к которому применяется эта схема, чтобы вы могли получить информацию из конфигурации проекта.

Сделайте это с помощью объекта `Tree`, который передается в функцию factory. Методы `Tree` дают вам доступ к полному дереву файлов в вашей рабочей области, позволяя вам читать и записывать файлы во время выполнения схемы.

### Получение конфигурации проекта

1.  Чтобы определить проект назначения, используйте метод `workspaces.readWorkspace` для чтения содержимого файла конфигурации рабочего пространства, `angular.json`.

    Чтобы использовать `workspaces.readWorkspace`, необходимо создать `workspaces.WorkspaceHost` из `Tree`.

    Добавьте следующий код в вашу фабричную функцию.

    ```ts
    import {
        Rule,
        Tree,
        SchematicsException,
        apply,
        url,
        applyTemplates,
        move,
        chain,
        mergeWith,
    } from '@angular-devkit/schematics';

    import {
        strings,
        normalize,
        virtualFs,
        workspaces,
    } from '@angular-devkit/core';

    import { Schema as MyServiceSchema } from './schema';

    function createHost(
        tree: Tree
    ): workspaces.WorkspaceHost {
        return {
            async readFile(path: string): Promise<string> {
                const data = tree.read(path);
                if (!data) {
                    throw new SchematicsException(
                        'File not found.'
                    );
                }
                return virtualFs.fileBufferToString(data);
            },
            async writeFile(
                path: string,
                data: string
            ): Promise<void> {
                return tree.overwrite(path, data);
            },
            async isDirectory(
                path: string
            ): Promise<boolean> {
                return (
                    !tree.exists(path) &&
                    tree.getDir(path).subfiles.length > 0
                );
            },
            async isFile(path: string): Promise<boolean> {
                return tree.exists(path);
            },
        };
    }

    export function myService(
        options: MyServiceSchema
    ): Rule {
        return async (tree: Tree) => {
            const host = createHost(tree);
            const {
                workspace,
            } = await workspaces.readWorkspace('/', host);
        };
    }
    ```

    Обязательно проверьте, что контекст существует, и выбросьте соответствующую ошибку.

2.  Теперь, когда у вас есть имя проекта, используйте его для получения информации о конфигурации, специфичной для проекта.

    ```ts
    const project =
        options.project != null
            ? workspace.projects.get(options.project)
            : null;
    if (!project) {
        throw new SchematicsException(
            `Invalid project name: ${options.project}`
        );
    }

    const projectType =
        project.extensions.projectType === 'application'
            ? 'app'
            : 'lib';
    ```

    Объект `workspace.projects` содержит всю специфическую для проекта информацию о конфигурации.

3.  Параметр `options.path` определяет, куда будут перемещены файлы шаблона схемы после применения схемы.

    Опция `path` в схеме схемы по умолчанию заменяется на текущий рабочий каталог.

    Если `path` не определен, используйте `sourceRoot` из конфигурации проекта вместе с `projectType`.

    ```ts
    if (options.path === undefined) {
        options.path = `${project.sourceRoot}/${projectType}`;
    }
    ```

### Определите правило

Правило `Rule` может использовать внешние файлы шаблонов, преобразовывать их и возвращать другой объект `Rule` с преобразованным шаблоном. Используйте шаблонизацию для создания любых пользовательских файлов, необходимых для вашей схемы.

1.  Add the following code to your factory function.

    ```ts
    const templateSource = apply(url('./files'), [
        applyTemplates({
            classify: strings.classify,
            dasherize: strings.dasherize,
            name: options.name,
        }),
        move(normalize(options.path as string)),
    ]);
    ```

    Методы:

    `apply()`
    : Применяет несколько правил к источнику и возвращает преобразованный источник. Принимает 2 аргумента - источник и массив правил.

    `url()`
    : Считывает исходные файлы из файловой системы относительно схемы.

    `applyTemplates()`
    : Получает аргумент, содержащий методы и свойства, которые необходимо сделать доступными для шаблона схемы, и имена файлов схемы. Возвращает `Rule`. В нем определяются методы `classify()` и `dasherize()`, а также свойство `name`.

    `classify()`
    : Принимает значение и возвращает его в заглавном регистре. Например, если предоставленное имя - `my service`, то оно возвращается как `MyService`.

    `dasherize()`
    : Принимает значение и возвращает его в прочерках и строчных буквах. Например, если предоставленное имя - MyService, то оно возвращается в виде `my-service`.

    `move()`
    : Перемещает предоставленные исходные файлы в место назначения при применении схемы.

2.  Наконец, фабрика правил должна возвращать правило.

    ```ts
    return chain([mergeWith(templateSource)]);
    ```

    Метод `chain()` позволяет объединить несколько правил в одно правило, чтобы выполнить несколько операций в одной схеме.

    В данном случае объединяются только правила шаблона и любой код, выполняемый схемой.

Смотрите полный пример следующей схемы функции правила.

```ts
import {
    Rule,
    Tree,
    SchematicsException,
    apply,
    url,
    applyTemplates,
    move,
    chain,
    mergeWith,
} from '@angular-devkit/schematics';

import {
    strings,
    normalize,
    virtualFs,
    workspaces,
} from '@angular-devkit/core';

import { Schema as MyServiceSchema } from './schema';

function createHost(tree: Tree): workspaces.WorkspaceHost {
    return {
        async readFile(path: string): Promise<string> {
            const data = tree.read(path);
            if (!data) {
                throw new SchematicsException(
                    'File not found.'
                );
            }
            return virtualFs.fileBufferToString(data);
        },
        async writeFile(
            path: string,
            data: string
        ): Promise<void> {
            return tree.overwrite(path, data);
        },
        async isDirectory(path: string): Promise<boolean> {
            return (
                !tree.exists(path) &&
                tree.getDir(path).subfiles.length > 0
            );
        },
        async isFile(path: string): Promise<boolean> {
            return tree.exists(path);
        },
    };
}

export function myService(options: MyServiceSchema): Rule {
    return async (tree: Tree) => {
        const host = createHost(tree);
        const {
            workspace,
        } = await workspaces.readWorkspace('/', host);

        const project =
            options.project != null
                ? workspace.projects.get(options.project)
                : null;
        if (!project) {
            throw new SchematicsException(
                `Invalid project name: ${options.project}`
            );
        }

        const projectType =
            project.extensions.projectType === 'application'
                ? 'app'
                : 'lib';

        if (options.path === undefined) {
            options.path = `${project.sourceRoot}/${projectType}`;
        }

        const templateSource = apply(url('./files'), [
            applyTemplates({
                classify: strings.classify,
                dasherize: strings.dasherize,
                name: options.name,
            }),
            move(normalize(options.path as string)),
        ]);

        return chain([mergeWith(templateSource)]);
    };
}
```

Для получения дополнительной информации о правилах и методах утилиты смотрите [Provided Rules](https://github.com/angular/angular-cli/tree/main/packages/angular_devkit/schematics#provided-rules).

## Запуск схемы вашей библиотеки

После сборки библиотеки и схем вы можете установить коллекцию схем для запуска в вашем проекте. Следующие шаги показывают, как сгенерировать сервис, используя схему, которую вы создали ранее.

### Создайте библиотеку и схемы

В корне рабочей области выполните команду `ng build` для вашей библиотеки.

```shell
ng build my-lib
```

Затем вы переходите в каталог библиотеки для создания схемы

```shell
cd projects/my-lib
npm run build
```

### Свяжите библиотеку

Ваша библиотека и схемы упакованы и помещены в папку `dist/my-lib` в корне вашего рабочего пространства. Чтобы запустить схему, вам нужно связать библиотеку в папке `node_modules`.

Из корня рабочей области выполните команду `npm link`, указав путь к вашей распространяемой библиотеке.

```shell
npm link dist/my-lib
```

### Запустите схему

Теперь, когда библиотека установлена, запустите схему с помощью команды `ng generate`.

```shell
ng generate my-lib:my-service --name my-data
```

В консоли вы видите, что схема была запущена и файл `my-data.service.ts` был создан в папке вашего приложения.

```shell
CREATE src/app/my-data.service.ts (208 bytes)
```

<!-- links -->

<!-- external links -->

<!-- end links -->

## Ссылки

-   [Schematics for libraries](https://angular.io/guide/schematics-for-libraries)
