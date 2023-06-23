# Подготовка компонента к переводу

Чтобы подготовить проект к переводу, выполните следующие действия.

-   Используйте атрибут `i18n` для маркировки текста в шаблонах компонентов

-   Используйте атрибут `i18n-` для маркировки текстовых строк атрибутов в шаблонах компонентов

-   Используйте строку сообщения с меткой `$localize` для пометки текстовых строк в коде компонента

## Пометить текст в шаблоне компонента

В шаблоне компонента метаданные i18n являются значением атрибута `i18n`.

<code-example format="html" language="html">

&lt;element i18n="{i18n_metadata}"&gt;{string_to_translate}&lt;/element&gt;

</code-example>

Используйте атрибут `i18n`, чтобы пометить статический текст в шаблонах ваших компонентов для перевода. Поместите его на каждый тег элемента, который содержит фиксированный текст, который вы хотите перевести.

<div class="alert is-helpful">

Атрибут `i18n` - это пользовательский атрибут, который распознается инструментами и компиляторами Angular.

</div>

### `i18n` пример

Следующий тег `<h1>` отображает простое приветствие на английском языке "Hello i18n!".

<code-example header="src/app/app.component.html" path="i18n/doc-files/app.component.html" region="greeting"></code-example>.

Чтобы пометить приветствие для перевода, добавьте атрибут `i18n` к тегу `<h1>`.

<code-example header="src/app/app.component.html" path="i18n/doc-files/app.component.html" region="i18n-attribute"></code-example>

### Перевод встроенного текста без элемента HTML

Используйте элемент `<ng-container>`, чтобы связать поведение перевода для определенного текста, не изменяя способ отображения текста.

<div class="alert is-helpful">

Каждый элемент HTML создает новый элемент DOM. Чтобы избежать создания нового элемента DOM, оберните текст в элемент `<ng-container>`.
В следующем примере элемент `<ng-container>` преобразован в неотображаемый HTML-комментарий.

<code-example path="i18n/src/app/app.component.html" region="i18n-ng-container"></code-example>.

</div>

## Пометить атрибуты элементов для перевода

В шаблоне компонента метаданные i18n являются значением атрибута `i18n-{имя_атрибута}`.

<code-example format="html" language="html">

&lt;element i18n-{attribute_name}="{i18n_metadata}" {attribute_name}="{attribute_value}" /&gt;

</code-example>

Атрибуты элементов HTML включают текст, который должен быть переведен вместе с остальным отображаемым текстом в шаблоне компонента.

Используйте `i18n-{имя_атрибута}` с любым атрибутом любого элемента и замените `{имя_атрибута}` на имя атрибута. Используйте следующий синтаксис для присвоения значения, описания и пользовательского идентификатора.

<!--todo: replace with code-example -->

<code-example format="html" language="html">

i18n-{имя_атрибута}="{значение}|{описание}&commat;&commat;{id}"

</code-example>

### `i18n-title` пример

Чтобы перевести название изображения, рассмотрите этот пример. В следующем примере отображается изображение с атрибутом `title`.

<code-example header="src/app/app.component.html" path="i18n/doc-files/app.component.html" region="i18n-title"></code-example>

To mark the title attribute for translation, complete the following action.

1.  Add the `i18n-title` attribute

    The following example displays how to mark the `title` attribute on the `img` tag by adding `i18n-title`.

    <code-example header="src/app/app.component.html" path="i18n/src/app/app.component.html" region="i18n-title-translate"></code-example>

## Mark text in component code

