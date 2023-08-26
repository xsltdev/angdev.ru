# Работа с файлами перевода

:date: 28.02.2022

После подготовки компонента к переводу используйте команду [`extract-i18n`][aiocliextracti18n] [Angular CLI][aioclimain] для извлечения помеченного текста компонента в файл _исходного языка_.

Размеченный текст включает текст, помеченный `i18n`, атрибуты, помеченные `i18n-`_attribute_, и текст, помеченный `$localize`, как описано в [Подготовка компонента к переводу][aioguidei18ncommonprepare].

Выполните следующие шаги, чтобы создать и обновить файлы перевода для вашего проекта.

1.  [Извлечение файла исходного языка][aioguidei18ncommontranslationfilesextractthesourcelanguagefile].

    1.  По желанию измените местоположение, формат и имя.

2.  Скопируйте исходный языковой файл в [создать файл перевода для каждого языка][aioguidei18ncommontranslationfilescreateatranslationfileforeachlanguage].

3.  Переведите каждый файл перевода

4.  Переведите множественное число и альтернативные выражения отдельно.

    1.  [Переведите множественное число][aioguidei18ncommontranslationfilestranslateplurals].

    2.  [Переведите альтернативные выражения][aioguidei18ncommontranslationfilestranslatealternateexpressions].

    3.  [Перевести вложенные выражения][aioguidei18ncommontranslationfilestranslatenestedexpressions].

## Извлечение файла исходного языка

Чтобы извлечь исходный языковой файл, выполните следующие действия.

1.  Откройте окно терминала.

2.  Перейдите в корневой каталог вашего проекта.

3.  Выполните следующую команду CLI.

    ```
    ng extract-i18n
    ```

Команда `extract-i18n` создает файл исходного языка с именем `messages.xlf` в корневом каталоге вашего проекта. Подробнее о XML Localization Interchange File Format (XLIFF, версия 1.2) смотрите в [XLIFF][wikipediawikixliff].

Используйте следующие опции команды [`extract-i18n`][aiocliextracti18n], чтобы изменить местоположение, формат и имя файла исходного языка.

| Опция команды   | Подробности                          |
| :-------------- | :----------------------------------- |
| `--format`      | Установить формат выходного файла    |
| `--out-file`    | Установите имя выходного файла       |
| `--output-path` | Установите путь к выходному каталогу |

### Изменить расположение файла исходного языка

Чтобы создать файл в каталоге `src/locale`, укажите путь вывода в качестве опции.

#### `extract-i18n --output-path` пример

В следующем примере путь вывода указан в качестве опции.

```
ng extract-i18n --output-path src/locale
```

### Изменение формата файла исходного языка

Команда `extract-i18n` создает файлы в следующих форматах перевода.

| Формат перевода | Подробности                                                                                                     | Расширение файла |
| :-------------- | :-------------------------------------------------------------------------------------------------------------- | :--------------- |
| ARB             | [Application Resource Bundle][githubgoogleappresourcebundlewikiapplicationresourcebundlespecification]          | `.arb`           |
| JSON            | [JavaScript Object Notation][jsonmain]                                                                          | `.json`          |
| XLIFF 1.2       | [XML Localization Interchange File Format, version 1.2][oasisopendocsxliffxliffcorexliffcorehtml]               | `.xlf`           |
| XLIFF 2         | [XML Localization Interchange File Format, версия 2][oasisopendocsxliffxliffcorev20cos01xliffcorev20cose01html] | `.xlf`           |
| XMB             | [XML Message Bundle][unicodecldrdevelopmentdevelopmentprocessdesignproposalsxmb]                                | `.xmb` (`.xtb`)  |

Укажите формат перевода в явном виде с помощью опции команды `--format`.

!!!note ""

    Формат XMB генерирует файлы исходного языка `.xmb`, но использует файлы перевода `.xtb`.

#### `extract-i18n --format` пример

Следующий пример демонстрирует несколько форматов перевода.

```
ng extract-i18n --format=xlf
ng extract-i18n --format=xlf2
ng extract-i18n --format=xmb
ng extract-i18n --format=json
ng extract-i18n --format=arb
```

### Изменить имя файла исходного языка

Чтобы изменить имя файла исходного языка, создаваемого инструментом извлечения, используйте опцию команды `--out-file`.

#### `extract-i18n --out-file` пример

Следующий пример демонстрирует присвоение имени выходному файлу.

```
ng extract-i18n --out-file source.xlf
```

## Создание файла перевода для каждого языка

