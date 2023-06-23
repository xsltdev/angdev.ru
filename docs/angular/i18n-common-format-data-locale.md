# Форматирование данных на основе локали

Angular предоставляет следующие встроенные средства преобразования данных [pipes][aioguideglossarypipe]. Трубы преобразования данных используют токен [`LOCALE_ID`][aioapicorelocaleid] для форматирования данных на основе правил каждой локали.

| Труба преобразования данных | Подробности | | | :----------------------------------------- | :------------------------------------------------ |.

| [`DatePipe`][aioapicommondatepipe] | Форматирует значение даты. |

| [`CurrencyPipe`][aioapicommoncurrencypipe] | Преобразование числа в строку валюты. |

| | [`DecimalPipe`][aioapicommondecimalpipe] | Преобразование числа в десятичную строку. |

| | [`PercentPipe`][aioapicommonpercentpipe] | Преобразование числа в процентную строку. |

## Использование DatePipe для отображения текущей даты

Чтобы отобразить текущую дату в формате для текущей локали, используйте следующий формат для `DatePipe`.

<!--todo: replace with code-example -->

<code-example format="typescript" language="typescript">

{{ today &verbar; date }}

</code-example>

## Переопределение текущей локали для CurrencyPipe

Добавьте параметр `locale` в трубу, чтобы переопределить текущее значение токена `LOCALE_ID`.

Чтобы заставить валюту использовать американский английский \(`en-US`\), используйте следующий формат для `CurrencyPipe`

<!--todo: replace with code-example -->

<code-example format="typescript" language="typescript">

{{ amount &verbar; currency : 'en-US' }}

</code-example>

<div class="alert is-helpful">

**NOTE**: <br /> The locale specified for the `CurrencyPipe` overrides the global `LOCALE_ID` token of your application.

</div>

## Что дальше

-   [Подготовка компонента к переводу][aioguidei18ncommonprepare]

<!-- links -->

[aioapicommoncurrencypipe]: api/common/CurrencyPipe 'CurrencyPipe | Common - API | Angular'
[aioapicommondatepipe]: api/common/DatePipe 'DatePipe | Common - API | Angular'
[aioapicommondecimalpipe]: api/common/DecimalPipe 'DecimalPipe | Common - API | Angular'
[aioapicommonpercentpipe]: api/common/PercentPipe 'PercentPipe | Common - API | Angular'
[aioapicorelocaleid]: api/core/LOCALE_ID 'LOCALE_ID | Core - API | Angular'
[aioguideglossarypipe]: guide/glossary#pipe 'pipe - Glossary | Angular'
[aioguidei18ncommonprepare]: guide/i18n-common-prepare 'Prepare component for translation | Angular'

<!-- external links -->

<!-- end links -->

:date: 28.02.2022
