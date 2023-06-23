# Объединить переводы в приложение

Чтобы объединить готовые переводы в ваш проект, выполните следующие действия

1.  Используйте [Angular CLI][aioclimain] для создания копии дистрибутивных файлов вашего проекта.

1.  Используйте опцию `"localize"` для замены всех сообщений i18n на правильные переводы и создания локализованного варианта приложения.

    Вариант приложения - это полная копия дистрибутивных файлов вашего приложения, переведенная для одной локали.

После объединения переводов обслуживайте каждую распространяемую копию приложения, используя определение языка на стороне сервера или разные подкаталоги.

<div class="alert is-helpful">

Дополнительную информацию о том, как обслуживать каждую распространяемую копию приложения, см. в разделе [deploying multiple locales][aioguidei18ncommondeploy].

</div>

Для перевода приложения во время компиляции процесс сборки использует [опережающую компиляцию (AOT)][aioguideglossaryaheadoftimeaotcompilation] для создания небольшого, быстрого, готового к запуску приложения.

<div class="alert is-helpful">

Подробное описание процесса сборки см. в разделе [Создание и обслуживание приложений Angular][aioguidebuild]. Процесс сборки работает для файлов перевода в формате `.xlf` или в другом формате, который понимает Angular, например `.xtb`.
Дополнительную информацию о форматах файлов перевода, используемых Angular, см. в разделе [Изменение формата файла исходного языка][aioguidei18ncommontranslationfileschangethesourcelanguagefileformat].

</div>

Чтобы собрать отдельную распространяемую копию приложения для каждой локали, [определите локали в конфигурации сборки] [aioguidei18ncommonmergedefinelocalesinthebuildconfiguration] в файле конфигурации сборки рабочего пространства [`angular.json`] [aioguideworkspaceconfig] вашего проекта.

Этот метод сокращает процесс сборки, устраняя необходимость выполнять полную сборку приложения для каждой локали.

Чтобы [генерировать варианты приложений для каждой локали][aioguidei18ncommonmergegenerateapplicationvariantsforeachlocale], используйте опцию ` localize` в файле конфигурации сборки рабочего пространства [`angular.json`][aioguideworkspaceconfig]. Также для [сборки из командной строки][aioguidei18ncommonmergebuildfromthecommandline] используйте команду [`build`][aioclibuild][Angular CLI][aioclimain] с опцией `--localize`.

<div class="alert is-helpful">

Опционально, [apply specific build options for just one locale][aioguidei18ncommonmergeapplyspecificbuildoptionsforjustonelocale] для пользовательской конфигурации локали.

</div>

## Определение локалей в конфигурации сборки

Используйте опцию проекта `i18n` в файле конфигурации сборки рабочего пространства [`angular.json`][aioguideworkspaceconfig] вашего проекта, чтобы определить локали для проекта.

Следующие под-опции определяют язык источника и указывают компилятору, где найти поддерживаемые переводы для проекта.

| Подпараметр | Подробности | | :------------- | :--------------------------------------------------------------------------- | |

| `sourceLocale` | Локаль, которую вы используете в исходном коде приложения\(`en-US` по умолчанию\)|.

| `locales` | Карта идентификаторов локалей к файлам перевода | `angular.json`.

### `angular.json` для примера `en-US` и `fr`.

Например, следующая выдержка из файла конфигурации сборки рабочего пространства [`angular.json`][aioguideworkspaceconfig] устанавливает исходную локаль на `en-US` и указывает путь к файлу перевода французской локали \(`fr`\).

<code-example header="angular.json" path="i18n/angular.json" region="locale-config"></code-example>.

## Генерируем варианты приложения для каждой локали

Чтобы использовать определение локали в конфигурации сборки, используйте опцию ` localize` в файле конфигурации сборки рабочего пространства [`angular.json`][aioguideworkspaceconfig], чтобы указать CLI, какие локали генерировать для конфигурации сборки.

