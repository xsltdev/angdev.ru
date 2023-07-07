# Структурные директивы

:date: 28.02.2022

Это руководство посвящено структурным директивам и содержит концептуальную информацию о том, как работают такие директивы, как Angular интерпретирует их сокращенный синтаксис, и как добавить свойства защиты шаблона для отлова ошибок типа шаблона.

**Структурные директивы** - это директивы, которые изменяют макет DOM путем добавления и удаления элементов DOM.

Angular предоставляет набор встроенных структурных директив (таких как `NgIf`, `NgForOf`, `NgSwitch` и другие), которые часто используются во всех проектах Angular. Более подробную информацию можно найти в [Встроенные директивы](built-in-directives.md).

!!!note ""

    Пример [приложения](https://angular.io/generated/live-examples/structural-directives/stackblitz.html), которое описывается на этой странице.

## Сокращение структурных директив

Когда применяются структурные директивы, они обычно сопровождаются звездочкой, `*`, например, `*ngIf`. Это соглашение является сокращением, которое Angular интерпретирует и преобразует в более длинную форму. Angular преобразует звездочку перед структурной директивой в `<ng-template>`, который окружает основной элемент и его потомков.

Например, возьмем следующий код, который использует `*ngIf` для отображения имени героя, если `hero` существует:

```html
<div *ngIf="hero" class="name">{{hero.name}}</div>
```

В Angular создается элемент `<ng-template>` и к нему применяется директива `*ngIf`, где она становится свойством, заключенным в квадратные скобки, `[ngIf]`. Затем остальная часть `<div>`, включая его атрибут class, перемещается внутрь `<ng-template>`:

```html
<ng-template [ngIf]="hero">
    <div class="name">{{hero.name}}</div>
</ng-template>
```

Обратите внимание, что Angular не создает реальный элемент `<ng-template>`, а вместо этого только отображает элемент `<div>`.

```html
<div _ngcontent-c0>Mr. Nice</div>
```

В следующем примере сравнивается сокращенное использование звездочки в `*ngFor` с длинной формой `<ng-template>`:

```html
<div
    *ngFor="let hero of heroes; let i=index; let odd=odd; trackBy: trackById"
    [class.odd]="odd"
>
    ({{i}}) {{hero.name}}
</div>

<ng-template
    ngFor
    let-hero
    [ngForOf]="heroes"
    let-i="index"
    let-odd="odd"
    [ngForTrackBy]="trackById"
>
    <div [class.odd]="odd">({{i}}) {{hero.name}}</div>
</ng-template>
```

Здесь все, что связано со структурной директивой `ngFor`, переносится в `<ng-template>`. Все остальные привязки и атрибуты элемента применяются к элементу `<div>` внутри `<ng-template>`.

Другие модификаторы принимающего элемента, помимо строки `ngFor`, остаются на месте по мере перемещения элемента внутрь `<ng-template>`.

В этом примере `[class.odd]="odd"` остается на `<div>`.

Ключевое слово `let` объявляет входную переменную шаблона, на которую вы можете ссылаться внутри шаблона. В данном примере входными переменными являются `hero`, `i` и `odd`.

Парсер переводит `let hero`, `let i` и `let odd` в переменные с именами `let-hero`, `let-i` и `let-odd`.

Переменные `let-i` и `let-odd` становятся `let i=index` и `let odd=odd`.

Angular устанавливает `i` и `odd` в текущее значение свойств контекста `index` и `odd`.

Парсер применяет PascalCase ко всем директивам и префиксирует их именем атрибута директивы, например, ngFor. Например, входные свойства `ngFor`, `of` и `trackBy`, отображаются на `ngForOf` и `ngForTrackBy`.

По мере того, как директива `NgFor` проходит по списку, она устанавливает и сбрасывает свойства своего контекстного объекта. Эти свойства могут включать, но не ограничиваться, `index`, `odd` и специальное свойство под названием `$implicit`.

Angular устанавливает `let-hero` в значение свойства контекста `$implicit`, которое `NgFor` инициализировал героем для текущей итерации.

Для получения дополнительной информации смотрите документацию [NgFor API](https://angular.io/api/common/NgFor) и [NgForOf API](https://angular.io/api/common/NgForOf).

!!!note ""

    Обратите внимание, что элемент `<ng-template>` в Angular определяет шаблон, который по умолчанию ничего не отображает, если вы просто обернете элементы в `<ng-template>` без применения структурной директивы, эти элементы не будут отображены.

    Для получения дополнительной информации смотрите документацию [ng-template API](https://angular.io/api/core/ng-template).

## Одна структурная директива на элемент

Довольно распространенным случаем является повторение блока HTML, но только при выполнении определенного условия. Интуитивно понятным способом сделать это является размещение `*ngFor` и `*ngIf` на одном и том же элементе. Однако, поскольку и `*ngFor`, и `*ngIf` являются структурными директивами, это будет расценено компилятором как ошибка. Вы можете применить только одну _структурную_ директиву к элементу.

Причина в простоте. Структурные директивы могут делать сложные вещи с основным элементом и его потомками.

Когда две директивы претендуют на один и тот же элемент-хозяин, какая из них должна иметь приоритет?

Что должно быть первым, `NgIf` или `NgFor`? Может ли `NgIf` отменить эффект `NgFor`? Если да (а кажется, что так и должно быть), то как Angular должен обобщить возможность отмены для других структурных директив?

На эти вопросы нет простых ответов. Запрет на использование нескольких структурных директив делает их спорными. Есть простое решение для этого случая использования: поместите `*ngIf` в элемент-контейнер, который обертывает элемент `*ngFor`. Один или оба элемента могут быть `<ng-container>`, чтобы не создавать лишних элементов DOM.

## Создание структурной директивы

В этом разделе вы узнаете, как создать `UnlessDirective` и как задать значения `condition`. Директива `UnlessDirective` делает противоположное `NgIf`, а значения `condition` могут быть установлены в `true` или `false`.

`NgIf` отображает содержимое шаблона, когда условие равно `true`.

`UnlessDirective` отображает содержимое, когда условие равно `false`.

Ниже приведен селектор `UnlessDirective`, `appUnless`, примененный к элементу paragraph. Когда `condition` равно `false`, браузер отображает предложение.

```html
<p *appUnless="condition">
    Show this sentence unless the condition is true.
</p>
```

1.  Используя Angular CLI, выполните следующую команду, где `unless` - имя директивы:

    ```shell
    ng generate directive unless
    ```

    Angular создает класс директивы и определяет CSS-селектор `appUnless`, который идентифицирует директиву в шаблоне.

2.  Импортируйте `Input`, `TemplateRef` и `ViewContainerRef`.

    ```ts
    import {
        Directive,
        Input,
        TemplateRef,
        ViewContainerRef,
    } from '@angular/core';

    @Directive({ selector: '[appUnless]' })
    export class UnlessDirective {}
    ```

3.  Вставьте `TemplateRef` и `ViewContainerRef` в конструктор директивы как приватные переменные.

    ```ts
    constructor(
    	private templateRef: TemplateRef<any>,
    	private viewContainer: ViewContainerRef
    ) { }
    ```

    Директива `UnlessDirective` создает [встроенное представление](https://angular.io/api/core/EmbeddedViewRef) из сгенерированного Angular `<ng-template>` и вставляет это представление в [контейнер представления](https://angular.io/api/core/ViewContainerRef) рядом с исходным элементом директивы `<p>`.

    [`TemplateRef`](https://angular.io/api/core/TemplateRef) помогает добраться до содержимого `<ng-template>`, а [`ViewContainerRef`](https://angular.io/api/core/ViewContainerRef) открывает доступ к контейнеру представления.

4.  Добавьте свойство `appUnless` `@Input()` с сеттером.

    ```ts
    @Input() set appUnless(condition: boolean) {
    	if (!condition && !this.hasView) {
    		this.viewContainer.createEmbeddedView(this.templateRef);
    		this.hasView = true;
    	} else if (condition && this.hasView) {
    		this.viewContainer.clear();
    		this.hasView = false;
    	}
    }
    ```

    Angular устанавливает свойство `appUnless` всякий раз, когда значение условия изменяется.

    -   Если условие ложно и Angular не создал представление ранее, то сеттер заставляет контейнер представления создать встроенное представление из шаблона.
    -   Если условие истинно, и представление отображается в данный момент, сеттер очищает контейнер, который утилизирует представление.

Полный текст директивы выглядит следующим образом:

```ts
import {
    Directive,
    Input,
    TemplateRef,
    ViewContainerRef,
} from '@angular/core';

/**
 * Add the template content to the DOM unless the condition is true.
 */
@Directive({ selector: '[appUnless]' })
export class UnlessDirective {
    private hasView = false;

    constructor(
        private templateRef: TemplateRef<any>,
        private viewContainer: ViewContainerRef
    ) {}

    @Input() set appUnless(condition: boolean) {
        if (!condition && !this.hasView) {
            this.viewContainer.createEmbeddedView(
                this.templateRef
            );
            this.hasView = true;
        } else if (condition && this.hasView) {
            this.viewContainer.clear();
            this.hasView = false;
        }
    }
}
```

### Тестирование директивы

В этом разделе вы обновите свое приложение, чтобы протестировать `UnlessDirective`.

1.  Добавьте `condition`, установленное в `false` в `AppComponent`.

    ```ts
    condition = false;
    ```

2.  Обновите шаблон для использования директивы.

    Здесь `*appUnless` находится на двух тегах `<p>` с противоположными значениями `condition`, одно `true` и одно `false`.

    ```html
    <p *appUnless="condition" class="unless a">
        (A) This paragraph is displayed because the
        condition is false.
    </p>

    <p *appUnless="!condition" class="unless b">
        (B) Although the condition is true, this paragraph
        is displayed because appUnless is set to false.
    </p>
    ```

    Звездочка - это сокращение, обозначающее `appUnless` как структурную директиву.

    Когда `condition` ложно, верхний (A) параграф появляется, а нижний (B) параграф исчезает.

    Когда `condition` истинно, верхний (A) параграф исчезает, а нижний (B) параграф появляется.

3.  Чтобы изменить и отобразить значение `условия` в браузере, добавьте разметку, отображающую статус и кнопку.

    ```html
    <p>
        The condition is currently
        <span
            [ngClass]="{ 'a': !condition, 'b': condition, 'unless': true }"
            >{{condition}}</span
        >.
        <button
            type="button"
            (click)="condition = !condition"
            [ngClass]="{ 'a': condition, 'b': !condition }"
        >
            Toggle condition to {{condition ? 'false' :
            'true'}}
        </button>
    </p>
    ```

Чтобы убедиться, что директива работает, нажмите на кнопку, чтобы изменить значение `condition`.

![UnlessDirective in action](unless-anim.gif)

## Справочник по синтаксису структурных директив

Когда вы пишете свои собственные структурные директивы, используйте следующий синтаксис:

```
*:prefix="( :let | :expression ) (';' | ',')? ( :let | :as | :keyExp )*"
```

В следующих таблицах описана каждая часть грамматики структурной директивы:

=== "as"

    ```
    as = :export "as" :local ";"?
    ```

=== "keyExp"

    ```
    keyExp = :key ":"? :expression ("as" :local)? ";"?
    ```

=== "let"

    ```
    let = "let" :local "=" :export ";"?
    ```

| Keyword      | Details                                                 |
| :----------- | :------------------------------------------------------ |
| `prefix`     | Ключ атрибута HTML                                      |
| `key`        | Ключ атрибута HTML                                      |
| `local`      | Имя локальной переменной, используемой в шаблоне        |
| `export`     | Значение, экспортируемое директивой под заданным именем |
| `expression` | Стандартное угловое выражение                           |

### Как Angular переводит стенографические директивы

Angular переводит сокращение структурных директив в обычный синтаксис связывания следующим образом:

| Сокращение                      | Translation                                                                      |
| :------------------------------ | :------------------------------------------------------------------------------- |
| `prefix` and naked `expression` | `[prefix]="expression"`                                                          |
| `keyExp`                        | `[prefixKey] "expression" (let-prefixKey="export")` `prefix` добавляется к `key` |
| `let`                           | `let-local="export"`                                                             |

### Примеры сокращений

В следующей таблице приведены примеры сокращений:

<table>
<tr>
<th>Сокращение</th>
<th>Как Angular интерпретирует синтаксис</th>
</tr>
<tr>
<td>
``` linenums="0"
*ngFor="let item of [1,2,3]"
```
</td>
<td>
``` linenums="0"
<ng-template ngFor
             let-item
             [ngForOf]="[1,2,3]">
```
</td>
</tr>
<tr>
<td>
```
*ngFor="let item of [1,2,3] as items;
        trackBy: myTrack; index as i"
```
</td>
<td>
```
<ng-template ngFor
             let-item
             [ngForOf]="[1,2,3]"
             let-items="ngForOf"
             [ngForTrackBy]="myTrack"
             let-i="index">
```
</td>
</tr>
<tr>
<td>
```
*ngIf="exp"
```
</td>
<td>
```
<ng-template [ngIf]="exp">
```
</td>
</tr>
<tr>
<td>
```
*ngIf="exp as value"
```
</td>
<td>
```
<ng-template [ngIf]="exp"
             let-value="ngIf">
```
</td>
</tr>
</table>

## Улучшение проверки типов шаблонов для пользовательских директив

Вы можете улучшить проверку типов шаблонов для пользовательских директив, добавив свойства защиты шаблона в определение директивы. Эти свойства помогают программе проверки типов шаблонов Angular находить ошибки в шаблоне во время компиляции, что позволяет избежать ошибок во время выполнения.

Эти свойства выглядят следующим образом:

-   Свойство `ngTemplateGuard_(someInputProperty)` позволяет вам указать более точный тип для входного выражения в шаблоне.
-   Статическое свойство `ngTemplateContextGuard` объявляет тип контекста шаблона.

В этом разделе приведены примеры обоих типов свойств защиты типа. Для получения дополнительной информации смотрите [Проверка типов шаблонов](template-typecheck.md).

### Уточнение требований к типам в шаблоне с помощью защит шаблона

Структурная директива в шаблоне управляет тем, будет ли этот шаблон отображаться во время выполнения, основываясь на его входном выражении. Чтобы помочь компилятору отловить ошибки типа шаблона, вы должны как можно точнее определить требуемый тип входного выражения директивы, когда оно встречается внутри шаблона.

Функция защиты типа сужает ожидаемый тип входного выражения до подмножества типов, которые могут быть переданы директиве внутри шаблона во время выполнения. Вы можете предоставить такую функцию, чтобы помочь программе проверки типов вывести правильный тип для выражения во время компиляции.

Например, реализация `NgIf` использует сужение типов, чтобы гарантировать, что шаблон будет инстанцирован только в том случае, если входное выражение `*ngIf` истинно. Для обеспечения конкретного требования к типу, директива `NgIf` определяет [статическое свойство `ngTemplateGuard_ngIf: 'binding'`](https://angular.io/api/common/NgIf#static-properties).

Значение `binding` является особым случаем для распространенного вида сужения типа, когда входное выражение оценивается для того, чтобы удовлетворить требованию типа.

Чтобы задать более конкретный тип входного выражения для директивы в шаблоне, добавьте к директиве свойство `ngTemplateGuard_xx`, где суффикс к имени статического свойства, `xx`, является именем поля `@Input()`. Значением свойства может быть либо общая функция сужения типов на основе ее возвращаемого типа, либо строка `"binding"`, как в случае `NgIf`.

Например, рассмотрим следующую структурную директиву, которая принимает результат шаблонного выражения в качестве входных данных:

=== "src/app/if-loaded.directive.ts"

    ```ts
    import {
    	Directive,
    	Input,
    	TemplateRef,
    	ViewContainerRef,
    } from '@angular/core';

    import { Loaded, LoadingState } from './loading-state';

    @Directive({ selector: '[appIfLoaded]' })
    export class IfLoadedDirective<T> {
    	private isViewCreated = false;

    	@Input('appIfLoaded') set state(
    		state: LoadingState<T>
    	) {
    		if (
    			!this.isViewCreated &&
    			state.type === 'loaded'
    		) {
    			this.viewContainerRef.createEmbeddedView(
    				this.templateRef
    			);
    			this.isViewCreated = true;
    		} else if (
    			this.isViewCreated &&
    			state.type !== 'loaded'
    		) {
    			this.viewContainerRef.clear();
    			this.isViewCreated = false;
    		}
    	}

    	constructor(
    		private readonly viewContainerRef: ViewContainerRef,
    		private readonly templateRef: TemplateRef<unknown>
    	) {}

    	static ngTemplateGuard_appIfLoaded<T>(
    		dir: IfLoadedDirective<T>,
    		state: LoadingState<T>
    	): state is Loaded<T> {
    		return true;
    	}
    }
    ```

=== "src/app/loading-state.ts"

    ```ts
    export type Loaded<T> = { type: 'loaded'; data: T };
    export type Loading = { type: 'loading' };
    export type LoadingState<T> = Loaded<T> | Loading;
    ```

=== "src/app/hero.component.ts"

    ```ts
    import { Component } from '@angular/core';

    import { LoadingState } from './loading-state';
    import { Hero, heroes } from './hero';

    @Component({
    	selector: 'app-hero',
    	template: `
    		<button (click)="onLoadHero()">Load Hero</button>
    		<p *appIfLoaded="heroLoadingState">
    			{{ heroLoadingState.data | json }}
    		</p>
    	`,
    })
    export class HeroComponent {
    	heroLoadingState: LoadingState<Hero> = {
    		type: 'loading',
    	};

    	onLoadHero(): void {
    		this.heroLoadingState = {
    			type: 'loaded',
    			data: heroes[0],
    		};
    	}
    }
    ```

В данном примере тип `LoadingState<T>` допускает одно из двух состояний, `Loaded<T>` или `Loading`. Выражение, используемое в качестве входного `state` директивы (псевдоним `appIfLoaded`), имеет зонтичный тип `LoadingState`, поскольку неизвестно, в каком состоянии находится загрузка в данный момент.

Определение `IfLoadedDirective` объявляет статическое поле `ngTemplateGuard_appIfLoaded`, которое выражает поведение сужения. Внутри шаблона `AppComponent` структурная директива `*appIfLoaded` должна выводить этот шаблон только тогда, когда `state` действительно `Loaded<Hero>`.

Защита типа позволяет программе проверки типов сделать вывод, что допустимым типом `state` в шаблоне является `Loaded<T>`, и далее сделать вывод, что `T` должен быть экземпляром `Hero`.

### Типизация контекста директивы

Если ваша структурная директива предоставляет контекст инстанцированному шаблону, вы можете правильно типизировать его внутри шаблона, предоставив статическую функцию `ngTemplateContextGuard`. В следующем фрагменте показан пример такой функции.

=== "src/app/trigonometry.directive.ts"

    ```ts
    import {
    	Directive,
    	Input,
    	TemplateRef,
    	ViewContainerRef,
    } from '@angular/core';

    @Directive({ selector: '[appTrigonometry]' })
    export class TrigonometryDirective {
    	private isViewCreated = false;
    	private readonly context = new TrigonometryContext();

    	@Input('appTrigonometry') set angle(
    		angleInDegrees: number
    	) {
    		const angleInRadians = toRadians(angleInDegrees);
    		this.context.sin = Math.sin(angleInRadians);
    		this.context.cos = Math.cos(angleInRadians);
    		this.context.tan = Math.tan(angleInRadians);

    		if (!this.isViewCreated) {
    			this.viewContainerRef.createEmbeddedView(
    				this.templateRef,
    				this.context
    			);
    			this.isViewCreated = true;
    		}
    	}

    	constructor(
    		private readonly viewContainerRef: ViewContainerRef,
    		private readonly templateRef: TemplateRef<
    			TrigonometryContext
    		>
    	) {}

    	// Make sure the template checker knows the type of the context with which the
    	// template of this directive will be rendered
    	static ngTemplateContextGuard(
    		directive: TrigonometryDirective,
    		context: unknown
    	): context is TrigonometryContext {
    		return true;
    	}
    }

    class TrigonometryContext {
    	sin = 0;
    	cos = 0;
    	tan = 0;
    }

    function toRadians(degrees: number): number {
    	return degrees * (Math.PI / 180);
    }
    ```

=== "src/app/app.component.html (appTrigonometry)"

    ```html
    <ul *appTrigonometry="30; sin as s; cos as c; tan as t">
    	<li>sin(30°): {{ s }}</li>
    	<li>cos(30°): {{ c }}</li>
    	<li>tan(30°): {{ t }}</li>
    </ul>
    ```
