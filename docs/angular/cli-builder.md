---
description: Ряд команд Angular CLI запускает сложные процессы в вашем коде, такие как линтинг, сборка или тестирование
---

# Angular CLI builders

:date: 28.02.2022

Ряд команд Angular CLI запускает сложные процессы в вашем коде, такие как линтинг, сборка или тестирование. Эти команды используют внутренний инструмент под названием Architect для запуска _CLI builders_, которые применяют другой инструмент для выполнения нужной задачи.

В версии 8 Angular API CLI Builder стал стабильным и доступным для разработчиков, которые хотят настроить Angular CLI, добавляя или изменяя команды. Например, вы можете поставить конструктор для выполнения совершенно новой задачи или изменить, какой сторонний инструмент используется существующей командой.

Этот документ объясняет, как билдеры CLI интегрируются с файлом конфигурации рабочего пространства, и показывает, как вы можете создать свой собственный билдер.

!!!note ""

    Найти код используемых здесь примеров можно в этом [репозитории GitHub](https://github.com/mgechev/cli-builders-demo).

## CLI builders

Внутренний инструмент Architect делегирует работу функциям-обработчикам, называемым [_builders_](glossary.md#builder). Функция-обработчик строителя получает два аргумента: набор входных `опций` (объект JSON) и `контекст` (объект `BuilderContext`).

Разделение задач здесь такое же, как и в [schematics](glossary.md#schematic), которые используются для других команд CLI, которые касаются вашего кода (например, `ng generate`).

-   Объект `options` предоставляется пользователем CLI, а объект `context` предоставляется API CLI Builder.

-   В дополнение к контекстной информации, объект `context`, который является экземпляром `BuilderContext`, также предоставляет доступ к методу планирования, `context.scheduleTarget()`.

    Планировщик выполняет функцию-обработчик строителя с заданной [целевой конфигурацией](glossary.md#target).

Функция-обработчик может быть синхронной (return a value) или асинхронной (return a Promise), или она может наблюдать и возвращать несколько значений (return an Observable). Возвращаемое значение или значения всегда должны быть типа `BuilderOutput`.

Этот объект содержит булево поле `success` и необязательное поле `error`, которое может содержать сообщение об ошибке.

Angular предоставляет некоторые билдеры, которые используются в CLI для таких команд, как `ng build` и `ng test`. Целевые конфигурации по умолчанию для этих и других встроенных CLI-строителей можно найти (и настроить) в разделе "architect" [файла конфигурации рабочего пространства](workspace-config.md), `angular.json`.

Кроме того, расширяйте и настраивайте Angular, создавая свои собственные конструкторы, которые можно запустить с помощью команды [`ng run` CLI](https://angular.io/cli/run).

### Структура проекта Builder

Builder находится в папке "project", которая по структуре похожа на рабочее пространство Angular, с глобальными конфигурационными файлами на верхнем уровне и более конкретной конфигурацией в папке с исходными кодами, определяющими поведение. Например, ваша папка `myBuilder` может содержать следующие файлы.

| Files                    | Purpose                                                                                                  |
| :----------------------- | :------------------------------------------------------------------------------------------------------- |
| `src/my-builder.ts`      | Основной исходный файл для определения билдера.                                                          |
| `src/my-builder.spec.ts` | Исходный файл для тестов.                                                                                |
| `src/schema.json`        | Определение входных опций билдера.                                                                       |
| `builders.json`          | Определение билдеров.                                                                                    |
| `package.json`           | Зависимости. См. [https://docs.npmjs.com/files/package.json](https://docs.npmjs.com/files/package.json). |
| `tsconfig.json`          | [TypeScript configuration](https://www.typescriptlang.org/docs/handbook/tsconfig-json.html).             |

Опубликуйте конструктор в `npm` (см. [Публикация вашей библиотеки](creating-libraries.md#publishing-your-library)). Если вы опубликовали его как `@example/my-builder`, установите его с помощью следующей команды.

```shell
npm install @example/my-builder
```

## Создание конструктора

В качестве примера создадим построитель, который копирует файл. Чтобы создать построитель, используйте функцию `createBuilder()` CLI Builder и верните объект `Promise<BuilderOutput>`.

```ts
import {
    BuilderContext,
    BuilderOutput,
    createBuilder,
} from '@angular-devkit/architect';
import { JsonObject } from '@angular-devkit/core';

interface Options extends JsonObject {
    source: string;
    destination: string;
}

export default createBuilder(copyFileBuilder);

async function copyFileBuilder(
    options: Options,
    context: BuilderContext
): Promise<BuilderOutput> {}
```

Теперь давайте добавим к нему немного логики. Следующий код получает пути к исходному и целевому файлам из опций пользователя и копирует файл из исходного в целевой (используя [Promise версию встроенной функции NodeJS `copyFile()`](https://nodejsdev.ru/api/fs/#fspromisescopyfile)).

Если операция копирования не удалась, возвращается ошибка с сообщением об основной проблеме.

```ts
import {
    BuilderContext,
    BuilderOutput,
    createBuilder,
} from '@angular-devkit/architect';
import { JsonObject } from '@angular-devkit/core';
import { promises as fs } from 'fs';

interface Options extends JsonObject {
    source: string;
    destination: string;
}

export default createBuilder(copyFileBuilder);

async function copyFileBuilder(
    options: Options,
    context: BuilderContext
): Promise<BuilderOutput> {
    try {
        await fs.copyFile(
            options.source,
            options.destination
        );
    } catch (err) {
        return {
            success: false,
            error: err.message,
        };
    }

    return { success: true };
}
```

### Обработка вывода

По умолчанию `copyFile()` ничего не выводит на стандартный вывод процесса или в ошибку. Если возникает ошибка, может быть трудно понять, что именно пытался сделать билдер, когда возникла проблема.

Добавьте дополнительный контекст, записывая в журнал дополнительную информацию с помощью API `Logger`.

Это также позволяет выполнять сам конструктор в отдельном процессе, даже если стандартный вывод и ошибки отключены (как в [Electron app](https://electronjs.org)).

Вы можете получить экземпляр `Logger` из контекста.

```ts
import {
    BuilderContext,
    BuilderOutput,
    createBuilder,
} from '@angular-devkit/architect';
import { JsonObject } from '@angular-devkit/core';
import { promises as fs } from 'fs';

interface Options extends JsonObject {
    source: string;
    destination: string;
}

export default createBuilder(copyFileBuilder);

async function copyFileBuilder(
    options: Options,
    context: BuilderContext
): Promise<BuilderOutput> {
    try {
        await fs.copyFile(
            options.source,
            options.destination
        );
    } catch (err) {
        context.logger.error('Failed to copy file.');
        return {
            success: false,
            error: err.message,
        };
    }

    return { success: true };
}
```

### Отчеты о ходе выполнения и состоянии

API CLI Builder включает в себя средства отчетов о ходе выполнения и состоянии, которые могут дать подсказки для определенных функций и интерфейсов.

Чтобы сообщить о ходе выполнения, используйте метод `context.reportProgress()`, который принимает в качестве аргументов текущее значение, (необязательно) итог и строку состояния. Total может быть любым числом; например, если вы знаете, сколько файлов вам нужно обработать, total может быть числом файлов, а current должно быть числом обработанных на данный момент.

Строка состояния не изменяется, если вы не передадите новое значение строки.

Вы можете посмотреть [пример](https://github.com/angular/angular-cli/blob/ba21c855c0c8b778005df01d4851b5a2176edc6f/packages/angular_devkit/build_angular/src/tslint/index.ts#L107) того, как построитель `tslint` сообщает о ходе работы.

В нашем примере операция копирования либо завершается, либо все еще выполняется, поэтому отчет о ходе выполнения не нужен, но вы можете сообщить о статусе, чтобы родительский билдер, вызвавший наш билдер, знал, что происходит. Используйте метод `context.reportStatus()` для создания строки состояния любой длины.

!!!note ""

    Нет гарантии, что длинная строка будет показана полностью; она может быть обрезана в соответствии с пользовательским интерфейсом, который ее отображает.

Передайте пустую строку, чтобы удалить статус.

```ts
import {
    BuilderContext,
    BuilderOutput,
    createBuilder,
} from '@angular-devkit/architect';
import { JsonObject } from '@angular-devkit/core';
import { promises as fs } from 'fs';

interface Options extends JsonObject {
    source: string;
    destination: string;
}

export default createBuilder(copyFileBuilder);

async function copyFileBuilder(
    options: Options,
    context: BuilderContext
): Promise<BuilderOutput> {
    context.reportStatus(
        `Copying ${options.source} to ${options.destination}.`
    );
    try {
        await fs.copyFile(
            options.source,
            options.destination
        );
    } catch (err) {
        context.logger.error('Failed to copy file.');
        return {
            success: false,
            error: err.message,
        };
    }

    context.reportStatus('Done.');
    return { success: true };
}
```

## Ввод конструктора

Вы можете вызвать конструктор косвенно через команду CLI или напрямую с помощью команды Angular CLI `ng run`. В любом случае, вы должны предоставить необходимые входные данные, но можете позволить другим входным данным принимать значения по умолчанию, которые предварительно настроены для конкретной [_цели_](glossary.md#target), предоставить предопределенную, именованную конфигурацию переопределения, а также предоставить дополнительные значения опций переопределения в командной строке.

### Валидация входов

Вы определяете входные данные конструктора в схеме JSON, связанной с этим конструктором. Инструмент Architect собирает разрешенные входные значения в объект `options` и проверяет их типы по схеме, прежде чем передать их в функцию builder.

(Библиотека Schematics делает аналогичную проверку пользовательского ввода.)

Для нашего примера конструктора, вы ожидаете, что значение `options` будет `JsonObject` с двумя ключами: `source` и `destination`, каждый из которых является строкой.

Вы можете предоставить следующую схему для проверки типов этих значений.

```json
{
    "$schema": "http://json-schema.org/schema",
    "type": "object",
    "properties": {
        "source": {
            "type": "string"
        },
        "destination": {
            "type": "string"
        }
    }
}
```

!!!note ""

    Это очень простой пример, но использование схемы для валидации может быть очень мощным. Более подробную информацию можно найти на сайте [JSON schemas website](http://json-schema.org).

Чтобы связать реализацию нашего конструктора с его схемой и именем, необходимо создать файл _builder definition_, на который можно указать в `package.json`.

Создайте файл с именем `builders.json`, который будет выглядеть следующим образом:

```json
{
    "builders": {
        "copy": {
            "implementation": "./dist/my-builder.js",
            "schema": "./src/schema.json",
            "description": "Copies a file."
        }
    }
}
```

В файл `package.json` добавьте ключ `builders`, который укажет инструменту Architect, где найти наш файл определения строителя.

```json
{
    "name": "@example/copy-file",
    "version": "1.0.0",
    "description": "Builder for copying files",
    "builders": "builders.json",
    "dependencies": {
        "@angular-devkit/architect": "~0.1200.0",
        "@angular-devkit/core": "^12.0.0"
    }
}
```

Официальное имя нашего конструктора теперь `@example/copy-file:copy`. Первая часть этого имени - это имя пакета (определяется с помощью разрешения узлов), а вторая часть - это имя билдера (определяется с помощью файла `builders.json`).

Использование одной из наших `опций` очень просто. Вы делали это в предыдущем разделе, когда обращались к `options.source` и `options.destination`.

```ts
context.reportStatus(
    `Copying ${options.source} to ${options.destination}.`
);
try {
    await fs.copyFile(options.source, options.destination);
} catch (err) {
    context.logger.error('Failed to copy file.');
    return {
        success: false,
        error: err.message,
    };
}

context.reportStatus('Done.');
return { success: true };
```

### Конфигурация цели

Строитель должен иметь определенную цель, которая связывает его с определенной входной конфигурацией и [проектом](glossary.md#project).

Цели определяются в файле `angular.json` [CLI configuration file](workspace-config.md). Цель определяет конструктор, который будет использоваться, его конфигурацию опций по умолчанию и названные альтернативные конфигурации.

Инструмент Architect использует определение цели для определения входных опций для данного запуска.

В файле `angular.json` есть раздел для каждого проекта, и в разделе "architect" каждого проекта настраиваются цели для конструкторов, используемых командами CLI, такими как 'build', 'test' и 'lint'. По умолчанию, например, команда `build` запускает конструктор `@angular-devkit/build-angular:browser` для выполнения задачи сборки и передает значения опций по умолчанию, указанные для цели `build` в файле `angular.json`.

```json
{
    "myApp": {
        // …
        "architect": {
            "build": {
                "builder": "@angular-devkit/build-angular:browser",
                "options": {
                    "outputPath": "dist/myApp",
                    "index": "src/index.html"
                    // …
                },
                "configurations": {
                    "production": {
                        "fileReplacements": [
                            {
                                "replace": "src/environments/environment.ts",
                                "with": "src/environments/environment.prod.ts"
                            }
                        ],
                        "optimization": true,
                        "outputHashing": "all"
                        // …
                    }
                }
            }
            // …
        }
    }
}
```

Команда передает сборщику набор опций по умолчанию, указанных в разделе "options". Если вы передадите флаг `--configuration=production`, он использует значения переопределения, указанные в альтернативной конфигурации `production`.
Укажите дополнительные переопределения опций отдельно в командной строке.

Вы также можете добавить больше альтернативных конфигураций к цели `build`, чтобы определить другие окружения, такие как `stage` или `qa`.

#### Целевые строки

Общая команда CLI `ng run` принимает в качестве первого аргумента целевую строку следующего вида.

```shell
project:target[:configuration]
```

|               | Детали                                                                                                          |
| :------------ | :-------------------------------------------------------------------------------------------------------------- |
| project       | Имя проекта Angular CLI, с которым связана цель.                                                                |
| target        | Именованная конфигурация построителя из секции `architect` файла `angular.json`.                                |
| configuration | (optional) Имя конкретного переопределения конфигурации для данной цели, как определено в файле `angular.json`. |

Если ваш билдер вызывает другой билдер, ему может потребоваться прочитать переданную целевую строку. Разберите эту строку на объекты с помощью функции `targetFromTargetString()` из `@angular-devkit/architect`.

## Планирование и запуск

Architect запускает билдеры асинхронно. Чтобы вызвать конструктор, вы планируете задачу, которая будет запущена после завершения разрешения всех конфигураций.

Функция построителя не выполняется, пока планировщик не вернет объект управления `BuilderRun`. CLI обычно планирует задачи, вызывая функцию `context.scheduleTarget()`, а затем разрешает входные параметры, используя определение цели в файле `angular.json`.

Architect определяет входные параметры для заданной цели, беря объект опций по умолчанию, затем перезаписывая значения из используемой конфигурации\(если таковая имеется\), затем еще раз перезаписывая значения из объекта overrides, переданного в `context.scheduleTarget()`. Для Angular CLI объект overrides строится из аргументов командной строки.

Architect проверяет полученные значения опций на соответствие схеме построителя. Если входные данные действительны, Architect создает контекст и выполняет построитель.

Дополнительные сведения см. в разделе [Конфигурация рабочего пространства](workspace-config.md).

!!!note ""

    Вы также можете вызвать построитель непосредственно из другого построителя или теста, вызвав `context.scheduleBuilder()`. Вы передаете объект `options` непосредственно в этот метод, и значения опций проверяются на соответствие схеме построителя без дополнительной настройки.

    Только метод `context.scheduleTarget()` разрешает конфигурацию и переопределяет ее через файл `angular.json`.

### Конфигурация архитектора по умолчанию

Давайте создадим простой файл `angular.json`, который вводит целевые конфигурации в контекст.

Вы можете опубликовать конструктор на npm (см. [Публикация вашей библиотеки](creating-libraries.md#publishing-your-library)), и установить его с помощью следующей команды:

```shell
npm install @example/copy-file
```

Если вы создадите новый проект с помощью `ng new builder-test`, сгенерированный файл `angular.json` будет выглядеть примерно так, только с конфигурациями билдера по умолчанию.

```json
{
    // …
    "projects": {
        // …
        "builder-test": {
            // …
            "architect": {
                // …
                "build": {
                    "builder": "@angular-devkit/build-angular:browser",
                    "options": {
                        // … more options…
                        "outputPath": "dist/builder-test",
                        "index": "src/index.html",
                        "main": "src/main.ts",
                        "polyfills": "src/polyfills.ts",
                        "tsConfig": "src/tsconfig.app.json"
                    },
                    "configurations": {
                        "production": {
                            // … more options…
                            "optimization": true,
                            "aot": true,
                            "buildOptimizer": true
                        }
                    }
                }
            }
        }
    }
    // …
}
```

### Добавление цели

Добавьте новую цель, которая будет запускать наш конструктор для копирования файла. Эта цель указывает конструктору скопировать файл `package.json`.

Необходимо обновить файл `angular.json`, чтобы добавить цель для этого билдера в раздел "architect" нашего нового проекта.

-   Мы добавим новую целевую секцию в объект "architect" нашего проекта

-   Цель с именем "copy-package" использует наш конструктор, который вы опубликовали в `@example/copy-file`.

    (См. [Публикация вашей библиотеки](creating-libraries.md#publishing-your-library).)

-   Объект options предоставляет значения по умолчанию для двух входов, которые вы определили; `source`, который является существующим файлом, который вы копируете, и `destination`, путь, куда вы хотите скопировать.

-   Ключ `configurations` является необязательным, мы его пока опустим.

```json
{
    "projects": {
        "builder-test": {
            "architect": {
                "copy-package": {
                    "builder": "@example/copy-file:copy",
                    "options": {
                        "source": "package.json",
                        "destination": "package-copy.json"
                    }
                },
                "build": {
                    "builder": "@angular-devkit/build-angular:browser",
                    "options": {
                        "outputPath": "dist/builder-test",
                        "index": "src/index.html",
                        "main": "src/main.ts",
                        "polyfills": "src/polyfills.ts",
                        "tsConfig": "src/tsconfig.app.json"
                    },
                    "configurations": {
                        "production": {
                            "fileReplacements": [
                                {
                                    "replace": "src/environments/environment.ts",
                                    "with": "src/environments/environment.prod.ts"
                                }
                            ],
                            "optimization": true,
                            "aot": true,
                            "buildOptimizer": true
                        }
                    }
                }
            }
        }
    }
}
```

### Запуск конструктора

Чтобы запустить наш конструктор с конфигурацией по умолчанию новой цели, используйте следующую команду CLI.

```shell
ng run builder-test:copy-package
```

Это копирует файл `package.json` в файл `package-copy.json`.

Используйте аргументы командной строки для отмены настроенных значений по умолчанию. Например, для запуска с другим значением `destination` используйте следующую команду CLI.

```shell
ng run builder-test:copy-package --destination=package-other.json
```

Это копирует файл в `package-other.json` вместо `package-copy.json`. Поскольку вы не переопределили параметр _source_, он будет скопирован из файла `package.json` (значение по умолчанию, предоставленное для цели).

## Тестирование билдера

Используйте интеграционное тестирование для вашего конструктора, чтобы вы могли использовать планировщик Architect для создания контекста, как в этом [примере](https://github.com/mgechev/cli-builders-demo).

-   В каталоге исходных текстов построителя вы создали новый тестовый файл `my-builder.spec.ts`.

    Код создает новые экземпляры `JsonSchemaRegistry` (для валидации схемы), `TestingArchitectHost` (реализация в памяти `ArchitectHost`), и `Architect`.

-   Мы добавили файл `builders.json` рядом с файлом `package.json` сборщика и изменили файл пакета, чтобы он указывал на него.

Вот пример теста, который запускает конструктор копирования файлов. Тест использует конструктор для копирования файла `package.json` и проверяет, что содержимое скопированного файла совпадает с исходным.

```ts
import { Architect } from '@angular-devkit/architect';
import { TestingArchitectHost } from '@angular-devkit/architect/testing';
import { schema } from '@angular-devkit/core';
import { promises as fs } from 'fs';

describe('Copy File Builder', () => {
    let architect: Architect;
    let architectHost: TestingArchitectHost;

    beforeEach(async () => {
        const registry = new schema.CoreSchemaRegistry();
        registry.addPostTransform(
            schema.transforms.addUndefinedDefaults
        );

        // TestingArchitectHost() takes workspace and current directories.
        // Since we don't use those, both are the same in this case.
        architectHost = new TestingArchitectHost(
            __dirname,
            __dirname
        );
        architect = new Architect(architectHost, registry);

        // This will either take a Node package name, or a path to the directory
        // for the package.json file.
        await architectHost.addBuilderFromPackage('..');
    });

    it('can copy files', async () => {
        // A "run" can have multiple outputs, and contains progress information.
        const run = await architect.scheduleBuilder(
            '@example/copy-file:copy',
            {
                source: 'package.json',
                destination: 'package-copy.json',
            }
        );

        // The "result" member (of type BuilderOutput) is the next output.
        const output = await run.result;

        // Stop the builder from running. This stops Architect from keeping
        // the builder-associated states in memory, since builders keep waiting
        // to be scheduled.
        await run.stop();

        // Expect that the copied file is the same as its source.
        const sourceContent = await fs.readFile(
            'package.json',
            'utf8'
        );
        const destinationContent = await fs.readFile(
            'package-copy.json',
            'utf8'
        );
        expect(destinationContent).toBe(sourceContent);
    });
});
```

!!!note ""

    При выполнении этого теста в вашем репозитории вам понадобится пакет [`ts-node`](https://github.com/TypeStrong/ts-node). Вы можете избежать этого, переименовав `my-builder.spec.ts` в `my-builder.spec.js`.

### Режим наблюдения

Architect ожидает, что сборщики будут запущены один раз (по умолчанию) и возвращены. Такое поведение не совсем совместимо со сборщиком, который следит за изменениями (как Webpack, например).

Architect может поддерживать режим наблюдения, но есть некоторые моменты, на которые следует обратить внимание.

-   Чтобы использовать режим наблюдения, функция-обработчик билдера должна возвращать Observable.

    Architect подписывается на Observable до его завершения и может повторно использовать его, если построитель будет запланирован снова с теми же аргументами.

-   После каждого выполнения построитель всегда должен выдавать объект `BuilderOutput`.

    После выполнения он может перейти в режим наблюдения, чтобы быть вызванным внешним событием.

    Если событие вызывает его перезапуск, построитель должен выполнить функцию `context.reportRunning()`, чтобы сообщить Architect, что он снова запущен.

    Это не позволит Architect остановить построитель, если запланирован другой запуск.

Когда ваш билдер вызывает `BuilderRun.stop()` для выхода из режима наблюдения, Architect отписывается от Observable билдера и вызывает логику разрушения билдера для очистки. (Это поведение также позволяет останавливать и очищать давно запущенные билды.)

В целом, если ваш билдер следит за внешним событием, вам следует разделить выполнение на три фазы.

| Phases     | Details                                                                                                                                                                                                                                                    |
| :--------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Выполнение | Например, webpack компилируется. Она заканчивается, когда webpack завершает работу и ваш билдер выдает объект `BuilderOutput`.                                                                                                                             |
| Наблюдение | Между двумя запусками наблюдайте за внешним потоком событий. Например, webpack следит за изменениями в файловой системе. Это заканчивается, когда webpack перезапускает сборку, и вызывается `context.reportRunning()`. Это возвращает нас к шагу 1.       |
| Завершение | Либо задача полностью выполнена (например, webpack должен был запуститься несколько раз), либо выполнение сборки было остановлено (с помощью `BuilderRun.stop()`). Ваша логика разрыва выполняется, и Architect отписывается от Observable вашего билдера. |

## Резюме

API CLI Builder предоставляет новый способ изменения поведения Angular CLI с помощью билдеров для выполнения пользовательской логики.

-   Конструкторы могут быть синхронными или асинхронными, выполняться однократно или следить за внешними событиями, и могут планировать другие конструкторы или цели.
-   Builders имеют параметры по умолчанию, указанные в конфигурационном файле `angular.json`, которые могут быть перезаписаны альтернативной конфигурацией для цели, а также флагами командной строки.

-   Мы рекомендуем использовать интеграционные тесты для тестирования сборщиков Architect.

    Используйте модульные тесты для проверки логики, которую выполняет билдер.

-   Если ваш построитель возвращает наблюдаемую величину, он должен очистить логику разрушения этой наблюдаемой величины.

<!-- links -->

<!-- external links -->

<!-- end links -->