-   Установите значение `"localize"` в `true` для всех локалей, ранее определенных в конфигурации сборки.

-   Установите `"localize"` в массив подмножества ранее определенных идентификаторов локалей, чтобы собрать только эти версии локалей.

-   Установите `"localize"` в `false`, чтобы отключить локализацию и не генерировать никаких версий, специфичных для локали.

<div class="alert is-helpful">

**NOTE**: <br /> [Ahead-of-time (AOT) compilation][aioguideglossaryaheadoftimeaotcompilation] is required to localize component templates.

If you changed this setting, set `"aot"` to `true` in order to use AOT.

</div>

<div class="alert is-helpful">

В связи со сложностью развертывания i18n и необходимостью минимизировать время пересборки, сервер разработки поддерживает локализацию только одной локали за раз. Если вы установите опцию `"localize"` в `true`, определите более одной локали и используете `ng serve`, то возникнет ошибка.
Если вы хотите разрабатывать для определенной локали, установите опцию `"localize"` в определенную локаль.

Например, для французского языка \(`fr`\), укажите `"localize": ["fr"]`.

</div>

CLI загружает и регистрирует данные о локали, помещает каждую сгенерированную версию в специфический для локали каталог, чтобы отделить ее от других версий локали, и помещает каталоги в настроенный `outputPath` для проекта. Для каждого варианта приложения атрибут `lang` элемента `html` устанавливается на локаль.
CLI также корректирует базовый HREF HTML для каждой версии приложения, добавляя локаль к настроенному `baseHref`.

Установите свойство `"localize"` как общую конфигурацию для эффективного наследования для всех конфигураций. Также установите свойство для переопределения других конфигураций.

### `angular.json` включает все локали из примера сборки

Следующий пример отображает опцию `"localize"`, установленную в `true` в файле конфигурации сборки рабочего пространства [`angular.json`][aioguideworkspaceconfig], так что все локали, определенные в конфигурации сборки, будут собраны.

<code-example header="angular.json" path="i18n/angular.json" region="build-localize-true"></code-example>.

## Сборка из командной строки

Также используйте опцию `--localize` с командой [`ng build`][aioclibuild] и существующей конфигурацией `production`. CLI собирает все локали, определенные в конфигурации сборки.

Если вы задаете локали в конфигурации сборки, это аналогично тому, как если бы вы установили опцию `"localize"` в `true`.

<div class="alert is-helpful">

Более подробную информацию о том, как установить локали, смотрите в разделе [Генерировать варианты приложений для каждой локали][aioguidei18ncommonmergegenerateapplicationvariantsforeachlocale].

</div>

<code-example path="i18n/doc-files/commands.sh" region="build-localize"></code-example>

## Применение определенных опций сборки только для одной локали

Чтобы применить определенные опции сборки только для одной локали, укажите одну локаль для создания пользовательской конфигурации, специфичной для локали.

<div class="alert is-important">

Используйте сервер разработки [Angular CLI][aioclimain]\(`ng serve`\) только с одной локалью.

</div>

### сборка для французского примера

Следующий пример отображает пользовательскую конфигурацию, специфичную для локали, с использованием одной локали.

<code-example header="angular.json" path="i18n/angular.json" region="build-single-locale"></code-example>.

Передайте эту конфигурацию командам `ng serve` или `ng build`. Следующий пример кода показывает, как обслуживать файл французского языка.

<code-example path="i18n/doc-files/commands.sh" region="serve-french"></code-example>.

Для производственных сборок используйте композицию конфигураций для запуска обеих конфигураций.

<code-example path="i18n/doc-files/commands.sh" region="build-production-french"></code-example>.

<code-example header="angular.json" path="i18n/angular.json" region="build-production-french"></code-example>.

## Сообщить об отсутствующих переводах

Если перевод отсутствует, сборка проходит успешно, но генерируется предупреждение типа `Missing translation for message "{translation_text}"`. Чтобы настроить уровень предупреждения, выдаваемого компилятором Angular, укажите один из следующих уровней.

