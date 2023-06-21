# Структурные директивы

Это руководство посвящено структурным директивам и содержит концептуальную информацию о том, как работают такие директивы, как Angular интерпретирует их сокращенный синтаксис, и как добавить свойства защиты шаблона для отлова ошибок типа шаблона.

Структурные директивы - это директивы, которые изменяют макет DOM путем добавления и удаления элементов DOM.

Angular предоставляет набор встроенных структурных директив (таких как `NgIf`, `NgForOf`, `NgSwitch` и другие), которые часто используются во всех проектах Angular. Более подробную информацию можно найти в [Built-in directives](guide/built-in-directives).

<div class="alert is-helpful">

Пример приложения, которое описывается на этой странице, смотрите в <live-example name="structural-directives"></live-example>.

</div>

<a id="shorthand"></a> <a id="asterisk"></a>

## Сокращение структурных директив

Когда применяются структурные директивы, они обычно сопровождаются звездочкой, `*`, например, `*ngIf`. Это соглашение является сокращением, которое Angular интерпретирует и преобразует в более длинную форму. Angular преобразует звездочку перед структурной директивой в `<ng-template>`, который окружает основной элемент и его потомков.

Например, возьмем следующий код, который использует `*ngIf` для отображения имени героя, если `hero` существует:

<code-example path="structural-directives/src/app/app.component.html" header="src/app/app.component.html (asterisk)" region="asterisk"></code-example>

Angular creates an `<ng-template>` element and applies the `*ngIf` directive onto it where it becomes a property binding in square brackets, `[ngIf]`. The rest of the `<div>`, including its class attribute, is then moved inside the `<ng-template>`:

<code-example path="structural-directives/src/app/app.component.html" header="src/app/app.component.html (ngif-template)" region="ngif-template"></code-example>

Note that Angular does not actually create a real `<ng-template>` element, but instead only renders the `<div>` element.

```html <div _ngcontent-c0>Mr. Nice</div>

```

В следующем примере сравнивается сокращенное использование звездочки в `*ngFor` с длинной формой `<ng-template>`:

<code-example path="structural-directives/src/app/app.component.html" header="src/app/app.component.html (inside-ngfor)" region="inside-ngfor"></code-example>

Here, everything related to the `ngFor` structural directive is moved to the `<ng-template>`. All other bindings and attributes on the element apply to the `<div>` element within the `<ng-template>`.

Other modifiers on the host element, in addition to the `ngFor` string, remain in place as the element moves inside the `<ng-template>`.

In this example, the `[class.odd]="odd"` stays on the `<div>`.

The `let` keyword declares a template input variable that you can reference within the template. The input variables in this example are `hero`, `i`, and `odd`.

The parser translates `let hero`, `let i`, and `let odd` into variables named `let-hero`, `let-i`, and `let-odd`.

The `let-i` and `let-odd` variables become `let i=index` and `let odd=odd`.

Angular sets `i` and `odd` to the current value of the context's `index` and `odd` properties.

The parser applies PascalCase to all directives and prefixes them with the directive's attribute name, such as ngFor. For example, the `ngFor` input properties, `of` and `trackBy`, map to `ngForOf` and `ngForTrackBy`.

As the `NgFor` directive loops through the list, it sets and resets properties of its own context object. Эти свойства могут включать, но не ограничиваться, `index`, `odd` и специальное свойство

под названием `$implicit`.

Angular устанавливает `let-hero` в значение свойства контекста `$implicit`, которое `NgFor` инициализировал героем для текущей итерации.

Для получения дополнительной информации смотрите документацию [NgFor API](api/common/NgFor 'API: NgFor') и [NgForOf API](api/common/NgForOf).

<div class="alert is-helpful">

Обратите внимание, что элемент `<ng-template>` в Angular определяет шаблон, который по умолчанию ничего не отображает, если вы просто обернете элементы в `<ng-template>` без применения структурной директивы, эти элементы не будут отображены.

Для получения дополнительной информации смотрите документацию [ng-template API](api/core/ng-template).

</div>

<a id="one-per-element"></a>

## Одна структурная директива на элемент

Довольно распространенным случаем является повторение блока HTML, но только при выполнении определенного условия. Интуитивно понятным способом сделать это является размещение `*ngFor` и `*ngIf` на одном и том же элементе. Однако, поскольку и `*ngFor`, и `*ngIf` являются структурными директивами, это будет расценено компилятором как ошибка. Вы можете применить только одну _структурную_ директиву к элементу.

