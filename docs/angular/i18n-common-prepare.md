# Подготовка компонента к переводу

:date: 28.02.2022

Чтобы подготовить проект к переводу, выполните следующие действия.

-   Используйте атрибут `i18n` для маркировки текста в шаблонах компонентов
-   Используйте атрибут `i18n-` для маркировки текстовых строк атрибутов в шаблонах компонентов
-   Используйте строку сообщения с меткой `$localize` для пометки текстовых строк в коде компонента

## Пометить текст в шаблоне компонента

В шаблоне компонента метаданные i18n являются значением атрибута `i18n`.

```html
<element i18n="{i18n_metadata}"
    >{string_to_translate}</element
>
```

Используйте атрибут `i18n`, чтобы пометить статический текст в шаблонах ваших компонентов для перевода. Поместите его на каждый тег элемента, который содержит фиксированный текст, который вы хотите перевести.

!!!note ""

    Атрибут `i18n` — это пользовательский атрибут, который распознается инструментами и компиляторами Angular.

### `i18n` пример

Следующий тег `<h1>` отображает простое приветствие на английском языке "Hello i18n!".

```html
<h1>Hello i18n!</h1>
```

Чтобы пометить приветствие для перевода, добавьте атрибут `i18n` к тегу `<h1>`.

```html
<h1 i18n>Hello i18n!</h1>
```

### Перевод встроенного текста без элемента HTML

Используйте элемент `<ng-container>`, чтобы связать поведение перевода для определенного текста, не изменяя способ отображения текста.

!!!note ""

    Каждый элемент HTML создает новый элемент DOM. Чтобы избежать создания нового элемента DOM, оберните текст в элемент `<ng-container>`.
    В следующем примере элемент `<ng-container>` преобразован в неотображаемый HTML-комментарий.

    ```html
    <ng-container i18n>I don't output any element</ng-container>
    ```

## Пометить атрибуты элементов для перевода

В шаблоне компонента метаданные i18n являются значением атрибута `i18n-{attribute_name}`.

```html
<element
    i18n-{attribute_name}="{i18n_metadata}"
    {attribute_name}="{attribute_value}"
/>
```

Атрибуты элементов HTML включают текст, который должен быть переведен вместе с остальным отображаемым текстом в шаблоне компонента.

Используйте `i18n-{attribute_name}` с любым атрибутом любого элемента и замените `{attribute_name}` на имя атрибута. Используйте следующий синтаксис для присвоения значения, описания и пользовательского идентификатора.

```
i18n-{attribute_name}="{meaning}|{description}@@{id}"
```

### `i18n-title` пример

Чтобы перевести название изображения, рассмотрите этот пример. В следующем примере отображается изображение с атрибутом `title`.

```html
<img [src]="logo" title="Angular logo" alt="Angular logo" />
```

Чтобы пометить атрибут title для перевода, выполните следующие действия.

1.  Добавьте атрибут `i18n-title`.

    В следующем примере показано, как пометить атрибут `title` в теге `img` путем добавления `i18n-title`.

    ```html
    <img
        [src]="logo"
        i18n-title
        title="Angular logo"
        alt="Angular logo"
    />
    ```

## Mark text in component code

