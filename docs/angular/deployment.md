# Развертывание

Когда вы готовы развернуть свое приложение Angular на удаленном сервере, у вас есть различные варианты развертывания.

<a id="dev-deploy"></a> <a id="copy-files"></a>

## Простые варианты развертывания

Перед полным развертыванием приложения вы можете протестировать процесс, конфигурацию сборки и поведение развернутого приложения, используя один из этих промежуточных методов.

### Сборка и обслуживание с диска

Во время разработки вы обычно используете команду `ng serve` для сборки, просмотра и обслуживания приложения из локальной памяти, используя [webpack-dev-server](https://webpack.js.org/guides/development/#webpack-dev-server). Однако, когда вы готовы к развертыванию, вы должны использовать команду `ng build` для сборки приложения и развертывания артефактов сборки в другом месте.

И `ng build`, и `ng serve` очищают выходную папку перед сборкой проекта, но только команда `ng build` записывает сгенерированные артефакты сборки в выходную папку.

<div class="alert is-helpful">

По умолчанию папкой вывода является `dist/project-name/`. Для вывода в другую папку измените `outputPath` в файле `angular.json`.

</div>

По мере приближения к завершению процесса разработки, просмотр содержимого папки вывода с локального веб-сервера может дать вам лучшее представление о том, как будет вести себя ваше приложение при развертывании на удаленном сервере. Для получения опыта живой загрузки вам понадобятся два терминала.

-   На первом терминале выполните команду [`ng build`](cli/build) в режиме _watch_ для компиляции приложения в папку `dist`.

      <code-example format="shell" language="shell">

    ng build --watch

    </code-example>.

    Как и команда `ng serve`, эта команда регенерирует выходные файлы при изменении исходных файлов.

-   На втором терминале установите веб-сервер \(например, [lite-server](https://github.com/johnpapa/lite-server)\), и запустите его в папке output.

    Например:

      <code-example format="shell" language="shell">

    lite-server --baseDir="dist/project-name"

    </code-example>.

    Сервер будет автоматически перезагружать ваш браузер при выводе новых файлов.

<div class="alert is-critical">

Этот метод предназначен только для разработки и тестирования и не является поддерживаемым или безопасным способом развертывания приложения.

</div>

### Автоматическое развертывание с помощью CLI

Команда Angular CLI `ng deploy` \(введена в версии 8.3.0\) выполняет `deploy` [CLI builder](guide/cli-builder), связанный с вашим проектом. Ряд сторонних билдеров реализуют возможности развертывания на различных платформах.

Вы можете добавить любой из них в свой проект, выполнив команду `ng add [имя пакета]`.

Когда вы добавите пакет с возможностью развертывания, он автоматически обновит конфигурацию вашего рабочего пространства \(файл `angular.json`\) с секцией `deploy` для выбранного проекта. Затем вы можете использовать команду `ng deploy` для развертывания этого проекта.

Например, следующая команда автоматически развертывает проект на Firebase.

<code-example format="shell" language="shell">

ng add @angular/fire ng deploy

</code-example>

Команда является интерактивной. В этом случае вы должны иметь или создать учетную запись Firebase и пройти аутентификацию с ее помощью.
Команда предлагает вам выбрать проект Firebase для развертывания.

Команда создает ваше приложение и загружает производственные активы в Firebase.

В таблице ниже вы можете найти список пакетов, которые реализуют функциональность развертывания на различных платформах. Команда `deploy` для каждого пакета может требовать различных опций командной строки.

Вы можете узнать больше, перейдя по ссылкам, связанным с названиями пакетов ниже:

| Развертывание на | Пакет | | :---------------------------------------------------------------- | :----------------------------------------------------------------------------------- |.

| [Firebase hosting](https://firebase.google.com/docs/hosting) | [`@angular/fire`](https://npmjs.org/package/@angular/fire)|

| [Vercel](https://vercel.com/solutions/angular) | [`vercel init angular`](https://github.com/vercel/vercel/tree/main/examples/angular)|

| [Netlify](https://www.netlify.com) | [`@netlify-builder/deploy`](https://npmjs.org/package/@netlify-builder/deploy)| |

| [GitHub pages](https://pages.github.com) | [`angular-cli-ghpages`](https://npmjs.org/package/angular-cli-ghpages)|

| [NPM](https://npmjs.com) | [`ngx-deploy-npm`](https://npmjs.org/package/ngx-deploy-npm)| |

| [Amazon Cloud S3](https://aws.amazon.com/s3/?nc2=h_ql_prod_st_s3) | [`@jefiozie/ngx-aws-deploy`](https://www.npmjs.com/package/@jefiozie/ngx-aws-deploy)|

Если вы развертываете на самоуправляемом сервере или для вашей любимой облачной платформы нет конструктора, вы можете либо создать конструктор, который позволит вам использовать команду `ng deploy`, либо прочитать это руководство, чтобы узнать, как вручную развернуть ваше приложение.

### Базовое развертывание на удаленном сервере

Для простейшего развертывания создайте производственную сборку и скопируйте выходной каталог на веб-сервер.

1.  Начните с производственной сборки:

    <code-example format="shell" language="shell">.

    ng build

    </code-example>.

1.  Скопируйте _все_ в выходную папку \(`dist/project-name/` по умолчанию\) в папку на сервере.

1.  Настройте сервер на перенаправление запросов на недостающие файлы на `index.html`.

    Узнайте больше о перенаправлениях на стороне сервера [ниже](#fallback).

Это самое простое развертывание вашего приложения, готовое к производству.

<a id="deploy-to-github"></a>

### Развертывание на GitHub Pages

Чтобы развернуть ваше приложение Angular на [GitHub Pages](https://help.github.com/articles/what-is-github-pages), выполните следующие шаги:

1.  [Create a GitHub repository](https://help.github.com/articles/create-a-repo) for your project.
1.  Configure `git` in your local project by adding a remote that specifies the GitHub repository you created in previous step.
    GitHub provides these commands when you create the repository so that you can copy and paste them at your command prompt.
    The commands should be similar to the following, though GitHub fills in your project-specific settings for you:

    <code-example format="shell" language="shell">

    git remote add origin https://github.com/your-username/your-project-name.git
    git branch -M main
    git push -u origin main

    </code-example>

    When you paste these commands from GitHub, they run automatically.

1.  Create and check out a `git` branch named `gh-pages`.

    <code-example format="shell" language="shell">

    git checkout -b gh-pages

    </code-example>

1.  Build your project using the GitHub project name, with the Angular CLI command [`ng build`](cli/build) and the following options, where `your_project_name` is the name of the project that you gave the GitHub repository in step 1.

    Be sure to include the slashes on either side of your project name as in `/your_project_name/`.

    <code-example format="shell" language="shell">

    ng build --output-path docs --base-href /your_project_name/

    </code-example>

1.  When the build is complete, make a copy of `docs/index.html` and name it `docs/404.html`.
1.  Commit your changes and push.
1.  On the GitHub project page, go to Settings and select the Pages option from the left sidebar to configure the site to [publish from the docs folder](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site#choosing-a-publishing-source).
1.  Click Save.
1.  Click on the GitHub Pages link at the top of the GitHub Pages section to see your deployed application.
    The format of the link is `https://<user_name>.github.io/<project_name>`.

<div class="alert is-helpful">

Посмотрите [angular-cli-ghpages](https://github.com/angular-buch/angular-cli-ghpages), полнофункциональный пакет, который делает все это за вас и имеет дополнительную функциональность.

</div>

<a id="server-configuration"></a>

## Конфигурация сервера

В этом разделе рассматриваются изменения, которые вам, возможно, придется внести в сервер или в файлы, развернутые на сервере.

<a id="fallback"></a>

### Маршрутизируемые приложения должны возвращаться к `index.html`.

Ангулярные приложения - идеальные кандидаты для обслуживания с помощью простого статического HTML-сервера. Вам не нужен движок на стороне сервера для динамической компоновки страниц приложения, потому что

Angular делает это на стороне клиента.

Если приложение использует маршрутизатор Angular, вы должны настроить сервер так, чтобы он возвращал страницу хоста приложения \(`index.html`\) при запросе файла, которого у него нет.

<a id="deep-link"></a>

Маршрутизируемое приложение должно поддерживать "глубокие ссылки". Глубокая ссылка\_ - это URL, указывающий путь к компоненту внутри приложения.

Например, `http://www.mysite.com/heroes/42` - это _глубокая ссылка_ на страницу детализации героя, которая отображает героя с `id: 42`.

Нет никаких проблем, когда пользователь переходит по этому URL из запущенного клиента. Маршрутизатор Angular интерпретирует URL и направляет на эту страницу и героя.

Но щелчок по ссылке в электронном письме, ввод в адресной строке браузера или просто обновление браузера на странице с подробной информацией о герое &mdash; все эти действия обрабатываются самим браузером, _вне_ запущенного приложения. Браузер делает прямой запрос к серверу для этого URL, минуя маршрутизатор.

Статический сервер обычно возвращает `index.html`, когда получает запрос `http://www.mysite.com/`. Но он отвергает `http://www.mysite.com/heroes/42` и возвращает ошибку `404 - Not Found`, если только он не настроен на возврат `index.html` вместо этого.

Примеры конфигурации #### Fallback

Не существует единой конфигурации, подходящей для каждого сервера. В следующих разделах описаны конфигурации для некоторых наиболее популярных серверов.

Этот список ни в коем случае не является исчерпывающим, но должен послужить вам хорошей отправной точкой.

| Servers                                                      | Details                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| :----------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Apache](https://httpd.apache.org)                           | Add a [rewrite rule](https://httpd.apache.org/docs/current/mod/mod_rewrite.html) to the `.htaccess` file as shown \([ngmilk.rocks/2015/03/09/angularjs-html5-mode-or-pretty-urls-on-apache-using-htaccess](https://ngmilk.rocks/2015/03/09/angularjs-html5-mode-or-pretty-urls-on-apache-using-htaccess)\): <code-example format="apache" language="apache"> RewriteEngine On &NewLine;&nbsp; &num; If an existing asset or directory is requested go to it as it is &NewLine;&nbsp; RewriteCond %{DOCUMENT_ROOT}%{REQUEST_URI} -f [OR] &NewLine;&nbsp; RewriteCond %{DOCUMENT_ROOT}%{REQUEST_URI} -d &NewLine;&nbsp; RewriteRule ^ - [L] &NewLine; &NewLine;&nbsp; &num; If the requested resource doesn't exist, use index.html &NewLine;&nbsp; RewriteRule ^ /index.html </code-example>                                                                                                                                                                                                                                                                                                                                                                                                           |
| [Nginx](https://nginx.org)                                   | Use `try_files`, as described in [Front Controller Pattern Web Apps](https://www.nginx.com/resources/wiki/start/topics/tutorials/config_pitfalls/#front-controller-pattern-web-apps), modified to serve `index.html`: <code-example format="nginx" language="nginx"> try_files \$uri \$uri/ /index.html; </code-example>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| [Ruby](https://www.ruby-lang.org)                            | Create a Ruby server using \([sinatra](http://sinatrarb.com)\) with a basic Ruby file that configures the server `server.rb`: <code-example format="ruby" language="ruby"> require 'sinatra' &NewLine; &NewLine;&num; Folder structure &NewLine;&num; . &NewLine;&num; -- server.rb &NewLine;&num; -- public &NewLine;&num; &nbsp;&nbsp; &verbar;-- project-name &NewLine;&num; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &verbar;-- index.html &NewLine; &NewLine;get '/' do &NewLine;&nbsp; folderDir = settings.public_folder + '/project-name' &num; ng build output folder &NewLine;&nbsp; send_file File.join(folderDir, 'index.html') &NewLine;end </code-example>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| [IIS](https://www.iis.net)                                   | Add a rewrite rule to `web.config`, similar to the one shown [here](https://stackoverflow.com/a/26152011): <code-example format="xml" language="xml"> &lt;system.webServer&gt; &NewLine;&nbsp; &lt;rewrite&gt; &NewLine;&nbsp;&nbsp;&nbsp; &lt;rules&gt; &NewLine;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &lt;rule name="Angular Routes" stopProcessing="true"&gt; &NewLine;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &lt;match url=".\*" /&gt; &NewLine;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &lt;conditions logicalGrouping="MatchAll"&gt; &NewLine;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &lt;add input="{REQUEST_FILENAME}" matchType="IsFile" negate="true" /&gt; &NewLine;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &lt;add input="{REQUEST_FILENAME}" matchType="IsDirectory" negate="true" /&gt; &NewLine;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &lt;/conditions&gt; &NewLine;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &lt;action type="Rewrite" url="/index.html" /&gt; &NewLine;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &lt;/rule&gt; &NewLine;&nbsp;&nbsp;&nbsp; &lt;/rules&gt; &NewLine;&nbsp; &lt;/rewrite&gt; &NewLine;&lt;/system.webServer&gt; </code-example> |
| [GitHub Pages](https://pages.github.com)                     | You can't [directly configure](https://github.com/isaacs/github/issues/408) the GitHub Pages server, but you can add a 404 page. Copy `index.html` into `404.html`. It will still be served as the 404 response, but the browser will process that page and load the application properly. It's also a good idea to [serve from `docs` on main](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site#choosing-a-publishing-source) and to [create a `.nojekyll` file](https://www.bennadel.com/blog/3181-including-node-modules-and-vendors-folders-in-your-github-pages-site.htm)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| [Firebase hosting](https://firebase.google.com/docs/hosting) | Add a [rewrite rule](https://firebase.google.com/docs/hosting/url-redirects-rewrites#section-rewrites). <code-example language="json"> "rewrites": [ { &NewLine;&nbsp; "source": "**", &NewLine;&nbsp; "destination": "/index.html" &NewLine;} ] </code-example>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |

<a id="mime"></a>

### Настройка правильного MIME-типа для JavaScript-активов

Все файлы JavaScript вашего приложения должны обслуживаться сервером с заголовком [`Content-Type`](https://developer.mozilla.org/docs/Web/HTTP/Headers/Content-Type), установленным на `text/javascript` или другой [JavaScript-совместимый MIME-тип](https://developer.mozilla.org/docs/Web/HTTP/Basics_of_HTTP/MIME_types#textjavascript).

Большинство серверов и хостинговых служб уже делают это по умолчанию.

Сервер с неправильно настроенным mime-типом для файлов JavaScript приведет к тому, что приложение не запустится со следующей ошибкой:

<code-example format="output" hideCopy language="shell">

Не удалось загрузить скрипт модуля: Сервер ответил с MIME-типом "text/plain", не относящимся к JavaScript. Строгая проверка типа MIME применяется для скриптов модуля в соответствии со спецификацией HTML.

</code-example>

Если это так, вам необходимо проверить конфигурацию вашего сервера и перенастроить его на обслуживание файлов `.js` с `Content-Type: text/javascript`. Инструкции о том, как это сделать, см. в руководстве по эксплуатации вашего сервера.

<a id="cors"></a>

### Запрос услуг с другого сервера (CORS)

Разработчики Angular могут столкнуться с ошибкой [_cross-origin resource sharing_](https://en.wikipedia.org/wiki/Cross-origin_resource_sharing 'Cross-origin resource sharing'), когда делают запрос сервиса\(обычно запрос сервиса данных\) на сервер, отличный от собственного сервера приложения. Браузеры запрещают такие запросы, если только сервер не разрешает их явно.

Клиентское приложение ничего не может сделать с этими ошибками. Сервер должен быть настроен на прием запросов приложения.

О том, как включить CORS для определенных серверов, читайте на [enable-cors.org] (https://enable-cors.org/server.html 'Enabling CORS server').

<a id="optimize"></a>

## Оптимизация производства

Конфигурация `production` задействует следующие возможности оптимизации сборки.

| Features | Details | | :---------------------------------------------------- | :----------------------------------------------------------------------- | |

| [Ahead-of-Time (AOT) Compilation](guide/aot-compiler) | Предварительная компиляция шаблонов компонентов Angular. |

| [Производственный режим](#prod-mode) | Оптимизирует приложение для наилучшей производительности во время выполнения |

| Пакетирование | Конкатенирует множество файлов приложения и библиотек в несколько пакетов. |

| Минификация | Удаляет лишние пробельные символы, комментарии и необязательные лексемы. |

| Углификация | Переписывает код для использования коротких, загадочных имен переменных и функций. |

| | Устранение мертвого кода | Удаление модулей без ссылок и много неиспользуемого кода. |

См. [`ng build`](cli/build) для получения дополнительной информации о параметрах сборки CLI и о том, что они делают.

<a id="prod-mode"></a>

### Production mode at runtime

When you run an application locally using `ng serve`, Angular uses the development mode configuration at runtime. The development mode at runtime enables extra safety checks, more detailed error messages

and debugging utilities, such as the [expression-changed-after-checked](errors/NG0100) detection. Angular outputs

a message in the browser console to indicate that the development mode is enabled.

Those extra checks are helpful during the development, but they require an extra code in a bundle, which is undesirable in production. To ensure that there are no implications on the bundle size, the build optimizer

removes the development-only code from the bundle when building in production mode.

Building your application with the production configuration automatically enables Angular's runtime production mode. <a id="lazy-loading"></a>

### Lazy loading

You can dramatically reduce launch time by only loading the application modules that absolutely must be present when the application starts.

Configure the Angular Router to defer loading of all other modules \(and their associated code\), either by [waiting until the app has launched](guide/router-tutorial-toh#preloading 'Preloading') or by [_lazy loading_](guide/router#lazy-loading 'Lazy loading') them on demand.

<div class="callout is-helpful">

<header>Don't eagerly import something from a lazy-loaded module</header>

Если вы хотите лениво загрузить модуль, будьте осторожны и не импортируйте его в файл, который загружается с нетерпением при запуске приложения (например, корневой `AppModule`\). Если вы это сделаете, модуль будет загружен немедленно.

Конфигурация комплектации должна учитывать ленивую загрузку. Поскольку модули с ленивой загрузкой не импортируются в JavaScript, бандлеры исключают их по умолчанию.

Пакеты не знают о конфигурации маршрутизатора и не могут создавать отдельные пакеты для модулей с ленивой загрузкой.

Вам придется создавать эти пакеты вручную.

CLI запускает [Angular Ahead-of-Time Webpack Plugin](https://github.com/angular/angular-cli/tree/main/packages/ngtools/webpack), который автоматически распознает лениво загруженные `NgModules` и создает для них отдельные пакеты.

</div>

<a id="measure"></a>

### Измерение производительности

Вы можете принимать лучшие решения о том, что и как оптимизировать, если у вас есть четкое и точное понимание того, что заставляет приложение работать медленно. Причина может быть совсем не той, о которой вы думаете.

Вы можете потратить много времени и денег на оптимизацию того, что не принесет ощутимой пользы или даже сделает приложение медленнее.

Вам следует измерить реальное поведение приложения при работе в важных для вас средах.

Страница [Chrome DevTools Network Performance] (https://developer.chrome.com/docs/devtools/network/reference 'Chrome DevTools Network Performance') - хорошее место для начала изучения измерения производительности.

Инструмент [WebPageTest](https://www.webpagetest.org) - еще один хороший выбор, который также поможет убедиться, что развертывание прошло успешно.

<a id="inspect-bundle"></a>

### Инспектировать пакеты

Инструмент [source-map-explorer](https://github.com/danvk/source-map-explorer/blob/master/README.md) - это отличный способ проверить сгенерированные JavaScript-пакеты после сборки.

Установите `source-map-explorer`:

<code-example format="shell" language="shell">

npm install source-map-explorer --save-dev

</code-example>

Создайте свое приложение для производства _включая карты исходных текстов_.

<code-example format="shell" language="shell">

ng build --source-map

</code-example>

Перечислите созданные пакеты в папке `dist/project-name/`.

<code-example format="shell" language="shell">

ls dist/project-name/\*.js

</code-example>

Запустите проводник, чтобы создать графическое представление одного из пучков. В следующем примере показан график для пакета _main_.

<code-example format="shell" language="shell">

node_modules/.bin/source-map-explorer dist/project-name/main\*

</code-example>

`source-map-explorer` анализирует карту исходных текстов, созданную с помощью пакета, и рисует карту всех зависимостей, показывая, какие именно классы включены в пакет.

Вот результат для пакета _main_ примера приложения под названием `cli-quickstart`.

<div class="lightbox">

<img alt="quickstart sourcemap explorer" src="generated/images/guide/deployment/quickstart-sourcemap-explorer.png">

</div>

<a id="base-tag"></a>

## Тег `base`

HTML [`<base href="..." />`](guide/router) определяет базовый путь для преобразования относительных URL-адресов к таким ресурсам, как изображения, скрипты и таблицы стилей. Например, учитывая `<base href="/my/app/">`, браузер преобразует URL, такой как `some/place/foo.jpg`, в запрос сервера для `my/app/some/place/foo.jpg`.

Во время навигации маршрутизатор Angular использует _base href_ в качестве базового пути к файлам компонентов, шаблонов и модулей.

<div class="alert is-helpful">

См. также альтернативу [`APP_BASE_HREF`](api/common/APP_BASE_HREF 'API: APP_BASE_HREF').

</div>

При разработке вы обычно запускаете сервер в папке, содержащей `index.html`. Это корневая папка, и вы добавляете `<base href="/">` в начало `index.html`, потому что `/` - это корень приложения.

Но на общем или рабочем сервере вы можете обслуживать приложение из вложенной папки. Например, если URL для загрузки приложения имеет вид `http://www.mysite.com/my/app`, то подпапка будет `my/app/`, и вы должны добавить `<base href="/my/app/">` в серверную версию `index.html`.

Когда тег `base` неправильно настроен, приложение не загружается, и в консоли браузера появляются ошибки `404 - Not Found` для отсутствующих файлов. Посмотрите, где он _пытался_ найти эти файлы, и настройте тег base соответствующим образом.

<a id="deploy-url"></a>

## Урл `deploy`.

Опция командной строки, используемая для указания базового пути для разрешения относительных URL для активов, таких как изображения, скрипты и таблицы стилей во время _компиляции_. Например: `ng build --deploy-url /my/assets`.

Эффекты от определения `deploy url` и `base href` могут перекрываться.

-   Оба могут быть использованы для начальных скриптов, таблиц стилей, ленивых скриптов и css ресурсов.

Однако определение `base href` имеет несколько уникальных эффектов.

-   Определение `базового href` может использоваться для определения местоположения относительных активов шаблона \(HTML\) и относительных fetch/XMLHttpRequests.

Также `base href` может быть использован для определения базы Angular router'а по умолчанию \(см. [`APP_BASE_HREF`](api/common/APP_BASE_HREF)\). Пользователям с более сложными настройками может понадобиться вручную настроить токен `APP_BASE_HREF` в приложении\(например, база маршрутизации приложения - `/`, но ` assets/scripts/etc.` находятся по адресу `/assets/`\).

В отличие от `base href`, который может быть определен в одном месте, `deploy url` должен быть жестко закодирован в приложении во время сборки. Это означает, что указание `deploy url` снизит скорость сборки, но это печальная плата за использование опции, которая внедряется в приложение.

Вот почему `base href` обычно является лучшим вариантом.

<!-- links -->

<!-- external links -->

<!-- end links -->

:date: 28.02.2022
