---
description: "Встроенная защита снижает риск типичных атак на веб-приложение, включая межсайтовый скриптинг"
---

# Безопасность {: #security}

:date: 30.09.2026

Здесь — встроенная защита Angular от типичных уязвимостей и атак на веб-приложения, в том числе от межсайтового скриптинга.
Безопасность на уровне приложения, например аутентификация и авторизация, сюда не входит.

Подробнее об атаках и мерах ниже — в [руководстве Open Web Application Security Project (OWASP)](https://www.owasp.org/index.php/Category:OWASP_Guide_Project).

<a id="report-issues"></a>

!!! info "Сообщения об уязвимостях"

    Angular входит в [программу вознаграждений Google за уязвимости в открытом ПО](https://bughunters.google.com/about/rules/6521337925468160/google-open-source-software-vulnerability-reward-program-rules). Об уязвимостях в Angular сообщайте на [https://bughunters.google.com](https://bughunters.google.com/report).

    Как Google разбирает вопросы безопасности, описано в [философии безопасности Google](https://www.google.com/about/appsecurity).

## Практические приёмы {: #best-practices}

Так приложение Angular остаётся защищённее.

1.  **Держите библиотеки Angular актуальными.** Библиотеки обновляются регулярно, и в обновлениях закрывают уязвимости прошлых версий. Смотрите [журнал изменений](https://github.com/angular/angular/blob/main/CHANGELOG.md) Angular.
2.  **Не правьте свою копию Angular.** Закрытые форки отстают от текущей версии и могут не получить важные исправления и улучшения безопасности. Делитесь улучшениями с сообществом и открывайте пул-реквест.
3.  **Не вызывайте API Angular, которые в документации помечены как «_Security Risk_».** Подробнее — в разделе [Доверие к безопасным значениям](#trusting-safe-values).

## Защита от межсайтового скриптинга (XSS) {: #preventing-cross-site-scripting-xss}

[Межсайтовый скриптинг (XSS)](https://en.wikipedia.org/wiki/Cross-site_scripting) позволяет злоумышленнику внедрить вредоносный код в веб-страницы.
Такой код, например, крадёт данные пользователя и логин или действует от его имени.
Это одна из самых частых атак в вебе.

Чтобы закрыть XSS, вредоносный код не должен попасть в объектную модель документа (DOM).
Например, если злоумышленник заставит вставить в DOM тег `<script>`, он выполнит произвольный код на сайте.
Атака не ограничивается тегами `<script>`: выполнять код позволяют многие элементы и свойства DOM, например `<img alt="" onerror="...">` и `<a href="javascript:...">`.
Если в DOM попадают данные под контролем злоумышленника, ждите уязвимостей.

### Модель защиты Angular от межсайтового скриптинга {: #angulars-cross-site-scripting-security-model}

Чтобы систематически закрывать XSS, Angular по умолчанию считает все значения недоверенными.
Когда значение попадает в DOM из привязки шаблона или интерполяции, Angular санитизирует и экранирует недоверенные значения.
Если значение уже санитизировали вне Angular и оно безопасно, сообщите об этом фреймворку: [пометьте значение как доверенное](#trusting-safe-values).

В отличие от значений для отрисовки, шаблоны Angular по умолчанию считаются доверенными, и к ним нужно относиться как к исполняемому коду.
Никогда не собирайте шаблоны, склеивая пользовательский ввод и синтаксис шаблона.
Иначе злоумышленник сможет [внедрить произвольный код](https://en.wikipedia.org/wiki/Code_injection) в приложение.
Чтобы этого не было, в продакшене всегда используйте [компилятор шаблонов Ahead-Of-Time (AOT)](#use-the-aot-template-compiler) по умолчанию.

Дополнительный слой дают политика безопасности содержимого и Trusted Types.
Эти возможности веб-платформы работают на уровне DOM — там XSS закрывается эффективнее всего. Обойти их через другие, более низкоуровневые API нельзя.
Имеет смысл ими пользоваться. Настройте [политику безопасности содержимого](#content-security-policy) приложения и включите [принудительные Trusted Types](#enforcing-trusted-types).

### Санитизация и контексты безопасности {: #sanitization-and-security-contexts}

_Санитизация_ — проверка недоверенного значения и превращение его в значение, которое безопасно вставлять в DOM.
Часто санитизация значение вообще не меняет.
Она зависит от контекста.
Например, значение, безвредное в CSS, может быть опасно в URL.

Angular задаёт такие контексты безопасности:

| Контексты безопасности | Подробности                                                                           |
| :---------------- | :-------------------------------------------------------------------------------- |
| HTML              | Значение трактуется как HTML, например при привязке к `innerHtml`. |
| Style             | CSS попадает в свойство `style`.                                  |
| URL               | Свойства URL, например `<a href>`.                                      |
| Resource URL      | URL, который загружается и выполняется как код, например в `<script src>`.        |

Недоверенные значения Angular санитизирует для HTML и URL. Санитизировать URL ресурсов нельзя: в них произвольный код.
В режиме разработки Angular пишет в консоль предупреждение, если во время санитизации пришлось изменить значение.

### Пример санитизации {: #sanitization-example}

Шаблон ниже привязывает значение `htmlSnippet`. Один раз — интерполяцией в содержимое элемента, второй — привязкой к свойству `innerHTML`:

_inner-html-binding.component.html_

```html
<h3>Binding innerHTML</h3>
<p>Bound value:</p>
<p class="e2e-inner-html-interpolated">{{ htmlSnippet }}</p>
<p>Result of binding to innerHTML:</p>
<p class="e2e-inner-html-bound" [innerHTML]="htmlSnippet"></p>
```

Интерполированное содержимое всегда экранируется: HTML не интерпретируется, и браузер показывает угловые скобки в тексте элемента.

Чтобы HTML интерпретировался, привяжите его к HTML-свойству, например `innerHTML`.
Учтите: привязка к `innerHTML` значения, которым может управлять злоумышленник, обычно открывает XSS.
Например, JavaScript запускают так:

_inner-html-binding.component.ts (class)_

```ts
export class InnerHtmlBindingComponent {
  // For example, a user/attacker-controlled value from a URL.
  htmlSnippet = 'Template <script>alert("0wned")</script> <b>Syntax</b>';
}
```

Angular распознаёт значение как небезопасное и санитизирует его сам: элемент `script` удаляется, безопасное содержимое вроде `<b>` остаётся.

### Прямые вызовы DOM API и явная санитизация {: #direct-use-of-the-dom-apis-and-explicit-sanitization-calls}

Если Trusted Types не включены, встроенные DOM API браузера сами от уязвимостей не защищают.
Например, небезопасные методы есть у `document`, у узла из `ElementRef` и у многих сторонних API.
То же с библиотеками, которые меняют DOM: автоматической санитизации, как у интерполяции Angular, скорее всего не будет.
По возможности не работайте с DOM напрямую и пользуйтесь шаблонами Angular.

Если без прямого доступа не обойтись, берите встроенные функции санитизации Angular.
Недоверенные значения очищают методом [DomSanitizer.sanitize](https://angular.dev/api/platform-browser/DomSanitizer#sanitize) и подходящим `SecurityContext`.
Функция принимает и значения, помеченные как доверенные через функции `bypassSecurityTrust`, и не санитизирует их, как [описано ниже](#trusting-safe-values).

### Доверие к безопасным значениям {: #trusting-safe-values}

Иногда приложению действительно нужно включить исполняемый код, показать `<iframe>` с какого-то URL или собрать потенциально опасный URL.
Чтобы в этих случаях отключить автоматическую санитизацию, сообщите Angular, что значение проверено: понятно, как оно создано, и оно безопасно.
Будьте _осторожны_.
Доверие к значению, которое может оказаться вредоносным, вносит в приложение уязвимость.
Если есть сомнения, позовите профессионального рецензента по безопасности.

Чтобы пометить значение как доверенное, внедрите `DomSanitizer` и вызовите один из методов:

-   `bypassSecurityTrustHtml`
-   `bypassSecurityTrustScript`
-   `bypassSecurityTrustStyle`
-   `bypassSecurityTrustUrl`
-   `bypassSecurityTrustResourceUrl`

Безопасность значения зависит от контекста, поэтому выбирайте контекст под то, как значение будет использовано.
Допустим, шаблону ниже нужно привязать URL к вызову `javascript:alert(...)`:

_bypass-security.component.html (URL)_

```html
<h4>An untrusted URL:</h4>
<p><a class="e2e-dangerous-url" [href]="dangerousUrl">Click me</a></p>
<h4>A trusted URL:</h4>
<p><a class="e2e-trusted-url" [href]="trustedUrl">Click me</a></p>
```

Обычно Angular сам санитизирует URL, отключает опасный код и в режиме разработки пишет об этом в консоль.
Чтобы этого не было, пометьте URL как доверенный вызовом `bypassSecurityTrustUrl`:

_bypass-security.component.ts (trust-url)_

```ts
import {Component, inject} from '@angular/core';
import {DomSanitizer, SafeResourceUrl, SafeUrl} from '@angular/platform-browser';

@Component({
  selector: 'app-bypass-security',
  templateUrl: './bypass-security.component.html',
})
export class BypassSecurityComponent {
  dangerousUrl: string;
  trustedUrl: SafeUrl;
  dangerousVideoUrl!: string;
  videoUrl!: SafeResourceUrl;

  // #docregion trust-url
  private sanitizer = inject(DomSanitizer);
  constructor() {
    // javascript: URLs are dangerous if attacker controlled.
    // Angular sanitizes them in data binding, but you can
    // explicitly tell Angular to trust this value:
    this.dangerousUrl = 'javascript:alert("Hi there")';
    this.trustedUrl = this.sanitizer.bypassSecurityTrustUrl(this.dangerousUrl);
    // #enddocregion trust-url
    this.updateVideoUrl('PUBnlbjZFAI');
  }

  // #docregion trust-video-url
  updateVideoUrl(id: string) {
    // Appending an ID to a YouTube URL is safe.
    // Always make sure to construct SafeValue objects as
    // close as possible to the input data so
    // that it's easier to check if the value is safe.
    this.dangerousVideoUrl = 'https://www.youtube.com/embed/' + id;
    this.videoUrl = this.sanitizer.bypassSecurityTrustResourceUrl(this.dangerousVideoUrl);
  }
  // #enddocregion trust-video-url
}
```

Если пользовательский ввод нужно превратить в доверенное значение, делайте это методом компонента.
Шаблон ниже даёт ввести идентификатор ролика YouTube и загрузить ролик в `<iframe>`.
Атрибут `<iframe src>` — контекст безопасности URL ресурса: недоверенный источник может, например, протащить скачивание файла, который пользователь запустит.
Чтобы этого не было, доверенный URL ролика собирает метод компонента, и тогда Angular разрешает привязку к `<iframe src>`:

_bypass-security.component.html (iframe)_

```html
<h4>Resource URL:</h4>
<p>Showing: {{ dangerousVideoUrl }}</p>
<p>Trusted:</p>
<iframe
  class="e2e-iframe-trusted-src"
  width="640"
  height="390"
  [src]="videoUrl"
  title="trusted video url"
></iframe>
<p>Untrusted:</p>
<iframe
  class="e2e-iframe-untrusted-src"
  width="640"
  height="390"
  [src]="dangerousVideoUrl"
  title="unTrusted video url"
></iframe>
```

_bypass-security.component.ts (trust-video-url)_

```ts
import {Component, inject} from '@angular/core';
import {DomSanitizer, SafeResourceUrl, SafeUrl} from '@angular/platform-browser';

@Component({
  selector: 'app-bypass-security',
  templateUrl: './bypass-security.component.html',
})
export class BypassSecurityComponent {
  dangerousUrl: string;
  trustedUrl: SafeUrl;
  dangerousVideoUrl!: string;
  videoUrl!: SafeResourceUrl;

  // #docregion trust-url
  private sanitizer = inject(DomSanitizer);
  constructor() {
    // javascript: URLs are dangerous if attacker controlled.
    // Angular sanitizes them in data binding, but you can
    // explicitly tell Angular to trust this value:
    this.dangerousUrl = 'javascript:alert("Hi there")';
    this.trustedUrl = this.sanitizer.bypassSecurityTrustUrl(this.dangerousUrl);
    // #enddocregion trust-url
    this.updateVideoUrl('PUBnlbjZFAI');
  }

  // #docregion trust-video-url
  updateVideoUrl(id: string) {
    // Appending an ID to a YouTube URL is safe.
    // Always make sure to construct SafeValue objects as
    // close as possible to the input data so
    // that it's easier to check if the value is safe.
    this.dangerousVideoUrl = 'https://www.youtube.com/embed/' + id;
    this.videoUrl = this.sanitizer.bypassSecurityTrustResourceUrl(this.dangerousVideoUrl);
  }
  // #enddocregion trust-video-url
}
```

### Политика безопасности содержимого {: #content-security-policy}

Политика безопасности содержимого (CSP) — это защита в глубину от XSS.
Чтобы включить CSP, настройте веб-сервер: он должен отдавать подходящий HTTP-заголовок `Content-Security-Policy`.
Подробнее о политике — в [руководстве Web Fundamentals](https://developers.google.com/web/fundamentals/security/csp) на сайте Google Developers.

Минимальная политика для нового приложения Angular:

```text
default-src 'self'; style-src 'self' 'nonce-randomNonceGoesHere'; script-src 'self' 'nonce-randomNonceGoesHere';
```

Когда сервер отдаёт приложение Angular, в HTTP-заголовок каждого запроса нужно вкладывать случайно сгенерированный nonce.
Этот nonce передают Angular, чтобы фреймворк мог отрисовать элементы `<style>`.
Nonce для Angular задают одним из способов:

1.  Атрибут `ngCspNonce` на корневом элементе приложения: `<app ngCspNonce="randomNonceGoesHere"></app>`. Так делают, если серверный шаблон может добавить nonce и в заголовок, и в `index.html` при сборке ответа.
1.  Токен инъекции `CSP_NONCE`. Так делают, если nonce доступен во время выполнения и `index.html` нужно кэшировать.

```ts
import {CSP_NONCE} from '@angular/core';
import {bootstrapApplication} from '@angular/platform-browser';
import {AppComponent} from './app/app.component';

bootstrapApplication(AppComponent, {
  providers: [
    {
      provide: CSP_NONCE,
      useValue: globalThis.myRandomNonceValue,
    },
  ],
});
```

!!! info "Уникальные nonce"

    Nonce должны быть **уникальны для каждого запроса**, и их нельзя предсказать или угадать.
    Если злоумышленник предскажет будущие nonce, он обойдёт защиту CSP.

    Генерировать nonce на исходном сервере при работе через CDN обычно не стоит: ответы часто кэшируются. Если сервер создал nonce, а CDN закэшировала этот HTML, каждый следующий посетитель получает то же «уникальное» значение. Злоумышленник узнаёт статическое значение и обходит CSP.

    Чтобы nonce оставался одноразовым, его лучше создавать на границе (например, в CDN) непосредственно перед выдачей содержимого пользователю.

!!! info ""

    Если нужно [встроить критический CSS](https://angular.dev/tools/cli/build#critical-css-inlining) приложения, токен `CSP_NONCE` не подойдёт. Берите параметр `security.autoCsp` в [конфигурации рабочего пространства](https://angular.dev/reference/configs/workspace-config#extra-build-and-test-options) или атрибут `ngCspNonce` на корневом элементе приложения.

Если nonce в проекте генерировать нельзя, встроенные стили разрешают, добавив `'unsafe-inline'` в секцию `style-src` заголовка CSP.

| Секции                                         | Подробности                                                                                                                                                                                                                                                                                                                                                  |
| :----------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `default-src 'self';`                            | Страница загружает все нужные ресурсы с того же источника.                                                                                                                                                                                                                                                                                 |
| `style-src 'self' 'nonce-randomNonceGoesHere';`  | Страница загружает глобальные стили с того же источника (`'self'`) и стили, которые Angular вставил с `nonce-randomNonceGoesHere`.                                                                                                                                                                                                             |
| `script-src 'self' 'nonce-randomNonceGoesHere';` | Страница загружает JavaScript с того же источника (`'self'`) и скрипты, которые Angular CLI вставил с `nonce-randomNonceGoesHere`. Нужно только если включены встраивание критического CSS или целостность подресурсов (они добавляют карту импортов, чтобы проверять динамически импортируемые чанки): оба варианта добавляют встроенные скрипты в `index.html`. |

Самому Angular для корректной работы хватает этих настроек.
По мере роста проекта CSP, скорее всего, придётся расширить под возможности конкретного приложения.

#### Статический хостинг без nonce на каждый ответ {: #static-hosting-without-per-response-nonces}

Если хостинг или CDN умеет подменять токен-заполнитель в закэшированном HTML на границе (например, через SSI, ESI или граничную функцию), соберите `index.html` с заполнителем в `ngCspNonce` (например, `<app ngCspNonce="__CSP_NONCE__"></app>`) и подставляйте уникальный nonce в каждый ответ.

Если приложение лежит на статическом хосте, который отдаёт `index.html` как есть, без преобразования на границе, не зашивайте статический nonce. Берите один из подходов ниже.

##### Хеш встроенных скриптов через `autoCsp` {: #hash-inline-scripts-with-autocsp}

Поставьте `security.autoCsp` в `true` в [конфигурации рабочего пространства](https://angular.dev/reference/configs/workspace-config#extra-build-and-test-options).
На сборке Angular CLI считает хеш каждого встроенного скрипта в `index.html`, включая скрипты от встраивания критического CSS и целостности подресурсов.
CLI заменяет элементы `<script src>` скриптом-загрузчиком с хешем и добавляет тег `<meta>` в начало `<head>`:

```text
script-src 'strict-dynamic' 'sha256-...' https: 'unsafe-inline'; object-src 'none'; base-uri 'self';
```

Хеши зависят только от содержимого скриптов, поэтому `index.html` остаётся верным для каждого посетителя и его можно кэшировать.
Браузеры, которые поддерживают хеши и `'strict-dynamic'`, игнорируют запасные источники `https:` и `'unsafe-inline'`.

У политики, которую собрал `autoCsp`, есть ограничения:

-   Она покрывает только скрипты. `style-src` настраивают отдельно.
-   Браузер игнорирует часть директив, например `frame-ancestors`, `report-uri` и `sandbox`, если они стоят в теге `<meta>`. Такие директивы отправляйте в HTTP-заголовке `Content-Security-Policy`.
-   Если у страницы несколько политик, браузер применяет все. Если CSP-заголовок тоже отправляется, уберите из него и `script-src`, и `default-src`, чтобы они не блокировали встроенные скрипты с хешем.
-   `autoCsp` нельзя совместить с серверным рендерингом.

##### Без встроенных скриптов {: #avoid-inline-scripts}

Angular CLI добавляет встроенные скрипты в `index.html` только для встраивания критического CSS и целостности подресурсов (карта импортов несёт метаданные целостности динамических импортов модулей).
Если `optimization.styles.inlineCritical` равен `false` и `subresourceIntegrity` выключен, в `index.html` нет встроенных скриптов. Тогда в заголовке `Content-Security-Policy` достаточно `script-src 'self'`.

!!! info ""

    Если выключить встраивание критического CSS, первая отрисовка приложения может замедлиться, а без целостности подресурсов пропадут проверки целостности скриптов.

##### Стили для статического хостинга {: #configure-styles-for-static-hosting}

Angular во время выполнения вставляет элементы `<style>` для стилей компонентов, а встраивание критического CSS добавляет элемент `<style>` в `index.html`.
Ни `autoCsp`, ни отказ от встроенных скриптов эти стили не покрывают. Без nonce на каждый ответ разрешите их, добавив `'unsafe-inline'` в `style-src`.
Например, если сборка обходится без встроенных скриптов, хост должен отправлять такой заголовок:

```text
default-src 'self'; style-src 'self' 'unsafe-inline';
```

С `autoCsp` отправляйте `style-src 'self' 'unsafe-inline'` в HTTP-заголовке без `default-src` и `script-src`.

Код приложения и сторонние библиотеки в обоих случаях могут потребовать дополнительные директивы.

### Принудительные Trusted Types {: #enforcing-trusted-types}

[Trusted Types](https://w3c.github.io/trusted-types/dist/spec/) стоит включать как ещё одну защиту от межсайтового скриптинга.
Trusted Types — возможность [веб-платформы](https://en.wikipedia.org/wiki/Web_platform), которая снижает риск XSS за счёт более безопасных приёмов в коде.
Trusted Types также упрощают аудит кода приложения.

!!! info "Trusted Types"

    Trusted Types могут быть ещё не во всех браузерах, на которые рассчитано приложение.
    Если приложение с Trusted Types открыто в браузере без их поддержки, возможности приложения сохраняются. От XSS его по-прежнему защищает `DomSanitizer` Angular.
    Текущая поддержка браузерами — на [caniuse.com/trusted-types](https://caniuse.com/trusted-types).

Чтобы включить Trusted Types, веб-сервер приложения должен отдавать HTTP-заголовки с одной из политик Angular:

| Политики                 | Подробности                                                                                                                                                                                                                                                                                     |
| :----------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `angular`                | Политика для кода внутри Angular, который прошёл рецензию по безопасности. Нужна, чтобы Angular работал при принудительных Trusted Types. Встроенные значения шаблонов и содержимое, которое санитизировал Angular, эта политика считает безопасными.                                          |
| `angular#bundler`        | Политика сборщика Angular CLI, когда он создаёт файлы ленивых чанков.                                                                                                                                                                                                             |
| `angular#unsafe-bypass`  | Политика для приложений, которые вызывают методы [DomSanitizer](https://angular.dev/api/platform-browser/DomSanitizer), обходящие защиту, например `bypassSecurityTrustHtml`. Если такие методы есть, политику нужно включить.                                  |
| `angular#unsafe-jit`     | Политика [компилятора Just-In-Time (JIT)](https://angular.dev/api/core/Compiler). Включайте её, если приложение напрямую работает с JIT-компилятором или запущено в режиме JIT через [`platformBrowserDynamic`](https://angular.dev/api/platform-browser-dynamic/platformBrowserDynamic). |
| `angular#unsafe-upgrade` | Политика пакета [@angular/upgrade](https://angular.dev/api/upgrade/static/UpgradeModule). Включайте её, если приложение — гибрид с AngularJS.                                                                                                                           |

HTTP-заголовки для Trusted Types настраивают в таких местах:

-   Продакшен-инфраструктура, которая отдаёт приложение
-   Angular CLI (`ng serve`), свойство `headers` в файле `angular.json` — для локальной разработки и сквозных тестов
-   Karma (`ng test`), свойство `customHeaders` в файле `karma.config.js` — для модульных тестов

Пример заголовка именно под Trusted Types и Angular:

```html
Content-Security-Policy: trusted-types angular; require-trusted-types-for 'script';
```

Пример заголовка под Trusted Types и приложения Angular, которые вызывают методы [DomSanitizer](https://angular.dev/api/platform-browser/DomSanitizer), обходящие защиту:

```html
Content-Security-Policy: trusted-types angular angular#unsafe-bypass; require-trusted-types-for
'script';
```

Пример заголовка под Trusted Types и приложения Angular на JIT:

```html
Content-Security-Policy: trusted-types angular angular#unsafe-jit; require-trusted-types-for
'script';
```

Пример заголовка под Trusted Types и приложения Angular с ленивой загрузкой модулей:

```html
Content-Security-Policy: trusted-types angular angular#bundler; require-trusted-types-for 'script';
```

!!! info "Материалы сообщества"

    При разборе конфигурации Trusted Types может пригодиться материал:

    [Как Trusted Types закрывают межсайтовый скриптинг через DOM](https://web.dev/trusted-types/#how-to-use-trusted-types)

### Компилятор шаблонов AOT {: #use-the-aot-template-compiler}

Компилятор шаблонов AOT закрывает целый класс уязвимостей — внедрение шаблона — и заметно ускоряет приложение.
В приложениях Angular CLI компилятор AOT используется по умолчанию, и в продакшене стоит оставлять его.

Альтернатива — компилятор JIT: он компилирует шаблоны в исполняемый код шаблона в браузере во время выполнения.
Angular доверяет коду шаблона, поэтому динамическая сборка и компиляция шаблонов, особенно с пользовательскими данными, обходит встроенную защиту. Это антипаттерн безопасности.
Как безопасно собирать формы динамически, описано в руководстве [Динамические формы](https://angular.dev/guide/forms/dynamic-forms).

### Защита от XSS на сервере {: #server-side-xss-protection}

HTML, собранный на сервере, уязвим к внедрению.
Внедрить код шаблона в приложение Angular — то же самое, что внедрить исполняемый код:
у злоумышленника полный контроль над приложением.
Чтобы этого не было, на сервере берите язык шаблонов, который сам экранирует значения и закрывает XSS.
Не создавайте шаблоны Angular на сервере языком шаблонов. Риск внедрения шаблона здесь высокий.

## Уязвимости на уровне HTTP {: #http-level-vulnerabilities}

В Angular есть встроенная помощь против двух частых HTTP-уязвимостей: межсайтовой подделки запроса (CSRF или XSRF) и включения межсайтового скрипта (XSSI).
Обе в первую очередь закрывают на сервере, но Angular даёт средства, чтобы проще связать это с клиентом.

### Межсайтовая подделка запроса {: #cross-site-request-forgery}

При межсайтовой подделке запроса (CSRF или XSRF) злоумышленник заманивает пользователя на другую страницу (например, `evil.com`) с вредоносным кодом. Страница тайно отправляет злонамеренный запрос на сервер приложения (например, `example-bank.com`).

Допустим, пользователь вошёл в приложение на `example-bank.com`.
Он открывает письмо и переходит по ссылке на `evil.com`, которая открывается в новой вкладке.

Страница `evil.com` сразу шлёт злонамеренный запрос на `example-bank.com`.
Например, это перевод денег со счёта пользователя на счёт злоумышленника.
Браузер автоматически прикладывает к запросу куки `example-bank.com`, включая куку аутентификации.

Если на сервере `example-bank.com` нет защиты от XSRF, он не отличит законный запрос приложения от поддельного запроса с `evil.com`.

Чтобы этого не было, приложение должно убедиться, что запрос пользователя пришёл из настоящего приложения, а не с другого сайта.
Сервер и клиент действуют вместе.

В распространённом приёме против XSRF сервер приложения отправляет случайно созданный токен аутентификации в куке.
Клиентский код читает куку и во все следующие запросы добавляет свой заголовок с токеном.
Сервер сравнивает значение куки со значением заголовка и отклоняет запрос, если значений нет или они не совпали.

Приём работает, потому что все браузеры соблюдают _политику одного источника_.
Читать куки сайта и ставить свои заголовки на запросы к этому сайту может только код с того сайта, где куки заданы.
Значит, прочитать токен из куки и поставить свой заголовок может только ваше приложение.
Вредоносный код на `evil.com` этого не может.

### Защита `HttpClient` от XSRF/CSRF {: #httpclient-xsrfcsrf-security}

`HttpClient` поддерживает [распространённый механизм](https://en.wikipedia.org/wiki/Cross-site_request_forgery#Cookie-to-header_token) против атак XSRF. При HTTP-запросе перехватчик читает токен из куки, по умолчанию `XSRF-TOKEN`, и ставит его в HTTP-заголовок `X-XSRF-TOKEN`. Куку может прочитать только код вашего домена, поэтому сервер уверен, что запрос пришёл от клиентского приложения, а не от злоумышленника.

По умолчанию перехватчик отправляет этот заголовок со всеми мутирующими запросами (например, `POST`) на относительные URL и URL того же источника, но не с запросами `GET` и `HEAD`.

!!! tip "Почему не защищать запросы GET?"

    Защита от CSRF нужна только запросам, которые меняют состояние на сервере. Атаки CSRF пересекают границы домена, а [политика одного источника](https://developer.mozilla.org/docs/Web/Security/Same-origin_policy) не даёт атакующей странице прочитать результат аутентифицированных запросов `GET`.

Чтобы этим пользоваться, сервер должен записать токен в сессионную куку `XSRF-TOKEN`, которую может прочитать JavaScript, — при загрузке страницы или при первом GET-запросе. В следующих запросах сервер проверяет, что кука совпадает с HTTP-заголовком `X-XSRF-TOKEN`, и так убеждается, что запрос мог отправить только код вашего домена. Токен должен быть уникален для каждого пользователя, и сервер должен уметь его проверить: иначе клиент сможет выдумать свой токен. Для дополнительной защиты сделайте токен дайджестом куки аутентификации сайта с солью.

Чтобы не было коллизий, когда несколько приложений Angular делят домен или поддомен, дайте каждому приложению своё имя куки.

!!! warning "HttpClient закрывает только клиентскую половину схемы защиты от XSRF"

    Сервер должен ставить куку для страницы и проверять, что заголовок есть у всех подходящих запросов. Без этого защита Angular по умолчанию не работает.

### Свои имена куки и заголовка {: #configure-custom-cookieheader-names}

Если сервер называет куку или заголовок токена XSRF иначе, значения по умолчанию перекрывают через `withXsrfConfiguration`.

Добавьте его в вызов `provideHttpClient`:

```ts
export const appConfig: ApplicationConfig = {
  providers: [
    provideHttpClient(
      withXsrfConfiguration({
        cookieName: 'CUSTOM_XSRF_TOKEN',
        headerName: 'X-Custom-Xsrf-Header',
      }),
    ),
  ],
};
```

### Отключение защиты от XSRF {: #disabling-xsrf-protection}

Если встроенная защита от XSRF приложению не подходит, её отключают возможностью `withNoXsrfProtection`:

```ts
export const appConfig: ApplicationConfig = {
  providers: [provideHttpClient(withNoXsrfProtection())],
};
```

О CSRF в Open Web Application Security Project (OWASP) — [межсайтовая подделка запроса (CSRF)](https://owasp.org/www-community/attacks/csrf) и [памятка по защите от межсайтовой подделки запроса (CSRF)](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html).
Подробный разбор — в статье Стэнфорда [«Надёжная защита от межсайтовой подделки запроса»](https://seclab.stanford.edu/websec/csrf/csrf.pdf).

Смотрите также [доклад Dave Smith про XSRF на AngularConnect 2016](https://www.youtube.com/watch?v=9inczw6qtpY 'Cross Site Request Funkery Securing Your Angular Apps From Evil Doers').

### Включение межсайтового скрипта (XSSI) {: #cross-site-script-inclusion-xssi}

Включение межсайтового скрипта, также известное как уязвимость JSON, позволяет сайту злоумышленника прочитать данные из JSON API.
На старых браузерах атака подменяет встроенные конструкторы объектов JavaScript, а затем подключает URL API тегом `<script>`.

Атака удаётся, только если возвращённый JSON исполняется как JavaScript.
Сервер предотвращает атаку, добавляя ко всем JSON-ответам префикс, который делает их неисполняемыми. По соглашению это известная строка `")]}',\n"`.

Библиотека `HttpClient` в Angular знает это соглашение и перед дальнейшим разбором сама срезает строку `")]}',\n"` из всех ответов.

Подробнее — в разделе XSSI этой [заметки блога Google о веб-безопасности](https://security.googleblog.com/2011/05/website-security-for-webmasters.html).

## Защита от подделки запроса на стороне сервера (SSRF) {: #preventing-server-side-request-forgery-ssrf}

Angular строго проверяет заголовки `Host`, `Forwarded`, `X-Forwarded-Host`, `X-Forwarded-Proto`, `X-Forwarded-Prefix` и `X-Forwarded-Port` в конвейере обработки запроса, чтобы закрыть [подделку запроса на стороне сервера (SSRF)](https://developer.mozilla.org/en-US/docs/Web/Security/Attacks/SSRF) через заголовки.

Правила проверки:

-   `Host`, `X-Forwarded-Host` и параметр `host` заголовка `Forwarded` сверяются со строгим белым списком и не могут содержать разделители пути.
-   Заголовок `X-Forwarded-Port` должен быть числом.
-   Заголовок `X-Forwarded-Proto` и параметр `proto` заголовка `Forwarded` должны быть `http` или `https`.
-   Заголовок `X-Forwarded-Prefix` должен начинаться с `/` и содержать только буквы, цифры, дефисы и подчёркивания, разделённые одиночными слэшами.
-   По умолчанию заголовок `Forwarded` и все заголовки `X-Forwarded-*` считаются недоверенными и удаляются из запроса. Чтобы их оставить, их нужно явно разрешить через `trustProxyHeaders`.

Некорректные заголовки пишутся в журнал ошибок, а недопущенные прокси-заголовки удаляются из запроса. Запросы с нераспознанным именем хоста получают `400 Bad Request`.

!!! info ""

    Большинство облачных провайдеров и CDN проверяют эти заголовки сами, ещё до того как запрос дойдёт до источника приложения. Такая фильтрация сильно сужает практическую поверхность атаки.

### Разрешённые хосты {: #configuring-allowed-hosts}

Чтобы разрешить конкретные имена хостов, их добавляют в белый список. Это важно, чтобы приложение в развёртывании работало и корректно, и безопасно. В шаблонах допустимы подстановки, чтобы гибко сопоставлять имена хостов.

Параметр `allowedHosts` задают в `angular.json`:

```json
{
  // ...
  "projects": {
    "your-project-name": {
      // ...
      "architect": {
        "build": {
          "builder": "@angular/build:application",
          "options": {
            "security": {
              "allowedHosts": [
                "example.com",
                "*.example.com" // allows all subdomains of example.com
              ]
            }
            // ... other options
          }
        }
      }
    }
  }
}
```

`allowedHosts` можно задать и при создании движка приложения:

```ts
const appEngine = new AngularAppEngine({
  allowedHosts: ['example.com', '*.trusted-example.com'],
});

const nodeAppEngine = new AngularNodeAppEngine({
  allowedHosts: ['example.com', '*.trusted-example.com'],
});
```

Для варианта Node.js `AngularNodeAppEngine` хосты можно разрешить переменной окружения `NG_ALLOWED_HOSTS` (список через запятую).

```bash
export NG_ALLOWED_HOSTS="example.com,*.trusted-example.com"
```

!!! warning ""

    Значение `*` в `allowedHosts` разрешает все имена хостов. Так делать обычно не стоит: это риск для безопасности. Приём любого заголовка хоста открывает приложение для внедрения заголовка хоста и атак [подделки запроса на стороне сервера (SSRF)](https://developer.mozilla.org/en-US/docs/Web/Security/Attacks/SSRF). Такая настройка уместна, только если заголовки `Host` и `X-Forwarded-Host` проверяет другой слой, например балансировщик или обратный прокси. Для лучшей защиты по возможности держите явный список разрешённых хостов. Подробнее — в [GHSA-x288-3778-4hhx](https://github.com/angular/angular-cli/security/advisories/GHSA-x288-3778-4hhx).

### Доверенные прокси-заголовки {: #configuring-trusted-proxy-headers}

По умолчанию Angular игнорирует стандартный заголовок `Forwarded` и все заголовки `X-Forwarded-*`. Если приложение стоит за доверенным обратным прокси (например, балансировщиком), который эти заголовки ставит, Angular можно научить им доверять.

Если заголовок `Forwarded` доверенный, из него извлекаются параметры `host` и `proto`, и они важнее соответствующих заголовков `x-forwarded-host` и `x-forwarded-proto`.

`trustProxyHeaders` задают при создании движка приложения:

```ts
const appEngine = new AngularAppEngine({
  trustProxyHeaders: ['forwarded'], // Trust the standard Forwarded header
});

const appEngine = new AngularAppEngine({
  trustProxyHeaders: ['x-forwarded-host', 'x-forwarded-proto'], // Trust non-standard headers
});

const nodeAppEngine = new AngularNodeAppEngine({
  trustProxyHeaders: true, // Trust standard Forwarded and all X-Forwarded-* headers
});
```

Для варианта Node.js `AngularNodeAppEngine` те же заголовки разрешает переменная окружения `NG_TRUST_PROXY_HEADERS` (список заголовков через запятую).

```bash
export NG_TRUST_PROXY_HEADERS="X-FORWARDED-HOST,X-FORWARDED-PREFIX"
```

!!! warning ""

    Включайте `trustProxyHeaders`, только если приложение стоит за доверенным прокси, который строго проверяет или перезаписывает эти заголовки. Иначе злоумышленник подделает заголовки и устроит атаку [подделки запроса на стороне сервера (SSRF)](https://developer.mozilla.org/en-US/docs/Web/Security/Attacks/SSRF).

## Аудит приложений Angular {: #auditing-angular-applications}

Приложения Angular следуют тем же принципам безопасности, что и обычные веб-приложения, и аудит у них такой же.
API, специфичные для Angular, которые стоит проверить на рецензии по безопасности, например методы [_bypassSecurityTrust_](#trusting-safe-values), в документации помечены как чувствительные с точки зрения безопасности.


---

Источник: [https://angular.dev/best-practices/security](https://angular.dev/best-practices/security)
