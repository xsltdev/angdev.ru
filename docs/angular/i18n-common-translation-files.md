# Работа с файлами перевода

После подготовки компонента к переводу используйте команду [`extract-i18n`][aiocliextracti18n] [Angular CLI][aioclimain] для извлечения помеченного текста компонента в файл _исходного языка_.

Размеченный текст включает текст, помеченный `i18n`, атрибуты, помеченные `i18n-`_attribute_, и текст, помеченный `$localize`, как описано в [Подготовка компонента к переводу][aioguidei18ncommonprepare].

Выполните следующие шаги, чтобы создать и обновить файлы перевода для вашего проекта.

1.  [Извлечение файла исходного языка][aioguidei18ncommontranslationfilesextractthesourcelanguagefile].

    1.  По желанию измените местоположение, формат и имя.

1.  Скопируйте исходный языковой файл в [создать файл перевода для каждого языка][aioguidei18ncommontranslationfilescreateatranslationfileforeachlanguage].

1.  [Переведите каждый файл перевода][aioguidei18ncommontranslationfilesranslateeachtranslationfile].

1.  Переведите множественное число и альтернативные выражения отдельно.

    1.  [Переведите множественное число][aioguidei18ncommontranslationfilestranslateplurals].

    1.  [Переведите альтернативные выражения][aioguidei18ncommontranslationfilestranslatealternateexpressions].

    1.  [Перевести вложенные выражения][aioguidei18ncommontranslationfilestranslatenestedexpressions].

## Извлечение файла исходного языка

Чтобы извлечь исходный языковой файл, выполните следующие действия.

1.  Откройте окно терминала.

1.  Перейдите в корневой каталог вашего проекта.

1.  Выполните следующую команду CLI.

    <code-example path="i18n/doc-files/commands.sh" region="extract-i18n-default"></code-example>.

Команда `extract-i18n` создает файл исходного языка с именем `messages.xlf` в корневом каталоге вашего проекта. Подробнее о XML Localization Interchange File Format \(XLIFF, версия 1.2\) смотрите в [XLIFF][wikipediawikixliff].

Используйте следующие опции команды [`extract-i18n`][aiocliextracti18n], чтобы изменить местоположение, формат и имя файла исходного языка.

| Опция команды | Подробности | | :-------------- | :----------------------------------- |.

| `--format` | Установить формат выходного файла | `--out-file`.

| `--out-file` | Установите имя выходного файла |

| `--output-path` | Установите путь к выходному каталогу |

### Изменить расположение файла исходного языка

Чтобы создать файл в каталоге `src/locale`, укажите путь вывода в качестве опции.

#### `extract-i18n --output-path` пример

В следующем примере путь вывода указан в качестве опции.

<code-example path="i18n/doc-files/commands.sh" region="extract-i18n-output-path"></code-example>.

### Изменение формата файла исходного языка

Команда `extract-i18n` создает файлы в следующих форматах перевода.

| Формат перевода | Подробности | Расширение файла | :----------------- | :--------------------------------------------------------------------------------------------------------------- | :---------------- | :----------------- | :--------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------.

| ARB | [Application Resource Bundle][githubgoogleappresourcebundlewikiapplicationresourcebundlespecification] | | `.arb` | |

| JSON | [JavaScript Object Notation][jsonmain] | `.json` | | [JavaScript Object Notation][jsonmain] | `.json` |

| XLIFF 1.2 | [XML Localization Interchange File Format, version 1.2][oasisopendocsxliffxliffcorexliffcorehtml] | `.xlf` | | XLIFF 1.2 | [XML Localization Interchange File Format, version 1.2]oasisopendocsxliffxliffcorexliffcorehtml

| XLIFF 2 | [XML Localization Interchange File Format, версия 2][oasisopendocsxliffxliffcorev20cos01xliffcorev20cose01html] | `.xlf` | | XMB | [XML Localization Interchange File Format, версия 2]oasisopendocsxliffxliffcorev20cose01html

