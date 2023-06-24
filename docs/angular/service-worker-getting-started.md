# Начало работы с рабочими службами

В этом документе объясняется, как включить поддержку рабочих служб Angular в проектах, созданных с помощью [Angular CLI](cli). Затем на примере демонстрируется работа сервисного работника в действии, демонстрируется загрузка и базовое кэширование.

## Предварительные условия

Базовое понимание информации в [Introduction to Angular service workers](guide/service-worker-intro).

## Добавление сервисного работника в ваш проект

Чтобы установить Angular service worker в свой проект, используйте команду CLI `ng add @angular/pwa`. Она позаботится о настройке вашего приложения на использование работников сервисов, добавив пакет `@angular/service-worker` вместе с

с установкой необходимых файлов поддержки.

<code-example format="shell" language="shell">

ng add @angular/pwa --project &lt;project-name&gt;

</code-example>

Предыдущая команда выполняет следующие действия:

1.  Добавляет пакет `@angular/service-worker` в ваш проект.

1.  Включает поддержку сборки service worker в CLI.

1.  Импортирует и регистрирует сервисный работник в модуле приложения.

1.  Обновляет файл `index.html`:

    -   Включает ссылку для добавления файла `manifest.webmanifest`.

    -   Добавляет мета-тег для `theme-color`.

1.  Устанавливает файлы иконок для поддержки установленного Progressive Web App \(PWA\).

1.  Создает файл конфигурации рабочего сервиса под названием [`ngsw-config.json`](guide/service-worker-config), который определяет поведение кэширования и другие настройки.

Теперь соберите проект:

<code-example format="shell" language="shell">

строительство

</code-example>

Теперь проект CLI настроен на использование Angular service worker.

## Сервисный работник в действии: экскурсия

Этот раздел демонстрирует работу сервисного работника в действии, используя пример приложения.

### Начальная загрузка

Когда сервер запущен, направьте браузер на `http://localhost:8080`. Ваше приложение должно загрузиться нормально.

<div class="alert is-helpful">

**TIP**: <br /> When testing Angular service workers, it's a good idea to use an incognito or private window in your browser to ensure the service worker doesn't end up reading from a previous leftover state, which can cause unexpected behavior.

</div>

<div class="alert is-helpful">

**NOTE**: <br /> If you are not using HTTPS, the service worker will only be registered when accessing the application on `localhost`.

</div>

### Моделирование сетевой проблемы

Чтобы смоделировать сетевую проблему, отключите сетевое взаимодействие для вашего приложения.

В Chrome:

1.  Выберите **Инструменты** &gt; **Инструменты разработчика** \(в меню Chrome, расположенном в правом верхнем углу\).

1.  Перейдите на вкладку **Сеть**.

1.  Выберите **Offline** в выпадающем меню **Throttling**.

<div class="lightbox">

<img alt="The offline option in the Network tab is selected" src="generated/images/guide/service-worker/offline-option.png">

</div>

Теперь приложение не имеет доступа к сетевому взаимодействию.

Для приложений, не использующих Angular service worker, при обновлении теперь отображается страница Chrome "Internet disconnected" с надписью "There is no Internet connection".

С добавлением Angular service worker поведение приложения меняется. При обновлении страница загружается нормально.

Посмотрите на вкладку "Сеть", чтобы убедиться, что работник службы активен.

<div class="lightbox">

<img alt="Requests are marked as from ServiceWorker" src="generated/images/guide/service-worker/sw-active.png">

</div>

<div class="alert is-helpful">

**NOTE**: <br /> Under the "Size" column, the requests state is `(ServiceWorker)`.
This means that the resources are not being loaded from the network.

Instead, they are being loaded from the service worker's cache.

</div>

### Что кэшируется?

Обратите внимание, что все файлы, необходимые браузеру для рендеринга этого приложения, кэшируются. Шаблонная конфигурация `ngsw-config.json` настроена на кэширование специфических ресурсов, используемых CLI:

-   `index.html`

-   `favicon.ico`.

-   Build artifacts\(JS и CSS bundles\).

-   Все, что находится под `assets`.

-   Изображения и шрифты непосредственно под настроенным `outputPath` \(по умолчанию `./dist/<project-name>/`\) или `resourcesOutputPath`.

    Более подробную информацию об этих опциях смотрите в [`ng build`](cli/build).

<div class="alert is-important">

Обратите внимание на два ключевых момента:

1.  Сгенерированный `ngsw-config.json` включает ограниченный список кэшируемых шрифтов и расширений изображений.

    В некоторых случаях вам может понадобиться изменить шаблон glob в соответствии с вашими потребностями.

1.  Если пути `resourcesOutputPath` или `assets` изменены после генерации конфигурационного файла, вам необходимо вручную изменить пути в `ngsw-config.json`.

</div>

### Внесение изменений в ваше приложение

Теперь, когда вы увидели, как работники служб кэшируют ваше приложение, следующим шагом будет понимание того, как работают обновления. Внесите изменения в приложение и посмотрите, как работник службы установит обновление:

1.  Если вы тестируете в окне инкогнито, откройте вторую пустую вкладку.

    Это позволит сохранить состояние инкогнито и кэша во время тестирования.

1.  Закройте вкладку приложения, но не окно.

    Это также приведет к закрытию инструментов разработчика.

1.  Выключите `http-сервер`.

1.  Откройте `src/app/app.component.html для редактирования.

1.  Измените текст `Welcome to {{title}}!` на `Bienvenue à {{title}}!`.

1.  Соберите и запустите сервер снова:

    <code-example format="shell" language="shell">.

    ng build

    http-server -p 8080 -c-1 dist/&lt;project-name&gt;

    </code-example>

### Обновление приложения в браузере

Теперь посмотрим, как браузер и сервисный работник обрабатывают обновленное приложение.

1.  Open [http://localhost:8080](http://localhost:8080) again in the same window.
    What happens?

    <div class="lightbox">

    <img alt="It still says Welcome to Service Workers!" src="generated/images/guide/service-worker/welcome-msg-en.png">

    </div>

    What went wrong?

    Nothing, actually.

    The Angular service worker is doing its job and serving the version of the application that it has **installed**, even though there is an update available.

    In the interest of speed, the service worker doesn't wait to check for updates before it serves the application that it has cached.

    Look at the `http-server` logs to see the service worker requesting `/ngsw.json`.

    This is how the service worker checks for updates.

1.  Refresh the page.

    <div class="lightbox">

    <img alt="The text has changed to say Bienvenue à app!" src="generated/images/guide/service-worker/welcome-msg-fr.png">

    </div>

    The service worker installed the updated version of your application _in the background_, and the next time the page is loaded or reloaded, the service worker switches to the latest version.

## More on Angular service workers

Вам также может быть интересно следующее:

-   [App Shell](guide/app-shell)

-   [Общение с рабочими службами](guide/service-worker-communications)

<!-- links -->

<!-- external links -->

<!-- end links -->

:date: 28.02.2022
