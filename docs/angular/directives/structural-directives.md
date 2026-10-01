---
description: "Структурные директивы применяют к элементу `<ng-template>` и по условию или повторно отрисовывают содержимое этого `<ng-template>`"
---

# Структурные директивы {: #structural-directives}

:date: 30.09.2026

Структурные директивы применяют к элементу `<ng-template>`, и они по условию или повторно отрисовывают содержимое этого `<ng-template>`.

Для обычной условной и повторной отрисовки берите встроенные [блоки управления потоком](../templates/control-flow.md) (`@if`, `@for` и `@switch`). Структурную директиву пишите, когда нужно переиспользуемое поведение отрисовки, которого в управлении потоком нет: например, показывать содержимое только после проверки прав или отдавать шаблону данные из внешнего источника.

## Пример {: #example-use-case}

Сквозной пример этого руководства — директива `SelectDirective`. Она забирает данные из заданного источника и отрисовывает свой шаблон, когда данные уже есть. Имя взято от ключевого слова SQL `SELECT`, селектор атрибута — `[select]`.

У `SelectDirective` есть вход `selectFrom`: он называет источник данных. Префикс `select` у этого входа важен для [сокращённого синтаксиса](#structural-directive-shorthand). Директива создаёт экземпляр своего `<ng-template>` с контекстом шаблона, в котором лежат выбранные данные.

Напрямую на `<ng-template>` это выглядит так:

```html
<ng-template select let-data [selectFrom]="source">
  <p>The data is: {{ data }}</p>
</ng-template>
```

Структурная директива может дождаться, пока данные появятся, и только потом отрисовать свой `<ng-template>`.

!!! tip ""

    Элемент `<ng-template>` в Angular задаёт шаблон, который по умолчанию ничего не рисует. Если обернуть элементы в `<ng-template>` и не применить структурную директиву, эти элементы не отрисуются.

Подробнее — в документации [API `ng-template`](https://angular.dev/api/core/ng-template).

## Сокращённый синтаксис структурных директив {: #structural-directive-shorthand}

У структурных директив есть сокращённый синтаксис: элемент `<ng-template>` писать явно не нужно.

Директиву можно повесить прямо на элемент, поставив звёздочку (`*`) перед селектором атрибута, например `*select`. Angular превращает звёздочку перед структурной директивой в `<ng-template>`, который принимает директиву и оборачивает элемент вместе с потомками.

С `SelectDirective` это выглядит так:

```html
<p *select="let data; from: source">The data is: {{ data }}</p>
```

На примере видна гибкость сокращённого синтаксиса структурных директив. Его иногда называют _микросинтаксисом_.

В таком виде на `<ng-template>` попадают только структурная директива и её привязки. Остальные атрибуты и привязки тега `<p>` остаются на месте. Например, две записи ниже равносильны:

```html
<!-- Shorthand syntax: -->
<p class="data-view" *select="let data; from: source">The data is: {{ data }}</p>

<!-- Long-form syntax: -->
<ng-template select let-data [selectFrom]="source">
  <p class="data-view">The data is: {{ data }}</p>
</ng-template>
```

Сокращение раскрывается по набору соглашений. Ниже задана более полная [грамматика](#structural-directive-syntax-reference), а превращение в примере выше устроено так.

Первая часть выражения `*select` — `let data`: объявляется переменная шаблона `data`. Присваивания после неё нет, поэтому переменная привязывается к свойству контекста шаблона `$implicit`.

Вторая часть — пара «ключ и выражение», `from source`. `from` — ключ привязки, `source` — обычное выражение шаблона. Ключи привязки сопоставляются со свойствами так: ключ переводят в PascalCase и спереди добавляют селектор структурной директивы. Ключ `from` становится `selectFrom` и привязывается к выражению `source`. Поэтому у многих структурных директив имена входов начинаются с селектора самой директивы.

## Одна структурная директива на элемент {: #one-structural-directive-per-element}

В сокращённом синтаксисе на элемент можно повесить только одну структурную директиву: раскрывается она в один элемент `<ng-template>`. Несколько директив потребовали бы нескольких вложенных `<ng-template>`, и неясно, какая должна быть первой. `<ng-container>` даёт слои-обёртки, когда несколько структурных директив нужно повесить вокруг одного и того же физического элемента DOM или компонента: вложенность задаёте вы сами.

## Создание структурной директивы {: #creating-a-structural-directive}

Структурная директива — класс директивы, который внедряет две зависимости:

-   [`TemplateRef`](https://angular.dev/api/core/TemplateRef) даёт директиве доступ к содержимому того `<ng-template>`, на который она повешена.
-   [`ViewContainerRef`](https://angular.dev/api/core/ViewContainerRef) — место в DOM, где директива может отрисовать этот шаблон.

Отрисовкой директива управляет сама: создаёт или не создаёт встроенные представления из шаблона в контейнере представлений. Полный `SelectDirective` выглядит так:

```ts
import {Directive, TemplateRef, ViewContainerRef, inject, input} from '@angular/core';

export interface DataSource<T> {
  load(): Promise<T>;
}

@Directive({
  selector: '[select]',
})
export class SelectDirective {
  private templateRef = inject(TemplateRef);
  private viewContainerRef = inject(ViewContainerRef);

  selectFrom = input.required<DataSource<unknown>>();

  async ngOnInit() {
    const data = await this.selectFrom().load();
    this.viewContainerRef.createEmbeddedView(this.templateRef, {
      // Create the embedded view with a context object that contains
      // the data via the key `$implicit`.
      $implicit: data,
    });
  }
}
```

Вход `selectFrom` называет источник, из которого директива читает данные. Здесь стоит [`input.required()`](../components/inputs.md#required-inputs): без источника директиве нечего делать.

Когда Angular инициализирует директиву, она загружает данные и отрисовывает шаблон вызовом `createEmbeddedView()`. Второй аргумент — _объект контекста_ шаблона: значения, к которым шаблон привязывается объявлениями `let`. Данные в ключе `$implicit` становятся значением по умолчанию, которое получает `let-data` (или `let data` в сокращении).

!!! info ""

    В этом примере шаблон отрисовывается один раз, при инициализации директивы. Когда привязанный источник данных меняется, повторной отрисовки нет.

Когда директива уже работает, имеет смысл [добавить поддержку проверки типов шаблона](#typing-the-directives-context).

!!! tip ""

    Команда CLI [`ng generate directive`](https://angular.dev/tools/cli/schematics) создаёт заготовку директивы и файл её теста.

## Справочник синтаксиса структурных директив {: #structural-directive-syntax-reference}

Для своих структурных директив используйте такой синтаксис:

```ts
_: prefix = "( :let | :expression ) (';' | ',')? ( :let | :as | :keyExp )_";
```

Каждую часть грамматики задают такие шаблоны:

```ts
as = :export "as" :local ";"?
keyExp = :key ":"? :expression ("as" :local)? ";"?
let = "let" :local "=" :export ";"?
```

| Ключевое слово | Подробности                                            |
| :------------- | :----------------------------------------------------- |
| `prefix`       | Ключ HTML-атрибута                                     |
| `key`          | Ключ HTML-атрибута                                     |
| `local`        | Имя локальной переменной в шаблоне                     |
| `export`       | Значение, которое директива экспортирует под заданным именем |
| `expression`   | Обычное выражение Angular                              |

### Как Angular раскрывает сокращение {: #how-angular-translates-shorthand}

Angular переводит сокращение структурной директивы в обычный синтаксис привязок так:

| Сокращение                      | Перевод                                                         |
| :------------------------------ | :-------------------------------------------------------------- |
| `prefix` и голое `expression`   | `[prefix]="expression"`                                         |
| `keyExp`                        | `[prefixKey]="expression"` (`prefix` добавляется к `key`)       |
| `let local`                     | `let-local="export"`                                            |

### Примеры сокращений {: #shorthand-examples}

В таблице — примеры сокращений:

| Сокращение                                                            | Как Angular читает синтаксис                                                                                  |
| :-------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------ |
| `*myDir="let item of [1,2,3]"`                                        | `<ng-template myDir let-item [myDirOf]="[1, 2, 3]">`                                                          |
| `*myDir="let item of [1,2,3] as items; trackBy: myTrack; index as i"` | `<ng-template myDir let-item [myDirOf]="[1,2,3]" let-items="myDirOf" [myDirTrackBy]="myTrack" let-i="index">` |
| `*ngComponentOutlet="componentClass"`                                 | `<ng-template [ngComponentOutlet]="componentClass">`                                                          |
| `*ngComponentOutlet="componentClass; inputs: myInputs"`               | `<ng-template [ngComponentOutlet]="componentClass" [ngComponentOutletInputs]="myInputs">`                     |
| `*myDir="exp as value"`                                               | `<ng-template [myDir]="exp" let-value="myDir">`                                                               |

## Проверка типов шаблона для своих директив {: #improving-template-type-checking-for-custom-directives}

Проверку типов шаблона для своих директив усиливают охранники шаблона в определении директивы.
Они помогают проверке типов шаблона Angular находить ошибки ещё при компиляции и тем самым избегать ошибок во время выполнения.
Охранники бывают двух видов:

-   `ngTemplateGuard_(input)` задаёт, как сужать выражение входа по типу конкретного входа.
-   `ngTemplateContextGuard` по типу самой директивы определяет тип объекта контекста шаблона.

Ниже — примеры обоих видов.
Подробнее — в разделе [Проверка типов шаблона](https://angular.dev/tools/cli/template-typecheck 'Руководство по проверке типов шаблона').

### Сужение типа охранниками шаблона {: #type-narrowing-with-template-guards}

Структурная директива в шаблоне решает, отрисовывать ли этот шаблон во время выполнения. Некоторым директивам нужно сузить тип по типу входного выражения.

Входные охранники дают два сужения:

-   Сужение входного выражения функцией утверждения типа TypeScript.
-   Сужение входного выражения по его истинности.

Чтобы сузить входное выражение, объявите функцию утверждения типа:

```ts
// This directive only renders its template if the actor is a user.
// You want to assert that within the template, the type of the `actor`
// expression is narrowed to `User`.
@Directive(...)
class ActorIsUser {
  actor = input<User | Robot>();

  static ngTemplateGuard_actor(dir: ActorIsUser, expr: User | Robot): expr is User {
    // The return statement is unnecessary in practice, but included to
    // prevent TypeScript errors.
    return true;
  }
}
```

В шаблоне проверка типов идёт так, будто для выражения, привязанного ко входу, уже сработал `ngTemplateGuard_actor`.

Некоторые директивы рисуют шаблон только при истинном входе. Семантику истинности целиком в функции утверждения типа не передать, поэтому вместо неё указывают литеральный тип `'binding'`: он говорит проверке типов шаблона, что охранником должно быть само выражение привязки.

```ts
@Directive(...)
class CustomIf {
  condition = input.required<boolean>();

  static ngTemplateGuard_condition: 'binding';
}
```

Проверка типов шаблона считает, что выражение, привязанное к `condition`, внутри шаблона истинно.

### Типизация контекста директивы {: #typing-the-directives-context}

Если структурная директива отдаёт контекст созданному шаблону, тип этого контекста внутри шаблона задаёт статическая функция утверждения типа `ngTemplateContextGuard`. Она выводит тип контекста из типа директивы. Это нужно, когда директива обобщённая.

Для `SelectDirective` выше можно описать `ngTemplateContextGuard` и верно задать тип данных, даже если источник данных обобщённый.

```ts
// Declare an interface for the template context:
export interface SelectTemplateContext<T> {
  $implicit: T;
}

@Directive(...)
export class SelectDirective<T> {
  // The directive's generic type `T` will be inferred from the `DataSource` type
  // passed to the input.
  selectFrom = input.required<DataSource<T>>();

  // Narrow the type of the context using the generic type of the directive.
  static ngTemplateContextGuard<T>(dir: SelectDirective<T>, ctx: any): ctx is SelectTemplateContext<T> {
    // As before the guard body is not used at runtime, and included only to avoid
    // TypeScript errors.
    return true;
  }
}
```

## Что дальше {: #whats-next}

-   [API композиции директив](https://angular.dev/guide/directives/directive-composition-api)
-   [ng-template](https://angular.dev/guide/templates/ng-template)
-   [Управление потоком](../templates/control-flow.md)

---

Источник: [https://angular.dev/guide/directives/structural-directives](https://angular.dev/guide/directives/structural-directives)