Причина в простоте. Структурные директивы могут делать сложные вещи с основным элементом и его потомками.

Когда две директивы претендуют на один и тот же элемент-хозяин, какая из них должна иметь приоритет?

Что должно быть первым, `NgIf` или `NgFor`? Может ли `NgIf` отменить эффект `NgFor`? Если да (а кажется, что так и должно быть), то как Angular должен обобщить возможность отмены для других структурных директив?

На эти вопросы нет простых ответов. Запрет на использование нескольких структурных директив делает их спорными. Есть простое решение для этого случая использования: поместите `*ngIf` в элемент-контейнер, который обертывает элемент `*ngFor`. Один или оба элемента могут быть `<ng-container>`, чтобы не создавать лишних элементов DOM.

<a id="unless"></a>

## Создание структурной директивы

В этом разделе вы узнаете, как создать `UnlessDirective` и как задать значения `condition`. Директива `UnlessDirective` делает противоположное `NgIf`, а значения `condition` могут быть установлены в `true` или `false`.

`NgIf` отображает содержимое шаблона, когда условие равно `true`.

`UnlessDirective` отображает содержимое, когда условие равно `false`.

Ниже приведен селектор `UnlessDirective`, `appUnless`, примененный к элементу paragraph. Когда `условие` равно `false`, браузер отображает предложение.

<code-example header="src/app/app.component.html (appUnless-1)" path="structural-directives/src/app/app/app.component.html" region="appUnless-1"></code-example>.

1.  Используя Angular CLI, выполните следующую команду, где `unless` - имя директивы:

    <code-example format="shell" language="shell">.

    ng generate директива unless

    </code-example>.

    Angular создает класс директивы и определяет CSS-селектор `appUnless`, который идентифицирует директиву в шаблоне.

1.  Импортируйте `Input`, `TemplateRef` и `ViewContainerRef`.

    <code-example header="src/app/unless.directive.ts (skeleton)" path="structural-directives/src/app/unless.directive.ts" region="skeleton"></code-example>.

1.  Вставьте `TemplateRef` и `ViewContainerRef` в конструктор директивы как приватные переменные.

    <code-example header="src/app/unless.directive.ts (ctor)" path="structural-directives/src/app/unless.directive.ts" region="ctor"></code-example>.

    Директива `UnlessDirective` создает [встроенное представление](api/core/EmbeddedViewRef 'API: EmbeddedViewRef') из сгенерированного Angular `<ng-template>` и вставляет это представление в [контейнер представления](api/core/ViewContainerRef 'API: ViewContainerRef') рядом с исходным элементом директивы `<p>`.

    [`TemplateRef`](api/core/TemplateRef 'API: TemplateRef') помогает добраться до содержимого `<ng-template>`, а [`ViewContainerRef`](api/core/ViewContainerRef 'API: ViewContainerRef') открывает доступ к контейнеру представления.

1.  Добавьте свойство `appUnless` `@Input()` с сеттером.

    <code-example header="src/app/unless.directive.ts (set)" path="structural-directives/src/app/unless.directive.ts" region="set"></code-example>.

    Angular устанавливает свойство `appUnless` всякий раз, когда значение условия изменяется.

    -   Если условие ложно и Angular не создал представление ранее, то сеттер заставляет контейнер представления создать встроенное представление из шаблона.

    -   Если условие истинно, и представление отображается в данный момент, сеттер очищает контейнер, который утилизирует представление.

Полный текст директивы выглядит следующим образом:

<code-example header="src/app/unless.directive.ts (excerpt)" path="structural-directives/src/app/unless.directive.ts" region="no-docs"></code-example>.

### Тестирование директивы

В этом разделе вы обновите свое приложение, чтобы протестировать `UnlessDirective`.

1.  Добавьте `условие`, установленное в `false` в `AppComponent`.

    <code-example header="src/app/app.component.ts (excerpt)" path="structural-directives/src/app/app/app.component.ts" region="condition"></code-example>.

