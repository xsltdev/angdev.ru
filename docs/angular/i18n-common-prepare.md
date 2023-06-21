# Prepare component for translation

To prepare your project for translation, complete the following actions.

-   Use the `i18n` attribute to mark text in component templates
-   Use the `i18n-` attribute to mark attribute text strings in component templates
-   Use the `$localize` tagged message string to mark text strings in component code

## Mark text in component template

In a component template, the i18n metadata is the value of the `i18n` attribute.

<code-example format="html" language="html">

&lt;element i18n="{i18n_metadata}"&gt;{string_to_translate}&lt;/element&gt;

</code-example>

Use the `i18n` attribute to mark a static text message in your component templates for translation.
Place it on every element tag that contains fixed text you want to translate.

<div class="alert is-helpful">

The `i18n` attribute is a custom attribute that the Angular tools and compilers recognize.

</div>

### `i18n` example

The following `<h1>` tag displays a simple English language greeting, "Hello i18n!".

<code-example header="src/app/app.component.html" path="i18n/doc-files/app.component.html" region="greeting"></code-example>

To mark the greeting for translation, add the `i18n` attribute to the `<h1>` tag.

<code-example header="src/app/app.component.html" path="i18n/doc-files/app.component.html" region="i18n-attribute"></code-example>

### Translate inline text without HTML element

Use the `<ng-container>` element to associate a translation behavior for specific text without changing the way text is displayed.

<div class="alert is-helpful">

Each HTML element creates a new DOM element.
To avoid creating a new DOM element, wrap the text in an `<ng-container>` element.
The following example shows the `<ng-container>` element transformed into a non-displayed HTML comment.

<code-example path="i18n/src/app/app.component.html" region="i18n-ng-container"></code-example>

</div>

## Mark element attributes for translations

In a component template, the i18n metadata is the value of the `i18n-{attribute_name}` attribute.

<code-example format="html" language="html">

&lt;element i18n-{attribute_name}="{i18n_metadata}" {attribute_name}="{attribute_value}" /&gt;

</code-example>

The attributes of HTML elements include text that should be translated along with the rest of the displayed text in the component template.

Use `i18n-{attribute_name}` with any attribute of any element and replace `{attribute_name}` with the name of the attribute.
Use the following syntax to assign a meaning, description, and custom ID.

<!--todo: replace with code-example -->

<code-example format="html" language="html">

i18n-{attribute_name}="{meaning}|{description}&commat;&commat;{id}"

</code-example>

### `i18n-title` example

To translate the title of an image, review this example.
The following example displays an image with a `title` attribute.

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

The i18n metadata is surrounded by colon \(`:`\) characters and prepends the translation source text.

<!--todo: replace with code-example -->

<code-example format="typescript" language="typescript">

\$localize `:{i18n_metadata}:string_to_translate`

</code-example>

### Include interpolated text

Include [interpolations][aioguideglossaryinterpolation] in a [`$localize`][aioapilocalizeinitlocalize] tagged message string.

<!--todo: replace with code-example -->

<code-example format="typescript" language="typescript">

\$localize `string_to_translate &dollar;{variable_name}`;

</code-example>

### Name the interpolation placeholder

<code-example format="typescript" language="typescript">

\$localize `string_to_translate &dollar;{variable_name}:placeholder_name:`;

</code-example>

## i18n metadata for translation

<!--todo: replace with code-example -->

<code-example>

{meaning}|{description}&commat;&commat;{custom_id}

</code-example>

The following parameters provide context and additional information to reduce confusion for your translator.

| Metadata parameter | Details                                                               |
| :----------------- | :-------------------------------------------------------------------- |
| Custom ID          | Provide a custom identifier                                           |
| Description        | Provide additional information or context                             |
| Meaning            | Provide the meaning or intent of the text within the specific context |

For additional information about custom IDs, see [Manage marked text with custom IDs][aioguidei18noptionalmanagemarkedtext].

### Add helpful descriptions and meanings

To translate a text message accurately, provide additional information or context for the translator.

Add a _description_ of the text message as the value of the `i18n` attribute or [`$localize`][aioapilocalizeinitlocalize] tagged message string.

The following example shows the value of the `i18n` attribute.

<code-example header="src/app/app.component.html" path="i18n/doc-files/app.component.html" region="i18n-attribute-desc"></code-example>

The following example shows the value of the [`$localize`][aioapilocalizeinitlocalize] tagged message string with a description.

<!--todo: replace with code-example -->

<code-example format="typescript" language="typescript">

\$localize `:An introduction header for this sample:Hello i18n!`;

</code-example>

The translator may also need to know the meaning or intent of the text message within this particular application context, in order to translate it the same way as other text with the same meaning.
Start the `i18n` attribute value with the _meaning_ and separate it from the _description_ with the `|` character: `{meaning}|{description}`.

#### `h1` example

For example, you may want to specify that the `<h1>` tag is a site header that you need translated the same way, whether it is used as a header or referenced in another section of text.

The following example shows how to specify that the `<h1>` tag must be translated as a header or referenced elsewhere.

<code-example header="src/app/app.component.html" path="i18n/doc-files/app.component.html" region="i18n-attribute-meaning"></code-example>

The result is any text marked with `site header`, as the _meaning_ is translated exactly the same way.

The following code example shows the value of the [`$localize`][aioapilocalizeinitlocalize] tagged message string with a meaning and a description.