В коде компонента исходный текст перевода и метаданные окружены символами обратного знака (<code>&#96;</code>).

Используйте строку сообщения с меткой [`$localize`][aioapilocalizeinitlocalize], чтобы пометить строку в коде для перевода.

```
$localize `string_to_translate`;
```

Метаданные i18n окружены символами двоеточия (`:`) и дополняют исходный текст перевода.

```
$localize `:{i18n_metadata}:string_to_translate`
```

### Включить интерполированный текст

Включение [интерполяции][aioguideglossaryinterpolation] в строку сообщения с меткой [`$localize`][aioapilocalizeinitlocalize].

```
$localize `string_to_translate ${variable_name}`;
```

### Имя интерполяционного держателя

```
$localize `string_to_translate ${variable_name}:placeholder_name:`;
```

## i18n метаданные для перевода

```
{meaning}|{description}@@{custom_id}
```

Следующие параметры обеспечивают контекст и дополнительную информацию, чтобы ваш переводчик не запутался.

| Параметр метаданных            | Подробности                                               |
| :----------------------------- | :-------------------------------------------------------- |
| Пользовательский идентификатор | Укажите пользовательский идентификатор                    |
| Описание                       | Предоставьте дополнительную информацию или контекст       |
| Значение                       | Укажите смысл или намерение текста в конкретном контексте |

Дополнительные сведения о пользовательских идентификаторах см. в разделе [Управление отмеченным текстом с помощью пользовательских идентификаторов][aioguidei18noptionalmanagemarkedtext].

### Добавляйте полезные описания и значения

Чтобы точно перевести текстовое сообщение, предоставьте переводчику дополнительную информацию или контекст.

Добавьте _описание_ текстового сообщения в качестве значения атрибута `i18n` или [`$localize`][aioapilocalizeinitlocalize] маркированной строки сообщения.

В следующем примере показано значение атрибута `i18n`.

```html
<h1 i18n="An introduction header for this sample">
    Hello i18n!
</h1>
```

Следующий пример показывает значение строки сообщения с меткой [`$localize`][aioapilocalizeinitlocalize] с описанием.

```
$localize `:An introduction header for this sample:Hello i18n!`;
```

Переводчику также может понадобиться знать смысл или намерение текстового сообщения в данном конкретном контексте приложения, чтобы перевести его так же, как и другой текст с тем же смыслом. Начните значение атрибута `i18n` со значения _meaning_ и отделите его от _description_ символом `|`: `{meaning}|{description}`.

#### `h1` пример

Например, вы можете указать, что тег `<h1>` является заголовком сайта, который нужно перевести одинаково, независимо от того, используется ли он в качестве заголовка или является ссылкой в другом разделе текста.

В следующем примере показано, как указать, что тег `<h1>` должен быть переведен как заголовок или как ссылка в другом месте.

```html
<h1
    i18n="site header|An introduction header for this sample"
>
    Hello i18n!
</h1>
```

В результате любой текст, помеченный `site header`, как _значение_ переводится точно так же.

Следующий пример кода показывает значение строки сообщения с меткой [`$localize`][aioapilocalizeinitlocalize] со значением и описанием.

```
$localize `:site header|An introduction header for this sample:Hello i18n!`;
```

!!!note "Как значения управляют извлечением и объединением текста"

    Инструмент извлечения Angular генерирует запись единицы перевода для каждого атрибута `i18n` в шаблоне. Инструмент извлечения Angular присваивает каждой единице перевода уникальный идентификатор, основанный на _значении_ и _описании_.

    Подробнее об инструменте извлечения Angular см. в разделе [Работа с файлами переводов][aioguidei18ncommontranslationfiles].

    Одни и те же элементы текста с разными _значениями_ извлекаются с разными идентификаторами. Например, если для слова "right" используются следующие два определения в двух разных местах, это слово переводится по-разному и объединяется обратно в приложение в виде разных записей перевода.

    -   `correct` в значении "вы правы"
    -   `direction` в значении "повернуть направо".

    Если одни и те же элементы текста удовлетворяют следующим условиям, элементы текста извлекаются только один раз и используют один и тот же идентификатор.

    -   Одинаковое значение или определение
    -   Разные описания

    Эта одна запись перевода объединяется обратно в приложение везде, где появляются одинаковые элементы текста.

## Выражения ICU

Выражения ICU помогают отметить альтернативный текст в шаблонах компонентов для выполнения условий. Выражение ICU включает свойство компонента, условие ICU и утверждения case, окруженные символами открытой фигурной скобки (`{`) и закрытой фигурной скобки (`}`).

```
{ component_property, icu_clause, case_statements }
```

Свойство компонента определяет переменную В ICU-клаузе определяется тип условного текста.

| ICU clause                                                              | Подробности                                                                             |
| :---------------------------------------------------------------------- | :-------------------------------------------------------------------------------------- |
| [`plural`][aioguidei18ncommonpreparemarkplurals]                        | Отметить использование множественного числа                                             |
| [`select`][aioguidei18ncommonpreparemarkalternatesandnestedexpressions] | Отметьте варианты альтернативного текста на основе определенных вами строковых значений |

Чтобы упростить перевод, используйте Международные компоненты для Юникода (ICU clauses) с регулярными выражениями.

!!!note ""

    Клаузулы ICU придерживаются [формата сообщений ICU][githubunicodeorgicuuserguideformatparsemessages], указанного в [правилах плюрализации CLDR][unicodecldrindexcldrspecpluralrules].

### Обозначьте множественное число

В разных языках действуют разные правила использования множественного числа, что увеличивает сложность перевода. Поскольку в других языках по-разному выражается кардинальность, вам может понадобиться установить категории множественного числа, которые не совпадают с английскими.

Используйте предложение `plural`, чтобы отметить выражения, которые могут не иметь смысла при дословном переводе.

```
{ component_property, plural, pluralization_categories }
```

После категории множественного числа введите текст по умолчанию (English), окруженный символами открытой фигурной скобки (`{`) и закрытой фигурной скобки (`}`).

<!--todo: replace with code-example -->

```
pluralization_category { }
```

Следующие категории множественного числа доступны для английского языка и могут меняться в зависимости от локали.

| Pluralization category | Details                    | Example                    |
| :--------------------- | :------------------------- | :------------------------- |
| `zero`                 | Quantity is zero           | `=0 { }` <br /> `zero { }` |
| `one`                  | Quantity is 1              | `=1 { }` <br /> `one { }`  |
| `two`                  | Quantity is 2              | `=2 { }` <br /> `two { }`  |
| `few`                  | Quantity is 2 or more      | `few { }`                  |
| `many`                 | Quantity is a large number | `many { }`                 |
| `other`                | The default quantity       | `other { }`                |

Если ни одна из категорий множественного числа не совпадает, Angular использует `other` для стандартного возврата к отсутствующей категории.

```
other { default_quantity }
```

!!!note ""

    Для получения дополнительной информации о категориях множественного числа см. раздел [Выбор имен категорий множественного числа][unicodecldrindexcldrspecpluralrulestocchoosingpluralcategorynames] в [CLDR - Unicode Common Locale Data Repository][unicodecldrmain].

!!!warning "Предыстория: Локалы могут не поддерживать некоторые категории множественного числа"

    Многие локали не поддерживают некоторые категории множественного числа. Локаль по умолчанию (`en-US`) использует очень простую функцию `plural()`, которая не поддерживает категорию множественного числа `few`.

    Другой локалью с простой функцией `plural()` является `es`.

    В следующем примере кода показана функция [en-US `plural()`][githubangularangularblobecffc3557fe1bff9718c01277498e877ca44588dpackagescoresrci18nlocaleentsl14l18].

    ```ts
    function plural(n: number): number {
    	let i = Math.floor(Math.abs(n)),
    		v = n.toString().replace(/^[^.]*\.?/, '').length;
    	if (i === 1 && v === 0) return 1;
    	return 5;
    }
    ```

    Функция `plural()` возвращает только 1 (`один`) или 5 (`другой`). Категория `несколько` никогда не подходит.

#### `minutes` пример

Если вы хотите отобразить следующую фразу на английском языке, где `x` — число.

```
updated x minutes ago
```

И вы также хотите отобразить следующие фразы на основе кардинальности `x`.

```
updated just now
```

```
updated one minute ago
```

Используйте HTML-разметку и [интерполяцию][aioguideglossaryinterpolation].
Следующий пример кода показывает, как использовать предложение `plural` для выражения трех предыдущих ситуаций в элементе `<span>`.

```html
<span i18n
    >Updated {minutes, plural, =0 {just now} =1 {one minute
    ago} other {{{minutes}} minutes ago}}</span
>
```

Просмотрите следующие детали в предыдущем примере кода.

| Параметры                        | Детали                                                                                                                                      |
| :------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------ |
| `minutes`                        | Первый параметр указывает на свойство компонента `minutes` и определяет количество минут.                                                   |
| `plural`                         | Второй параметр определяет свойство ICU — `plural`.                                                                                         |
| `=0 {только что}`                | Для нулевых минут категория множественного числа — `=0`. Значение — `только что`.                                                           |
| `=1 {одна минута}`               | Для одной минуты категория множественного числа — `=1`. Значение — `одна минута`.                                                           |
| `other {{minutes}} minutes ago}` | Для любой несопоставимой кардинальности категорией множественного числа по умолчанию является `other`. Значение — `{{минуты}} минут назад`. |

`{{minutes}}` является [интерполяцией][aioguideglossaryinterpolation].

### Отметка альтернатив и вложенных выражений

Пункт `select` отмечает варианты альтернативного текста на основе определенных вами строковых значений.

```
{ component_property, select, selection_categories }
```

Переведите все альтернативы для отображения альтернативного текста на основе значения переменной.

После категории выбора введите текст (English), окруженный символами открытой фигурной скобки (`{`) и закрытой фигурной скобки (`}`).

```
selection_category { text }
```

В разных странах существуют разные грамматические конструкции, что увеличивает сложность перевода. Используйте HTML-разметку.

Если ни одна из категорий выбора не совпадает, Angular использует `other` для стандартного возврата к отсутствующей категории.

```
other { default_value }
```

#### `gender` пример

Если вы хотите отобразить следующую фразу на английском языке.

```
The author is other
```

И вы также хотите отобразить следующие фразы на основе свойства `gender` компонента.

```
The author is female
```

```
The author is male
```

Следующий пример кода показывает, как связать свойство `gender` компонента и использовать предложение `select` для выражения трех предыдущих ситуаций в элементе `<span>`.

Свойство `gender` связывает выходы с каждым из следующих строковых значений.

| Value  | English value |
| :----- | :------------ |
| female | `female`      |
| male   | `male`        |
| other  | `other`       |

Предложение `select` сопоставляет значения с соответствующими переводами.
В следующем примере кода свойство `gender` используется с предложением select.

```html
<span i18n
    >The author is {gender, select, male {male} female
    {female} other {other}}</span
>
```

#### `gender` и `minutes` примеры

Объединяйте различные предложения вместе, например, предложения `plural` и `select`.
Следующий пример кода показывает вложенные предложения, основанные на примерах `gender` и `minutes`.

```html
<span i18n
    >Updated: {minutes, plural, =0 {just now} =1 {one minute
    ago} other {{{minutes}} minutes ago by {gender, select,
    male {male} female {female} other {other}}}}
</span>
```

## Что дальше

-   [Работа с файлами переводов][aioguidei18ncommontranslationfiles]

[aioapilocalizeinitlocalize]: https://angular.io/api/localize/init/$localize
[aioguideglossaryinterpolation]: glossary.md#interpolation
[aioguidei18ncommonprepare]: i18n-common-prepare.md
[aioguidei18ncommonprepareaddhelpfuldescriptionsandmeanings]: i18n-common-prepare.md#add-helpful-descriptions-and-meanings
[aioguidei18ncommonpreparemarkalternatesandnestedexpressions]: i18n-common-prepare.md#mark-alternates-and-nested-expressions
[aioguidei18ncommonpreparemarkelementattributesfortranslations]: i18n-common-prepare.md#mark-element-attributes-for-translations
[aioguidei18ncommonpreparemarkplurals]: i18n-common-prepare.md#mark-plurals
[aioguidei18ncommonpreparemarktextincomponenttemplate]: i18n-common-prepare.md#mark-text-in-component-template
[aioguidei18ncommontranslationfiles]: i18n-common-translation-files.md
[aioguidei18noptionalmanagemarkedtext]: i18n-optional-manage-marked-text.md
[githubangularangularblobecffc3557fe1bff9718c01277498e877ca44588dpackagescoresrci18nlocaleentsl14l18]: https://github.com/angular/angular/blob/ecffc3557fe1bff9718c01277498e877ca44588d/packages/core/src/i18n/locale_en.ts#L14-L18
[githubunicodeorgicuuserguideformatparsemessages]: https://unicode-org.github.io/icu/userguide/format_parse/messages
[unicodecldrmain]: https://cldr.unicode.org
[unicodecldrindexcldrspecpluralrules]: http://cldr.unicode.org/index/cldr-spec/plural-rules
[unicodecldrindexcldrspecpluralrulestocchoosingpluralcategorynames]: http://cldr.unicode.org/index/cldr-spec/plural-rules#TOC-Choosing-Plural-Category-Names