| XMB | [XML Message Bundle][unicodecldrdevelopmentdevelopmentprocessdesignproposalsxmb] | `.xmb` \(`.xtb`\) |

Укажите формат перевода в явном виде с помощью опции команды `--format`.

<div class="alert is-helpful">

Формат XMB генерирует файлы исходного языка `.xmb`, но использует файлы перевода `.xtb`.

</div>

#### `extract-i18n --format` пример

Следующий пример демонстрирует несколько форматов перевода.

<code-example path="i18n/doc-files/commands.sh" region="extract-i18n-formats"></code-example>.

### Изменить имя файла исходного языка

Чтобы изменить имя файла исходного языка, создаваемого инструментом извлечения, используйте опцию команды `--out-file`.

#### `extract-i18n --out-file` пример

Следующий пример демонстрирует присвоение имени выходному файлу.

<code-example path="i18n/doc-files/commands.sh" region="extract-i18n-out-file"></code-example>.

## Создание файла перевода для каждого языка

Чтобы создать файл перевода для локали или языка, выполните следующие действия.

1.  [Извлечение файла исходного языка][aioguidei18ncommontranslationfilesextractthesourcelanguagefile].

1.  Сделайте копию исходного языкового файла, чтобы создать _переводной_ файл для каждого языка.

1.  Переименуйте файл _translation_, чтобы добавить локаль.

    <code-example language="file">

    messages.xlf --&gt; messages.{locale}.xlf

    </code-example>.

1.  Создайте новый каталог в корне проекта с именем `locale`.

    <code-example language="file">

    src/locale

    </code-example>

1.  Переместите файл _translation_ в новый каталог.

1.  Отправьте файл _translation_ своему переводчику.

1.  Повторите описанные выше шаги для каждого языка, который вы хотите добавить в свое приложение.

### `extract-i18n` пример для французского языка

Например, чтобы создать файл перевода на французский язык, выполните следующие действия.

1.  Выполните команду `extract-i18n`.

1.  Создайте копию исходного языкового файла `messages.xlf`.

1.  Переименуйте копию в `messages.fr.xlf` для перевода на французский язык \(`fr`\).

1.  Переместите файл перевода `fr` в каталог `src/locale`.

1.  Отправьте файл перевода `fr` переводчику.

## Переведите каждый файл перевода.

Если вы не владеете языком и у вас нет времени на редактирование переводов, вы, скорее всего, выполните следующие шаги.

1.  Отправьте каждый файл перевода переводчику.

1.  Переводчик использует редактор файлов XLIFF для выполнения следующих действий.

    1.  Создайте перевод.

    1.  Отредактируйте перевод.

### Пример процесса перевода для французского языка

Чтобы продемонстрировать этот процесс, просмотрите файл `messages.fr.xlf` в [Example Angular Internationalization application][aioguidei18nexample]. В [Пример приложения Angular Internationalization][aioguidei18nexample] включен перевод на французский язык, который можно редактировать без специального редактора XLIFF или знания французского языка.

Следующие действия описывают процесс перевода на французский язык.

1.  Откройте файл `messages.fr.xlf` и найдите первый элемент `<trans-unit>`.
    Это _переводной блок_, также известный как _текстовый узел_, который представляет собой перевод тега приветствия `<h1>`, который ранее был помечен атрибутом `i18n`.

    <code-example header="src/locale/messages.fr.xlf (&lt;trans-unit&gt;)" path="i18n/doc-files/messages.fr.xlf.html" region="translated-hello-before"></code-example>.

    `id="introductionHeader"` - это [пользовательский ID][aioguidei18noptionalmanagemarkedtext], но без префикса `@@`, необходимого в исходном HTML.

1.  Продублируйте элемент `<source>... </source>` элемент в узле text, переименуйте его в `target`, а затем замените содержимое французским текстом.

    <code-example header="src/locale/messages.fr.xlf (&lt;trans-unit&gt;, после перевода)" path="i18n/doc-files/messages.fr.xlf.html" region="translated-hello"></code-example>.

    При более сложном переводе информация и контекст в [элементах описания и значения][aioguidei18ncommonprepareaddhelpfuldescriptionsandmeanings] помогают выбрать правильные слова для перевода.

