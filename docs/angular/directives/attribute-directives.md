---
description: "Директивы атрибутов меняют внешний вид или поведение элементов DOM и компонентов Angular"
---

# Директивы атрибутов {: #attribute-directives}

:date: 30.09.2026

Директивы атрибутов меняют внешний вид или поведение элементов DOM и компонентов Angular.

## Разовое поведение — через привязки шаблона {: #use-template-bindings-for-one-off-behavior}

Синтаксис шаблона Angular уже умеет менять классы, стили, свойства и события одного элемента:

-   [Привязки класса и стиля](../templates/binding.md#css-class-and-style-property-bindings) добавляют и убирают CSS-классы и встроенные стили.
-   [Привязки свойств и атрибутов](../templates/binding.md) задают свойства DOM и HTML-атрибуты.
-   [Обработчики событий](../templates/event-listeners.md) реагируют на действия пользователя.

Директива атрибута нужна, когда такое поведение стоит собрать в одну единицу и вешать на любой элемент или компонент.

## Создание директивы атрибута {: #building-an-attribute-directive}

Своя директива атрибута — это класс JavaScript с декоратором `@Directive()`. Свойство `selector` декоратора задаёт атрибут, которым директиву применяют. Квадратные скобки делают селектор атрибутным: директива совпадает с элементами, у которых есть этот атрибут. По соглашению берут префикс вроде `app`, чтобы не столкнуться с чужими именами:

```ts
import {Directive} from '@angular/core';

@Directive({
  selector: '[appHighlight]',
})
export class HighlightDirective {}
```

!!! tip ""

    Команда CLI [`ng generate directive`](https://angular.dev/tools/cli/schematics) создаёт заготовку директивы и файл её теста.

Хост директивы можно менять декларативно, через привязки хоста, или императивно, через ссылку на элемент-хост. В примере [внедряется](../di/overview.md) [`ElementRef`](https://angular.dev/api/core/ElementRef): элемент берётся из свойства `nativeElement`, и фон красится в жёлтый.

_highlight.directive.ts_

```ts
import {Directive, ElementRef, inject} from '@angular/core';

@Directive({
  selector: '[appHighlight]',
})
export class HighlightDirective {
  private el = inject(ElementRef);

  constructor() {
    this.el.nativeElement.style.backgroundColor = 'yellow';
  }
}
```

!!! warning ""

    Директивы _не_ поддерживают пространства имён.

```html
<p app:Highlight>This is invalid</p>
```

## Применение директивы атрибута {: #applying-an-attribute-directive}

Чтобы применить директиву, добавьте её селектор атрибутом элемента.

_app.component.html_

```html
<p appHighlight>Highlight me!</p>
```

Angular создаёт экземпляр `HighlightDirective` для этого элемента `<p>`, внедряет ссылку на элемент и красит его фон в жёлтый.

## Обработка действий пользователя {: #handling-user-events}

Чтобы реагировать на действия пользователя, привяжите события элемента-хоста к методам-обработчикам через свойство `host` декоратора `@Directive()`. Следующая директива подсвечивает элемент-хост, пока над ним указатель, и снимает подсветку, когда указатель уходит.

_highlight.directive.ts_

```ts
import {Directive, ElementRef, inject} from '@angular/core';

@Directive({
  selector: '[appHighlight]',
  host: {
    '(mouseenter)': 'onMouseEnter()',
    '(mouseleave)': 'onMouseLeave()',
  },
})
export class HighlightDirective {
  private el = inject(ElementRef);

  // #docregion mouse-methods
  onMouseEnter() {
    this.highlight('yellow');
  }

  onMouseLeave() {
    this.highlight('');
  }

  private highlight(color: string) {
    this.el.nativeElement.style.backgroundColor = color;
  }
  // #enddocregion mouse-methods
}
```

Свойство `host` сопоставляет события `mouseenter` и `mouseleave` с методами `onMouseEnter()` и `onMouseLeave()`. Те вызывают вспомогательный `highlight()`, который задаёт цвет фона элемента-хоста. Подробнее о привязках событий хоста — в разделе [привязка к элементу-хосту](../components/host-elements.md#binding-to-the-host-element).

## Входные значения {: #accepting-input-values}

Как и компоненты, директивы принимают входы через функцию [`input()`](../components/inputs.md). Назовите вход так же, как селектор: тогда одна привязка и применяет директиву, и передаёт ей значение.

_highlight.directive.ts_

```ts
  appHighlight = input('');
```

Вход читают вызовом, как сигнал. Если цвет не задан, берут значение по умолчанию.

_highlight.directive.ts_

```ts
import {Directive, ElementRef, inject, input} from '@angular/core';

@Directive({
  selector: '[appHighlight]',
  host: {
    '(mouseenter)': 'onMouseEnter()',
    '(mouseleave)': 'onMouseLeave()',
  },
})
export class HighlightDirective {
  private el = inject(ElementRef);

  appHighlight = input('');

  // #docregion mouse-enter
  onMouseEnter() {
    this.highlight(this.appHighlight() || 'red');
  }
  // #enddocregion mouse-enter

  onMouseLeave() {
    this.highlight('');
  }

  private highlight(color: string) {
    this.el.nativeElement.style.backgroundColor = color;
  }
}
```

В шаблоне значение привязывают к селектору. Вход называется так же, как селектор, поэтому `[appHighlight]` и применяет директиву, и задаёт её значение. Здесь привязанный `color` — свойство компонента.

_app.component.html_

```html
<p [appHighlight]="color">Highlight me!</p>
```

_app.component.ts_

```ts
export class AppComponent {
  color = '';
}
```

У директивы может быть больше одного входа. Следующая добавляет вход `defaultColor` и перебирает запасные значения: сначала `appHighlight`, затем `defaultColor` и в конце `red`.

_highlight.directive.ts_

```ts
import {Directive, ElementRef, inject, input} from '@angular/core';

@Directive({
  selector: '[appHighlight]',
  host: {
    '(mouseenter)': 'onMouseEnter()',
    '(mouseleave)': 'onMouseLeave()',
  },
})
export class HighlightDirective {
  private el = inject(ElementRef);

  defaultColor = input('');

  appHighlight = input('');

  // #docregion mouse-enter
  onMouseEnter() {
    this.highlight(this.appHighlight() || this.defaultColor() || 'red');
  }
  // #enddocregion mouse-enter

  onMouseLeave() {
    this.highlight('');
  }

  private highlight(color: string) {
    this.el.nativeElement.style.backgroundColor = color;
  }
}
```

Оба входа привязывают на одном элементе. `defaultColor` получает статическую строку, а не динамическое выражение, поэтому квадратные скобки не нужны.

_app.component.html_

```html
<p [appHighlight]="color" defaultColor="violet">Highlight me too!</p>
```

## Отключение обработки Angular через `NgNonBindable` {: #deactivating-angular-processing-with-ngnonbindable}

Чтобы браузер не вычислял выражения, добавьте `ngNonBindable` на элемент-хост.
`ngNonBindable` отключает в шаблонах интерполяцию, директивы и привязки.

В примере выражение `{{ 1 + 1 }}` выводится так же, как в редакторе кода, и не превращается в `2`.

_app.component.html_

```html
<p>Use ngNonBindable to stop evaluation.</p>
<p ngNonBindable>This should not evaluate: {{ 1 + 1 }}</p>
```

`ngNonBindable` на элементе отключает привязки у его дочерних элементов.
При этом директивы на том самом элементе, куда повесили `ngNonBindable`, продолжают работать.
В примере директива `appHighlight` всё ещё активна, но выражение `{{ 1 + 1 }}` Angular не вычисляет.

_app.component.html_

```html
<h1>My First Attribute Directive</h1>

<h2>Pick a highlight color</h2>
<div>
  <input type="radio" name="colors" (click)="color = 'lightgreen'" />Green
  <input type="radio" name="colors" (click)="color = 'yellow'" />Yellow
  <input type="radio" name="colors" (click)="color = 'cyan'" />Cyan
</div>
<p [appHighlight]="color">Highlight me!</p>

<p [appHighlight]="color" defaultColor="violet">Highlight me too!</p>

<hr />
<h2>Mouse over the following lines to see fixed highlights</h2>

<p [appHighlight]="'yellow'">Highlighted in yellow</p>
<p appHighlight="orange">Highlighted in orange</p>

<hr />

<h2>ngNonBindable</h2>
<p>Use ngNonBindable to stop evaluation.</p>
<p ngNonBindable>This should not evaluate: {{ 1 + 1 }}</p>

<!-- #docregion ngNonBindable-with-directive -->
<h3>ngNonBindable with a directive</h3>
<div ngNonBindable [appHighlight]="'yellow'">
  This should not evaluate: {{ 1 + 1 }}, but will highlight yellow.
</div>
<!-- #enddocregion ngNonBindable-with-directive -->
```

Если повесить `ngNonBindable` на родительский элемент, Angular отключает у его потомков интерполяцию и любые привязки, в том числе привязку свойства и привязку события.

## Что дальше {: #whats-next}

-   [Структурные директивы](structural-directives.md)
-   [API композиции директив](https://angular.dev/guide/directives/directive-composition-api)

---

Источник: [https://angular.dev/guide/directives/attribute-directives](https://angular.dev/guide/directives/attribute-directives)
