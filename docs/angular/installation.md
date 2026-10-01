---
description: "Быстрый старт с Angular: песочница в браузере или локальный проект в терминале."
---

# Установка {: #installation}

:date: 30.09.2026

Быстрый старт с Angular: песочница в браузере или локальный проект в терминале.

## Попробовать онлайн {: #play-online}

Если нужно просто попробовать Angular в браузере, без создания проекта, подойдёт онлайн-песочница:

**Песочница**

Самый быстрый способ поработать с приложением Angular. Настройка не нужна.

[Открыть песочницу](https://angular.dev/playground)

## Локальный новый проект {: #set-up-a-new-project-locally}

Для нового проекта обычно создают локальный каталог, чтобы подключить инструменты вроде Git.

### Что понадобится {: #prerequisites}

-   **Node.js** — [v22.22.3 или новее](https://angular.dev/reference/versions)
-   **Текстовый редактор** — рекомендуем [Visual Studio Code](https://code.visualstudio.com/)
-   **Терминал** — нужен для команд [Angular CLI](tools/cli/overview.md)
-   **Инструмент разработки** — чтобы ускорить работу, рекомендуем [Angular Language Service](https://angular.dev/tools/language-service)

### Инструкция {: #instructions}

Ниже — как поднять локальный проект Angular.

#### Установка Angular CLI {: #install-angular-cli}

Откройте терминал (в [Visual Studio Code](https://code.visualstudio.com/) это [встроенный терминал](https://code.visualstudio.com/docs/editor/integrated-terminal)) и выполните команду:

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

Если команда не выполняется в Windows или Unix, подробности есть в [документации CLI](tools/cli/setup-local.md#install-the-angular-cli).

#### Новый проект {: #create-a-new-project}

В терминале выполните команду CLI [`ng new`](https://angular.dev/cli/new) и укажите имя проекта. В примерах ниже используется `my-first-angular-app`.

```shell
ng new <project-name>
```

CLI предложит варианты настройки. Стрелками и Enter выбирают нужные пункты.

Если предпочтений нет, нажимайте Enter: подставятся значения по умолчанию, и установка продолжится.

Когда параметры выбраны и CLI закончит установку, появится сообщение:

```text
✔ Packages installed successfully.
    Successfully initialized git.
```

После этого проект можно запускать локально.

#### Локальный запуск {: #running-your-new-project-locally}

В терминале перейдите в новый проект Angular.

```shell
cd my-first-angular-app
```

К этому моменту зависимости уже установлены (это видно по каталогу `node_modules` в проекте). Запустите проект командой:

```shell
npm start
```

Если всё прошло успешно, в терминале появится похожее подтверждение:

```text
Watch mode enabled. Watching for file changes...
NOTE: Raw file sizes do not reflect development server per-request transformations.
  ➜  Local:   http://localhost:4200/
  ➜  press h + enter to show help
```

Откройте адрес из строки `Local` (например, `http://localhost:4200`) — там будет приложение. Удачной разработки! 🎉

### Разработка с ИИ {: #using-ai-for-development}

Чтобы начать сборку в привычной IDE с ИИ, [посмотрите правила промптов и рекомендации Angular](https://angular.dev/ai/develop-with-ai).

## Следующие шаги {: #next-steps}

Проект создан. Дальше — [руководство «Основы»](essentials/overview.md) или любая тема из подробных руководств.


---

Источник: [https://angular.dev/installation](https://angular.dev/installation)