1.  Переведите остальные текстовые узлы.

    В следующем примере показан способ перевода.

    <code-example header="src/locale/messages.fr.xlf (&lt;trans-unit&gt;)" path="i18n/doc-files/messages.fr.xlf.html" region="translated-other-nodes"></code-example>

    <div class="alert is-important">

    Don't change the IDs for translation units.

    Each `id` attribute is generated by Angular and depends on the content of the component text and the assigned meaning.

    If you change either the text or the meaning, then the `id` attribute changes.

    For more about managing text updates and IDs, see [custom IDs][aioguidei18noptionalmanagemarkedtext].

    </div>

## Translate plurals

Add or remove plural cases as needed for each language.

<div class="alert is-helpful">

Правила множественного числа языка см. в [CLDR plural rules][githubunicodeorgcldrstagingchartslatestsupplementallanguagepluralruleshtml].

</div>

### `минута` `множественное число` пример

Чтобы перевести `множественное число`, переведите значения соответствия формата ICU.

-   `только что`

-   `минуту назад`

-   `<x id="INTERPOLATION" equiv-text="{{minutes}}"/> минут назад`.

В следующем примере показан способ перевода.

<code-example header="src/locale/messages.fr.xlf (&lt;trans-unit&gt;)" path="i18n/doc-files/messages.fr.xlf.html" region="translated-plural"></code-example>.

## Перевод альтернативных выражений

Angular также извлекает альтернативные выражения `select` ICU в виде отдельных единиц перевода.

### Пример `gender` `select`.

Следующий пример отображает ICU-выражение `select` в шаблоне компонента.

<code-example header="src/app/app.component.html" path="i18n/src/app/app.component.html" region="i18n-select"></code-example>

В этом примере Angular разделяет выражение на две единицы перевода. Первая содержит текст вне клаузы `select` и использует место для `select` \(`<x id="ICU">`\):

<code-example header="src/locale/messages.fr.xlf (&lt;trans-unit&gt;)" path="i18n/doc-files/messages.fr.xlf.html" region="translate-select-1"></code-example>.

<div class="alert is-important">

Когда вы переводите текст, при необходимости переместите заполнитель, но не удаляйте его. Если вы удалите заполнитель, выражение ICU будет удалено из переведенного приложения.

</div>

В следующем примере отображается вторая единица перевода, содержащая предложение `select`.

<code-example header="src/locale/messages.fr.xlf (&lt;trans-unit&gt;)" path="i18n/doc-files/messages.fr.xlf.html" region="translate-select-2"></code-example>.

В следующем примере после завершения перевода отображаются обе единицы перевода.

<code-example header="src/locale/messages.fr.xlf (&lt;trans-unit&gt;)" path="i18n/doc-files/messages.fr.xlf.html" region="translated-select"></code-example>.

## Перевод вложенных выражений

Angular обрабатывает вложенное выражение таким же образом, как и альтернативное выражение. Angular разделяет выражение на две единицы перевода.

### Пример вложенного выражения `plural`.

В следующем примере отображается первая единица перевода, содержащая текст вне вложенного выражения.

<code-example header="src/locale/messages.fr.xlf (&lt;trans-unit&gt;)" path="i18n/doc-files/messages.fr.xlf.html" region="translate-nested-1"></code-example>.

В следующем примере отображается вторая единица перевода, содержащая полное вложенное выражение.

<code-example header="src/locale/messages.fr.xlf (&lt;trans-unit&gt;)" path="i18n/doc-files/messages.fr.xlf.html" region="translate-nested-2"></code-example>.

В следующем примере после перевода отображаются обе единицы перевода.

<code-example header="src/locale/messages.fr.xlf (&lt;trans-unit&gt;)" path="i18n/doc-files/messages.fr.xlf.html" region="translate-nested"></code-example>.