In component code, the translation source text and the metadata are surrounded by backtick \(<code>&#96;</code>\) characters.

Use the [`$localize`][aioapilocalizeinitlocalize] tagged message string to mark a string in your code for translation.

<!--todo: replace with code-example -->

<code-example format="typescript" language="typescript">

\$localize `string_to_translate`;

</code-example>

Метаданные i18n окружены символами двоеточия \(`:`\) и дополняют исходный текст перевода.

<!--todo: replace with code-example -->

<code-example format="typescript" language="typescript">

\$localize `:{i18n_metadata}:string_to_translate`

</code-example>

### Включить интерполированный текст

Включение [интерполяции][aioguideglossaryinterpolation] в строку сообщения с меткой [`$localize`][aioapilocalizeinitlocalize].

<!--todo: replace with code-example -->

<code-example format="typescript" language="typescript">

\$localize `string_to_translate &dollar;{variable_name}`;

</code-example>

### Имя интерполяционного держателя

<code-example format="typescript" language="typescript">

\$localize `string_to_translate &dollar;{variable_name}:placeholder_name:`;

</code-example>

## i18n метаданные для перевода

<!--todo: replace with code-example -->

<code-example>

{meaning}|{description}&commat;&commat;{custom_id}

</code-example>

Следующие параметры обеспечивают контекст и дополнительную информацию, чтобы ваш переводчик не запутался.

| Параметр метаданных | Подробности | | :----------------- | :-------------------------------------------------------------------- |

| Пользовательский идентификатор | Укажите пользовательский идентификатор |

| Описание | Предоставьте дополнительную информацию или контекст |

| Значение | Укажите смысл или намерение текста в конкретном контексте | |

Дополнительные сведения о пользовательских идентификаторах см. в разделе [Управление отмеченным текстом с помощью пользовательских идентификаторов][aioguidei18noptionalmanagemarkedtext].

### Добавляйте полезные описания и значения

Чтобы точно перевести текстовое сообщение, предоставьте переводчику дополнительную информацию или контекст.

Добавьте _описание_ текстового сообщения в качестве значения атрибута `i18n` или [`$localize`][aioapilocalizeinitlocalize] маркированной строки сообщения.

В следующем примере показано значение атрибута `i18n`.

<code-example header="src/app/app.component.html" path="i18n/doc-files/app.component.html" region="i18n-attribute-desc"></code-example>.

Следующий пример показывает значение строки сообщения с меткой [`$localize`][aioapilocalizeinitlocalize] с описанием.

<!--todo: replace with code-example -->

<code-example format="typescript" language="typescript">

\$localize`:Вводный заголовок для этого образца:Hello i18n!`;

</code-example>

Переводчику также может понадобиться знать смысл или намерение текстового сообщения в данном конкретном контексте приложения, чтобы перевести его так же, как и другой текст с тем же смыслом. Начните значение атрибута `i18n` со значения _meaning_ и отделите его от _description_ символом `|`: `{meaning}|{description}`.

#### `h1` пример

Например, вы можете указать, что тег `<h1>` является заголовком сайта, который нужно перевести одинаково, независимо от того, используется ли он в качестве заголовка или является ссылкой в другом разделе текста.

В следующем примере показано, как указать, что тег `<h1>` должен быть переведен как заголовок или как ссылка в другом месте.

<code-example header="src/app/app.component.html" path="i18n/doc-files/app.component.html" region="i18n-attribute-meaning"></code-example>.

В результате любой текст, помеченный `site header`, как _значение_ переводится точно так же.

Следующий пример кода показывает значение строки сообщения с меткой [`$localize`][aioapilocalizeinitlocalize] со значением и описанием.

<!--todo: replace with code-example -->

<code-example format="typescript" language="typescript">

\$localize `:site header|Вводный заголовок для этого образца:Hello i18n!`;

</code-example>

<div class="callout is-helpful">

<header>
 <a name="how-meanings-control-text-extraction-and-merges"></a> How meanings control text extraction and merges
</header>

Инструмент извлечения Angular генерирует запись единицы перевода для каждого атрибута `i18n` в шаблоне. Инструмент извлечения Angular присваивает каждой единице перевода уникальный идентификатор, основанный на _значении_ и _описании_.

<div class="alert is-helpful">

Подробнее об инструменте извлечения Angular см. в разделе [Работа с файлами переводов][aioguidei18ncommontranslationfiles].

</div>

Одни и те же элементы текста с разными _значениями_ извлекаются с разными идентификаторами. Например, если для слова "right" используются следующие два определения в двух разных местах, это слово переводится по-разному и объединяется обратно в приложение в виде разных записей перевода.

-   `корректный` в значении "вы правы"

-   `направление` в значении "повернуть направо".

Если одни и те же элементы текста удовлетворяют следующим условиям, элементы текста извлекаются только один раз и используют один и тот же идентификатор.

-   Одинаковое значение или определение

-   Разные описания

Эта одна запись перевода объединяется обратно в приложение везде, где появляются одинаковые элементы текста.

</div>

## Выражения ICU

Выражения ICU помогают отметить альтернативный текст в шаблонах компонентов для выполнения условий. Выражение ICU включает свойство компонента, условие ICU и утверждения case, окруженные символами открытой фигурной скобки \(`{`\) и закрытой фигурной скобки \(`}`\).

<!--todo: replace with code-example -->

<code-example>

{ component_property, icu_clause, case_statements }

</code-example>

Свойство компонента определяет переменную В ICU-клаузе определяется тип условного текста.

| ICU clause | Details | | | :---------------------------------------------------------------------- | :------------------------------------------------------------------ | |

| [`plural`][aioguidei18ncommonpreparemarkplurals] | Отметить использование множественного числа |

| [`select`][aioguidei18ncommonpreparemarkalternatesandnestedexpressions] | Отметьте варианты альтернативного текста на основе определенных вами строковых значений |

Чтобы упростить перевод, используйте Международные компоненты для Юникода \(ICU clauses\) с регулярными выражениями.

<div class="alert is-helpful">

Клаузулы ICU придерживаются [формата сообщений ICU][githubunicodeorgicuuserguideformatparsemessages], указанного в [правилах плюрализации CLDR][unicodecldrindexcldrspecpluralrules].

</div>

### Обозначьте множественное число

В разных языках действуют разные правила использования множественного числа, что увеличивает сложность перевода. Поскольку в других языках по-разному выражается кардинальность, вам может понадобиться установить категории множественного числа, которые не совпадают с английскими.

Используйте предложение `plural`, чтобы отметить выражения, которые могут не иметь смысла при дословном переводе.

<!--todo: replace with code-example -->

<code-example>

{ component_property, plural, pluralization_categories }

</code-example>

После категории множественного числа введите текст по умолчанию \(English\), окруженный символами открытой фигурной скобки \(`{`\) и закрытой фигурной скобки \(`}`\).

<!--todo: replace with code-example -->

<code-example>

pluralization_category { }

</code-example>

The following pluralization categories are available for English and may change based on the locale.

| Pluralization category | Details | Example | | :--------------------- | :------------------------- | :------------------------- |

| `zero` | Quantity is zero | `=0 { }` <br /> `zero { }` |

| `one` | Quantity is 1 | `=1 { }` <br /> `one { }` |

| `two` | Quantity is 2 | `=2 { }` <br /> `two { }` |

| `few` | Quantity is 2 or more | `few { }` |

| `many` | Quantity is a large number | `many { }` |

| `other` | The default quantity | `other { }` |

If none of the pluralization categories match, Angular uses `other` to match the standard fallback for a missing category.

<!--todo: replace with code-example -->

<code-example>

другие { default_quantity }

</code-example>

<div class="alert is-helpful">

Для получения дополнительной информации о категориях множественного числа см. раздел [Выбор имен категорий множественного числа][unicodecldrindexcldrspecpluralrulestocchoosingpluralcategorynames] в [CLDR - Unicode Common Locale Data Repository][unicodecldrmain].

</div>

<div class="callout is-important">

<a name="background-locales-may-not-support-some-pluralization-categories"></a>

<header>Background: Locales may not support some pluralization categories</header>

Многие локали не поддерживают некоторые категории множественного числа. Локаль по умолчанию \(`en-US`\) использует очень простую функцию `plural()`, которая не поддерживает категорию множественного числа `few`.
Другой локалью с простой функцией `plural()` является `es`.

В следующем примере кода показана функция [en-US `plural()`][githubangularangularblobecffc3557fe1bff9718c01277498e877ca44588dpackagescoresrci18nlocaleentsl14l18].

<code-example path="i18n/doc-files/locale_plural_function.ts" class="no-box" hideCopy></code-example>.

Функция `plural()` возвращает только 1 \(`один`\) или 5 \(`другой`\). Категория `несколько` никогда не подходит.

</div>

#### `минуты` пример

Если вы хотите отобразить следующую фразу на английском языке, где `x` - число.

<!--todo: replace output code-example with screen capture image --->

<code-example>

updated x minutes ago

</code-example>

And you also want to display the following phrases based on the cardinality of `x`.

<!--todo: replace output code-example with screen capture image --->

<code-example>

updated just now

</code-example>

<!--todo: replace output code-example with screen capture image --->

<code-example>

updated one minute ago

</code-example>

Use HTML markup and [interpolations][aioguideglossaryinterpolation].
The following code example shows how to use the `plural` clause to express the previous three situations in a `<span>` element.

<code-example header="src/app/app.component.html" path="i18n/src/app/app.component.html" region="i18n-plural"></code-example>

Review the following details in the previous code example.

| Parameters                        | Details                                                                                                               |
| :-------------------------------- | :-------------------------------------------------------------------------------------------------------------------- |
| `minutes`                         | The first parameter specifies the component property is `minutes` and determines the number of minutes.               |
| `plural`                          | The second parameter specifies the ICU clause is `plural`.                                                            |
| `=0 {just now}`                   | For zero minutes, the pluralization category is `=0`. The value is `just now`.                                        |
| `=1 {one minute}`                 | For one minute, the pluralization category is `=1`. The value is `one minute`.                                        |
| `other {{{minutes}} minutes ago}` | For any unmatched cardinality, the default pluralization category is `other`. The value is `{{minutes}} minutes ago`. |

`{{minutes}}` is an [interpolation][aioguideglossaryinterpolation].

### Mark alternates and nested expressions

The `select` clause marks choices for alternate text based on your defined string values.

<!--todo: replace with code-example -->

<code-example>

{ component_property, select, selection_categories }

</code-example>

Переведите все альтернативы для отображения альтернативного текста на основе значения переменной.

После категории выбора введите текст \(English\), окруженный символами открытой фигурной скобки \(`{`\) и закрытой фигурной скобки \(`}`\).

<!--todo: replace with code-example -->

<code-example>

selection_category { text }

</code-example>

В разных странах существуют разные грамматические конструкции, что увеличивает сложность перевода. Используйте HTML-разметку.
Если ни одна из категорий выбора не совпадает, Angular использует `other` для стандартного возврата к отсутствующей категории.

<!--todo: replace with code-example -->

<code-example>

other { default_value }

</code-example>

#### `gender` пример

Если вы хотите отобразить следующую фразу на английском языке.

<!--todo: replace output code-example with screen capture image --->

<code-example>

The author is other

</code-example>

And you also want to display the following phrases based on the `gender` property of the component.

<!--todo: replace output code-example with screen capture image --->

<code-example>

The author is female

</code-example>

<!--todo: replace output code-example with screen capture image --->

<code-example>

The author is male

</code-example>

The following code example shows how to bind the `gender` property of the component and use the `select` clause to express the previous three situations in a `<span>` element.

The `gender` property binds the outputs to each of following string values.

| Value  | English value |
| :----- | :------------ |
| female | `female`      |
| male   | `male`        |
| other  | `other`       |

The `select` clause maps the values to the appropriate translations.
The following code example shows `gender` property used with the select clause.

<code-example header="src/app/app.component.html" path="i18n/src/app/app.component.html" region="i18n-select"></code-example>

#### `gender` and `minutes` example

Combine different clauses together, such as the `plural` and `select` clauses.
The following code example shows nested clauses based on the `gender` and `minutes` examples.

<code-example header="src/app/app.component.html" path="i18n/src/app/app.component.html" region="i18n-nested"></code-example>

## What's next

-   [Work with translation files][aioguidei18ncommontranslationfiles]

<!-- links -->

[aioapilocalizeinitlocalize]: api/localize/init/$localize '$localize | init - localize - API  | Angular'
[aioguideglossaryinterpolation]: guide/glossary#interpolation 'interpolation - Glossary | Angular'
[aioguidei18ncommonprepare]: guide/i18n-common-prepare 'Prepare component for translation | Angular'
[aioguidei18ncommonprepareaddhelpfuldescriptionsandmeanings]: guide/i18n-common-prepare#add-helpful-descriptions-and-meanings 'Add helpful descriptions and meanings - Prepare component for translation | Angular'
[aioguidei18ncommonpreparemarkalternatesandnestedexpressions]: guide/i18n-common-prepare#mark-alternates-and-nested-expressions 'Mark alternates and nested expressions - Prepare templates for translation | Angular'
[aioguidei18ncommonpreparemarkelementattributesfortranslations]: guide/i18n-common-prepare#mark-element-attributes-for-translations 'Mark element attributes for translations - Prepare component for translation | Angular'
[aioguidei18ncommonpreparemarkplurals]: guide/i18n-common-prepare#mark-plurals 'Mark plurals - Prepare component for translation | Angular'
[aioguidei18ncommonpreparemarktextincomponenttemplate]: guide/i18n-common-prepare#mark-text-in-component-template 'Mark text in component template - Prepare component for translation | Angular'
[aioguidei18ncommontranslationfiles]: guide/i18n-common-translation-files 'Work with translation files | Angular'
[aioguidei18noptionalmanagemarkedtext]: guide/i18n-optional-manage-marked-text 'Manage marked text with custom IDs | Angular'

<!-- external links -->

[githubangularangularblobecffc3557fe1bff9718c01277498e877ca44588dpackagescoresrci18nlocaleentsl14l18]: https://github.com/angular/angular/blob/ecffc3557fe1bff9718c01277498e877ca44588d/packages/core/src/i18n/locale_en.ts#L14-L18 'Line 14 to 18 - angular/packages/core/src/i18n/locale_en.ts | angular/angular | GitHub'
[githubunicodeorgicuuserguideformatparsemessages]: https://unicode-org.github.io/icu/userguide/format_parse/messages 'ICU Message Format - ICU Documentation | Unicode | GitHub'
[unicodecldrmain]: https://cldr.unicode.org 'Unicode CLDR Project'
[unicodecldrindexcldrspecpluralrules]: http://cldr.unicode.org/index/cldr-spec/plural-rules 'Plural Rules | CLDR - Unicode Common Locale Data Repository | Unicode'
[unicodecldrindexcldrspecpluralrulestocchoosingpluralcategorynames]: http://cldr.unicode.org/index/cldr-spec/plural-rules#TOC-Choosing-Plural-Category-Names 'Choosing Plural Category Names - Plural Rules | CLDR - Unicode Common Locale Data Repository | Unicode'

<!-- end links -->

:date: 28.02.2022
