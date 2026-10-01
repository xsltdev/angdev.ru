---
description: На этой странице обсуждаются специфические для сборки параметры конфигурации для проектов Angular
---

# Создание и обслуживание приложений Angular

:date: 17.01.2023

На этой странице обсуждаются специфические для сборки параметры конфигурации для проектов Angular.

## Конфигурирование окружений приложений {#app-environments}

Вы можете определить различные именованные конфигурации сборки для вашего проекта, такие как `development` и `staging`, с различными значениями по умолчанию.

Каждая именованная конфигурация может иметь значения по умолчанию для любых опций, которые применяются к различным [builder targets](glossary.md#target), таким как `build`, `serve` и `test`. Команды [Angular CLI](https://angular.io/cli) `build`, `serve` и `test` могут затем заменить файлы на соответствующие версии для вашего целевого окружения.

### Настройка параметров по умолчанию для конкретного окружения

Используя Angular CLI, начните с выполнения команды [generate environments](https://angular.io/cli/generate#environments-command), показанной здесь, чтобы создать каталог `src/environments/` и настроить проект на использование этих файлов.

```
ng generate environments
```

Каталог `src/environments/` проекта содержит базовый конфигурационный файл `environment.ts`, который обеспечивает конфигурацию для `production`, среды по умолчанию. Вы можете переопределить значения по умолчанию для дополнительных окружений, таких как `development` и `staging`, в конфигурационных файлах для конкретной цели.

Например:

```
myProject/src/environments
+-- environment.ts
+-- environment.development.ts
+-- environment.staging.ts
```

Базовый файл `environment.ts` содержит настройки окружения по умолчанию. Например:

```ts
export const environment = {
    production: true,
};
```

Команда `build` использует его в качестве цели сборки, если окружение не указано. Вы можете добавить дополнительные переменные, либо как дополнительные свойства объекта окружения, либо как отдельные объекты.
Например, следующее добавляет значение по умолчанию для переменной в среду по умолчанию:

```ts
export const environment = {
    production: true,
    apiUrl: 'http://my-prod-url',
};
```

Вы можете добавить файлы конфигурации, специфичные для конкретной цели, такие как `environment.development.ts`. Следующее содержимое устанавливает значения по умолчанию для цели сборки разработки:

```ts
export const environment = {
    production: false,
    apiUrl: 'http://my-api-url',
};
```

### Использование переменных, специфичных для среды, в вашем приложении

Следующая структура приложения настраивает цели сборки для сред `development` и `staging`:

```
src
+-- app
    +-- app.component.html
    +-- app.component.ts
+-- environments
    +-- environment.ts
    +-- environment.development.ts
    +-- environment.staging.ts
```

Чтобы использовать определенные вами конфигурации окружения, ваши компоненты должны импортировать исходный файл окружения:

```ts
import { environment } from './../environments/environment';
```

Это гарантирует, что команды `build` и `serve` смогут найти конфигурации для конкретных целей сборки.

Следующий код в файле компонента (`app.component.ts`) использует переменную окружения, определенную в конфигурационных файлах.

```ts
import { Component } from '@angular/core';
import { environment } from './../environments/environment';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css'],
})
export class AppComponent {
    constructor() {
        // Logs false for development environment
        console.log(environment.production);
    }

    title = 'app works!';
}
```

## Настройка замены файлов для конкретной цели {#file-replacement}

Основной файл конфигурации CLI, `angular.json`, содержит секцию `fileReplacements` в конфигурации для каждой цели сборки, которая позволяет вам заменить любой файл в программе TypeScript на версию этого файла для конкретной цели. Это полезно для включения специфичного для конкретной цели кода или переменных в сборку, предназначенную для конкретной среды, такой как `production` или `staging`.

По умолчанию никакие файлы не заменяются. Вы можете добавить замену файлов для определенных целей сборки.

Например:

```json
"configurations": {
  "development": {
    "fileReplacements": [
        {
          "replace": "src/environments/environment.ts",
          "with": "src/environments/environment.development.ts"
        }
      ],
      // …
  },
}
```

Это означает, что когда вы собираете конфигурацию разработки с помощью команды `ng build --configuration development`, файл `src/environments/environment.ts` заменяется на версию файла `src/environments/environment.development.ts` для конкретной цели.

При необходимости вы можете добавить дополнительные конфигурации. Чтобы добавить окружение staging, создайте копию `src/environments/environment.ts` под названием `src/environments/environment.staging.ts`, затем добавьте конфигурацию `staging` в `angular.json`:

```json
"configurations": {
  "development": { … },
  "production": { … },
  "staging": {
    "fileReplacements": [
      {
        "replace": "src/environments/environment.ts",
        "with": "src/environments/environment.staging.ts"
      }
    ]
  }
}
```

Вы можете добавить дополнительные параметры конфигурации в эту целевую среду. Любая опция, которую поддерживает ваша сборка, может быть переопределена в целевой конфигурации сборки.

Чтобы выполнить сборку с использованием конфигурации staging, выполните следующую команду:

```shell
ng build --configuration=staging
```

Вы также можете настроить команду `serve` на использование целевой конфигурации сборки, если добавите ее в раздел `"serve:configurations"` в файле `angular.json`:

```json
"serve": {
  "builder": "@angular-devkit/build-angular:dev-server",
  "options": {
    "browserTarget": "your-project-name:build"
  },
  "configurations": {
    "development": {
      "browserTarget": "your-project-name:build:development"
    },
    "production": {
      "browserTarget": "your-project-name:build:production"
    },
    "staging": {
      "browserTarget": "your-project-name:build:staging"
    }
  }
},
```

## Настройка бюджетов размеров {#configure-size-budgets}

По мере роста функциональности приложений увеличивается и их размер. CLI позволяет установить пороговые значения размеров в конфигурации, чтобы гарантировать, что части приложения не выйдут за пределы определенных вами границ.

Определите границы размеров в конфигурационном файле CLI, `angular.json`, в разделе `budgets` для каждой [настроенной среды](#app-environments).

```json
{
    // …
    "configurations": {
        "production": {
            // …
            "budgets": []
        }
    }
}
```

Вы можете задать бюджеты размеров для всего приложения и для отдельных частей. Каждая запись бюджета настраивает бюджет определенного типа.

Укажите значения размеров в следующих форматах:

| Значение размера | Подробности                                                                           |
| :--------------- | :------------------------------------------------------------------------------------ |
| `123` или `123b` | Размер в байтах.                                                                      |
| `123kb`          | Размер в килобайтах.                                                                  |
| `123mb`          | Размер в мегабайтах.                                                                  |
| `12%`            | Процент размера относительно базового уровня. (Недействительно для базовых значений.) |

Когда вы настраиваете бюджет, система сборки предупреждает или сообщает об ошибке, когда определенная часть приложения достигает или превышает установленный вами граничный размер.

Каждая запись бюджета представляет собой объект JSON со следующими свойствами:

`type`
: Тип бюджета. Одно из:

-   `bundle` — Размер конкретного пакета.
-   `initial` — Размер JavaScript, необходимый для загрузки приложения. По умолчанию предупреждение при 500 кб и ошибка при 1 мб.
-   `allScript` — Размер всех скриптов.
-   `all` — Размер всего приложения.
-   `anyComponentStyle` — Размер таблицы стилей любого одного компонента. По умолчанию предупреждение при размере 2 кб и ошибка при размере 4 кб.
-   `anyScript` — Размер любого одного скрипта.
-   `any` — Размер любого файла.

`name`
: Имя пакета (для `type=bundle`).

`baseline`
: Базовая величина для сравнения.

`maximumWarning`
: Максимальный порог предупреждения относительно базовой величины.

`maximumError`
: Максимальный порог ошибки относительно базовой величины.

`minimumWarning`
: Минимальный порог предупреждения относительно базовой величины.

`minimumError`
: Минимальный порог ошибки относительно базовой величины.

`warning`
: Порог предупреждения относительно базовой величины (min &amp max).

`error`
: Порог ошибки относительно базовой величины (min &amp max).

## Настройка зависимостей CommonJS {#commonjs}

!!!warning ""

    Рекомендуется избегать использования модулей CommonJS в приложениях Angular. Зависимость от модулей CommonJS может помешать пакетным и минификаторам оптимизировать ваше приложение, что приведет к увеличению размера пакета.

    Вместо этого рекомендуется использовать [ECMAScript modules](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Statements/import) во всех приложениях.

    Для получения дополнительной информации смотрите [Как CommonJS делает ваши пакеты больше](https://web.dev/commonjs-larger-bundles).

Angular CLI выводит предупреждения, если обнаруживает, что ваше браузерное приложение зависит от модулей CommonJS. Чтобы отключить эти предупреждения, добавьте имя модуля CommonJS в опцию `allowedCommonJsDependencies` в опциях `build`, расположенных в файле `angular.json`.

```json
"build": {
  "builder": "@angular-devkit/build-angular:browser",
  "options": {
     "allowedCommonJsDependencies": [
        "lodash"
     ],
     // …
   },
   // …
},
```

## Настройка совместимости с браузерами {#browser-compat}

Angular CLI использует [Browserslist](https://github.com/browserslist/browserslist) для обеспечения совместимости с различными версиями браузеров. [Autoprefixer](https://github.com/postcss/autoprefixer) используется для префиксации поставщиков CSS и [@babel/preset-env](https://babeljs.io/docs/en/babel-preset-env) для преобразования синтаксиса JavaScript.

Внутри Angular CLI используется приведенная ниже конфигурация `browserslist`, которая соответствует [поддерживаемым браузерам](https://angular.io/guide/browser-support) Angular.

```
last 2 Chrome versions
last 1 Firefox version
last 2 Edge major versions
last 2 Safari major versions
last 2 iOS major versions
Firefox ESR
```

Чтобы переопределить внутреннюю конфигурацию, выполните команду [`ng generate config browserslist`](https://angular.io/cli/generate#config-command), которая создаст файл конфигурации `.browserslistrc` в каталоге проекта.

Смотрите репозиторий [browserslist repository](https://github.com/browserslist/browserslist) для более подробных примеров того, как нацеливаться на определенные браузеры и версии.

!!!note ""

    Используйте [browsersl.ist](https://browsersl.ist) для отображения совместимых браузеров для запроса `browserslist`.

## Проксирование на внутренний сервер {#proxy}

Используйте [proxying support](https://webpack.js.org/configuration/dev-server/#devserverproxy) в сервере разработки `webpack` для перенаправления определенных URL на внутренний сервер, передавая файл в опцию сборки `--proxy-config`. Например, чтобы перенаправить все обращения к `http://localhost:4200/api` на сервер, работающий на `http://localhost:3000/api`, выполните следующие действия.

1.  Создайте файл `proxy.conf.json` в папке `src/` вашего проекта.

2.  Добавьте следующее содержимое в новый файл proxy:

    ```json
    {
        "/api": {
            "target": "http://localhost:3000",
            "secure": false
        }
    }
    ```

3.  В конфигурационном файле CLI, `angular.json`, добавьте опцию `proxyConfig` к цели `serve`:

    ```json
    // …
    "architect": {
    	"serve": {
    		"builder": "@angular-devkit/build-angular:dev-server",
    		"options": {
    			"browserTarget": "your-application-name:build",
    			"proxyConfig": "src/proxy.conf.json"
    		},
    	}
    }
    // …
    ```

4.  Чтобы запустить сервер разработки с данной конфигурацией прокси, вызовите `ng serve`.

Отредактируйте файл конфигурации прокси, чтобы добавить опции конфигурации; ниже приведены примеры. Описание всех опций приведено в [документации webpack DevServer](https://webpack.js.org/configuration/dev-server/#devserverproxy).

!!!note ""

    Если вы изменили конфигурационный файл прокси, то для того, чтобы изменения вступили в силу, необходимо заново запустить процесс `ng serve`.

### Переписать путь к URL

Опция конфигурации прокси `pathRewrite` позволяет вам переписывать путь URL во время выполнения. Например, укажите следующее значение `pathRewrite` в конфигурации прокси, чтобы удалить "api" из конца пути.

```json
{
    "/api": {
        "target": "http://localhost:3000",
        "secure": false,
        "pathRewrite": {
            "^/api": ""
        }
    }
}
```

Если вам нужно получить доступ к бэкенду, который находится не на `localhost`, установите также параметр `changeOrigin`. Например:

```json
{
    "/api": {
        "target": "http://npmjs.org",
        "secure": false,
        "pathRewrite": {
            "^/api": ""
        },
        "changeOrigin": true
    }
}
```

Чтобы определить, работает ли ваш прокси как положено, установите параметр `logLevel`. Например:

```json
{
    "/api": {
        "target": "http://localhost:3000",
        "secure": false,
        "pathRewrite": {
            "^/api": ""
        },
        "logLevel": "debug"
    }
}
```

Уровни журнала прокси: `info` (по умолчанию), `debug`, `warn`, `error` и `silent`.

### Проксирование нескольких записей

Вы можете проксировать несколько записей на одну и ту же цель, определив конфигурацию в JavaScript.

Установите файл конфигурации прокси в `proxy.conf.mjs` (вместо `proxy.conf.json`), и укажите файлы конфигурации, как показано в следующем примере.

```ts
export default [
    {
        context: [
            '/my',
            '/many',
            '/endpoints',
            '/i',
            '/need',
            '/to',
            '/proxy',
        ],
        target: 'http://localhost:3000',
        secure: false,
    },
];
```

В конфигурационном файле CLI, `angular.json`, укажите на файл конфигурации JavaScript-прокси:

```json
"architect": {
  "serve": {
    "builder": "@angular-devkit/build-angular:dev-server",
    "options": {
      "browserTarget": "your-application-name:build",
      "proxyConfig": "src/proxy.conf.mjs"
    }
  }
}
```

### Обход прокси

Если вам нужно по желанию обойти прокси или динамически изменить запрос перед отправкой, добавьте опцию обхода, как показано в этом примере JavaScript.

```ts
export default {
    '/api/proxy': {
        target: 'http://localhost:3000',
        secure: false,
        bypass: function (req, res, proxyOptions) {
            if (req.headers.accept.includes('html')) {
                console.log(
                    'Skipping proxy for browser request.'
                );
                return '/index.html';
            }
            req.headers['X-Custom-Header'] = 'yes';
        },
    },
};
```

### Использование корпоративного прокси-сервера

Если вы работаете за корпоративным прокси, бэкенд не может напрямую проксировать вызовы на любой URL за пределами вашей локальной сети. В этом случае вы можете настроить внутренний прокси-сервер на перенаправление вызовов через ваш корпоративный прокси-сервер с помощью агента:

```shell
npm install --save-dev https-proxy-agent
```

Когда вы определяете переменную окружения `http_proxy` или `HTTP_PROXY`, автоматически добавляется агент для передачи вызовов через ваш корпоративный прокси при запуске `npm start`.

Используйте следующее содержание в конфигурационном файле JavaScript.

```js
import HttpsProxyAgent from 'https-proxy-agent';

const proxyConfig = [
    {
        context: '/api',
        target: 'http://your-remote-server.com:3000',
        secure: false,
    },
];

export default (proxyConfig) => {
    const proxyServer =
        process.env.http_proxy || process.env.HTTP_PROXY;
    if (proxyServer) {
        const agent = new HttpsProxyAgent(proxyServer);
        console.log(
            'Using corporate proxy server: ' + proxyServer
        );

        for (const entry of proxyConfig) {
            entry.agent = agent;
        }
    }

    return proxyConfig;
};
```

<!-- links -->

<!-- external links -->

<!-- end links -->

## Ссылки

-   [Building and serving Angular apps](https://angular.io/guide/build)
