# Рендеринг на стороне сервера (SSR) с помощью Angular Universal

Это руководство описывает **Angular Universal**, технологию, которая позволяет Angular рендерить приложения на сервере.

По умолчанию Angular отображает приложения только в _браузере_. Angular Universal позволяет Angular рендерить приложение на _сервере_, генерируя _статическое_ содержимое HTML, которое представляет собой состояние приложения. Когда содержимое HTML отображается в браузере, Angular загружает приложение и повторно использует информацию, имеющуюся в HTML, сгенерированном на сервере.

При серверном рендеринге приложение обычно быстрее отображается в браузере, давая пользователям возможность просмотреть пользовательский интерфейс приложения до того, как оно станет полностью интерактивным. Дополнительную информацию см. ниже ([раздел "Зачем использовать рендеринг на стороне сервера?"](#why-do-it)).

Также для более детального рассмотрения различных техник и концепций, связанных с SSR, ознакомьтесь с этой [статьей](https://developers.google.com/web/updates/2019/02/rendering-on-the-web).

Вы можете включить рендеринг на стороне сервера в вашем приложении Angular, используя схему `@nguniversal/express-engine`, как описано ниже.

<div class="alert is-helpful">

Для Angular Universal требуется [активная LTS или maintenance LTS](https://nodejs.org/about/releases) версия Node.js. Для получения информации смотрите руководство [совместимость версий](guide/versions), чтобы узнать о поддерживаемых в настоящее время версиях.

</div>

<a id="the-example"></a>

## Универсальный учебник

Учебник [Tour of Heroes](tutorial/tour-of-heroes) является основой для этого руководства.

В этом примере Angular CLI компилирует и собирает универсальную версию приложения с помощью [Ahead-of-Time (AOT) compiler](guide/aot-compiler). Веб-сервер Node.js Express компилирует HTML-страницы с Universal на основе запросов клиентов.

<div class="alert is-helpful">

<live-example downloadOnly>Скачайте готовый код примера</live-example>, который запускается на сервере [Node.js® Express](https://expressjs.com).

</div>

### Шаг 1. Включите рендеринг на стороне сервера

Выполните следующую команду, чтобы добавить поддержку SSR в ваше приложение:

<code-example format="shell" language="shell">

ng add &commat;nguniversal/express-engine

</code-example>

Команда обновляет код приложения для включения SSR и добавляет дополнительные файлы в структуру проекта (файлы, отмеченные символом `*`).

<div class='filetree'>     <div class='file'>
        src
    </div>
    <div class='children'>
        <div class='file'>
          index.html &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; // &lt;-- app web page
        </div>
        <div class='file'>
          main.ts &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; // &lt;-- bootstrapper for client app
        </div>
        <div class='file'>
          main.server.ts &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; // &lt;-- &ast; bootstrapper for server app
        </div>
        <div class='file'>
          style.css &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; // &lt;-- styles for the app
        </div>
        <div class='file'>
          app/ &nbsp;&hellip; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; // &lt;-- application code
        </div>
        <div class='children'>
            <div class='file'>
              app.config.ts &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; // &lt; client-side application configuration (standalone app only)
            </div>
            <div class='file'>
              app.module.ts &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; // &lt; client-side application module (NgModule app only)
            </div>
        </div>
        <div class='children'>
            <div class='file'>
              app.config.server.ts &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; // &lt;-- &ast; server-side application configuration (standalone app only)
            </div>
            <div class='file'>
              app.module.server.ts &nbsp;&nbsp;&nbsp; // &lt;-- &ast; server-side application module (NgModule app only)
            </div>
        </div>
        <div class='file'>
          server.ts &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; // &lt;-- &ast; express web server
        </div>
        <div class='file'>
          tsconfig.json &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; // &lt;-- TypeScript base configuration
        </div>
        <div class='file'>
          tsconfig.app.json &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; // &lt;-- TypeScript browser application configuration
        </div>
        <div class='file'>
          tsconfig.server.json &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; // &lt;-- TypeScript server application configuration
        </div>
        <div class='file'>
          tsconfig.spec.json &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; // &lt;-- TypeScript tests configuration
        </div>
    </div>
</div>

### Шаг 2. Включите гидратацию клиента

<div class="alert is-important">

Функция гидратации доступна для [предварительного просмотра разработчиком](/guide/releases#developer-preview). Она готова к тому, чтобы вы попробовали ее, но она может измениться до того, как станет стабильной.

</div>

Гидратация - это процесс, который восстанавливает отрисованное на стороне сервера приложение на клиенте. Сюда входят такие вещи, как повторное использование серверных DOM-структур, сохранение состояния приложения, передача данных приложения, которые уже были получены сервером, и другие процессы. Узнайте больше о гидратации в [этом руководстве](guide/hydration).

Вы можете включить гидратацию, обновив файл `app.module.ts`. Импортируйте функцию `provideClientHydration` из `@angular/platform-browser` и добавьте вызов функции в секцию `providers` модуля `AppModule`, как показано ниже.

```typescript import { provideClientHydration } from '@angular/platform-browser';
// ...

@NgModule({
    // ...
    providers: [provideClientHydration()], // add this line
    bootstrap: [AppComponent],
})
export class AppModule {
    // ...
}
```

### Шаг 3. Запустите сервер

Чтобы начать рендеринг вашего приложения с помощью Universal на вашей локальной системе, используйте следующую команду.

<code-example format="shell" language="shell">

npm run dev:ssr

</code-example>

### Step 4. Run your application in a browser

Once the web server starts, open a browser and navigate to `http://localhost:4200`. You should see the familiar Tour of Heroes dashboard page.

Navigation using `routerLinks` works correctly because they use the built-in anchor \(`<a>`\) elements. You can go from the Dashboard to the Heroes page and back.

Click a hero on the Dashboard page to display its Details page.

If you throttle your network speed so that the client-side scripts take longer to download \(instructions following\), you'll notice:

-   You can't add or delete a hero

-   The search box on the Dashboard page is ignored

-   The _Back_ and _Save_ buttons on the Details page don't work

The transition from the server-rendered application to the client application happens quickly on a development machine, but you should always test your applications in real-world scenarios.

You can simulate a slower network to see the transition more clearly as follows:

1.  Open the Chrome Dev Tools and go to the Network tab.

1.  Find the [Network Throttling](https://developers.google.com/web/tools/chrome-devtools/network-performance/reference#throttling) dropdown on the far right of the menu bar.

1.  Попробуйте одну из скоростей "3G".

Приложение с рендерингом сервера по-прежнему запускается быстро, но полная загрузка клиентского приложения может занять несколько секунд.

<a id="why-do-it"></a>

## Зачем использовать рендеринг на стороне сервера?

Есть три основные причины для создания универсальной версии вашего приложения.

-   Облегчить работу веб-гусениц благодаря [поисковой оптимизации (SEO)](https://static.googleusercontent.com/media/www.google.com/en//webmasters/docs/search-engine-optimization-starter-guide.pdf)

-   Улучшить производительность на мобильных и маломощных устройствах

-   Быстро показывать первую страницу с помощью [first-contentful paint (FCP)](https://developers.google.com/web/tools/lighthouse/audits/first-contentful-paint)

<a id="seo"></a> <a id="web-crawlers"></a>

### Облегчение работы веб-ползунков (SEO)

Google, Bing, Facebook, Twitter и другие сайты социальных сетей полагаются на веб-гусеницы для индексации содержимого вашего приложения и обеспечения возможности поиска по нему в Интернете. Эти веб-гусеницы могут быть не в состоянии перемещаться и индексировать ваше высокоинтерактивное приложение Angular так, как это может сделать пользователь.

Angular Universal может генерировать статическую версию вашего приложения, которая легко доступна для поиска, ссылок и навигации без JavaScript. Universal также делает доступным предварительный просмотр сайта, поскольку каждый URL возвращает полностью отрисованную страницу.

<a id="no-javascript"></a>

### Улучшение производительности на мобильных и маломощных устройствах

Некоторые устройства не поддерживают JavaScript или выполняют его настолько плохо, что пользовательское восприятие становится неприемлемым. В таких случаях вам может потребоваться серверная версия приложения без JavaScript.

Эта версия, пусть и ограниченная, может быть единственной практической альтернативой для людей, которые иначе не смогут использовать приложение вообще.

<a id="startup-performance"></a>

### Быстрое отображение первой страницы

Быстрый показ первой страницы может иметь решающее значение для вовлечения пользователей. Страницы, которые загружаются быстрее, работают лучше [даже при изменениях размером в 100 мс] (https://web.dev/shopping-for-speed-on-ebay).

Возможно, ваше приложение должно запускаться быстрее, чтобы привлечь пользователей до того, как они решат заняться чем-то другим.

С помощью Angular Universal вы можете создавать целевые страницы для приложения, которые выглядят как полноценное приложение. Страницы представляют собой чистый HTML и могут отображаться даже при отключенном JavaScript.

Страницы не обрабатывают события браузера, но они _до_ поддерживают навигацию по сайту с помощью [`routerLink`](guide/router-reference#router-link).

На практике вы будете обслуживать статическую версию целевой страницы, чтобы удержать внимание пользователя. В то же время, вы загрузите полное приложение Angular, расположенное за ней.

Пользователь воспринимает практически мгновенную производительность целевой страницы и получает полный интерактивный опыт после полной загрузки приложения.

<a id="how-does-it-work"></a>

## Универсальные веб-серверы

Универсальный веб-сервер отвечает на запросы страниц приложений статическим HTML, отображаемым [универсальным шаблонизатором](#universal-engine). Сервер получает и отвечает на HTTP-запросы от клиентов\(обычно браузеров\), и обслуживает статические активы, такие как скрипты, CSS и изображения.

Он может отвечать на запросы данных, либо напрямую, либо как прокси на отдельный сервер данных.

Образец веб-сервера для данного руководства основан на популярном фреймворке [Express](https://expressjs.com).

<div class="alert is-helpful">

**NOTE**: <br /> _Any_ web server technology can serve a Universal application as long as it can call Angular `platform-server` package [`renderModule`](api/platform-server/renderModule) or [`renderApplication`](api/platform-server/renderApplication) functions.
The principles and decision points discussed here apply to any web server technology.

</div>

Универсальные приложения используют пакет Angular `platform-server` \(в отличие от `platform-browser`\), который предоставляет серверные реализации DOM, `XMLHttpRequest` и других низкоуровневых функций, которые не зависят от браузера.

Сервер \([Node.js Express](https://expressjs.com) в примере этого руководства\) передает клиентские запросы на страницы приложения в NgUniversal `ngExpressEngine`. Под капотом находятся функции рендеринга, обеспечивающие кэширование и другие полезные утилиты.

Функция рендеринга принимает в качестве входных данных _шаблон_ HTML страницы\ (обычно `index.html`\), и *модуль Angular, содержащий компоненты или функцию, которая при вызове возвращает `Promise`, разрешающуюся в `ApplicationRef`, и *маршрут\_, определяющий, какие компоненты отображать. Маршрут формируется из запроса клиента к серверу.

Каждый запрос приводит к появлению соответствующего представления для запрошенного маршрута. Функция render рендерит представление внутри тега `<app>` шаблона, создавая готовую HTML-страницу для клиента.

Наконец, сервер возвращает клиенту отрисованную страницу.

### Работа вокруг API браузера

Поскольку универсальное приложение не выполняется в браузере, некоторые API и возможности браузера могут отсутствовать на сервере.

Например, серверные приложения не могут ссылаться на глобальные объекты браузера, такие как `window`, `document`, `navigator` или `location`.

Angular предоставляет некоторые инжектируемые абстракции над этими объектами, такие как [`Location`](api/common/Location) или [`DOCUMENT`](api/common/DOCUMENT); это может адекватно заменить эти API. Если Angular не предоставляет такой возможности, можно написать новые абстракции, которые делегируют API браузера в браузере и альтернативную реализацию на сервере\(также известную как шимминг\).

Аналогично, без событий мыши или клавиатуры приложение на стороне сервера не может полагаться на то, что пользователь нажмет на кнопку, чтобы показать компонент. Приложение должно определить, что отобразить, основываясь исключительно на входящем запросе клиента.
Это хороший аргумент в пользу того, чтобы сделать приложение [маршрутизируемым] (guide/router).

<a id="service-worker"></a>

### Universal и Angular Service Worker

Если вы используете Universal в сочетании с Angular service worker, поведение будет отличаться от обычного рендеринга на стороне сервера. Первоначальный запрос к серверу будет отрисован на сервере, как и ожидалось. Однако после этого первоначального запроса последующие запросы обрабатываются работником службы. При последующих запросах файл `index.html` обслуживается статически и обходится без рендеринга на стороне сервера.

<a id="universal-engine"></a>

### Универсальный шаблонизатор

Важный бит в файле `server.ts` - это функция `ngExpressEngine()`.

<code-example header="server.ts" path="universal/server.ts" region="ngExpressEngine"></code-example>.

Функция `ngExpressEngine()` является оберткой вокруг функций [`renderModule`](api/platform-server/renderModule) и [`renderApplication`](api/platform-server/renderApplication) пакета Angular `platform-server`, которые превращают запросы клиента в отрисованные сервером HTML-страницы.

Она принимает объект со следующими свойствами:

| Properties | Details | | :--------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

| `bootstrap` | Корневой `NgModule` или функция, которая при вызове возвращает `Promise`, который разрешается в `ApplicationRef` приложения при рендеринге на сервере. Для примера приложения это `AppServerModule`. Это мост между серверным рендерером Universal и приложением Angular. |

| `extraProviders` | Это свойство необязательно и позволяет вам указать провайдеры зависимостей, которые применяются только при рендеринге приложения на сервере. Делайте это, когда вашему приложению нужна информация, которая может быть определена только текущим запущенным экземпляром сервера. |

Функция `ngExpressEngine()` возвращает обратный вызов `Promise`, который разрешается на отрисованную страницу. Движок сам решает, что делать с этой страницей.
Обратный вызов `Promise` этого движка возвращает отрисованную страницу веб-серверу, который затем передает ее клиенту в HTTP-ответе.

### Фильтрация URL-адресов запросов

<div class="alert is-helpful">

**NOTE**: <br /> The basic behavior described below is handled automatically when using the NgUniversal Express schematic.
This is helpful when trying to understand the underlying behavior or replicate it without using the schematic.

</div>

Веб-сервер должен отличать _запросы страниц приложения_ от других видов запросов.

Это не так просто, как перехватить запрос к корневому адресу `/`. Браузер может запросить один из маршрутов приложения, например `/dashboard`, `/heroes` или `/detail:12`.

На самом деле, если бы приложение отображалось только на сервере, _каждая_ ссылка приложения, на которую нажимают, приходила бы на сервер как навигационный URL, предназначенный для маршрутизатора.

К счастью, у маршрутов приложений есть кое-что общее: в их URL отсутствуют расширения файлов. \(Запросы данных также не имеют расширений, но их можно распознать, потому что они всегда начинаются с `/api`.\)

Все запросы статических активов имеют расширение файла \(например, `main.js` или `/node_modules/zone.js/bundles/zone.umd.js`\).

Поскольку вы используете маршрутизацию, вы можете распознать три типа запросов и обрабатывать их по-разному.

Типы запросов маршрутизации | Подробности | | | :-------------------- | :---------------------------------- |

| Запрос данных | URL запроса, начинающийся с `/api`. |

| Навигация по приложениям | Запрос URL без расширения файла. |

| Статический актив | Все остальные запросы. |

Экспресс-сервер Node.js - это конвейер промежуточного программного обеспечения, которое фильтрует и обрабатывает запросы один за другим. Вы настраиваете конвейер Node.js Express-сервера с помощью вызовов `server.get()`, как, например, в данном случае для запросов данных.

<code-example header="server.ts (URL данных)" path="universal/server.ts" region="data-request"></code-example>.

<div class="alert is-helpful">

**NOTE**: <br /> This sample server doesn't handle data requests.

The tutorial's "in-memory web API" module, a demo and development tool, intercepts all HTTP calls and simulates the behavior of a remote data server. In practice, you would remove that module and register your web API middleware on the server here.

</div>

Следующий код фильтрует URL запроса без расширений и рассматривает их как навигационные запросы.

<code-example header="server.ts (navigation)" path="universal/server.ts" region="navigation-request"></code-example>

### Безопасное обслуживание статических файлов

Единственный `server.use()` рассматривает все остальные URL как запросы на статические активы, такие как JavaScript, изображения и файлы стилей.

Чтобы гарантировать, что клиенты могут загружать только те файлы, которые им разрешено видеть, поместите все файлы активов для клиентов в папку `/dist` и выполняйте запросы на файлы только из папки `/dist`.

Следующий код Node.js Express направляет все остальные запросы в папку `/dist` и возвращает ошибку `404 - NOT FOUND`, если файл не найден.

<code-example header="server.ts (статические файлы)" path="universal/server.ts" region="static"></code-example>

### Использование абсолютных URL для HTTP (данных) запросов на сервере

В учебнике `HeroService` и `HeroSearchService` делегируют модулю Angular `HttpClient` для получения данных приложения. Эти сервисы отправляют запросы на _относительные_ URL, такие как `api/heroes`.

В приложении с рендерингом на стороне сервера, HTTP URL должны быть _абсолютными_\ (например, `https://my-server.com/api/heroes`\).

Это означает, что URL должны быть каким-то образом преобразованы в абсолютные при работе на сервере и оставлены относительными при работе в браузере.

Если вы используете один из пакетов `@nguniversal/*-engine`\ (например, `@nguniversal/express-engine`\), это будет сделано автоматически. Вам не нужно ничего делать для того, чтобы относительные URL работали на сервере.

Если по какой-то причине вы не используете пакет `@nguniversal/*-engine`, вам может понадобиться сделать это самостоятельно.

Рекомендуемое решение - передавать полный URL запроса в аргумент `options` в [renderModule](api/platform-server/renderModule). Этот вариант является наименее навязчивым, так как не требует изменений в приложении.

Здесь "URL запроса" относится к URL запроса, в ответ на который приложение рендерится на сервере.

Например, если клиент запросил `https://my-server.com/dashboard` и вы отображаете приложение на сервере в ответ на этот запрос, `options.url` должен быть установлен в `https://my-server.com/dashboard`.

Теперь при каждом HTTP-запросе, выполняемом в процессе рендеринга приложения на сервере, Angular сможет правильно преобразовать URL запроса в абсолютный URL, используя предоставленный `options.url`.

### Полезные скрипты

| Scripts | Details | | :-------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| <code-example format="shell" language="shell"> npm run dev:ssr </code-example> | Similar to [`ng serve`](cli/serve), which offers live reload during development, but uses server-side rendering. The application runs in watch mode and refreshes the browser after every change. This command is slower than the actual `ng serve` command. |
| <code-example format="shell" language="shell"> ng build &amp;&amp; ng run app-name:server </code-example> | Builds both the server script and the application in production mode. Use this command when you want to build the project for deployment. |
| <code-example format="shell" language="shell"> npm run serve:ssr </code-example> | Starts the server script for serving the application locally with server-side rendering. It uses the build artifacts created by `ng run build:ssr`, so make sure you have run that command as well. <div class="alert is-helpful"> **NOTE**: <br /> `serve:ssr` is not intended to be used to serve your application in production, but only for testing the server-side rendered application locally. </div> |
| <code-example format="shell" language="shell"> npm run prerender </code-example> | Used to prerender an application's pages. Read more about prerendering [here](guide/prerendering). |

<!-- links -->

<!-- external links -->

<!-- end links -->

:date: 25.04.2023