1.  Обновите шаблон для использования директивы.

    Здесь `*appUnless` находится на двух тегах `<p>` с противоположными значениями `condition`, одно `true` и одно `false`.

    <code-example header="src/app/app.component.html (appUnless)" path="structural-directives/src/app/app/app.component.html" region="appUnless"></code-example>.

    Звездочка - это сокращение, обозначающее `appUnless` как структурную директиву.

    Когда `условие` ложно, верхний \(A\) параграф появляется, а нижний \(B\) параграф исчезает.

    Когда `условие` истинно, верхний \(A\) параграф исчезает, а нижний (B) параграф появляется.

1.  Чтобы изменить и отобразить значение `условия` в браузере, добавьте разметку, отображающую статус и кнопку.

    <code-example header="src/app/app.component.html" path="structural-directives/src/app/app/app.component.html" region="toggle-info"></code-example>.

Чтобы убедиться, что директива работает, нажмите на кнопку, чтобы изменить значение `condition`.

<div class="lightbox">

<img alt="UnlessDirective in action" src="generated/images/guide/structural-directives/unless-anim.gif">

</div>

## Справочник по синтаксису структурных директив

Когда вы пишете свои собственные структурные директивы, используйте следующий синтаксис:

<code-example format="typescript" hideCopy language="typescript">

\*:prefix=""( :let &verbar; :expression ) (';' &verbar; ',')? ( :let &verbar; :as &verbar; :keyExp )\*".

</code-example>

В следующих таблицах описана каждая часть грамматики структурной директивы:

<code-tabs> <code-pane format="typescript" header="as" hideCopy language="typescript"> as = :export "as" :local ";"? </code-pane>
<code-pane format="typescript" header="keyExp" hideCopy language="typescript"> keyExp = :key ":"? :expression ("as" :local)? ";"? </code-pane>
<code-pane format="typescript" header="let" hideCopy language="typescript"> let = "let" :local "=" :export ";"? </code-pane>
</code-tabs>

| Keyword | Details | |:--- |:--- |
| `prefix` | HTML attribute key |

| `key` | HTML attribute key |

| `local` | Local variable name used in the template |

| `export` | Value exported by the directive under a given name |

| `expression` | Standard Angular expression |

### How Angular translates shorthand

Angular translates structural directive shorthand into the normal binding syntax as follows:

| Shorthand | Translation | |:--- |:--- |

| `prefix` and naked `expression` | <code-example format="typescript" hideCopy language="typescript"> [prefix]="expression" </code-example> |

| `keyExp` | <code-example format="typescript" hideCopy language="typescript"> [prefixKey] "expression" (let-prefixKey="export") </code-example> <div class="alert is-helpful"> **NOTE**: <br /> The `prefix` is added to the `key` </div> |

| `let` | <code-example format="typescript" hideCopy language="typescript"> let-local="export" </code-example> |

### Shorthand examples

The following table provides shorthand examples:

| Shorthand | How Angular interprets the syntax | |:--- |:--- |
| <code-example format="typescript" hideCopy language="typescript"> \*ngFor="let item of [1,2,3]" </code-example> | <code-example format="html" hideCopy language="html"> &lt;ng-template ngFor &NewLine;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; let-item &NewLine;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; [ngForOf]="[1,2,3]"&gt; </code-example> |
| <code-example format="typescript" hideCopy language="typescript"> \*ngFor="let item of [1,2,3] as items; &NewLine;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; trackBy: myTrack; index as i" </code-example> | <code-example format="html" hideCopy language="html"> &lt;ng-template ngFor &NewLine;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; let-item &NewLine;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; [ngForOf]="[1,2,3]" &NewLine;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; let-items="ngForOf" &NewLine;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; [ngForTrackBy]="myTrack" &NewLine;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; let-i="index"&gt; </code-example> |
| <code-example format="typescript" hideCopy language="typescript"> \*ngIf="exp" </code-example> | <code-example format="html" hideCopy language="html"> &lt;ng-template [ngIf]="exp"&gt; </code-example> |
| <code-example format="typescript" hideCopy language="typescript"> \*ngIf="exp as value" </code-example> | <code-example format="html" hideCopy language="html"> &lt;ng-template [ngIf]="exp" &NewLine;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; let-value="ngIf"&gt; </code-example> |

<a id="directive-type-checks"></a>

<!--todo: To do follow up PR: move this section to a more general location because it also applies to attribute directives. -->

## Улучшение проверки типов шаблонов для пользовательских директив

