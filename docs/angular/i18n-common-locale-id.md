# Обращение к локалям по идентификатору

Angular использует идентификатор _локали Unicode_ \(Unicode locale ID\), чтобы найти правильные данные локали для интернационализации текстовых строк.

<div class="callout is-helpful">

<header>Unicode locale ID</header>

-   Идентификатор локали соответствует [Unicode Common Locale Data Repository (CLDR) core specification][unicodecldrdevelopmentcorespecification].
    Дополнительную информацию об идентификаторах локалей см. в [Unicode Language and Locale Identifiers][unicodecldrdevelopmentcorespecificationhvgyyng33o798].

-   CLDR и Angular используют [теги BCP 47][rfceditorinfobcp47] в качестве основы для идентификатора локали

</div>

Идентификатор локали определяет язык, страну и необязательный код для дальнейших вариантов или подразделений. Идентификатор локали состоит из идентификатора языка, символа дефиса \(`-`\) и расширения локали.

<code-example>

{language_id}-{locale_extension}

</code-example>

<div class="alert is-helpful">

Чтобы точно перевести ваш проект Angular, вы должны решить, на какие языки и локали вы ориентируетесь для интернационализации.

Многие страны используют один и тот же язык, но различаются в его использовании. Различия включают грамматику, пунктуацию, форматы валюты, десятичных чисел, дат и так далее.

</div>

Для примеров, приведенных в данном руководстве, используйте следующие языки и локали.

| Язык | Локаль | ID локали Unicode | | :------- | :----------------------- | :---------------- | |

| Английский | Канада | `en-CA` |

| Английский | Соединенные Штаты Америки | `en-US'| |

| Французский | Канада | `fr-CA` | |

| Французский | Франция | `fr-FR'| |

В [репозитории Angular][githubangularangulartreemasterpackagescommonlocales] содержатся общие локали.

<div class="callout is-helpful">

Список кодов языков см. в [ISO 639-2][locstandardsiso6392].

</div>

## Установите идентификатор локали источника

Используйте Angular CLI, чтобы установить язык источника, на котором вы пишете шаблон и код компонента.

По умолчанию Angular использует `en-US` в качестве исходной локали вашего проекта.

Чтобы изменить локаль источника вашего проекта для сборки, выполните следующие действия.

1.  Откройте файл конфигурации сборки рабочего пространства [`angular.json`][aioguideworkspaceconfig].

1.  Измените локаль источника в поле `sourceLocale`.

## Что дальше

-   [Форматирование данных на основе локали][aioguidei18ncommonformatdatalocale].

<!-- links -->

[aioguidei18ncommonformatdatalocale]: guide/i18n-common-format-data-locale 'Format data based on locale | Angular'
[aioguidei18ncommonmerge]: guide/i18n-common-merge 'Merge translations into the application | Angular'
[aioguideworkspaceconfig]: guide/workspace-config 'Angular workspace configuration | Angular'

<!-- external links -->

[githubangularangulartreemasterpackagescommonlocales]: https://github.com/angular/angular/tree/main/packages/common/locales 'angular/packages/common/locales | angular/angular | GitHub'
[locstandardsiso6392]: https://www.loc.gov/standards/iso639-2 'ISO 639-2 Registration Authority | Library of Congress'
[rfceditorinfobcp47]: https://www.rfc-editor.org/info/bcp47 'BCP 47 | RFC Editor'
[unicodecldrdevelopmentcorespecification]: https://cldr.unicode.org/development/core-specification 'Core Specification | Unicode CLDR Project'
[unicodecldrdevelopmentcorespecificationhvgyyng33o798]: https://cldr.unicode.org/development/core-specification#h.vgyyng33o798 'Unicode Language and Locale Identifiers - Core Specification | Unicode CLDR Project'

<!-- end links -->

:date: 28.10.2021
