# Объединить переводы в приложение

:date: 28.02.2022

Чтобы объединить готовые переводы в ваш проект, выполните следующие действия

1.  Используйте [Angular CLI][aioclimain] для создания копии дистрибутивных файлов вашего проекта.

2.  Используйте опцию `"localize"` для замены всех сообщений i18n на правильные переводы и создания локализованного варианта приложения.

    Вариант приложения — это полная копия дистрибутивных файлов вашего приложения, переведенная для одной локали.

После объединения переводов обслуживайте каждую распространяемую копию приложения, используя определение языка на стороне сервера или разные подкаталоги.

!!!note ""

    Дополнительную информацию о том, как обслуживать каждую распространяемую копию приложения, см. в разделе [deploying multiple locales][aioguidei18ncommondeploy].

Для перевода приложения во время компиляции процесс сборки использует [опережающую компиляцию (AOT)][aioguideglossaryaheadoftimeaotcompilation] для создания небольшого, быстрого, готового к запуску приложения.

!!!note ""

    Подробное описание процесса сборки см. в разделе [Создание и обслуживание приложений Angular][aioguidebuild]. Процесс сборки работает для файлов перевода в формате `.xlf` или в другом формате, который понимает Angular, например `.xtb`.

    Дополнительную информацию о форматах файлов перевода, используемых Angular, см. в разделе [Изменение формата файла исходного языка][aioguidei18ncommontranslationfileschangethesourcelanguagefileformat].

Чтобы собрать отдельную распространяемую копию приложения для каждой локали, [определите локали в конфигурации сборки] [aioguidei18ncommonmergedefinelocalesinthebuildconfiguration] в файле конфигурации сборки рабочего пространства [`angular.json`] [aioguideworkspaceconfig] вашего проекта.

Этот метод сокращает процесс сборки, устраняя необходимость выполнять полную сборку приложения для каждой локали.

Чтобы [генерировать варианты приложений для каждой локали][aioguidei18ncommonmergegenerateapplicationvariantsforeachlocale], используйте опцию ` localize` в файле конфигурации сборки рабочего пространства [`angular.json`][aioguideworkspaceconfig]. Также для [сборки из командной строки][aioguidei18ncommonmergebuildfromthecommandline] используйте команду [`build`][aioclibuild][Angular CLI][aioclimain] с опцией `--localize`.

!!!note ""

    Опционально, [apply specific build options for just one locale][aioguidei18ncommonmergeapplyspecificbuildoptionsforjustonelocale] для пользовательской конфигурации локали.

## Определение локалей в конфигурации сборки

Используйте опцию проекта `i18n` в файле конфигурации сборки рабочего пространства [`angular.json`][aioguideworkspaceconfig] вашего проекта, чтобы определить локали для проекта.

Следующие под-опции определяют язык источника и указывают компилятору, где найти поддерживаемые переводы для проекта.

| Подпараметр    | Подробности                                                                      |
| :------------- | :------------------------------------------------------------------------------- |
| `sourceLocale` | Локаль, которую вы используете в исходном коде приложения (`en-US` по умолчанию) |
| `locales`      | Карта идентификаторов локалей к файлам перевода                                  |

### `angular.json` для примера `en-US` и `fr`.

Например, следующая выдержка из файла конфигурации сборки рабочего пространства [`angular.json`][aioguideworkspaceconfig] устанавливает исходную локаль на `en-US` и указывает путь к файлу перевода французской локали (`fr`).

```json
"projects": {
    "angular.io-example": {
      // ...
      "i18n": {
        "sourceLocale": "en-US",
        "locales": {
          "fr": {
            "translation": "src/locale/messages.fr.xlf",
            // ...
          }
        }
      },
      "architect": {
        // ...
      }
    }
  }
}
```

## Генерируем варианты приложения для каждой локали

Чтобы использовать определение локали в конфигурации сборки, используйте опцию `localize` в файле конфигурации сборки рабочего пространства [`angular.json`][aioguideworkspaceconfig], чтобы указать CLI, какие локали генерировать для конфигурации сборки.

