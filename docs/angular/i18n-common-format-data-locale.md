# Форматирование данных на основе локали

:date: 28.02.2022

Angular предоставляет следующие встроенные средства преобразования данных [pipes][aioguideglossarypipe]. Трубы преобразования данных используют токен [`LOCALE_ID`][aioapicorelocaleid] для форматирования данных на основе правил каждой локали.

| Пайп преобразования данных                 | Подробности                               |
| :----------------------------------------- | :---------------------------------------- |
| [`DatePipe`][aioapicommondatepipe]         | Форматирует значение даты.                |
| [`CurrencyPipe`][aioapicommoncurrencypipe] | Преобразование числа в строку валюты.     |
| [`DecimalPipe`][aioapicommondecimalpipe]   | Преобразование числа в десятичную строку. |
| [`PercentPipe`][aioapicommonpercentpipe]   | Преобразование числа в процентную строку. |

## Использование DatePipe для отображения текущей даты

Чтобы отобразить текущую дату в формате для текущей локали, используйте следующий формат для `DatePipe`.

```
{{ today | date }}
```

## Переопределение текущей локали для CurrencyPipe

Добавьте параметр `locale` в пайп, чтобы переопределить текущее значение токена `LOCALE_ID`.

Чтобы заставить валюту использовать американский английский (`en-US`), используйте следующий формат для `CurrencyPipe`

<!--todo: replace with code-example -->

```
{{ amount | currency : 'en-US' }}
```

!!!note ""

    Локаль, указанная для `CurrencyPipe`, переопределяет глобальный токен `LOCALE_ID` вашего приложения.

## Что дальше

-   [Подготовка компонента к переводу][aioguidei18ncommonprepare]

[aioapicommoncurrencypipe]: https://angular.io/api/common/CurrencyPipe
[aioapicommondatepipe]: https://angular.io/api/common/DatePipe
[aioapicommondecimalpipe]: https://angular.io/api/common/DecimalPipe
[aioapicommonpercentpipe]: https://angular.io/api/common/PercentPipe
[aioapicorelocaleid]: https://angular.io/api/core/LOCALE_ID
[aioguideglossarypipe]: glossary.md#pipe
[aioguidei18ncommonprepare]: i18n-common-prepare.md
