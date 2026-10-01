---
description: "Пайпы декларативно преобразуют данные в выражениях шаблона: преобразование объявляют один раз и используют в разных шаблонах."
---

# Пайпы {: #pipes}

:date: 30.09.2026

## Обзор {: #overview}

Пайпы — особые операторы в выражениях шаблона Angular: они декларативно преобразуют данные прямо в шаблоне. Функцию преобразования объявляют один раз и затем используют в разных шаблонах. Пайпы Angular записывают вертикальной чертой (`|`) — по аналогии с [конвейером Unix](<https://en.wikipedia.org/wiki/Pipeline_(Unix)>).

!!! info ""

    Синтаксис пайпов Angular отличается от обычного JavaScript, где вертикальная черта означает [оператор побитового ИЛИ](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Bitwise_OR). Выражения шаблона Angular не поддерживают побитовые операторы.

Пример с несколькими встроенными пайпами Angular:

```ts
import {Component} from '@angular/core';
import {CurrencyPipe, DatePipe, TitleCasePipe} from '@angular/common';

@Component({
  selector: 'app-root',
  imports: [CurrencyPipe, DatePipe, TitleCasePipe],
  template: `
    <main>
      <!-- Transform the company name to title-case and
       transform the purchasedOn date to a locale-formatted string -->
      <h1>Purchases from {{ company | titlecase }} on {{ purchasedOn | date }}</h1>

      <!-- Transform the amount to a currency-formatted string -->
      <p>Total: {{ amount | currency }}</p>
    </main>
  `,
})
export class ShoppingCart {
  amount = 123.45;
  company = 'acme corporation';
  purchasedOn = '2024-07-08';
}
```

При отрисовке компонента Angular подбирает формат даты и валюты по локали пользователя. Для пользователя из США получится так:

```html
<main>
  <h1>Purchases from Acme Corporation on Jul 8, 2024</h1>
  <p>Total: $123.45</p>
</main>
```

Подробнее о том, как Angular локализует значения, — в [подробном руководстве по интернационализации](https://angular.dev/guide/i18n).

### Встроенные пайпы {: #built-in-pipes}

В пакете `@angular/common` есть набор встроенных пайпов:

| Имя | Описание |
| --------------------------------------------- | --------------------------------------------------------------------------------------------- |
| [`AsyncPipe`](https://angular.dev/api/common/AsyncPipe) | Читает значение из `Promise` или RxJS `Observable`. |
| [`CurrencyPipe`](https://angular.dev/api/common/CurrencyPipe) | Преобразует число в строку валюты по правилам локали. |
| [`DatePipe`](https://angular.dev/api/common/DatePipe) | Форматирует значение `Date` по правилам локали. |
| [`DecimalPipe`](https://angular.dev/api/common/DecimalPipe) | Преобразует число в строку с десятичной точкой по правилам локали. |
| [`I18nPluralPipe`](https://angular.dev/api/common/I18nPluralPipe) | Сопоставляет значение со строкой, которая ставит его во множественное число по правилам локали. |
| [`I18nSelectPipe`](https://angular.dev/api/common/I18nSelectPipe) | Сопоставляет ключ с пользовательским селектором, который возвращает нужное значение. |
| [`JsonPipe`](https://angular.dev/api/common/JsonPipe) | Преобразует объект в строку через `JSON.stringify`, предназначен для отладки. |
| [`KeyValuePipe`](https://angular.dev/api/common/KeyValuePipe) | Преобразует Object или Map в массив пар «ключ — значение». |
| [`LowerCasePipe`](https://angular.dev/api/common/LowerCasePipe) | Переводит текст в нижний регистр. |
| [`PercentPipe`](https://angular.dev/api/common/PercentPipe) | Преобразует число в строку процентов по правилам локали. |
| [`SlicePipe`](https://angular.dev/api/common/SlicePipe) | Создаёт новый Array или String с подмножеством (срезом) элементов. |
| [`TitleCasePipe`](https://angular.dev/api/common/TitleCasePipe) | Переводит текст в регистр заголовка. |
| [`UpperCasePipe`](https://angular.dev/api/common/UpperCasePipe) | Переводит текст в верхний регистр. |

## Использование пайпов {: #using-pipes}

Оператор пайпа Angular — вертикальная черта (`|`) внутри выражения шаблона. Это бинарный оператор: левый операнд — значение, которое передаётся функции преобразования, правый — имя пайпа и дополнительные аргументы (о них ниже).

```html
<p>Total: {{ amount | currency }}</p>
```

В этом примере значение `amount` передаётся в `CurrencyPipe`, имя пайпа — `currency`. Затем отрисовывается валюта по умолчанию для локали пользователя.

### Несколько пайпов в одном выражении {: #combining-multiple-pipes-in-the-same-expression}

К одному значению можно применить несколько преобразований, поставив несколько операторов пайпа. Angular выполняет пайпы слева направо.

В примере ниже пайпы вместе показывают локализованную дату в верхнем регистре:

```html
<p>The event will occur on {{ scheduledOn | date | uppercase }}.</p>
```

### Передача параметров пайпам {: #passing-parameters-to-pipes}

Некоторые пайпы принимают параметры, которые настраивают преобразование. Параметр указывают после имени пайпа через двоеточие (`:`) и значение параметра.

Например, `DatePipe` принимает параметры, чтобы отформатировать дату определённым образом.

```html
<p>The event will occur at {{ scheduledOn | date: 'hh:mm' }}.</p>
```

Некоторые пайпы принимают несколько параметров. Дополнительные значения разделяют двоеточием (`:`).

Например, вторым необязательным параметром можно задать часовой пояс.

```html
<p>The event will occur at {{ scheduledOn | date: 'hh:mm' : 'UTC' }}.</p>
```

## Как работают пайпы {: #how-pipes-work}

По сути пайпы — функции: они принимают входное значение и возвращают преобразованное.

```ts
import {Component} from '@angular/core';
import {CurrencyPipe} from '@angular/common';

@Component({
  selector: 'app-root',
  imports: [CurrencyPipe],
  template: `
    <main>
      <p>Total: {{ amount | currency }}</p>
    </main>
  `,
})
export class AppComponent {
  amount = 123.45;
}
```

В этом примере:

1.  `CurrencyPipe` импортируется из `@angular/common`
1.  `CurrencyPipe` добавляется в массив `imports`
1.  Данные `amount` передаются пайпу `currency`

### Приоритет оператора пайпа {: #pipe-operator-precedence}

Приоритет оператора пайпа ниже, чем у других бинарных операторов, включая `+`, `-`, `*`, `/`, `%`, `&&`, `||` и `??`.

```html
<!-- firstName and lastName are concatenated before the result is passed to the uppercase pipe -->
{{ firstName + lastName | uppercase }}
```

Приоритет оператора пайпа выше, чем у условного (тернарного) оператора.

```html
{{ (isAdmin ? 'Access granted' : 'Access denied') | uppercase }}
```

Если то же выражение записать без скобок:

```html
{{ isAdmin ? 'Access granted' : 'Access denied' | uppercase }}
```

Оно будет разобрано так:

```html
{{ isAdmin ? 'Access granted' : ('Access denied' | uppercase) }}
```

Если приоритет операторов может быть неоднозначным, ставьте в выражениях скобки.

### Обнаружение изменений и пайпы {: #change-detection-with-pipes}

По умолчанию все пайпы считаются `pure`: они выполняются только когда меняется примитивное входное значение (например, `String`, `Number`, `Boolean` или `Symbol`) или ссылка на объект (например, `Array`, `Object`, `Function` или `Date`). Чистые пайпы выгодны по производительности: Angular не вызывает функцию преобразования, если переданное значение не изменилось.

Поэтому мутации свойств объекта или элементов массива не обнаруживаются, пока всю ссылку на объект или массив не заменят другим экземпляром. Если нужно обнаружение изменений такого уровня, смотрите [обнаружение изменений внутри массивов и объектов](#detecting-change-within-arrays-or-objects).

## Создание собственных пайпов {: #creating-custom-pipes}

Собственный пайп задают классом TypeScript с декоратором `@Pipe`. У пайпа должно быть две вещи:

-   Имя, указанное в декораторе пайпа
-   Метод с именем `transform`, который выполняет преобразование значения.

Класс TypeScript дополнительно должен реализовать интерфейс `PipeTransform`, чтобы удовлетворять сигнатуре типа пайпа.

Пример собственного пайпа, который переводит строки в kebab-case:

_kebab-case.pipe.ts_

```ts
import {Pipe, PipeTransform} from '@angular/core';

@Pipe({
  name: 'kebabCase',
})
export class KebabCasePipe implements PipeTransform {
  transform(value: string): string {
    return value.toLowerCase().replace(/ /g, '-');
  }
}
```

### Декоратор `@Pipe` {: #using-the-pipe-decorator}

При создании собственного пайпа импортируйте `Pipe` из пакета `@angular/core` и повесьте его декоратором на класс TypeScript.

```ts
import {Pipe} from '@angular/core';

@Pipe({
  name: 'myCustomTransformation',
})
export class MyCustomTransformationPipe {}
```

Декоратору `@Pipe` нужен `name`: он задаёт, как пайп используется в шаблоне.

### Соглашение об именах собственных пайпов {: #naming-convention-for-custom-pipes}

Соглашение об именах собственных пайпов состоит из двух правил:

-   `name` — рекомендуется camelCase. Дефисы не используйте.
-   `class name` — вариант `name` в PascalCase с суффиксом `Pipe` в конце

### Реализация интерфейса `PipeTransform` {: #implement-the-pipetransform-interface}

Помимо декоратора `@Pipe`, собственные пайпы всегда должны реализовать интерфейс `PipeTransform` из `@angular/core`.

```ts
import {Pipe, PipeTransform} from '@angular/core';

@Pipe({
  name: 'myCustomTransformation',
})
export class MyCustomTransformationPipe implements PipeTransform {}
```

Реализация этого интерфейса гарантирует, что у класса пайпа правильная структура.

### Преобразование значения пайпа {: #transforming-the-value-of-a-pipe}

Каждое преобразование вызывает метод `transform`: первый параметр — передаваемое значение, возвращаемое значение — результат преобразования.

```ts
import {Pipe, PipeTransform} from '@angular/core';

@Pipe({
  name: 'myCustomTransformation',
})
export class MyCustomTransformationPipe implements PipeTransform {
  transform(value: string): string {
    return `My custom transformation of ${value}.`;
  }
}
```

### Параметры собственного пайпа {: #adding-parameters-to-a-custom-pipe}

Параметры преобразования добавляют дополнительными параметрами метода `transform`:

```ts
import {Pipe, PipeTransform} from '@angular/core';

@Pipe({
  name: 'myCustomTransformation',
})
export class MyCustomTransformationPipe implements PipeTransform {
  transform(value: string, format: string): string {
    let msg = `My custom transformation of ${value}.`;

    if (format === 'uppercase') {
      return msg.toUpperCase();
    } else {
      return msg;
    }
  }
}
```

### Обнаружение изменений внутри массивов и объектов {: #detecting-change-within-arrays-or-objects}

Чтобы пайп обнаруживал изменения внутри массивов или объектов, его помечают нечистой функцией: флаг `pure` со значением `false`.

!!! warning ""

    Не создавайте нечистые пайпы без крайней необходимости: при неосторожном использовании они сильно бьют по производительности.

```ts
import {Pipe, PipeTransform} from '@angular/core';

@Pipe({
  name: 'joinNamesImpure',
  pure: false,
})
export class JoinNamesImpurePipe implements PipeTransform {
  transform(names: string[]): string {
    return names.join();
  }
}
```

Разработчики Angular часто добавляют `Impure` в `name` пайпа и в имя класса, чтобы предупредить коллег о возможной потере производительности.

## Логика пайпа вне шаблонов {: #using-pipe-logic-outside-templates}

Пайпы — операторы шаблона для декларативного преобразования данных в шаблонах. Если та же логика нужна в сервисе, вспомогательном классе или любом другом контексте вне шаблона, **не внедряйте класс пайпа**. Пайпы не задуманы как внедряемые сервисы.

### Вынесите логику из собственных пайпов {: #extract-the-logic-from-custom-pipes}

Когда создаёте собственный пайп, вынесите преобразование в отдельную функцию. Метод `transform()` пайпа пусть делегирует этой функции, а саму функцию импортируйте напрямую везде, где она ещё нужна.

_kebab-case.ts_

```ts
export function toKebabCase(value: string): string {
  return value.toLowerCase().replace(/ /g, '-');
}
```

_kebab-case.pipe.ts_

```ts
import {Pipe, PipeTransform} from '@angular/core';
import {toKebabCase} from './kebab-case';

@Pipe({name: 'kebabCase'})
export class KebabCasePipe implements PipeTransform {
  transform(value: string): string {
    return toKebabCase(value);
  }
}
```

_formatter.service.ts_

```ts
import {Service} from '@angular/core';
import {toKebabCase} from './kebab-case';

@Service()
export class FormatterService {
  formatSlug(title: string): string {
    return toKebabCase(title);
  }
}
```

_formatter.service.ts_

```ts
import {Service} from '@angular/core';
import {KebabCasePipe} from './kebab-case.pipe';

@Service()
export class FormatterService {
  // Avoid injecting the pipe class into services or other classes.
  private kebabCasePipe = inject(KebabCasePipe);

  formatSlug(title: string): string {
    return this.kebabCasePipe.transform(title);
  }
}
```

### Функции форматирования вместо встроенных пайпов {: #use-formatting-functions-for-built-in-pipes}

У каждого встроенного пайпа Angular, который учитывает локаль, есть соответствующая отдельная функция форматирования, экспортируемая из `@angular/common`. Используйте эти функции вместо внедрения класса пайпа.

| Пайп | Отдельная функция |
| -------------- | ------------------- |
| `DatePipe` | `formatDate` |
| `CurrencyPipe` | `formatCurrency` |
| `DecimalPipe` | `formatNumber` |
| `PercentPipe` | `formatPercent` |

```ts
import {Service, LOCALE_ID, inject} from '@angular/core';
import {formatNumber} from '@angular/common';

@Service()
export class PriceService {
  private locale = inject(LOCALE_ID);

  format(value: number) {
    return formatNumber(value, this.locale, '1.2-2');
  }
}
```

```ts
import {Service} from '@angular/core';
import {DecimalPipe} from '@angular/common';

@Service()
export class PriceService {
  private decimalPipe = inject(DecimalPipe);

  format(value: number) {
    return this.decimalPipe.transform(value, '1.2-2');
  }
}
```


---

Источник: [https://angular.dev/guide/templates/pipes](https://angular.dev/guide/templates/pipes)