-   Установите значение `"localize"` в `true` для всех локалей, ранее определенных в конфигурации сборки.
-   Установите `"localize"` в массив подмножества ранее определенных идентификаторов локалей, чтобы собрать только эти версии локалей.
-   Установите `"localize"` в `false`, чтобы отключить локализацию и не генерировать никаких версий, специфичных для локали.

!!!note ""

    [Ahead-of-time (AOT) compilation][aioguideglossaryaheadoftimeaotcompilation] требуется для локализации шаблонов компонентов.

    Если вы изменили этот параметр, установите `"aot"` в `true`, чтобы использовать AOT.

!!!note ""

    В связи со сложностью развертывания i18n и необходимостью минимизировать время пересборки, сервер разработки поддерживает локализацию только одной локали за раз. Если вы установите опцию `"localize"` в `true`, определите более одной локали и используете `ng serve`, то возникнет ошибка.
    Если вы хотите разрабатывать для определенной локали, установите опцию `"localize"` в определенную локаль.

    Например, для французского языка (`fr`), укажите `"localize": ["fr"]`.

CLI загружает и регистрирует данные о локали, помещает каждую сгенерированную версию в специфический для локали каталог, чтобы отделить ее от других версий локали, и помещает каталоги в настроенный `outputPath` для проекта. Для каждого варианта приложения атрибут `lang` элемента `html` устанавливается на локаль.

CLI также корректирует базовый HREF HTML для каждой версии приложения, добавляя локаль к настроенному `baseHref`.

Установите свойство `"localize"` как общую конфигурацию для эффективного наследования для всех конфигураций. Также установите свойство для переопределения других конфигураций.

### `angular.json` включает все локали из примера сборки

Следующий пример отображает опцию `"localize"`, установленную в `true` в файле конфигурации сборки рабочего пространства [`angular.json`][aioguideworkspaceconfig], так что все локали, определенные в конфигурации сборки, будут собраны.

```json
"build": {
  "builder": "@angular-devkit/build-angular:browser",
  "options": {
    "localize": true,
    // ...
  },
}
```

## Сборка из командной строки

Также используйте опцию `--localize` с командой [`ng build`][aioclibuild] и существующей конфигурацией `production`. CLI собирает все локали, определенные в конфигурации сборки.

Если вы задаете локали в конфигурации сборки, это аналогично тому, как если бы вы установили опцию `"localize"` в `true`.

!!!note ""

    Более подробную информацию о том, как установить локали, смотрите в разделе [Генерировать варианты приложений для каждой локали][aioguidei18ncommonmergegenerateapplicationvariantsforeachlocale].

```
ng build --localize
```

## Применение определенных опций сборки только для одной локали

Чтобы применить определенные опции сборки только для одной локали, укажите одну локаль для создания пользовательской конфигурации, специфичной для локали.

!!!warning ""

    Используйте сервер разработки [Angular CLI][aioclimain] (`ng serve`) только с одной локалью.

### сборка для французского примера

Следующий пример отображает пользовательскую конфигурацию, специфичную для локали, с использованием одной локали.

```json
"build": {
    // ...
    "configurations": {
      // ...
      "fr": {
        "localize": ["fr"]
      }
    },
    // ...
  },
  "serve": {
    "builder": "@angular-devkit/build-angular:dev-server",
    "configurations": {
      // ...
      "fr": {
        "browserTarget": "angular.io-example:build:development,fr"
      }
    },
    // ...
  },
  // ...
}
```

Передайте эту конфигурацию командам `ng serve` или `ng build`. Следующий пример кода показывает, как обслуживать файл французского языка.

```
ng serve --configuration=fr
```

Для производственных сборок используйте композицию конфигураций для запуска обеих конфигураций.

```
ng build --configuration=production,fr
```

---