<!--todo: replace with code-example -->

<code-example format="typescript" language="typescript">

\$localize `:site header|An introduction header for this sample:Hello i18n!`;

</code-example>

<div class="callout is-helpful">

<header>
<a name="how-meanings-control-text-extraction-and-merges"></a> How meanings control text extraction and merges
</header>

The Angular extraction tool generates a translation unit entry for each `i18n` attribute in a template.
The Angular extraction tool assigns each translation unit a unique ID based on the _meaning_ and _description_.

<div class="alert is-helpful">

For more information about the Angular extraction tool, see [Work with translation files][aioguidei18ncommontranslationfiles].

</div>

The same text elements with different _meanings_ are extracted with different IDs.
For example, if the word "right" uses the following two definitions in two different locations, the word is translated differently and merged back into the application as different translation entries.

-   `correct` as in "you are right"
-   `direction` as in "turn right"

If the same text elements meet the following conditions, the text elements are extracted only once and use the same ID.

-   Same meaning or definition
-   Different descriptions

That one translation entry is merged back into the application wherever the same text elements appear.

</div>

## ICU expressions

ICU expressions help you mark alternate text in component templates to meet conditions.
An ICU expression includes a component property, an ICU clause, and the case statements surrounded by open curly brace \(`{`\) and close curly brace \(`}`\) characters.

<!--todo: replace with code-example -->

<code-example>

{ component_property, icu_clause, case_statements }

</code-example>

The component property defines the variable
An ICU clause defines the type of conditional text.

| ICU clause                                                              | Details                                                             |
| :---------------------------------------------------------------------- | :------------------------------------------------------------------ |
| [`plural`][aioguidei18ncommonpreparemarkplurals]                        | Mark the use of plural numbers                                      |
| [`select`][aioguidei18ncommonpreparemarkalternatesandnestedexpressions] | Mark choices for alternate text based on your defined string values |

To simplify translation, use International Components for Unicode clauses \(ICU clauses\) with regular expressions.

<div class="alert is-helpful">

The ICU clauses adhere to the [ICU Message Format][githubunicodeorgicuuserguideformatparsemessages] specified in the [CLDR pluralization rules][unicodecldrindexcldrspecpluralrules].

</div>

### Mark plurals

Different languages have different pluralization rules that increase the difficulty of translation.
Because other locales express cardinality differently, you may need to set pluralization categories that do not align with English.
Use the `plural` clause to mark expressions that may not be meaningful if translated word-for-word.

<!--todo: replace with code-example -->

<code-example>

{ component_property, plural, pluralization_categories }

</code-example>

After the pluralization category, enter the default text \(English\) surrounded by open curly brace \(`{`\) and close curly brace \(`}`\) characters.

<!--todo: replace with code-example -->

<code-example>

pluralization_category { }

</code-example>

The following pluralization categories are available for English and may change based on the locale.

| Pluralization category | Details                    | Example                    |
| :--------------------- | :------------------------- | :------------------------- |
| `zero`                 | Quantity is zero           | `=0 { }` <br /> `zero { }` |
| `one`                  | Quantity is 1              | `=1 { }` <br /> `one { }`  |
| `two`                  | Quantity is 2              | `=2 { }` <br /> `two { }`  |
| `few`                  | Quantity is 2 or more      | `few { }`                  |
| `many`                 | Quantity is a large number | `many { }`                 |
| `other`                | The default quantity       | `other { }`                |

If none of the pluralization categories match, Angular uses `other` to match the standard fallback for a missing category.

<!--todo: replace with code-example -->

<code-example>

other { default_quantity }

</code-example>

<div class="alert is-helpful">

For more information about pluralization categories, see [Choosing plural category names][unicodecldrindexcldrspecpluralrulestocchoosingpluralcategorynames] in the [CLDR - Unicode Common Locale Data Repository][unicodecldrmain].

</div>

<div class="callout is-important">

<a name="background-locales-may-not-support-some-pluralization-categories"></a>

<header>Background: Locales may not support some pluralization categories</header>

Many locales don't support some of the pluralization categories.
The default locale \(`en-US`\) uses a very simple `plural()` function that doesn't support the `few` pluralization category.
Another locale with a simple `plural()` function is `es`.
The following code example shows the [en-US `plural()`][githubangularangularblobecffc3557fe1bff9718c01277498e877ca44588dpackagescoresrci18nlocaleentsl14l18] function.

<code-example path="i18n/doc-files/locale_plural_function.ts" class="no-box" hideCopy></code-example>

The `plural()` function only returns 1 \(`one`\) or 5 \(`other`\).
The `few` category never matches.

</div>

#### `minutes` example

If you want to display the following phrase in English, where `x` is a number.

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

Translate all of the alternates to display alternate text based on the value of a variable.

After the selection category, enter the text \(English\) surrounded by open curly brace \(`{`\) and close curly brace \(`}`\) characters.

<!--todo: replace with code-example -->

<code-example>

selection_category { text }

</code-example>

Different locales have different grammatical constructions that increase the difficulty of translation.
Use HTML markup.
If none of the selection categories match, Angular uses `other` to match the standard fallback for a missing category.

<!--todo: replace with code-example -->

<code-example>

other { default_value }

</code-example>

#### `gender` example

If you want to display the following phrase in English.

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
