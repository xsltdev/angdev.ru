---
description: "Как подготовить окружение для разработки на Angular: установка CLI, рабочее пространство, стартовое приложение и локальный запуск."
---

# Локальное окружение и рабочее пространство {: #setting-up-the-local-environment-and-workspace}

:date: 30.09.2026

Это руководство объясняет, как подготовить окружение для разработки на Angular с помощью [Angular CLI](https://angular.dev/cli 'Справочник команд CLI').
Здесь — установка CLI, первое рабочее пространство со стартовым приложением и локальный запуск, чтобы проверить настройку.

!!! info "Angular без локальной установки"

    Если Angular ещё не знаком, начните с [Попробовать сейчас!](https://angular.dev/tutorials/learn-angular): он знакомит с основами Angular прямо в браузере.
    Этот самостоятельный учебник идёт в интерактивной среде [StackBlitz](https://stackblitz.com).
    Локальное окружение понадобится, только когда будете к нему готовы.

## Прежде чем начать {: #before-you-start}

Для Angular CLI нужно знакомство с:

-   [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
-   [HTML](https://developer.mozilla.org/en-US/docs/Web/HTML)
-   [CSS](https://developer.mozilla.org/en-US/docs/Web/CSS)

Нужен и опыт работы с инструментами командной строки (CLI), и общее представление о командных оболочках.
Знание [TypeScript](https://www.typescriptlang.org) помогает, но не обязательно.

## Зависимости {: #dependencies}

Чтобы поставить Angular CLI локально, нужен [Node.js](https://nodejs.org/).
CLI ставит и запускает инструменты JavaScript вне браузера через Node и связанный с ним менеджер пакетов npm.

[Скачайте и установите Node.js](https://nodejs.org/en/download) — вместе с ним будет CLI `npm`.
Angular нуждается в [активной LTS или maintenance LTS](https://nodejs.org/en/about/previous-releases) версии Node.js.
Подробности — в руководстве [совместимости версий Angular](https://angular.dev/reference/versions).

## Установка Angular CLI {: #install-the-angular-cli}

Чтобы установить Angular CLI, откройте терминал и выполните команду:

=== "npm"

    ```shell
    npm install -g @angular/cli
    ```

=== "pnpm"

    ```shell
    pnpm install -g @angular/cli
    ```

=== "yarn"

    ```shell
    yarn global add @angular/cli
    ```

=== "bun"

    ```shell
    bun install -g @angular/cli
    ```

### Политика выполнения PowerShell {: #powershell-execution-policy}

На клиентских компьютерах Windows выполнение сценариев PowerShell по умолчанию выключено, поэтому команда выше может завершиться ошибкой.
Глобальным исполняемым файлам npm нужно выполнение сценариев PowerShell. Задайте такую <a href="https://docs.microsoft.com/powershell/module/microsoft.powershell.core/about/about_execution_policies" target="_blank">политику выполнения</a>:

```shell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

Внимательно прочитайте сообщение после команды и следуйте ему. Нужно понимать, к чему ведёт смена политики выполнения.

### Права в Unix {: #unix-permissions}

На части Unix-систем глобальные сценарии принадлежат пользователю root, и команда выше может упасть с ошибкой прав.
Запустите её через `sudo`, чтобы выполнить команду от имени root, и введите пароль по запросу:

=== "npm"

    ```shell
    sudo npm install -g @angular/cli
    ```

=== "pnpm"

    ```shell
    sudo pnpm install -g @angular/cli
    ```

=== "yarn"

    ```shell
    sudo yarn global add @angular/cli
    ```

=== "bun"

    ```shell
    sudo bun install -g @angular/cli
    ```

Нужно понимать, к чему ведёт запуск команд от имени root.

## Рабочее пространство и первое приложение {: #create-a-workspace-and-initial-application}

Приложения разрабатывают в **рабочем пространстве** Angular.

Новое рабочее пространство и стартовое приложение создаёт команда CLI `ng new` с именем `my-app`, как ниже. Затем CLI спросит, какие возможности включить:

```shell
ng new my-app
```

Angular CLI ставит нужные пакеты npm Angular и остальные зависимости.
Это занимает несколько минут.

CLI создаёт новое рабочее пространство и небольшое приветственное приложение в каталоге с тем же именем. Оно готово к запуску.
Перейдите в этот каталог: следующие команды будут работать уже с этим рабочим пространством.

```shell
cd my-app
```

## Запуск приложения {: #run-the-application}

В Angular CLI есть сервер разработки: он собирает приложение и отдаёт его локально. Выполните команду:

```shell
ng serve --open
```

Команда `ng serve` запускает сервер, следит за файлами, пересобирает приложение и перезагружает браузер, когда файлы меняются.

Параметр `--open` (или просто `-o`) сам открывает браузер на `http://localhost:4200/`, где видно собранное приложение.

## Файлы рабочего пространства и проекта {: #workspaces-and-project-files}

Команда [`ng new`](https://angular.dev/cli/new) создаёт каталог [рабочего пространства Angular](https://angular.dev/reference/configs/workspace-config) и генерирует в нём новое приложение.
В одном рабочем пространстве может быть несколько приложений и библиотек.
Первое приложение, которое создаёт [`ng new`](https://angular.dev/cli/new), лежит в корне рабочего пространства.
Дополнительное приложение или библиотека в уже существующем пространстве по умолчанию попадает в подкаталог `projects/`.

Только что созданное приложение содержит исходники корневого компонента и шаблона.
У каждого приложения есть каталог `src` с компонентами, данными и ресурсами.

Сгенерированные файлы правят напрямую или через команды CLI.
Команда [`ng generate`](https://angular.dev/cli/generate) добавляет файлы новых компонентов, директив, пайпов, сервисов и другого.
Команды вроде [`ng add`](https://angular.dev/cli/add) и [`ng generate`](https://angular.dev/cli/generate), которые создают приложения и библиотеки или работают с ними, запускают изнутри рабочего пространства. Команду `ng new`, напротив, запускают _вне_ рабочего пространства: она создаёт новое.

## Следующие шаги {: #next-steps}

-   Подробнее о [структуре файлов](https://angular.dev/reference/configs/file-structure) и [конфигурации](https://angular.dev/reference/configs/workspace-config) созданного рабочего пространства.

-   Проверьте новое приложение командой [`ng test`](https://angular.dev/cli/test).

-   Заготовки компонентов, директив и пайпов даёт [`ng generate`](https://angular.dev/cli/generate).

-   Разверните приложение и отдайте его пользователям командой [`ng deploy`](https://angular.dev/cli/deploy).

-   Сквозные тесты приложения настраивают и запускают через [`ng e2e`](https://angular.dev/cli/e2e).


---

Источник: [https://angular.dev/tools/cli/setup-local](https://angular.dev/tools/cli/setup-local)