```json
"architect": {
  "build": {
    "builder": "@angular-devkit/build-angular:browser",
    "options": {
      // ...
    },
    "configurations": {
      // ...
      "fr": {
        "localize": ["fr"]
      }
    },
    // ...
  },
  "serve": {
    "builder": "@angular-devkit/build-angular:dev-server",
    "configurations": {
      "production": {
        "browserTarget": "angular.io-example:build:production"
      },
      // ...
      "fr": {
        "browserTarget": "angular.io-example:build:development,fr"
      }
    },
    // ...
  },
  // ...
}
```

## Сообщить об отсутствующих переводах

Если перевод отсутствует, сборка проходит успешно, но генерируется предупреждение типа `Missing translation for message "{translation_text}"`. Чтобы настроить уровень предупреждения, выдаваемого компилятором Angular, укажите один из следующих уровней.

| Уровень предупреждения | Подробности                                                   | Вывод                                                 |
| :--------------------- | :------------------------------------------------------------ | :---------------------------------------------------- |
| `error`                | Выбросить ошибку и сборка не удалась                          | n/a                                                   |
| `ignore`               | Ничего не делать                                              | n/a                                                   |
| `warning`              | Отображает предупреждение по умолчанию в консоли или оболочке | `Missing translation for message "{translation_text}" |

Укажите уровень предупреждения в разделе `options` для цели `build` вашего файла конфигурации сборки рабочего пространства [`angular.json`][aioguideworkspaceconfig].

### `angular.json` `error` пример предупреждения

В следующем примере показано, как установить уровень предупреждения на `error`.

```json
"build": {
  "builder": "@angular-devkit/build-angular:browser",
  "options": {
    // ...
    "i18nMissingTranslation": "error"
  },
}
```

!!!note ""

    Когда вы компилируете свой проект Angular в приложение Angular, экземпляры атрибута `i18n` заменяются экземплярами строки сообщения с меткой [`$localize`][aioapilocalizeinitlocalize]. Это означает, что ваше приложение Angular будет переведено после компиляции.

    Это также означает, что вы можете создавать локализованные версии вашего приложения Angular без повторной компиляции всего проекта Angular для каждой локали.

    Когда вы переводите ваше приложение Angular, _трансляционное преобразование_ заменяет и упорядочивает части (статические строки и выражения) строки шаблонного литерала строками из коллекции переводов. Для получения дополнительной информации смотрите [`$localize`][aioapilocalizeinitlocalize].

    **tldr;**.

    Компилируйте один раз, затем переводите для каждой локали.

## Что дальше

-   [Развертывание нескольких локалей][aioguidei18ncommondeploy]

<!-- links -->

[aioapilocalizeinitlocalize]: https://angular.io/api/localize/init/$localize
[aioclimain]: https://angular.io/cli
[aioclibuild]: https://angular.io/cli/build
[aioguidebuild]: build.md
[aioguideglossaryaheadoftimeaotcompilation]: glossary.md#ahead-of-time-aot-compilation
[aioguidei18ncommondeploy]: i18n-common-deploy.md
[aioguidei18ncommonmergeapplyspecificbuildoptionsforjustonelocale]: i18n-common-merge.md#apply-specific-build-options-for-just-one-locale
[aioguidei18ncommonmergebuildfromthecommandline]: i18n-common-merge.md#build-from-the-command-line
[aioguidei18ncommonmergedefinelocalesinthebuildconfiguration]: i18n-common-merge.md#define-locales-in-the-build-configuration
[aioguidei18ncommonmergegenerateapplicationvariantsforeachlocale]: i18n-common-merge.md#generate-application-variants-for-each-locale
[aioguidei18ncommontranslationfileschangethesourcelanguagefileformat]: i18n-common-translation-files.md#change-the-source-language-file-format
[aioguideworkspaceconfig]: workspace-config.md

<!-- external links -->

[angularv8guidei18nmergewiththejitcompiler]: https://v8.angular.io/guide/i18n-common#merge-translations-into-the-app-with-the-jit-compiler

<!-- end links -->