Вы можете улучшить проверку типов шаблонов для пользовательских директив, добавив свойства защиты шаблона в определение директивы. Эти свойства помогают программе проверки типов шаблонов Angular находить ошибки в шаблоне во время компиляции, что позволяет избежать ошибок во время выполнения.

Эти свойства выглядят следующим образом:

-   Свойство `ngTemplateGuard_(someInputProperty)` позволяет вам указать более точный тип для входного выражения в шаблоне.

-   Статическое свойство `ngTemplateContextGuard` объявляет тип контекста шаблона.

В этом разделе приведены примеры обоих типов свойств защиты типа. Для получения дополнительной информации смотрите [Проверка типов шаблонов](guide/template-typecheck 'Руководство по проверке типов шаблонов').

<a id="narrowing-input-types"></a>

### Уточнение требований к типам в шаблоне с помощью защит шаблона

Структурная директива в шаблоне управляет тем, будет ли этот шаблон отображаться во время выполнения, основываясь на его входном выражении. Чтобы помочь компилятору отловить ошибки типа шаблона, вы должны как можно точнее определить требуемый тип входного выражения директивы, когда оно встречается внутри шаблона.

Функция защиты типа сужает ожидаемый тип входного выражения до подмножества типов, которые могут быть переданы директиве внутри шаблона во время выполнения. Вы можете предоставить такую функцию, чтобы помочь программе проверки типов вывести правильный тип для выражения во время компиляции.

Например, реализация `NgIf` использует сужение типов, чтобы гарантировать, что шаблон будет инстанцирован только в том случае, если входное выражение `*ngIf` истинно. Для обеспечения конкретного требования к типу, директива `NgIf` определяет [статическое свойство `ngTemplateGuard_ngIf: 'binding'`] (api/common/NgIf#static-properties).

Значение `binding` является особым случаем для распространенного вида сужения типа, когда входное выражение оценивается для того, чтобы удовлетворить требованию типа.

Чтобы задать более конкретный тип входного выражения для директивы в шаблоне, добавьте к директиве свойство `ngTemplateGuard_xx`, где суффикс к имени статического свойства, `xx`, является именем поля `@Input()`. Значением свойства может быть либо общая функция сужения типов на основе ее возвращаемого типа, либо строка `"binding"`, как в случае `NgIf`.

Например, рассмотрим следующую структурную директиву, которая принимает результат шаблонного выражения в качестве входных данных:

<code-tabs linenums="true"> <code-pane
    header="src/app/if-loaded.directive.ts"
    path="structural-directives/src/app/if-loaded.directive.ts">
</code-pane>
<code-pane
    header="src/app/loading-state.ts"
    path="structural-directives/src/app/loading-state.ts">
</code-pane>
<code-pane
    header="src/app/hero.component.ts"
    path="structural-directives/src/app/hero.component.ts">
</code-pane>
</code-tabs>

В данном примере тип `LoadingState<T>` допускает одно из двух состояний, `Loaded<T>` или `Loading`. Выражение, используемое в качестве входного `state` директивы (псевдоним `appIfLoaded`), имеет зонтичный тип `LoadingState`, поскольку неизвестно, в каком состоянии находится загрузка в данный момент.

Определение `IfLoadedDirective` объявляет статическое поле `ngTemplateGuard_appIfLoaded`, которое выражает поведение сужения. Внутри шаблона `AppComponent` структурная директива `*appIfLoaded` должна выводить этот шаблон только тогда, когда `state` действительно `Loaded<Hero>`.

Защита типа позволяет программе проверки типов сделать вывод, что допустимым типом `state` в шаблоне является `Loaded<T>`, и далее сделать вывод, что `T` должен быть экземпляром `Hero`.

<a id="narrowing-context-type"></a>

### Типизация контекста директивы

Если ваша структурная директива предоставляет контекст инстанцированному шаблону, вы можете правильно типизировать его внутри шаблона, предоставив статическую функцию `ngTemplateContextGuard`. В следующем фрагменте показан пример такой функции.

<code-tabs linenums="true"> <code-pane
    header="src/app/trigonometry.directive.ts"
    path="structural-directives/src/app/trigonometry.directive.ts">
</code-pane>
<code-pane
    header="src/app/app.component.html (appTrigonometry)"
    path="structural-directives/src/app/app.component.html"
    region="appTrigonometry">
</code-pane>
</code-tabs>

<!-- links -->

<!-- external links -->

<!-- end links -->

:date: 28.02.2022