Чтобы создать файл перевода для локали или языка, выполните следующие действия.

1.  [Извлечение файла исходного языка][aioguidei18ncommontranslationfilesextractthesourcelanguagefile].

2.  Сделайте копию исходного языкового файла, чтобы создать _переводной_ файл для каждого языка.

3.  Переименуйте файл _translation_, чтобы добавить локаль.

    ```
    messages.xlf --> messages.{locale}.xlf
    ```

4.  Создайте новый каталог в корне проекта с именем `locale`.

    ```
    src/locale
    ```

5.  Переместите файл _translation_ в новый каталог.

6.  Отправьте файл _translation_ своему переводчику.

7.  Повторите описанные выше шаги для каждого языка, который вы хотите добавить в свое приложение.

### `extract-i18n` пример для французского языка

Например, чтобы создать файл перевода на французский язык, выполните следующие действия.

1.  Выполните команду `extract-i18n`.

2.  Создайте копию исходного языкового файла `messages.xlf`.

3.  Переименуйте копию в `messages.fr.xlf` для перевода на французский язык (`fr`).

4.  Переместите файл перевода `fr` в каталог `src/locale`.

5.  Отправьте файл перевода `fr` переводчику.

## Переведите каждый файл перевода.

Если вы не владеете языком и у вас нет времени на редактирование переводов, вы, скорее всего, выполните следующие шаги.

1.  Отправьте каждый файл перевода переводчику.

2.  Переводчик использует редактор файлов XLIFF для выполнения следующих действий.

    1.  Создайте перевод.

    2.  Отредактируйте перевод.

### Пример процесса перевода для французского языка

Чтобы продемонстрировать этот процесс, просмотрите файл `messages.fr.xlf` в [Example Angular Internationalization application][aioguidei18nexample]. В [Пример приложения Angular Internationalization][aioguidei18nexample] включен перевод на французский язык, который можно редактировать без специального редактора XLIFF или знания французского языка.

Следующие действия описывают процесс перевода на французский язык.

1.  Откройте файл `messages.fr.xlf` и найдите первый элемент `<trans-unit>`.
    Это _переводной блок_, также известный как _текстовый узел_, который представляет собой перевод тега приветствия `<h1>`, который ранее был помечен атрибутом `i18n`.

    ```xml
    <trans-unit id="introductionHeader" datatype="html">
        <source>Hello i18n!</source>
        <note priority="1" from="description">
            An introduction header for this sample
        </note>
        <note priority="1" from="meaning">
            User welcome
        </note>
    </trans-unit>
    ```

    `id="introductionHeader"` — это [пользовательский ID][aioguidei18noptionalmanagemarkedtext], но без префикса `@@`, необходимого в исходном HTML.

2.  Продублируйте элемент `<source>... </source>` элемент в узле text, переименуйте его в `target`, а затем замените содержимое французским текстом.

    ```xml
    <trans-unit id="introductionHeader" datatype="html">
        <source>Hello i18n!</source>
        <target>Bonjour i18n !</target>
        <note priority="1" from="description">
            An introduction header for this sample
        </note>
        <note priority="1" from="meaning">
            User welcome
        </note>
    </trans-unit>
    ```

    При более сложном переводе информация и контекст в [элементах описания и значения][aioguidei18ncommonprepareaddhelpfuldescriptionsandmeanings] помогают выбрать правильные слова для перевода.

3.  Переведите остальные текстовые узлы.

    В следующем примере показан способ перевода.

    ```xml
    <trans-unit
    	id="ba0cc104d3d69bf669f97b8d96a4c5d8d9559aa3"
    	datatype="html"
    >
    	<source>I don&apos;t output any element</source>
    	<target>Je n'affiche aucun élément</target>
    </trans-unit>
    <trans-unit
    	id="701174153757adf13e7c24a248c8a873ac9f5193"
    	datatype="html"
    >
    	<source>Angular logo</source>
    	<target>Logo d'Angular</target>
    </trans-unit>
    ```

    !!!warning ""

        Не изменяйте идентификаторы для единиц перевода.

        Каждый атрибут `id` генерируется Angular и зависит от содержания текста компонента и назначенного значения.

        Если вы измените либо текст, либо значение, то изменится и атрибут `id`.

        Подробнее об управлении обновлениями текста и идентификаторами см. в разделе [custom IDs][aioguidei18noptionalmanagemarkedtext].

## Переведите множественное число

Добавьте или удалите падежи множественного числа, если это необходимо для каждого языка.

