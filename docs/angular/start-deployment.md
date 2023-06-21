# Развертывание приложения

Развертывание приложения - это процесс компиляции, или сборки, вашего кода и размещения JavaScript, CSS и HTML на веб-сервере.

Этот раздел основывается на предыдущих шагах в руководстве [Начало работы](начало 'Попробуйте: базовое приложение') и показывает, как развернуть ваше приложение.

## Предварительные условия

Лучшей практикой является локальный запуск проекта перед его развертыванием. Чтобы запустить проект локально, на вашем компьютере должно быть установлено следующее:

-   [Node.js](https://nodejs.org/en).

-   [Angular CLI](https://cli.angular.io).

    В терминале установите Angular CLI глобально, используя:

    <code-example format="shell" language="shell">.

    npm install -g &commat;angular/cli

    </code-example>.

    С помощью Angular CLI вы можете использовать команду `ng` для создания новых рабочих пространств, новых проектов, обслуживания вашего приложения во время разработки или создания сборок для совместного использования или распространения.

## Запуск приложения локально

1.  Download the source code from your StackBlitz project by clicking the `Download Project` icon in the left menu, across from `Project`, to download your project as a zip archive.

    <div class="lightbox">

    <img alt="Download the stackblitz project" src="generated/images/guide/start/download-project.png">

    </div>

1.  Unzip the archive and change directory to the newly created project. For example:

    <code-example format="shell" language="shell">

    cd angular-ynqttp

    </code-example>

1.  To download and install npm packages, use the following npm CLI command:

    <code-example format="shell" language="shell">

    npm install

    </code-example>

1.  Use the following CLI command to run your application locally:

    <code-example format="shell" language="shell">

    ng serve

    </code-example>

1.  To see your application in the browser, go to http://localhost:4200/.

    If the default port 4200 is not available, you can specify another port with the port flag as in the following example:

    <code-example format="shell" language="shell">.

    ng serve --port 4201

    </code-example>.

    Во время обслуживания приложения вы можете редактировать свой код и видеть, как изменения автоматически обновляются в браузере.

    Чтобы остановить команду `ng serve`, нажмите `Ctrl`+`c`.

<a id="building"></a>

## Building and hosting your application

1.  To build your application for production, use the `build` command. By default, this command uses the `production` build configuration.

    <code-example format="shell" language="shell">

    ng build

    </code-example>

    This command creates a `dist` folder in the application root directory with all the files that a hosting service needs for serving your application.

    <div class="alert is-helpful">

    If the above `ng build` command throws an error about missing packages, append the missing dependencies in your local project's `package.json` file to match the one in the downloaded StackBlitz project.

    </div>

1.  Copy the contents of the `dist/my-project-name` folder to your web server.

    Because these files are static, you can host them on any web server capable of serving files; such as `Node.js`, Java, .NET, or any backend such as [Firebase](https://firebase.google.com/docs/hosting), [Google Cloud](https://cloud.google.com/solutions/web-hosting), or [App Engine](https://cloud.google.com/appengine/docs/standard/python/getting-started/hosting-a-static-website).

    For more information, see [Building & Serving](guide/build 'Building and Serving Angular Apps') and [Deployment](guide/deployment 'Deployment guide').

## What's next

В этом руководстве вы заложили основу для изучения мира Angular в таких областях, как мобильная разработка, разработка UX/UI и рендеринг на стороне сервера. Вы можете углубиться, изучая больше возможностей Angular, взаимодействуя с активным сообществом и исследуя мощную экосистему.

### Узнать больше об Angular

Более подробное руководство, которое поможет вам создать приложение на локальном уровне и изучить многие из наиболее популярных функций Angular, смотрите в [Tour of Heroes](tutorial).

Чтобы изучить основные концепции Angular, обратитесь к руководствам в разделе "Понимание Angular", таким как [Обзор компонентов Angular] (guide/component-overview) или [Синтаксис шаблонов] (guide/template-syntax).

### Присоединиться к сообществу

[Напишите в Twitter, что вы прошли этот учебник](https://twitter.com/intent/tweet?url=https://angular.io/start&text=I%20just%20finished%20the%20Angular%20Getting%20Started%20Tutorial 'Angular on Twitter'), расскажите нам, что вы думаете, или отправьте [предложения для будущих выпусков](https://github.com/angular/angular/issues/new/choose 'Angular GitHub repository new issue form').

Следите за новостями в [блоге Angular](https://blog.angular.io/ 'Angular blog').

### Изучение экосистемы Angular

Для поддержки разработки UX/UI смотрите [Angular Material](https://material.angular.io/ 'Angular Material web site').

Сообщество Angular также имеет обширную [сеть сторонних инструментов и библиотек](ресурсы 'Список ресурсов Angular').

:date: 15.09.2021