## Что дальше

-   [Слияние переводов в приложение][aioguidei18ncommonmerge]

<!-- links -->

[aioclimain]: cli 'CLI Overview and Command Reference | Angular'
[aiocliextracti18n]: cli/extract-i18n 'ng extract-i18n | CLI | Angular'
[aioguideglossarycommandlineinterfacecli]: guide/glossary#command-line-interface-cli 'command-line interface (CLI) - Glossary | Angular'
[aioguidei18ncommonmerge]: guide/i18n-common-merge 'Merge translations into the application | Angular'
[aioguidei18ncommonprepare]: guide/i18n-common-prepare 'Prepare component for translation | Angular'
[aioguidei18ncommonprepareaddhelpfuldescriptionsandmeanings]: guide/i18n-common-prepare#add-helpful-descriptions-and-meanings 'Add helpful descriptions and meanings - Prepare component for translation | Angular'
[aioguidei18ncommontranslationfilescreateatranslationfileforeachlanguage]: guide/i18n-common-translation-files#create-a-translation-file-for-each-language 'Create a translation file for each language - Work with translation files | Angular'
[aioguidei18ncommontranslationfilesextractthesourcelanguagefile]: guide/i18n-common-translation-files#extract-the-source-language-file 'Extract the source language file - Work with translation files | Angular'
[aioguidei18ncommontranslationfilestranslatealternateexpressions]: guide/i18n-common-translation-files#translate-alternate-expressions 'Translate alternate expressions - Work with translation files | Angular'
[aioguidei18ncommontranslationfilestranslateeachtranslationfile]: guide/i18n-common-translation-files#translate-each-translation-file 'Translate each translation file - Work with translation files | Angular'
[aioguidei18ncommontranslationfilestranslatenestedexpressions]: guide/i18n-common-translation-files#translate-nested-expressions 'Translate nested expressions - Work with translation files | Angular'
[aioguidei18ncommontranslationfilestranslateplurals]: guide/i18n-common-translation-files#translate-plurals 'Translate plurals - Work with translation files | Angular'
[aioguidei18nexample]: guide/i18n-example 'Example Angular Internationalization application | Angular'
[aioguidei18noptionalmanagemarkedtext]: guide/i18n-optional-manage-marked-text 'Manage marked text with custom IDs | Angular'
[aioguideworkspaceconfig]: guide/workspace-config 'Angular workspace configuration | Angular'

<!-- external links -->

[githubgoogleappresourcebundlewikiapplicationresourcebundlespecification]: https://github.com/google/app-resource-bundle/wiki/ApplicationResourceBundleSpecification 'ApplicationResourceBundleSpecification | google/app-resource-bundle | GitHub'
[githubunicodeorgcldrstagingchartslatestsupplementallanguagepluralruleshtml]: https://unicode-org.github.io/cldr-staging/charts/latest/supplemental/language_plural_rules.html 'Language Plural Rules - CLDR Charts | Unicode | GitHub'
[jsonmain]: https://www.json.org 'Introducing JSON | JSON'
[oasisopendocsxliffxliffcorexliffcorehtml]: http://docs.oasis-open.org/xliff/xliff-core/xliff-core.html 'XLIFF Version 1.2 Specification | Oasis Open Docs'
[oasisopendocsxliffxliffcorev20cos01xliffcorev20cose01html]: http://docs.oasis-open.org/xliff/xliff-core/v2.0/cos01/xliff-core-v2.0-cos01.html 'XLIFF Version 2.0 | Oasis Open Docs'
[unicodecldrdevelopmentdevelopmentprocessdesignproposalsxmb]: http://cldr.unicode.org/development/development-process/design-proposals/xmb 'XMB | CLDR - Unicode Common Locale Data Repository | Unicode'
[wikipediawikixliff]: https://en.wikipedia.org/wiki/XLIFF 'XLIFF | Wikipedia'

<!-- end links -->

:date: 28.02.2022