!!!note ""

    Правила множественного числа языка см. в [CLDR plural rules][githubunicodeorgcldrstagingchartslatestsupplementallanguagepluralruleshtml].

### `minute plural` пример

Чтобы перевести `множественное число`, переведите значения соответствия формата ICU.

-   `just now`
-   `one minute ago`
-   `<x id="INTERPOLATION" equiv-text="{{minutes}}"/> minutes ago`

В следующем примере показан способ перевода.

```xml
<trans-unit
    id="5a134dee893586d02bffc9611056b9cadf9abfad"
    datatype="html"
>
    <source>
        {VAR_PLURAL, plural, =0 {just now} =1 {one minute
        ago} other {
        <x id="INTERPOLATION" equiv-text="{{minutes}}" />
        minutes ago} }
    </source>
    <target>
        {VAR_PLURAL, plural, =0 {à l'instant} =1 {il y a une
        minute} other {il y a
        <x id="INTERPOLATION" equiv-text="{{minutes}}" />
        minutes} }
    </target>
</trans-unit>
```

## Перевод альтернативных выражений

Angular также извлекает альтернативные выражения `select` ICU в виде отдельных единиц перевода.

### Пример `gender` `select`

Следующий пример отображает ICU-выражение `select` в шаблоне компонента.

```html
<span i18n
    >The author is {gender, select, male {male} female
    {female} other {other}}</span
>
```

В этом примере Angular разделяет выражение на две единицы перевода. Первая содержит текст вне клаузы `select` и использует место для `select` (`<x id="ICU">`):

```xml
<trans-unit
    id="f99f34ac9bd4606345071bd813858dec29f3b7d1"
    datatype="html"
>
    <source>
        The author is
        <x
            id="ICU"
            equiv-text="{gender, select, male {...} female {...} other {...}}"
        />
    </source>
    <target>
        L'auteur est
        <x
            id="ICU"
            equiv-text="{gender, select, male {...} female {...} other {...}}"
        />
    </target>
</trans-unit>
```

!!!warning ""

    Когда вы переводите текст, при необходимости переместите заполнитель, но не удаляйте его. Если вы удалите заполнитель, выражение ICU будет удалено из переведенного приложения.

В следующем примере отображается вторая единица перевода, содержащая предложение `select`.

```xml
<trans-unit
    id="eff74b75ab7364b6fa888f1cbfae901aaaf02295"
    datatype="html"
>
    <source>
        {VAR_SELECT, select, male {male} female {female}
        other {other} }
    </source>
    <target>
        {VAR_SELECT, select, male {un homme} female {une
        femme} other {autre} }
    </target>
</trans-unit>
```

В следующем примере после завершения перевода отображаются обе единицы перевода.

```xml
<trans-unit
    id="f99f34ac9bd4606345071bd813858dec29f3b7d1"
    datatype="html"
>
    <source>
        The author is
        <x
            id="ICU"
            equiv-text="{gender, select, male {...} female {...} other {...}}"
        />
    </source>
    <target>
        L'auteur est
        <x
            id="ICU"
            equiv-text="{gender, select, male {...} female {...} other {...}}"
        />
    </target>
</trans-unit>
<trans-unit
    id="eff74b75ab7364b6fa888f1cbfae901aaaf02295"
    datatype="html"
>
    <source>
        {VAR_SELECT, select, male {male} female {female}
        other {other} }
    </source>
    <target>
        {VAR_SELECT, select, male {un homme} female {une
        femme} other {autre} }
    </target>
</trans-unit>
```

## Перевод вложенных выражений

Angular обрабатывает вложенное выражение таким же образом, как и альтернативное выражение. Angular разделяет выражение на две единицы перевода.

### Пример вложенного выражения `plural`

В следующем примере отображается первая единица перевода, содержащая текст вне вложенного выражения.

```xml
<trans-unit
    id="972cb0cf3e442f7b1c00d7dab168ac08d6bdf20c"
    datatype="html"
>
    <source>
        Updated:
        <x
            id="ICU"
            equiv-text="{minutes, plural, =0 {...} =1 {...} other {...}}"
        />
    </source>
    <target>
        Mis à jour:
        <x
            id="ICU"
            equiv-text="{minutes, plural, =0 {...} =1 {...} other {...}}"
        />
    </target>
</trans-unit>
```

В следующем примере отображается вторая единица перевода, содержащая полное вложенное выражение.

