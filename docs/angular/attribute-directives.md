# Директивы атрибутов

Измените внешний вид или поведение элементов DOM и компонентов Angular с помощью директив атрибутов.

<div class="alert is-helpful">

Смотрите <live-example></live-example> для рабочего примера, содержащего фрагменты кода, приведенные в этом руководстве.

</div>

## Создание директивы атрибута

В этом разделе рассказывается о создании директивы выделения, которая устанавливает желтый цвет фона основного элемента.

1.  Чтобы создать директиву, используйте команду CLI [`ng generate directive`](cli/generate).

    <code-example format="shell" language="shell">

    ng generate directive highlight

    </code-example>.

    CLI создает `src/app/highlight.directive.ts`, соответствующий тестовый файл `src/app/highlight.directive.spec.ts` и объявляет класс директивы в `AppModule`.

    CLI генерирует стандартный `src/app/highlight.directive.ts` следующим образом:

    <code-example header="src/app/app/highlight.directive.ts" path="attribute-directives/src/app/highlight.directive.0.ts"></code-example>.

    Свойство конфигурации декоратора `@Directive()` определяет селектор CSS-атрибутов директивы, `[appHighlight]`.

1.  Импортируйте `ElementRef` из `@angular/core`.

    `ElementRef` предоставляет прямой доступ к основному элементу DOM через свойство `nativeElement`.

1.  Добавьте `ElementRef` в `constructor()` директивы для [inject](guide/dependency-injection) ссылки на основной элемент DOM, элемент, к которому вы применяете `appHighlight`.

1.  Добавьте логику в класс `HighlightDirective`, которая устанавливает желтый фон.

    <code-example header="src/app/app/highlight.directive.ts" path="attribute-directives/src/app/highlight.directive.1.ts"></code-example>.

<div class="alert is-helpful">

Директивы _не_ поддерживают пространства имен.

<code-example header="src/app/app.component.avoid.html (unsupported)" path="attribute-directives/src/app/app.component.avoid.html" region="unsupported"></code-example>

</div>

<a id="apply-directive"></a>

## Применение директивы атрибута

1.  Чтобы использовать `HighlightDirective`, добавьте элемент `<p>` в HTML-шаблон с директивой в качестве атрибута.

    <code-example header="src/app/app.component.html" path="attribute-directives/src/app/app/app.component.1.html" region="applied"></code-example>.

Angular создает экземпляр класса `HighlightDirective` и вставляет ссылку на элемент `<p>` в конструктор директивы, который устанавливает стиль фона элемента `<p>` на желтый.

<a id="respond-to-user"></a>

## Обработка событий пользователя

В этом разделе показано, как определить, когда пользователь наводит мышь на элемент или выходит из него, и отреагировать, установив или убрав цвет подсветки.

1.  Импортируйте `HostListener` из '@angular/core'.

    <code-example header="src/app/highlight.directive.ts (imports)" path="attribute-directives/src/app/highlight.directive.2.ts" region="imports"></code-example>.

1.  Добавьте два обработчика событий, которые реагируют, когда мышь входит или выходит, каждый с декоратором `@HostListener()`.

    <code-example header="src/app/highlight.directive.ts (mouse-methods)" path="attribute-directives/src/app/highlight.directive.2.ts" region="mouse-methods"></code-example>.

Подписка на события элемента DOM, в котором размещена директива атрибутов, в данном случае `<p>`, с помощью декоратора `@HostListener()`.

<div class="alert is-helpful">

Обработчики делегируют вспомогательному методу `highlight()`, который устанавливает цвет для основного элемента DOM, `el`.

</div>

Полная директива выглядит следующим образом:

<code-example header="src/app/highlight.directive.ts" path="attribute-directives/src/app/highlight.directive.2.ts"></code-example>

Цвет фона появляется при наведении указателя на элемент абзаца и исчезает при перемещении указателя.

<div class="lightbox">

<img alt="Second Highlight" src="generated/images/guide/attribute-directives/highlight-directive-anim.gif">

</div>

<a id="bindings"></a>

## Передача значений в директиву атрибутов

В этом разделе мы рассмотрим установку цвета подсветки при применении директивы `HighlightDirective`.

1.  В `highlight.directive.ts` импортируйте `Input` из `@angular/core`.

    <code-example header="src/app/highlight.directive.ts (imports)" path="attribute-directives/src/app/highlight.directive.3.ts" region="imports"></code-example>.

1.  Добавьте свойство `appHighlight` `@Input()`.

    <code-example header="src/app/app/highlight.directive.ts" path="attribute-directives/src/app/highlight.directive.3.ts" region="input"></code-example>.

    Декоратор `@Input()` добавляет метаданные к классу, которые делают свойство директивы `appHighlight` доступным для привязки.

1.  В `app.component.ts` добавьте свойство `color` к `AppComponent`.

    <code-example header="src/app/app.component.ts (class)" path="attribute-directives/src/app/app/app.component.1.ts" region="class"></code-example>.