| Уровень предупреждения | Подробности | Вывод | | :------------ | :--------------------------------------------------- | :----------------------------------------------------- |.

| `error` | Выбросить ошибку и сборка не удалась | n/a |

| `ignore` | Ничего не делать | n/a |

| `warning` | Отображает предупреждение по умолчанию в консоли или оболочке | `Missing translation for message "{translation_text}"| |.

Укажите уровень предупреждения в разделе `options` для цели `build` вашего файла конфигурации сборки рабочего пространства [`angular.json`][aioguideworkspaceconfig].

### `angular.json` `error` пример предупреждения

В следующем примере показано, как установить уровень предупреждения на `error`.

<code-example header="angular.json" path="i18n/angular.json" region="missing-translation-error" ></code-example>.

<div class="alert is-helpful">

Когда вы компилируете свой проект Angular в приложение Angular, экземпляры атрибута `i18n` заменяются экземплярами строки сообщения с меткой [`$localize`][aioapilocalizeinitlocalize]. Это означает, что ваше приложение Angular будет переведено после компиляции.
Это также означает, что вы можете создавать локализованные версии вашего приложения Angular без повторной компиляции всего проекта Angular для каждой локали.

Когда вы переводите ваше приложение Angular, _трансляционное преобразование_ заменяет и упорядочивает части\(статические строки и выражения\) строки шаблонного литерала строками из коллекции переводов. Для получения дополнительной информации смотрите [`$localize`][aioapilocalizeinitlocalize].

<div class="alert is-helpful">

**tldr;**.

Компилируйте один раз, затем переводите для каждой локали.

</div>

</div>

## Что дальше

-   [Развертывание нескольких локалей][aioguidei18ncommondeploy]

<!-- links -->

[aioapilocalizeinitlocalize]: api/localize/init/$localize '$localize | init - localize - API | Angular'
[aioclimain]: cli 'CLI Overview and Command Reference | Angular'
[aioclibuild]: cli/build 'ng build | CLI | Angular'
[aioguidebuild]: guide/build 'Building and serving Angular apps | Angular'
[aioguideglossaryaheadoftimeaotcompilation]: guide/glossary#ahead-of-time-aot-compilation 'ahead-of-time (AOT) compilation - Glossary | Angular'
[aioguidei18ncommondeploy]: guide/i18n-common-deploy 'Deploy multiple locales | Angular'
[aioguidei18ncommonmergeapplyspecificbuildoptionsforjustonelocale]: guide/i18n-common-merge#apply-specific-build-options-for-just-one-locale 'Apply specific build options for just one locale - Merge translations into the application | Angular'
[aioguidei18ncommonmergebuildfromthecommandline]: guide/i18n-common-merge#build-from-the-command-line 'Build from the command line - Merge translations into the application | Angular'
[aioguidei18ncommonmergedefinelocalesinthebuildconfiguration]: guide/i18n-common-merge#define-locales-in-the-build-configuration 'Define locales in the build configuration - Merge translations into the application | Angular'
[aioguidei18ncommonmergegenerateapplicationvariantsforeachlocale]: guide/i18n-common-merge#generate-application-variants-for-each-locale 'Generate application variants for each locale - Merge translations into the application | Angular'
[aioguidei18ncommontranslationfileschangethesourcelanguagefileformat]: guide/i18n-common-translation-files#change-the-source-language-file-format 'Change the source language file format - Work with translation files | Angular'
[aioguideworkspaceconfig]: guide/workspace-config 'Angular workspace configuration | Angular'

<!-- external links -->

[angularv8guidei18nmergewiththejitcompiler]: https://v8.angular.io/guide/i18n-common#merge-translations-into-the-app-with-the-jit-compiler 'Merge with the JIT compiler - Internationalization (i18n) | Angular v8'

<!-- end links -->

:date: 28.02.2022