```xml
<trans-unit
    id="7151c2e67748b726f0864fc443861d45df21d706"
    datatype="html"
>
    <source>
        {VAR_PLURAL, plural, =0 {just now} =1 {one minute
        ago} other {
        <x id="INTERPOLATION" equiv-text="{{minutes}}" />
        minutes ago by {VAR_SELECT, select, male {male}
        female {female} other {other} }} }
    </source>
    <target>
        {VAR_PLURAL, plural, =0 {à l'instant} =1 {il y a une
        minute} other {il y a
        <x id="INTERPOLATION" equiv-text="{{minutes}}" />
        minutes par {VAR_SELECT, select, male {un homme}
        female {une femme} other {autre} }} }
    </target>
</trans-unit>
```

В следующем примере после перевода отображаются обе единицы перевода.

```xml
<trans-unit
    id="972cb0cf3e442f7b1c00d7dab168ac08d6bdf20c"
    datatype="html"
>
    <source>
        Updated:
        <x
            id="ICU"
            equiv-text="{minutes, plural, =0 {...} =1 {...} other {...}}"
        />
    </source>
    <target>
        Mis à jour:
        <x
            id="ICU"
            equiv-text="{minutes, plural, =0 {...} =1 {...} other {...}}"
        />
    </target>
</trans-unit>
<trans-unit
    id="7151c2e67748b726f0864fc443861d45df21d706"
    datatype="html"
>
    <source>
        {VAR_PLURAL, plural, =0 {just now} =1 {one minute
        ago} other {
        <x id="INTERPOLATION" equiv-text="{{minutes}}" />
        minutes ago by {VAR_SELECT, select, male {male}
        female {female} other {other} }} }
    </source>
    <target>
        {VAR_PLURAL, plural, =0 {à l'instant} =1 {il y a une
        minute} other {il y a
        <x id="INTERPOLATION" equiv-text="{{minutes}}" />
        minutes par {VAR_SELECT, select, male {un homme}
        female {une femme} other {autre} }} }
    </target>
</trans-unit>
```

## Что дальше

-   [Слияние переводов в приложение][aioguidei18ncommonmerge]

<!-- links -->

[aioclimain]: https://angular.io/cli
[aiocliextracti18n]: https://angular.io/cli/extract-i18n
[aioguideglossarycommandlineinterfacecli]: glossary.md#command-line-interface-cli
[aioguidei18ncommonmerge]: i18n-common-merge.md
[aioguidei18ncommonprepare]: i18n-common-prepare.md
[aioguidei18ncommonprepareaddhelpfuldescriptionsandmeanings]: i18n-common-prepare.md#add-helpful-descriptions-and-meanings
[aioguidei18ncommontranslationfilescreateatranslationfileforeachlanguage]: i18n-common-translation-files.md#create-a-translation-file-for-each-language
[aioguidei18ncommontranslationfilesextractthesourcelanguagefile]: i18n-common-translation-files.md#extract-the-source-language-file
[aioguidei18ncommontranslationfilestranslatealternateexpressions]: i18n-common-translation-files.md#translate-alternate-expressions
[aioguidei18ncommontranslationfilestranslateeachtranslationfile]: i18n-common-translation-files.md#translate-each-translation-file
[aioguidei18ncommontranslationfilestranslatenestedexpressions]: i18n-common-translation-files.md#translate-nested-expressions
[aioguidei18ncommontranslationfilestranslateplurals]: i18n-common-translation-files.md#translate-plurals
[aioguidei18nexample]: i18n-example.md
[aioguidei18noptionalmanagemarkedtext]: i18n-optional-manage-marked-text.md
[aioguideworkspaceconfig]: workspace-config.md

<!-- external links -->

[githubgoogleappresourcebundlewikiapplicationresourcebundlespecification]: https://github.com/google/app-resource-bundle/wiki/ApplicationResourceBundleSpecification
[githubunicodeorgcldrstagingchartslatestsupplementallanguagepluralruleshtml]: https://unicode-org.github.io/cldr-staging/charts/latest/supplemental/language_plural_rules.html
[jsonmain]: https://www.json.org
[oasisopendocsxliffxliffcorexliffcorehtml]: http://docs.oasis-open.org/xliff/xliff-core/xliff-core.html
[oasisopendocsxliffxliffcorev20cos01xliffcorev20cose01html]: http://docs.oasis-open.org/xliff/xliff-core/v2.0/cos01/xliff-core-v2.0-cos01.html
[unicodecldrdevelopmentdevelopmentprocessdesignproposalsxmb]: http://cldr.unicode.org/development/development-process/design-proposals/xmb
[wikipediawikixliff]: https://en.wikipedia.org/wiki/XLIFF

<!-- end links -->