1.  Чтобы одновременно применить директиву и цвет, используйте связывание свойств с селектором директивы `appHighlight`, установив его равным `color`.

    <code-example header="src/app/app.component.html (color)" path="attribute-directives/src/app/app/app.component.html" region="color"></code-example>.

    Привязка атрибута `[appHighlight]` выполняет две задачи:

    -   Применяет директиву подсветки к элементу `<p>`.

    -   Устанавливает цвет выделения директивы с помощью привязки свойства.

### Установка значения с помощью пользовательского ввода

Этот раздел поможет вам добавить радиокнопки для привязки выбора цвета к директиве `appHighlight`.

1.  Add markup to `app.component.html` for choosing a color as follows:

    <code-example header="src/app/app.component.html (v2)" path="attribute-directives/src/app/app.component.html" region="v2"></code-example>

1.  Revise the `AppComponent.color` so that it has no initial value.

    <code-example header="src/app/app.component.ts (class)" path="attribute-directives/src/app/app.component.ts" region="class"></code-example>

1.  In `highlight.directive.ts`, revise `onMouseEnter` method so that it first tries to highlight with `appHighlight` and falls back to `red` if `appHighlight` is `undefined`.

    <code-example header="src/app/highlight.directive.ts (mouse-enter)" path="attribute-directives/src/app/highlight.directive.3.ts" region="mouse-enter"></code-example>

1.  Serve your application to verify that the user can choose the color with the radio buttons.

    <div class="lightbox">

    <img alt="Animated gif of the refactored highlight directive changing color according to the radio button the user selects" src="generated/images/guide/attribute-directives/highlight-directive-v2-anim.gif">

    </div>

<a id="second-property"></a>

## Привязка ко второму свойству

Этот раздел поможет вам настроить приложение так, чтобы разработчик мог установить цвет по умолчанию.

1.  Добавьте второе свойство `Input()` в `HighlightDirective` под названием `defaultColor`.

    <code-example header="src/app/highlight.directive.ts (defaultColor)" path="attribute-directives/src/app/highlight.directive.ts" region="defaultColor"></code-example>.

1.  Пересмотрите директиву `onMouseEnter` так, чтобы она сначала пыталась выделить с помощью `appHighlight`, затем с помощью `defaultColor`, и возвращалась к `red`, если оба свойства `не определены`.

    <code-example header="src/app/highlight.directive.ts (mouse-enter)" path="attribute-directives/src/app/highlight.directive.ts" region="mouse-enter"></code-example>

1.  Чтобы привязать к `AppComponent.color` и вернуться к "фиолетовому" цвету по умолчанию, добавьте следующий HTML.

    В этом случае для привязки `defaultColor` не используются квадратные скобки, `[]`, поскольку она статична.

    <code-example header="src/app/app.component.html (defaultColor)" path="attribute-directives/src/app/app/app.component.html" region="defaultColor"></code-example>.

    Как и в случае с компонентами, вы можете добавить несколько привязок свойств директив к элементу host.

Если нет привязки цвета по умолчанию, то цвет по умолчанию красный. Когда пользователь выбирает цвет, выбранный цвет становится активным цветом подсветки.

<div class="lightbox">

<img alt="Animated gif of final highlight directive that shows red color with no binding and violet with the default color set. When user selects color, the selection takes precedence." src="generated/images/guide/attribute-directives/highlight-directive-final-anim.gif">

</div>

<a id="ngNonBindable"></a>

## Деактивация обработки Angular с помощью `NgNonBindable`.

Чтобы предотвратить оценку выражения в браузере, добавьте `ngNonBindable` к элементу host. `ngNonBindable` деактивирует интерполяцию, директивы и привязку в шаблонах.

В следующем примере выражение `{{ 1 + 1 }}` отображается так же, как и в вашем редакторе кода, и не отображает `2`.

<code-example header="src/app/app.component.html" linenums="false" path="attribute-directives/src/app/app/app.component.html" region="ngNonBindable"></code-example>.

Применение `ngNonBindable` к элементу останавливает привязку для дочерних элементов этого элемента. Однако `ngNonBindable` по-прежнему позволяет директивам работать с элементом, к которому вы применили `ngNonBindable`.

В следующем примере директива `appHighlight` все еще активна, но Angular не оценивает выражение `{{ 1 + 1 }}}`.

<code-example header="src/app/app.component.html" linenums="false" path="attribute-directives/src/app/app/app.component.html" region="ngNonBindable-with-directive"></code-example>.

Если вы примените `ngNonBindable` к родительскому элементу, Angular отключит интерполяцию и привязку любого рода, такую как привязка свойств или привязка событий, для дочерних элементов.

<!-- links -->

<!-- external links -->

<!-- end links -->

@ просмотрено 2022-02-28
