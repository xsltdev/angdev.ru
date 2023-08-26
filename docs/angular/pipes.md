---
description: Используйте пайпы для преобразования строк, сумм валют, дат и других данных для отображения на экране
---

# Преобразование данных с помощью пайпов

:date: 28.02.2022

Используйте [пайпы](glossary.md#pipe 'Определение пайпа') для преобразования строк, сумм валют, дат и других данных для отображения на экране. Пайпы — это простые функции, которые можно использовать в [шаблонных выражениях](glossary.md#template-expression 'Определение шаблонного выражения') для приема входного значения и возврата преобразованного значения. Пайпы полезны тем, что их можно использовать во всем приложении, объявляя каждый пайп только один раз. Например, с помощью пайпа можно отобразить дату в виде **April 15, 1988**, а не в виде необработанной строки.

!!!note ""

    Пример приложения, используемый в данной теме, приведен в [живом примере](https://angular.io/generated/live-examples/pipes/stackblitz.html).

Angular предоставляет встроенные пайпы для типичных преобразований данных, включая преобразования для интернационализации (i18n), которые используют информацию о локали для форматирования данных. Ниже перечислены часто используемые встроенные пайпы для форматирования данных:

| Трубы                                                          | Подробнее                                                                                               |
| :------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------ |
| [`DatePipe`](https://angular.io/api/common/DatePipe)           | Формирование значения даты в соответствии с правилами локали.                                           |
| [`UpperCasePipe`](https://angular.io/api/common/UpperCasePipe) | Преобразование текста в верхний регистр.                                                                |
| [`LowerCasePipe`](https://angular.io/api/common/LowerCasePipe) | Преобразование текста во все строчные регистры.                                                         |
| [`CurrencyPipe`](https://angular.io/api/common/CurrencyPipe)   | Преобразование числа в строку валюты, отформатированную в соответствии с правилами локали.              |
| [`DecimalPipe`](https://angular.io/api/common/DecimalPipe)     | Преобразование числа в строку с десятичной точкой, отформатированную в соответствии с правилами локали. |
| [`PercentPipe`](https://angular.io/api/common/PercentPipe)     | Преобразование числа в строку с процентами, оформленную в соответствии с правилами локали.              |

!!!note ""

    -   Полный список встроенных пайпов приведен в документации [pipes API](https://angular.io/api/common#pipes 'Pipes API reference summary').
    -   Подробнее об использовании пайпов для интернационализации (i18n) см. в разделе [Форматирование данных в зависимости от локали][aioguidei18ncommonformatdatalocale].

Создание пайпов для инкапсуляции пользовательских преобразований и использование пользовательских пайпов в шаблонных выражениях.

## Предварительные условия

Для использования пайпов необходимо иметь базовое представление о следующем:

-   [Typescript](glossary.md#typescript 'Определение Typescript') и программирования HTML5
-   [Шаблоны](glossary.md#template 'Определение шаблона') в HTML со стилями CSS
-   [Components](glossary.md#component 'Определение компонента')

## Использование пайпа в шаблоне

Чтобы применить пайп, используйте символ пайпа (`|`) в выражении шаблона, как показано в следующем примере кода, вместе с _именем_ пайпа, которым является `date` для встроенного [`DatePipe`](https://angular.io/api/common/DatePipe).
Вкладки в примере выглядят следующим образом:

| Файлы                         | Подробности                                                                                                           |
| :---------------------------- | :-------------------------------------------------------------------------------------------------------------------- |
| `app.component.html`          | Использует `date` в отдельном шаблоне для отображения дня рождения.                                                   |
| `hero-birthday1.component.ts` | Использует тот же пайп как часть встроенного шаблона в компоненте, который также устанавливает значение дня рождения. |

=== "src/app/app.component.html"

    ```html
    <p>The hero's birthday is {{ birthday | date }}</p>
    ```

=== "src/app/hero-birthday1.component.ts"

    ```ts
    import { Component } from '@angular/core';

    @Component({
    	selector: 'app-hero-birthday',
    	template:
    		"<p>The hero's birthday is {{ birthday | date }}</p>",
    })
    export class HeroBirthdayComponent {
    	birthday = new Date(1988, 3, 15); // April 15, 1988 -- since month parameter is zero-based
    }
    ```

Значение `birthday` компонента через оператор пайпа, `|`, попадает в функцию [`date`](https://angular.io/api/common/DatePipe).

<a id="parameterizing-a-pipe"></a>

## Преобразование данных с помощью параметров и цепочек пайпов

Используйте необязательные параметры для точной настройки выходных данных пайпа. Например, используйте [`CurrencyPipe`](https://angular.io/api/common/CurrencyPipe 'API reference') с кодом страны, например EUR, в качестве параметра. Шаблонное выражение `{{ amount | currency:'EUR' }}` преобразует `amount` в валюту в евро. После имени пайпа (`currency`) следует символ двоеточия (`:`) и значение параметра (`'EUR'`).

Если пайп принимает несколько параметров, разделяйте их значения двоеточиями. Например, `{{ amount | currency:'EUR':'Euros'}}` добавляет второй параметр, строковый литерал `'Euros'`, в выходную строку. В качестве параметра можно использовать любое допустимое выражение шаблона, например, строковый литерал или свойство компонента.

Некоторые пайпы требуют как минимум один параметр и допускают большее количество необязательных параметров, например [`SlicePipe`](https://angular.io/api/common/SlicePipe 'API reference for SlicePipe'). Например, `{{ slice:1:5 }}` создает новый массив или строку, содержащую подмножество элементов, начиная с элемента `1` и заканчивая элементом `5`.

### Пример: Форматирование даты

На вкладках в следующем примере демонстрируется переключение между двумя различными форматами (`'shortDate'` и `'fullDate'`):

-   Шаблон `app.component.html` использует параметр формата для [`DatePipe`](https://angular.io/api/common/DatePipe) (с именем `date`), чтобы показать дату как **04/15/88**.
-   Компонент `hero-birthday2.component.ts` привязывает параметр формата пайпа к свойству `format` компонента в секции `template` и добавляет кнопку для события click, привязанную к методу `toggleFormat()` компонента.
-   Метод `toggleFormat()` компонента `hero-birthday2.component.ts` переключает свойство `format` компонента между короткой формой (`'shortDate'`) и более длинной (`'fullDate'`).

=== "src/app/app.component.html"

    ```html
    <p>
    	The hero's birthday is {{ birthday | date:"MM/dd/yy" }}
    </p>
    ```

=== "src/app/hero-birthday2.component.ts (template)"

    ```ts
    template: `
    <p>The hero's birthday is {{ birthday | date:format }}</p>
    <button type="button" (click)="toggleFormat()">Toggle Format</button>
    `;
    ```

=== "src/app/hero-birthday2.component.ts (class)"

    ```ts
    export class HeroBirthday2Component {
    	birthday = new Date(1988, 3, 15); // April 15, 1988 -- since month parameter is zero-based
    	toggle = true; // start with true == shortDate

    	get format() {
    		return this.toggle ? 'shortDate' : 'fullDate';
    	}
    	toggleFormat() {
    		this.toggle = !this.toggle;
    	}
    }
    ```

При нажатии на кнопку **Toggle Format** формат даты чередуется между **04/15/1988** и **Friday, April 15, 1988**.

!!!note ""

    Параметры формата пайпа `date` см. в разделе [DatePipe](https://angular.io/api/common/DatePipe 'Справочная страница по API DatePipe').

### Пример: Применение двух форматов с помощью цепочки пайпов

Цепочка пайпов позволяет сделать так, чтобы выход одного пайпа стал входом для следующего.

В следующем примере цепочки пайпов сначала применяют формат к значению даты, а затем преобразуют отформатированную дату в заглавные символы. Первая вкладка шаблона `src/app/app.component.html` связывает `DatePipe` и `UpperCasePipe` для отображения дня рождения как **APR 15, 1988**. На второй вкладке шаблона `src/app/app.component.html` параметр `fullDate` передается в `date` перед цепочкой в `uppercase`, в результате чего получается **FRIDAY, APRIL 15, 1988**.

=== "src/app/app.component.html (1)"

    ```html
    The chained hero's birthday is {{ birthday | date |
    uppercase}}
    ```

=== "src/app/app.component.html (2)"

    ```html
    The chained hero's birthday is {{ birthday | date:'fullDate'
    | uppercase}}
    ```

<a id="Custom-pipes"></a>

## Создание пайпов для пользовательских преобразований данных

Создайте пользовательские пайпы для инкапсуляции преобразований, которые не предусмотрены встроенными пайпами. Затем используйте пользовательские пайпы в шаблонных выражениях так же, как и встроенные пайпы &mdash; для преобразования входных значений в выходные значения для отображения.

### Пометка класса как пайпа

Чтобы пометить класс как пайп и снабдить его конфигурационными метаданными, примените к классу [`@Pipe`](https://angular.io/api/core/Pipe 'API reference for Pipe') [decorator](glossary.md#decorator--decoration 'Definition for decorator'). Используйте [UpperCamelCase](glossary.md#case-types 'Определение типов регистра') (общее соглашение для имен классов) для имени класса пайпа и [camelCase](glossary.md#case-types 'Определение типов регистра') для соответствующей строки `name`. Не используйте дефисы в строке `name`. Подробности и примеры см. в разделе [Имена пайпов](https://angular.io/guide/styleguide#pipe-names 'Имена пайпов в руководстве по стилю кодирования Angular').

Используйте `name` в шаблонных выражениях так же, как и для встроенного пайпа.

!!!note ""

    -   Включите свой пайп в поле `declarations` метаданных `NgModule` для того, чтобы он был доступен шаблону.

    	См. файл `app.module.ts` в примере приложения ([живой пример](https://angular.io/generated/live-examples/pipes/stackblitz.html)).

    	Подробнее см. раздел [NgModules](ngmodules.md 'Введение в NgModules').

    -   Зарегистрируйте пользовательские пайпы.

    	Команда [Angular CLI](https://angular.io/cli 'CLI Overview and Command Reference') [`ng generate pipe`](https://angular.io/cli/generate#pipe 'ng generate pipe in the CLI Command Reference') регистрирует пайп автоматически.

### Использование интерфейса PipeTransform

Реализуйте интерфейс [`PipeTransform`](https://angular.io/api/core/PipeTransform 'API reference for PipeTransform') в своем пользовательском классе пайпа для выполнения трансформации.

Angular вызывает метод `transform` со значением привязки в качестве первого аргумента и любыми параметрами в качестве второго аргумента в виде списка и возвращает преобразованное значение.

### Пример: Экспоненциальное преобразование значения

В игре может потребоваться реализовать преобразование, которое экспоненциально увеличивает значение для повышения силы героя. Например, если количество очков героя равно 2, то при экспоненциальном увеличении силы героя на 10 количество очков будет равно 1024. Для этого преобразования используйте пользовательский пайп.

В следующем примере кода показаны два определения компонентов:

| Файлы                          | Подробности                                                                                                                                                                                                 |
| :----------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `exponential-strength.pipe.ts` | Определяет пользовательский пайп с именем `exponentialStrength` и методом `transform`, выполняющим преобразование. Определяет аргумент метода `transform` (`exponent`) для параметра, передаваемого в пайп. |
| `power-booster.component.ts`   | Демонстрирует использование пайпа с указанием значения (`2`) и параметра экспоненты (`10`).                                                                                                                 |

=== "src/app/exponential-strength.pipe.ts"

    ```ts
    import { Pipe, PipeTransform } from '@angular/core';
    /*
    * Raise the value exponentially
    * Takes an exponent argument that defaults to 1.
    * Usage:
    *   value | exponentialStrength:exponent
    * Example:
    *   {{ 2 | exponentialStrength:10 }}
    *   formats to: 1024
    */
    @Pipe({ name: 'exponentialStrength' })
    export class ExponentialStrengthPipe
    	implements PipeTransform {
    	transform(value: number, exponent = 1): number {
    		return Math.pow(value, exponent);
    	}
    }
    ```

=== "src/app/power-booster.component.ts"

    ```ts
    import { Component } from '@angular/core';

    @Component({
    	selector: 'app-power-booster',
    	template: `
    		<h2>Power Booster</h2>
    		<p>
    			Super power boost:
    			{{ 2 | exponentialStrength: 10 }}
    		</p>
    	`,
    })
    export class PowerBoosterComponent {}
    ```

В браузере отображается следующее:

```
Power Booster

Superpower boost: 1024
```

!!!note ""

    Чтобы исследовать поведение пайпа `exponentialStrength` в [живом примере](https://angular.io/generated/live-examples/pipes/stackblitz.html), измените значение и необязательную экспоненту в шаблоне.

<a id="change-detection"></a>

## Обнаружение изменений с помощью привязки данных в пайпах

Для отображения значений и реагирования на действия пользователя в пайпе используется [привязка данных](glossary.md#data-binding 'Определение привязки данных'). Если в качестве данных используется примитивное входное значение, например `String` или `Number`, или ссылка на объект, например `Date` или `Array`, Angular выполняет пайп всякий раз, когда обнаруживает изменение входного значения или ссылки.

Например, можно изменить предыдущий пример пользовательского пайпа, чтобы использовать двустороннее связывание данных с `ngModel` для ввода суммы и повышающего коэффициента, как показано в следующем примере кода.

```ts
import { Component } from '@angular/core';

@Component({
    selector: 'app-power-boost-calculator',
    template: `
        <h2>Power Boost Calculator</h2>
        <label for="power-input">Normal power: </label>
        <input
            id="power-input"
            type="text"
            [(ngModel)]="power"
        />
        <label for="boost-input">Boost factor: </label>
        <input
            id="boost-input"
            type="text"
            [(ngModel)]="factor"
        />
        <p>
            Super Hero Power:
            {{ power | exponentialStrength: factor }}
        </p>
    `,
    styles: ['input {margin: .5rem 0;}'],
})
export class PowerBoostCalculatorComponent {
    power = 5;
    factor = 1;
}
```

Пайп `exponentialStrength` выполняется каждый раз, когда пользователь изменяет значение "нормальной мощности" или "коэффициента усиления".

Angular обнаруживает каждое изменение и немедленно запускает пайп. Это хорошо подходит для примитивных входных значений. Однако если вы изменяете что-то _внутри_ составного объекта (например, месяц даты, элемент массива или свойство объекта), вам необходимо понять, как работает обнаружение изменений и как использовать `нечистый` пайп.

### Как работает обнаружение изменений

Angular ищет изменения в значениях, связанных с данными, в процессе [change detection](glossary.md#change-detection 'Определение change detection'), который запускается после каждого события DOM: каждого нажатия клавиши, перемещения мыши, тиканья таймера и ответа сервера. Следующий пример, в котором не используется пайп, демонстрирует, как Angular использует свою стандартную стратегию обнаружения изменений для отслеживания и обновления отображения каждого героя в массиве `heroes`. На вкладках примера показано следующее:

| Файлы                               | Подробности                                                          |
| :---------------------------------- | :------------------------------------------------------------------- |
| `flying-heroes.component.html (v1)` | Повторитель `*ngFor` отображает имена героев.                        |
| `flying-heroes.component.ts (v1)`   | Предоставляет героев, добавляет героев в массив и сбрасывает массив. |

=== "src/app/flying-heroes.component.html (v1)"

    ```html
    <label for="hero-name">New hero name: </label>
    <input
    	type="text"
    	#box
    	id="hero-name"
    	(keyup.enter)="addHero(box.value); box.value=''"
    	placeholder="hero name"
    />
    <button type="button" (click)="reset()">
    	Reset list of heroes
    </button>
    <div *ngFor="let hero of heroes">{{hero.name}}</div>
    ```

=== "src/app/flying-heroes.component.ts (v1)"

    ```ts
    export class FlyingHeroesComponent {
    	heroes: any[] = [];
    	canFly = true;
    	constructor() {
    		this.reset();
    	}

    	addHero(name: string) {
    		name = name.trim();
    		if (!name) {
    			return;
    		}
    		const hero = { name, canFly: this.canFly };
    		this.heroes.push(hero);
    	}

    	reset() {
    		this.heroes = HEROES.slice();
    	}
    }
    ```

Angular обновляет отображение каждый раз, когда пользователь добавляет героя. Если пользователь нажимает кнопку **Reset**, Angular заменяет `heroes` новым массивом исходных героев и обновляет отображение. Если добавить возможность удаления или изменения героя, то Angular обнаружит эти изменения и также обновит отображение.

Однако выполнение пайпа для обновления дисплея при каждом изменении приведет к снижению производительности приложения. Поэтому Angular использует более быстрый алгоритм обнаружения изменений для выполнения пайпа, как описано в следующем разделе.

<a id="pure-and-impure-pipes"></a>

### Обнаружение чистых изменений примитивов и ссылок на объекты

По умолчанию пайпы определяются как _чистые_, поэтому Angular выполняет пайп только тогда, когда обнаруживает _чистое изменение_ входного значения. Чистое изменение — это либо изменение примитивного входного значения (такого как `String`, `Number`, `Boolean` или `Symbol`), либо изменение объектной ссылки (такой как `Date`, `Array`, `Function` или `Object`).

<a id="pure-pipe-pure-fn"></a>

Чистый пайп должен использовать чистую функцию, то есть функцию, которая обрабатывает входные данные и возвращает значения без побочных эффектов. Другими словами, при одинаковых входных данных чистая функция всегда должна возвращать одинаковые выходные данные.

При использовании чистого пайпа Angular игнорирует изменения внутри составных объектов, например, вновь добавленный элемент существующего массива, поскольку проверка примитивного значения или ссылки на объект выполняется гораздо быстрее, чем глубокая проверка различий внутри объектов. Angular может быстро определить, можно ли пропустить выполнение пайпа и обновление представления.

Однако чистый пайп с массивом в качестве входных данных может работать не так, как вы хотите. Чтобы продемонстрировать эту проблему, изменим предыдущий пример так, чтобы отфильтровать список героев только по тем героям, которые умеют летать. Используйте `FlyingHeroesPipe` в ретрансляторе `*ngFor`, как показано в следующем коде. Вкладки для примера выглядят следующим образом:

-   Шаблон (`flying-heroes.component.html (flyers)`) с новым пайпом
-   Реализация пользовательского пайпа `FlyingHeroesPipe` (`flying-heroes.pipe.ts`)

=== "src/app/flying-heroes.component.html (flyers)"

    ```html
    <div *ngFor="let hero of (heroes | flyingHeroes)">
    	{{hero.name}}
    </div>
    ```

=== "src/app/flying-heroes.pipe.ts"

    ```ts
    import { Pipe, PipeTransform } from '@angular/core';

    import { Hero } from './heroes';

    @Pipe({ name: 'flyingHeroes' })
    export class FlyingHeroesPipe implements PipeTransform {
    	transform(allHeroes: Hero[]) {
    		return allHeroes.filter((hero) => hero.canFly);
    	}
    }
    ```

Теперь приложение демонстрирует неожиданное поведение: Когда пользователь добавляет летающих героев, ни один из них не появляется в разделе "Heroes who fly". Это происходит потому, что код, добавляющий героя, заталкивает его в массив `heroes`:

```ts
this.heroes.push(hero);
```

Детектор изменений игнорирует изменения элементов массива, поэтому пайп не выполняется.

Причина, по которой Angular игнорирует измененный элемент массива, заключается в том, что _ссылка_ на массив не изменилась. Поскольку массив остался прежним, Angular не обновляет отображение.

Один из способов добиться желаемого поведения — изменить саму ссылку на объект. Замените массив новым массивом, содержащим новые измененные элементы, а затем введите новый массив в пайп. В предыдущем примере создайте массив с добавлением нового героя и присвойте его `heroes`. Angular обнаружит изменение в ссылке на массив и выполнит пайп.

Подведем итог: если вы мутируете входной массив, то чистый пайп не выполняется. Если же входной массив _заменить_, то пайп будет выполнен, и отображение будет обновлено.

Приведенный пример демонстрирует изменение кода компонента для реализации пайпа.

Чтобы сохранить независимость компонента от HTML-шаблонов, использующих пайпы, в качестве альтернативы можно использовать _нечистый_ пайп для обнаружения изменений в составных объектах, таких как массивы, как описано в следующем разделе.

<a id="impure-flying-heroes"></a>

### Обнаружение нечистых изменений внутри составных объектов

Чтобы выполнить пользовательский пайп после изменения _внутри_ составного объекта, например, изменения элемента массива, необходимо определить пайп как `impure` для обнаружения нечистых изменений. Angular выполняет нечистый пайп каждый раз, когда обнаруживает изменение при каждом нажатии клавиши или движении мыши.

!!!warning ""

    Хотя нечистый пайп может быть полезен, использовать его следует с осторожностью. Долго работающий нечистый пайп может значительно замедлить работу приложения.

Сделать пайп нечистым, установив его флаг `pure` в значение `false`:

```ts
@Pipe({
  name: 'flyingHeroesImpure',
  pure: false
})
```

В приведенном ниже коде показана полная реализация `FlyingHeroesImpurePipe`, которая расширяет `FlyingHeroesPipe` для наследования его характеристик. Из примера видно, что больше ничего менять не нужно &mdash; единственное отличие — установка флага `pure` как `false` в метаданных пайпа.

=== "src/app/flying-heroes.pipe.ts (FlyingHeroesImpurePipe)"

    ```ts
    @Pipe({
    	name: 'flyingHeroesImpure',
    	pure: false,
    })
    export class FlyingHeroesImpurePipe extends FlyingHeroesPipe {}
    ```

=== "src/app/flying-heroes.pipe.ts (FlyingHeroesPipe)"

    ```ts
    import { Pipe, PipeTransform } from '@angular/core';

    import { Hero } from './heroes';

    @Pipe({ name: 'flyingHeroes' })
    export class FlyingHeroesPipe implements PipeTransform {
    	transform(allHeroes: Hero[]) {
    		return allHeroes.filter((hero) => hero.canFly);
    	}
    }
    ```

`FlyingHeroesImpurePipe` является хорошим кандидатом на роль нечистого пайпа, поскольку функция `transform` является тривиальной и быстрой:

```ts
return allHeroes.filter((hero) => hero.canFly);
```

От `FlyingHeroesImpureComponent` можно получить `FlyingHeroesComponent`. Как показано в следующем коде, изменяется только пайп в шаблоне.

```html
<div *ngFor="let hero of (heroes | flyingHeroesImpure)">
    {{hero.name}}
</div>
```

!!!note ""

    Чтобы убедиться в том, что при добавлении героев на экране происходит обновление, посмотрите [живой пример](https://angular.io/generated/live-examples/pipes/stackblitz.html).

<a id="async-pipe"></a>

## Развертывание данных из наблюдаемого объекта

[Observables](glossary.md#observable 'Определение observable') позволяют передавать сообщения между частями приложения. Обсерватории рекомендуются для обработки событий, асинхронного программирования и работы с несколькими значениями. Наблюдаемые могут передавать одиночные или множественные значения любого типа как синхронно (как функция передает значение вызывающему ее пользователю), так и асинхронно по расписанию.

!!!note ""

    Подробности и примеры использования observables см. в [Observables Overview](observables.md#using-observables-to-pass-values 'Использование observables для передачи значений').

Используйте встроенный [`AsyncPipe`](https://angular.io/api/common/AsyncPipe 'Описание API AsyncPipe') для приема наблюдаемого объекта в качестве входного и автоматической подписки на него. Без этого пайпа коду компонента пришлось бы подписываться на наблюдаемую, чтобы потреблять ее значения, извлекать разрешенные значения, выставлять их для связывания и отписываться от них при уничтожении наблюдаемой, чтобы избежать утечек памяти. `AsyncPipe` — это нечистый пайп, который избавляет ваш компонент от необходимости поддерживать подписку и продолжать передавать значения из наблюдаемой таблицы по мере их поступления.

Следующий пример кода привязывает наблюдаемое хранилище строк сообщений (`message$`) к представлению с помощью пайпа `async`.

```ts
import { Component } from '@angular/core';

import { Observable, interval } from 'rxjs';
import { map, take } from 'rxjs/operators';

@Component({
    selector: 'app-hero-async-message',
    template: ` <h2>Async Hero Message and AsyncPipe</h2>
        <p>Message: {{ message$ | async }}</p>
        <button type="button" (click)="resend()">
            Resend
        </button>`,
})
export class HeroAsyncMessageComponent {
    message$: Observable<string>;

    private messages = [
        'You are my hero!',
        'You are the best hero!',
        'Will you be my hero?',
    ];

    constructor() {
        this.message$ = this.getResendObservable();
    }

    resend() {
        this.message$ = this.getResendObservable();
    }

    private getResendObservable() {
        return interval(500).pipe(
            map((i) => this.messages[i]),
            take(this.messages.length)
        );
    }
}
```

<a id="no-filter-pipe"></a>

## Кэширование HTTP-запросов

Для [взаимодействия с внутренними сервисами по протоколу HTTP] (understanding-communicating-with-http.md 'Communicating with backend services using HTTP') сервис `HttpClient` использует наблюдаемые и предлагает метод `HttpClient.get()` для получения данных с сервера. Асинхронный метод посылает HTTP-запрос и возвращает наблюдаемую, которая выдает в ответ запрошенные данные.

Как было показано в предыдущем разделе, используйте нечистую трубу `AsyncPipe` для приема наблюдаемого объекта в качестве входного и автоматической подписки на него. Вы также можете создать нечистый пайп для выполнения и кэширования HTTP-запроса.

Нечистые пайпы вызываются каждый раз, когда для компонента выполняется обнаружение изменений, что может происходить как раз в несколько миллисекунд. Чтобы избежать проблем с производительностью, вызывайте сервер только при изменении запрашиваемого URL, как показано в следующем примере, и используйте пайп для кэширования ответа сервера. На вкладках показано следующее:

-   Пайп `fetch` (`fetch-json.pipe.ts`).
-   Компонент harness (`hero-list.component.ts`) для демонстрации запроса, использующий шаблон, определяющий две привязки к пайпу, запрашивающему героев из файла `heroes.json`.

    Вторая привязка связывает пайп `fetch` со встроенным `JsonPipe` для отображения тех же данных о героях в формате JSON.

=== "src/app/fetch-json.pipe.ts"

    ```ts
    import { HttpClient } from '@angular/common/http';
    import { Pipe, PipeTransform } from '@angular/core';

    @Pipe({
    	name: 'fetch',
    	pure: false,
    })
    export class FetchJsonPipe implements PipeTransform {
    	private cachedData: any = null;
    	private cachedUrl = '';

    	constructor(private http: HttpClient) {}

    	transform(url: string): any {
    		if (url !== this.cachedUrl) {
    			this.cachedData = null;
    			this.cachedUrl = url;
    			this.http
    				.get(url)
    				.subscribe(
    					(result) => (this.cachedData = result)
    				);
    		}

    		return this.cachedData;
    	}
    }
    ```

=== "src/app/hero-list.component.ts"

    ```ts
    import { Component } from '@angular/core';

    @Component({
    	selector: 'app-hero-list',
    	template: ` <h2>Heroes from JSON File</h2>

    		<div
    			*ngFor="
    				let hero of 'assets/heroes.json' | fetch
    			"
    		>
    			{{ hero.name }}
    		</div>

    		<p>
    			Heroes as JSON:
    			{{ 'assets/heroes.json' | fetch | json }}
    		</p>`,
    })
    export class HeroListComponent {}
    ```

В предыдущем примере точка останова на запросе пайпа на получение данных показывает следующее:

-   Каждое связывание получает свой собственный экземпляр пайпа.
-   Каждый экземпляр пайпа кэширует свой URL и данные и обращается к серверу только один раз.

Пайпы `fetch` и `fetch-json` отображают героев в браузере следующим образом:

```
Heroes from JSON File

Windstorm
Bombasto
Magneto
Tornado

Heroes as JSON: [ { "name": "Windstorm", "canFly": true }, { "name": "Bombasto", "canFly": false }, { "name": "Magneto", "canFly": false }, { "name": "Tornado", "canFly": true } ]
```

!!!note ""

    Встроенная функция [JsonPipe](https://angular.io/api/common/JsonPipe 'Описание API для JsonPipe') предоставляет возможность диагностировать загадочную неудачную привязку данных или проверить объект на предмет будущей привязки.

## Пайпы и старшинство

Оператор пайп имеет более высокий приоритет, чем тернарный оператор (`?:`), поэтому `a ? b : c | x` будет разобран как `a ? b : (c | x)`. Оператор пайп не может быть использован без круглых скобок в первом и втором операндах `?:`.

В силу старшинства, если вы хотите, чтобы пайп применялся к результату тернарного оператора, оберните все выражение круглыми скобками; например, `(a ? b : c) | x`.

```html
<!-- use parentheses in the third operand so the pipe applies to the whole expression -->
{{ (true ? 'true' : 'false') | uppercase }}
```

<!-- links -->

[aioguidei18ncommonformatdatalocale]: i18n-common-format-data-locale.md

## Ссылки

-   [Transforming Data Using Pipes](https://angular.io/guide/pipes)
