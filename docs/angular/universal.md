# Рендеринг на стороне сервера (SSR) с помощью Angular Universal

:date: 25.04.2023

Это руководство описывает **Angular Universal**, технологию, которая позволяет Angular рендерить приложения на сервере.

По умолчанию Angular отображает приложения только в _браузере_. Angular Universal позволяет Angular рендерить приложение на _сервере_, генерируя _статическое_ содержимое HTML, которое представляет собой состояние приложения. Когда содержимое HTML отображается в браузере, Angular загружает приложение и повторно использует информацию, имеющуюся в HTML, сгенерированном на сервере.

При серверном рендеринге приложение обычно быстрее отображается в браузере, давая пользователям возможность просмотреть пользовательский интерфейс приложения до того, как оно станет полностью интерактивным. Дополнительную информацию см. ниже ([раздел "Зачем использовать рендеринг на стороне сервера?"](#why-do-it)).

Также для более детального рассмотрения различных техник и концепций, связанных с SSR, ознакомьтесь с этой [статьей](https://developers.google.com/web/updates/2019/02/rendering-on-the-web).

Вы можете включить рендеринг на стороне сервера в вашем приложении Angular, используя схему `@nguniversal/express-engine`, как описано ниже.

!!!note ""

    Для Angular Universal требуется [активная LTS или maintenance LTS](https://nodejs.org/about/releases) версия Node.js. Для получения информации смотрите руководство [совместимость версий](https://angular.io/guide/versions), чтобы узнать о поддерживаемых в настоящее время версиях.

## Универсальный учебник {: #the-example}

Учебник [Tour of Heroes](toh.md) является основой для этого руководства.

В этом примере Angular CLI компилирует и собирает универсальную версию приложения с помощью [Ahead-of-Time (AOT) compiler](aot-compiler.md). Веб-сервер Node.js Express компилирует HTML-страницы с Universal на основе запросов клиентов.

!!!note ""

    [Скачайте готовый код примера](https://angular.io/generated/zips/universal/universal.zip), который запускается на сервере [Node.js® Express](https://expressjs.com).

### Шаг 1. Включите рендеринг на стороне сервера

Выполните следующую команду, чтобы добавить поддержку SSR в ваше приложение:

```
ng add @nguniversal/express-engine
```

Команда обновляет код приложения для включения SSR и добавляет дополнительные файлы в структуру проекта (файлы, отмеченные символом `*`).

```
src
+- index.html                  // <-- app web page
+- main.ts                     // <-- bootstrapper for client app
+- main.server.ts              // <-- * bootstrapper for server app
+- style.css                   // <-- styles for the app
+- app/  …                     // <-- application code
|  +- app.config.ts            // <-- client-side application configuration (standalone app only)
|  +- app.module.ts            // <-- client-side application module (NgModule app only)
|  +- app.config.server.ts     // <-- * server-side application configuration (standalone app only)
|  +- app.module.server.ts     // <-- * server-side application module (NgModule app only)
+- server.ts                   // <-- * express web server
+- tsconfig.json               // <-- TypeScript base configuration
+- tsconfig.app.json           // <-- TypeScript browser application configuration
+- tsconfig.server.json        // <-- TypeScript server application configuration
+- tsconfig.spec.json          // <-- TypeScript tests configuration
```

### Шаг 2. Включите гидратацию клиента

!!!warning ""

    Функция гидратации доступна для [предварительного просмотра разработчиком](https://angular.io/guide/releases#developer-preview). Она готова к тому, чтобы вы попробовали ее, но она может измениться до того, как станет стабильной.

Гидратация — это процесс, который восстанавливает отрисованное на стороне сервера приложение на клиенте. Сюда входят такие вещи, как повторное использование серверных DOM-структур, сохранение состояния приложения, передача данных приложения, которые уже были получены сервером, и другие процессы. Узнайте больше о гидратации в [этом руководстве](hydration.md).

Вы можете включить гидратацию, обновив файл `app.module.ts`. Импортируйте функцию `provideClientHydration` из `@angular/platform-browser` и добавьте вызов функции в секцию `providers` модуля `AppModule`, как показано ниже.

```typescript
import { provideClientHydration } from '@angular/platform-browser';
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

```shell
npm run dev:ssr
```

### Шаг 4. Запустите ваше приложение в браузере

Once the web server starts, open a browser and navigate to `http://localhost:4200`. Вы должны увидеть знакомую страницу приборной панели Tour of Heroes.

Навигация с помощью `routerLinks` работает правильно, поскольку они используют встроенные элементы якоря (`a`). Вы можете переходить от приборной панели к странице героев и обратно.

Щелкните героя на странице приборной панели, чтобы открыть страницу его подробностей.

Если вы уменьшите скорость сети, чтобы сценарии на стороне клиента загружались дольше (инструкции приведены ниже), вы это заметите:

-   Вы не можете добавить или удалить героя.

-   Поисковая строка на странице "Приборная панель" игнорируется

-   Кнопки _Назад_ и _Сохранить_ на странице подробностей не работают

Переход от серверного приложения к клиентскому происходит быстро на машине разработчика, но вы всегда должны тестировать свои приложения в реальных условиях.

Вы можете смоделировать более медленную сеть, чтобы увидеть переход более четко следующим образом:

1.  Откройте Chrome Dev Tools и перейдите на вкладку Network.

2.  Найдите выпадающий список [Network Throttling](https://developers.google.com/web/tools/chrome-devtools/network-performance/reference#throttling) в крайнем правом углу строки меню.

3.  Попробуйте одну из скоростей "3G".

Приложение с рендерингом сервера по-прежнему запускается быстро, но полная загрузка клиентского приложения может занять несколько секунд.

## Зачем использовать рендеринг на стороне сервера? {: #why-do-it}

Есть три основные причины для создания универсальной версии вашего приложения.

-   Облегчить работу веб-гусениц благодаря [поисковой оптимизации (SEO)](https://static.googleusercontent.com/media/www.google.com/en//webmasters/docs/search-engine-optimization-starter-guide.pdf)

-   Улучшить производительность на мобильных и маломощных устройствах

-   Быстро показывать первую страницу с помощью [first-contentful paint (FCP)](https://developers.google.com/web/tools/lighthouse/audits/first-contentful-paint)

### Облегчение работы веб-ползунков (SEO) {: #seo}

Google, Bing, Facebook, Twitter и другие сайты социальных сетей полагаются на веб-гусеницы для индексации содержимого вашего приложения и обеспечения возможности поиска по нему в Интернете. Эти веб-гусеницы могут быть не в состоянии перемещаться и индексировать ваше высокоинтерактивное приложение Angular так, как это может сделать пользователь.

Angular Universal может генерировать статическую версию вашего приложения, которая легко доступна для поиска, ссылок и навигации без JavaScript. Universal также делает доступным предварительный просмотр сайта, поскольку каждый URL возвращает полностью отрисованную страницу.

### Улучшение производительности на мобильных и маломощных устройствах {: #no-javascript}

Некоторые устройства не поддерживают JavaScript или выполняют его настолько плохо, что пользовательское восприятие становится неприемлемым. В таких случаях вам может потребоваться серверная версия приложения без JavaScript.

Эта версия, пусть и ограниченная, может быть единственной практической альтернативой для людей, которые иначе не смогут использовать приложение вообще.

### Быстрое отображение первой страницы {: #startup-performance}

Быстрый показ первой страницы может иметь решающее значение для вовлечения пользователей. Страницы, которые загружаются быстрее, работают лучше [даже при изменениях размером в 100 мс](https://web.dev/shopping-for-speed-on-ebay).

Возможно, ваше приложение должно запускаться быстрее, чтобы привлечь пользователей до того, как они решат заняться чем-то другим.

С помощью Angular Universal вы можете создавать целевые страницы для приложения, которые выглядят как полноценное приложение. Страницы представляют собой чистый HTML и могут отображаться даже при отключенном JavaScript.

Страницы не обрабатывают события браузера, но они _до_ поддерживают навигацию по сайту с помощью [`routerLink`](router-reference.md#router-link).

На практике вы будете обслуживать статическую версию целевой страницы, чтобы удержать внимание пользователя. В то же время, вы загрузите полное приложение Angular, расположенное за ней.

Пользователь воспринимает практически мгновенную производительность целевой страницы и получает полный интерактивный опыт после полной загрузки приложения.

## Универсальные веб-серверы {: #how-does-it-work}

Универсальный веб-сервер отвечает на запросы страниц приложений статическим HTML, отображаемым [универсальным шаблонизатором](#universal-engine). Сервер получает и отвечает на HTTP-запросы от клиентов (обычно браузеров), и обслуживает статические активы, такие как скрипты, CSS и изображения.

Он может отвечать на запросы данных, либо напрямую, либо как прокси на отдельный сервер данных.

Образец веб-сервера для данного руководства основан на популярном фреймворке [Express](https://expressjs.com).

!!!note ""

    Любая технология веб-сервера может обслуживать универсальное приложение, если она может вызывать функции [`renderModule`](https://angular.io/api/platform-server/renderModule) или [`renderApplication`](https://angular.io/api/platform-server/renderApplication) пакета Angular `platform-server`.

    Рассмотренные здесь принципы и точки принятия решений применимы к любой технологии веб-сервера.

Универсальные приложения используют пакет Angular `platform-server` (в отличие от `platform-browser`), который предоставляет серверные реализации DOM, `XMLHttpRequest` и других низкоуровневых функций, которые не зависят от браузера.

Сервер ([Node.js Express](https://expressjs.com) в примере этого руководства) передает клиентские запросы на страницы приложения в NgUniversal `ngExpressEngine`. Под капотом находятся функции рендеринга, обеспечивающие кэширование и другие полезные утилиты.

Функция рендеринга принимает в качестве входных данных _шаблон_ HTML страницы (обычно `index.html`), и \*модуль Angular, содержащий компоненты или функцию, которая при вызове возвращает `Promise`, разрешающуюся в `ApplicationRef`, и маршрут, определяющий, какие компоненты отображать. Маршрут формируется из запроса клиента к серверу.

Каждый запрос приводит к появлению соответствующего представления для запрошенного маршрута. Функция render рендерит представление внутри тега `<app>` шаблона, создавая готовую HTML-страницу для клиента.

Наконец, сервер возвращает клиенту отрисованную страницу.

### Работа вокруг API браузера

Поскольку универсальное приложение не выполняется в браузере, некоторые API и возможности браузера могут отсутствовать на сервере.

Например, серверные приложения не могут ссылаться на глобальные объекты браузера, такие как `window`, `document`, `navigator` или `location`.

Angular предоставляет некоторые инжектируемые абстракции над этими объектами, такие как [`Location`](https://angular.io/api/common/Location) или [`DOCUMENT`](https://angular.io/api/common/DOCUMENT); это может адекватно заменить эти API. Если Angular не предоставляет такой возможности, можно написать новые абстракции, которые делегируют API браузера в браузере и альтернативную реализацию на сервере (также известную как шимминг).

Аналогично, без событий мыши или клавиатуры приложение на стороне сервера не может полагаться на то, что пользователь нажмет на кнопку, чтобы показать компонент. Приложение должно определить, что отобразить, основываясь исключительно на входящем запросе клиента.

Это хороший аргумент в пользу того, чтобы сделать приложение [маршрутизируемым](router.md).

### Universal и Angular Service Worker {: #service-worker}

Если вы используете Universal в сочетании с Angular service worker, поведение будет отличаться от обычного рендеринга на стороне сервера. Первоначальный запрос к серверу будет отрисован на сервере, как и ожидалось. Однако после этого первоначального запроса последующие запросы обрабатываются работником службы. При последующих запросах файл `index.html` обслуживается статически и обходится без рендеринга на стороне сервера.

### Универсальный шаблонизатор {: #universal-engine}

Важный бит в файле `server.ts` — это функция `ngExpressEngine()`.

```ts
// Our Universal express-engine (found @ https://github.com/angular/universal/tree/main/modules/express-engine)
server.engine(
    'html',
    ngExpressEngine({
        bootstrap: AppServerModule,
    })
);
```

Функция `ngExpressEngine()` является оберткой вокруг функций [`renderModule`](https://angular.io/api/platform-server/renderModule) и [`renderApplication`](https://angular.io/api/platform-server/renderApplication) пакета Angular `platform-server`, которые превращают запросы клиента в отрисованные сервером HTML-страницы.

Она принимает объект со следующими свойствами:

| Свойства         | Подробности                                                                                                                                                                                                                                                                      |
| :--------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `bootstrap`      | Корневой `NgModule` или функция, которая при вызове возвращает `Promise`, который разрешается в `ApplicationRef` приложения при рендеринге на сервере. Для примера приложения это `AppServerModule`. Это мост между серверным рендерером Universal и приложением Angular.        |
| `extraProviders` | Это свойство необязательно и позволяет вам указать провайдеры зависимостей, которые применяются только при рендеринге приложения на сервере. Делайте это, когда вашему приложению нужна информация, которая может быть определена только текущим запущенным экземпляром сервера. |

Функция `ngExpressEngine()` возвращает обратный вызов `Promise`, который разрешается на отрисованную страницу. Движок сам решает, что делать с этой страницей.

Обратный вызов `Promise` этого движка возвращает отрисованную страницу веб-серверу, который затем передает ее клиенту в HTTP-ответе.

### Фильтрация URL-адресов запросов

!!!note ""

    Описанное ниже базовое поведение обрабатывается автоматически при использовании схемы NgUniversal Express.
    Это полезно при попытке понять основное поведение или воспроизвести его без использования схемы.

Веб-сервер должен отличать _запросы страниц приложения_ от других видов запросов.

Это не так просто, как перехватить запрос к корневому адресу `/`. Браузер может запросить один из маршрутов приложения, например `/dashboard`, `/heroes` или `/detail:12`.

На самом деле, если бы приложение отображалось только на сервере, _каждая_ ссылка приложения, на которую нажимают, приходила бы на сервер как навигационный URL, предназначенный для маршрутизатора.

К счастью, у маршрутов приложений есть кое-что общее: в их URL отсутствуют расширения файлов. (Запросы данных также не имеют расширений, но их можно распознать, потому что они всегда начинаются с `/api`.)

Все запросы статических активов имеют расширение файла (например, `main.js` или `/node_modules/zone.js/bundles/zone.umd.js`).

Поскольку вы используете маршрутизацию, вы можете распознать три типа запросов и обрабатывать их по-разному.

| Типы запросов маршрутизации | Подробности                         |
| :-------------------------- | :---------------------------------- |
| Запрос данных               | URL запроса, начинающийся с `/api`. |
| Навигация по приложениям    | Запрос URL без расширения файла.    |
| Статический актив           | Все остальные запросы.              |

Экспресс-сервер Node.js — это конвейер промежуточного программного обеспечения, которое фильтрует и обрабатывает запросы один за другим. Вы настраиваете конвейер Node.js Express-сервера с помощью вызовов `server.get()`, как, например, в данном случае для запросов данных.

```ts
// TODO: implement data requests securely
server.get('/api/**', (req, res) => {
    res.status(404).send(
        'data requests are not yet supported'
    );
});
```

!!!note ""

    Этот образец сервера не обрабатывает запросы данных.

    Модуль "in-memory web API" в учебнике, демонстрационный и инструмент разработки, перехватывает все HTTP-вызовы и имитирует поведение удаленного сервера данных. На практике вы удалите этот модуль и зарегистрируете на сервере промежуточное программное обеспечение веб-АПИ здесь.

Следующий код фильтрует URL запроса без расширений и рассматривает их как навигационные запросы.

```ts
// All regular routes use the Universal engine
server.get('*', (req, res) => {
    res.render(indexHtml, {
        req,
        providers: [
            {
                provide: APP_BASE_HREF,
                useValue: req.baseUrl,
            },
        ],
    });
});
```

### Безопасное обслуживание статических файлов

Единственный `server.use()` рассматривает все остальные URL как запросы на статические активы, такие как JavaScript, изображения и файлы стилей.

Чтобы гарантировать, что клиенты могут загружать только те файлы, которые им разрешено видеть, поместите все файлы активов для клиентов в папку `/dist` и выполняйте запросы на файлы только из папки `/dist`.

Следующий код Node.js Express направляет все остальные запросы в папку `/dist` и возвращает ошибку `404 — NOT FOUND`, если файл не найден.

```ts
// Serve static files from /browser
server.get(
    '*.*',
    express.static(distFolder, {
        maxAge: '1y',
    })
);
```

### Использование абсолютных URL для HTTP (данных) запросов на сервере

В учебнике `HeroService` и `HeroSearchService` делегируют модулю Angular `HttpClient` для получения данных приложения. Эти сервисы отправляют запросы на _относительные_ URL, такие как `api/heroes`.

В приложении с рендерингом на стороне сервера, HTTP URL должны быть _абсолютными_ (например, `https://my-server.com/api/heroes`).

Это означает, что URL должны быть каким-то образом преобразованы в абсолютные при работе на сервере и оставлены относительными при работе в браузере.

Если вы используете один из пакетов `@nguniversal/*-engine` (например, `@nguniversal/express-engine`), это будет сделано автоматически. Вам не нужно ничего делать для того, чтобы относительные URL работали на сервере.

Если по какой-то причине вы не используете пакет `@nguniversal/*-engine`, вам может понадобиться сделать это самостоятельно.

Рекомендуемое решение — передавать полный URL запроса в аргумент `options` в [renderModule](https://angular.io/api/platform-server/renderModule). Этот вариант является наименее навязчивым, так как не требует изменений в приложении.

Здесь "URL запроса" относится к URL запроса, в ответ на который приложение рендерится на сервере.

Например, если клиент запросил `https://my-server.com/dashboard` и вы отображаете приложение на сервере в ответ на этот запрос, `options.url` должен быть установлен в `https://my-server.com/dashboard`.

Теперь при каждом HTTP-запросе, выполняемом в процессе рендеринга приложения на сервере, Angular сможет правильно преобразовать URL запроса в абсолютный URL, используя предоставленный `options.url`.

### Полезные скрипты

```
npm run dev:ssr
```

Аналогичен [`ng serve`](https://angular.io/cli/serve), который предлагает живую перезагрузку во время разработки, но использует рендеринг на стороне сервера. Приложение работает в сторожевом режиме и обновляет браузер после каждого изменения. Эта команда работает медленнее, чем настоящая команда `ng serve`.

```
ng build && ng run app-name:server
```

Собирает как серверный сценарий, так и приложение в производственном режиме. Используйте эту команду, когда вы хотите собрать проект для развертывания.

```
npm run serve:ssr
```

Запускает серверный скрипт для локального обслуживания приложения с рендерингом на стороне сервера. Он использует артефакты сборки, созданные командой `ng run build:ssr`, поэтому убедитесь, что вы выполнили и эту команду.

!!!note ""

    `serve:ssr` не предназначен для обслуживания вашего приложения в продакшене, а только для локального тестирования приложения с рендерингом на стороне сервера.

```
npm run prerender
```

Используется для пререндеринга страниц приложения. Подробнее о пререндеринге [здесь](prerendering.md).
