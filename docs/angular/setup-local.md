# Настройка локального окружения и рабочего пространства

Это руководство объясняет, как настроить среду для разработки Angular с помощью [инструмента Angular CLI] (cli "Справочник команд CLI"). Оно включает информацию о предварительных требованиях, установке CLI, создании начального рабочего пространства и стартового приложения, а также о локальном запуске этого приложения для проверки настроек.

<div class="callout is-helpful">

<header>Try Angular without local setup</header>

Если вы новичок в Angular, вам лучше начать с [Try it now!](start), который знакомит с основами Angular в контексте готового базового приложения интернет-магазина, которое вы можете изучить и изменить. Этот отдельный учебник использует преимущества интерактивной среды [StackBlitz](https://stackblitz.com) для онлайн-разработки.
Вам не нужно настраивать локальную среду, пока вы не будете готовы.

</div>

<a id="devenv"></a> <a id="prerequisites"></a>

## Prerequisites

To use the Angular framework, you should be familiar with the following:

-   [JavaScript](https://developer.mozilla.org/docs/Web/JavaScript/A_re-introduction_to_JavaScript)

-   [HTML](https://developer.mozilla.org/docs/Learn/HTML/Introduction_to_HTML)

-   [CSS](https://developer.mozilla.org/docs/Learn/CSS/First_steps)

Knowledge of [TypeScript](https://www.typescriptlang.org) is helpful, but not required.

To install Angular on your local system, you need the following:

| Requirements | Details | |:--- |:--- |

| Node.js <a id="nodejs"></a> | Angular requires an [active LTS or maintenance LTS](https://nodejs.org/about/releases) version of Node.js. <div class="alert is-helpful">For information see the [version compatibility](guide/versions) guide.</div> For more information on installing Node.js, see [nodejs.org](https://nodejs.org 'Nodejs.org'). If you are unsure what version of Node.js runs on your system, run `node -v` in a terminal window. |

| npm package manager <a id="npm"></a> | Angular, the Angular CLI, and Angular applications depend on [npm packages](https://docs.npmjs.com/getting-started/what-is-npm) for many features and functions. To download and install npm packages, you need an npm package manager. В этом руководстве используется интерфейс командной строки [npm client](https://docs.npmjs.com/cli/install), который по умолчанию установлен с `Node.js`. Чтобы проверить, установлен ли у вас клиент npm, запустите в окне терминала команду `npm -v`. |

<a id="install-cli"></a>

## Установите Angular CLI

Вы можете использовать Angular CLI для создания проектов, генерации кода приложений и библиотек, а также для выполнения различных текущих задач разработки, таких как тестирование, комплектация и развертывание.

Чтобы установить Angular CLI, откройте окно терминала и выполните следующую команду:

<code-example format="shell" language="shell">

npm install -g &commat;angular/cli<aio-angular-dist-tag class="pln"></aio-angular-dist-tag>

</code-example>

<div class="alert is-helpful">   <p>On Windows client computers, the execution of PowerShell scripts is disabled by default. To allow the execution of PowerShell scripts, which is needed for npm global binaries, you must set the following <a href="https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies">execution policy</a>:</p>
  <code-example language="sh">
  Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
  </code-example>
  <p>Carefully read the message displayed after executing the command and follow the instructions. Make sure you understand the implications of setting an execution policy.</p>
</div>

<a id="create-proj"></a>

## Создание рабочего пространства и начального приложения

Вы разрабатываете приложения в контексте [**workspace**](guide/glossary#workspace) Angular.

Чтобы создать новое рабочее пространство и начальное приложение, выполните следующие действия:

1.  Выполните команду CLI `ng new` и укажите имя `my-app`, как показано здесь:

    <code-example format="shell" language="shell">

    ng new my-app

    </code-example

1.  Команда `ng new` запрашивает информацию о функциях, которые необходимо включить в первоначальное приложение.

    Примите значения по умолчанию, нажав клавишу Enter или Return.

Angular CLI устанавливает необходимые пакеты Angular npm и другие зависимости. Это может занять несколько минут.

CLI создает новое рабочее пространство и простое приложение Welcome, готовое к запуску.

<a id="serve"></a>

## Запуск приложения

В состав Angular CLI входит сервер, с помощью которого вы можете создавать и обслуживать свое приложение локально.

1.  Перейдите в папку рабочего пространства, например `my-app`.

1.  Выполните следующую команду:

    <code-example format="shell" language="shell">.

    cd my-app

    ng serve --open

    </code-example>.

Команда `ng serve` запускает сервер, следит за вашими файлами и перестраивает приложение, когда вы вносите изменения в эти файлы.

Опция `--open` \(или просто `-o`\) автоматически открывает ваш браузер на `http://localhost:4200/`.

Если установка и настройка прошли успешно, вы должны увидеть страницу, похожую на следующую.

<div class="lightbox">

<img alt="Welcome to my-app!" src="generated/images/guide/setup-local/app-works.png">

</div>

## Следующие шаги

-   Для более подробного ознакомления с фундаментальными концепциями и терминологией архитектуры и принципов проектирования одностраничных приложений Angular прочтите раздел [Angular Concepts](guide/architecture).

-   Проработайте [Tour of Heroes Tutorial](tutorial/tour-of-heroes), полное практическое упражнение, которое познакомит вас с процессом разработки приложений с использованием Angular CLI и проведет по важным подсистемам.

-   Чтобы узнать больше об использовании Angular CLI, смотрите [Обзор CLI](cli 'Обзор CLI').

    Помимо создания начального рабочего пространства и каркаса приложения, используйте CLI для создания кода Angular, такого как компоненты и сервисы.

    CLI поддерживает полный цикл разработки, включая сборку, тестирование, комплектацию и развертывание.

-   Для получения дополнительной информации о файлах Angular, создаваемых `ng new`, смотрите [Структура файлов рабочего пространства и проекта] (guide/file-structure).

<!-- links -->

<!-- external links -->

<!-- end links -->

@ просмотрено 2022-02-28
