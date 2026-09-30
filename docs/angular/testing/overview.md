---
description: "Модульные тесты проверяют, что приложение работает как задумано, и помогают ловить ошибки до рефакторинга"
---

# Модульное тестирование {: #unit-testing}

:date: 30.09.2026

Тесты проверяют, что приложение Angular работает так, как ожидается. Модульные тесты рано ловят ошибки, держат качество кода и позволяют безопасно рефакторить.

!!! info ""

    Здесь — настройка тестов по умолчанию для новых проектов Angular CLI на Vitest. Если существующий проект переезжает с Karma, смотрите [руководство по переходу с Karma на Vitest](https://angular.dev/guide/testing/migrating-to-vitest). Karma по-прежнему поддерживается; подробнее — в [руководстве по тестам на Karma](https://angular.dev/guide/testing/karma).

## Подготовка к тестам {: #set-up-for-testing}

Angular CLI скачивает и ставит всё, что нужно для тестов приложения на [фреймворке Vitest](https://vitest.dev). В новых проектах `vitest` и `jsdom` уже есть.

Vitest запускает модульные тесты в среде Node.js. DOM браузера имитирует библиотека `jsdom`, поэтому тесты идут быстрее: браузер не поднимается. `jsdom` можно заменить, например, на `happy-dom`: поставить его и удалить `jsdom`. Сейчас поддерживаются именно `jsdom` и `happy-dom`.

Проект, созданный через CLI, сразу готов к тестам. Запустите команду [`ng test`](https://angular.dev/cli/test):

```shell
ng test
```

Команда `ng test` собирает приложение в _режиме наблюдения_ и запускает [раннер Vitest](https://vitest.dev).

Вывод в консоли выглядит так:

```shell
 ✓ src/app/app.spec.ts (3)
   ✓ AppComponent should create the app
   ✓ AppComponent should have as title 'my-app'
   ✓ AppComponent should render title
 Test Files  1 passed (1)
      Tests  3 passed (3)
   Start at  18:18:01
   Duration  2.46s (transform 615ms, setup 2ms, collect 2.21s, tests 5ms)
```

`ng test` также следит за файлами. Если файл изменить и сохранить, тесты запустятся снова.

## Конфигурация {: #configuration}

Большую часть конфигурации Vitest берёт на себя Angular CLI. Поведение тестов меняют параметрами цели `test` в файле `angular.json`.

### Параметры `angular.json` {: #angularjson-options}

-   `include` — шаблоны glob файлов, которые попадают в тесты. По умолчанию `['**/*.spec.ts', '**/*.test.ts']`.
-   `exclude` — шаблоны glob файлов, которые из тестов исключают.
-   `setupFiles` — пути к глобальным файлам подготовки (например, полифилы или глобальные моки). Они выполняются до тестов.
-   `providersFile` — путь к файлу, который экспортирует массив провайдеров Angular для тестовой среды по умолчанию. Удобно для глобальных тестовых провайдеров, которые внедряются в тесты.
-   `coverage` — логический флаг, включает или выключает отчёт о покрытии кода. По умолчанию `false`.
-   `browsers` — массив имён браузеров, чтобы гонять тесты в настоящем браузере (например, `["chromium"]`). Нужен установленный провайдер браузера. Подробнее — в разделе [Запуск тестов в браузере](#running-tests-in-a-browser).

### Глобальная подготовка и провайдеры {: #global-test-setup-and-providers}

Параметры `setupFiles` и `providersFile` особенно удобны для общей конфигурации тестов.

Например, файл `src/test-providers.ts` может отдать `provideHttpClientTesting` всем тестам:

_src/test-providers.ts_

```ts
import {EnvironmentProviders, Provider} from '@angular/core';
import {provideHttpClientTesting} from '@angular/common/http/testing';

const testProviders: (Provider | EnvironmentProviders)[] = [provideHttpClientTesting()];

export default testProviders;
```

Дальше файл указывают в `angular.json`:

```json
{
  "projects": {
    "your-project-name": {
      "architect": {
        "test": {
          "builder": "@angular/build:unit-test",
          "options": {
            "providersFile": "src/test-providers.ts"
          }
        }
      }
    }
  }
}
```

!!! tip ""

    Новые файлы TypeScript для подготовки тестов или провайдеров, например `src/test-providers.ts`, должны входить в тестовую конфигурацию TypeScript проекта (обычно `tsconfig.spec.json`). Тогда компилятор TypeScript обработает их во время тестов.

### Расширенная конфигурация Vitest {: #advanced-vitest-configuration}

Для сложных случаев свой файл конфигурации Vitest подключают параметром `runnerConfig` в `angular.json`.

!!! warning ""

    Своя конфигурация открывает дополнительные параметры, но команда Angular не поддерживает содержимое этого файла и сторонние плагины. CLI также перезаписывает отдельные свойства (`test.projects`, `test.include`), чтобы интеграция оставалась корректной.

Файл конфигурации Vitest (например, `vitest-base.config.ts`) создают и указывают в `angular.json`:

```json
{
  "projects": {
    "your-project-name": {
      "architect": {
        "test": {
          "builder": "@angular/build:unit-test",
          "options": {
            "runnerConfig": "vitest-base.config.ts"
          }
        }
      }
    }
  }
}
```

Базовый файл можно сгенерировать через CLI:

```shell
ng generate config vitest
```

Команда создаёт `vitest-base.config.ts`, который дальше настраивают под себя.

!!! tip ""

    Подробнее о конфигурации Vitest — в [официальной документации Vitest](https://vitest.dev/config/).

## Покрытие кода {: #code-coverage}

Отчёт о покрытии кода получают флагом `--coverage` у команды `ng test`. Отчёт появляется в каталоге `coverage/`.

Подробнее — в [руководстве по покрытию кода](https://angular.dev/guide/testing/code-coverage).

## Запуск тестов в браузере {: #running-tests-in-a-browser}

Среда Node.js по умолчанию быстрее для большинства модульных тестов, но тесты можно запускать и в настоящем браузере. Это нужно, когда тест опирается на API браузера (например, отрисовку) или когда его отлаживают.

Сначала ставят провайдер браузера. Режим браузера Vitest описан в [официальной документации](https://vitest.dev/guide/browser).

После установки провайдера тесты в браузере включают параметром `browsers` в `angular.json` или флагом CLI `--browsers`. По умолчанию браузер запускается с интерфейсом. Если задана переменная окружения `CI`, используется режим headless. Чтобы управлять headless явно, к имени браузера добавляют суффикс `Headless` (например, `chromiumHeadless`).

```bash
# Example for Playwright (headed)
ng test --browsers=chromium

# Example for Playwright (headless)
ng test --browsers=chromiumHeadless

# Example for WebdriverIO (headed)
ng test --browsers=chrome

# Example for WebdriverIO (headless)
ng test --browsers=chromeHeadless
```

Дальше выбирают провайдер браузера под задачу.

### Playwright {: #playwright}

[Playwright](https://playwright.dev/) — библиотека автоматизации браузера. Поддерживает Chromium, Firefox и WebKit.

=== "npm"

    ```shell
    npm install --save-dev @vitest/browser-playwright playwright
    ```

=== "yarn"

    ```shell
    yarn add --dev @vitest/browser-playwright playwright
    ```

=== "pnpm"

    ```shell
    pnpm add -D @vitest/browser-playwright playwright
    ```

=== "bun"

    ```shell
    bun add --dev @vitest/browser-playwright playwright
    ```

### WebdriverIO {: #webdriverio}

[WebdriverIO](https://webdriver.io/) — фреймворк автоматизации браузера и мобильных приложений. Поддерживает Chrome, Firefox, Safari и Edge.

=== "npm"

    ```shell
    npm install --save-dev @vitest/browser-webdriverio webdriverio
    ```

=== "yarn"

    ```shell
    yarn add --dev @vitest/browser-webdriverio webdriverio
    ```

=== "pnpm"

    ```shell
    pnpm add -D @vitest/browser-webdriverio webdriverio
    ```

=== "bun"

    ```shell
    bun add --dev @vitest/browser-webdriverio webdriverio
    ```

### Preview {: #preview}

Провайдер `@vitest/browser-preview` рассчитан на среды WebContainer вроде StackBlitz и не предназначен для CI/CD.

=== "npm"

    ```shell
    npm install --save-dev @vitest/browser-preview
    ```

=== "yarn"

    ```shell
    yarn add --dev @vitest/browser-preview
    ```

=== "pnpm"

    ```shell
    pnpm add -D @vitest/browser-preview
    ```

=== "bun"

    ```shell
    bun add --dev @vitest/browser-preview
    ```

!!! tip ""

    Более тонкая настройка под конкретный браузер — в разделе [Расширенная конфигурация Vitest](#advanced-vitest-configuration).

## Другие тестовые фреймворки {: #other-test-frameworks}

Приложение Angular можно тестировать и другими библиотеками и раннерами. У каждой свои установка, конфигурация и синтаксис.

## Тесты в непрерывной интеграции {: #testing-in-continuous-integration}

Надёжный набор тестов — важная часть конвейера непрерывной интеграции (CI). CI-серверы запускают тесты на каждый коммит и пул-реквест.

Чтобы прогнать приложение Angular на CI-сервере, используют обычную команду тестов:

```shell
ng test
```

Большинство CI-серверов задаёт переменную окружения `CI=true`, и `ng test` её видит. Тесты сами переключаются в неинтерактивный однократный запуск.

Если сервер эту переменную не задаёт или однократный запуск нужно включить вручную, используйте флаги `--no-watch` и `--no-progress`:

```shell
ng test --no-watch --no-progress
```

## Дополнительно о тестах {: #more-information-on-testing}

Когда приложение подготовлено к тестам, пригодятся следующие руководства.

|                                                                    | Подробности                                                                           |
| :----------------------------------------------------------------- | :-------------------------------------------------------------------------------- |
| [Покрытие кода](https://angular.dev/guide/testing/code-coverage)                       | Какую часть приложения покрывают тесты и как задать требуемый объём. |
| [Тестирование сервисов](https://angular.dev/guide/testing/services)                         | Как тестировать сервисы, которыми пользуется приложение.                                   |
| [Основы тестирования компонентов](https://angular.dev/guide/testing/components-basics)    | Базовые приёмы тестов компонентов Angular.                                             |
| [Сценарии тестирования компонентов](https://angular.dev/guide/testing/components-scenarios)  | Разные сценарии и случаи тестов компонентов.                       |
| [Тестирование директив-атрибутов](https://angular.dev/guide/testing/attribute-directives) | Как тестировать директивы-атрибуты.                                            |
| [Тестирование пайпов](https://angular.dev/guide/testing/pipes)                               | Как тестировать пайпы.                                                                |
| [Отладка тестов](https://angular.dev/guide/testing/debugging)                         | Типичные ошибки в тестах.                                                              |
| [Служебные API для тестов](https://angular.dev/guide/testing/utility-apis)                 | Возможности Angular для тестов.                                                         |


---

Источник: [https://angular.dev/guide/testing](https://angular.dev/guide/testing)
