# Обращение к локалям по идентификатору

:date: 28.10.2021

Angular использует идентификатор _локали Unicode_ (Unicode locale ID), чтобы найти правильные данные локали для интернационализации текстовых строк.

!!!note "Unicode locale ID"

    -   Идентификатор локали соответствует [Unicode Common Locale Data Repository (CLDR) core specification][unicodecldrdevelopmentcorespecification].
    	Дополнительную информацию об идентификаторах локалей см. в [Unicode Language and Locale Identifiers][unicodecldrdevelopmentcorespecificationhvgyyng33o798].

    -   CLDR и Angular используют [теги BCP 47][rfceditorinfobcp47] в качестве основы для идентификатора локали

Идентификатор локали определяет язык, страну и необязательный код для дальнейших вариантов или подразделений. Идентификатор локали состоит из идентификатора языка, символа дефиса (`-`) и расширения локали.

```
{language_id}-{locale_extension}
```

!!!note ""

    Чтобы точно перевести ваш проект Angular, вы должны решить, на какие языки и локали вы ориентируетесь для интернационализации.

    Многие страны используют один и тот же язык, но различаются в его использовании. Различия включают грамматику, пунктуацию, форматы валюты, десятичных чисел, дат и так далее.

Для примеров, приведенных в данном руководстве, используйте следующие языки и локали.

| Язык        | Локаль                    | ID локали Unicode |
| :---------- | :------------------------ | :---------------- |
| Английский  | Канада                    | `en-CA`           |
| Английский  | Соединенные Штаты Америки | `en-US`           |
| Французский | Канада                    | `fr-CA`           |
| Французский | Франция                   | `fr-FR`           |

В [репозитории Angular][githubangularangulartreemasterpackagescommonlocales] содержатся общие локали.

!!!note ""

    Список кодов языков см. в [ISO 639-2][locstandardsiso6392].

## Установите идентификатор локали источника

Используйте Angular CLI, чтобы установить язык источника, на котором вы пишете шаблон и код компонента.

По умолчанию Angular использует `en-US` в качестве исходной локали вашего проекта.

Чтобы изменить локаль источника вашего проекта для сборки, выполните следующие действия.

1.  Откройте файл конфигурации сборки рабочего пространства [`angular.json`][aioguideworkspaceconfig].
2.  Измените локаль источника в поле `sourceLocale`.

## Что дальше

-   [Форматирование данных на основе локали][aioguidei18ncommonformatdatalocale].

[aioguidei18ncommonformatdatalocale]: i18n-common-format-data-locale.md
[aioguidei18ncommonmerge]: i18n-common-merge.md
[aioguideworkspaceconfig]: workspace-config.md
[githubangularangulartreemasterpackagescommonlocales]: https://github.com/angular/angular/tree/main/packages/common/locales
[locstandardsiso6392]: https://www.loc.gov/standards/iso639-2
[rfceditorinfobcp47]: https://www.rfc-editor.org/info/bcp47
[unicodecldrdevelopmentcorespecification]: https://cldr.unicode.org/development/core-specification
[unicodecldrdevelopmentcorespecificationhvgyyng33o798]: https://cldr.unicode.org/development/core-specification#h.vgyyng33o798
