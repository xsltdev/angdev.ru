# Understanding binding

In an Angular template, a binding creates a live connection between a part of the UI created from a template (a DOM element, directive, or component) and the model (the component instance to which the template belongs). This connection can be used to synchronize the view with the model, to notify the model when an event or user action takes place in the view, or both. Angular's [Change Detection](guide/change-detection) algorithm is responsible for keeping the view and the model in sync.

Examples of binding include:

-   text interpolations

-   property binding

-   event binding

-   two-way binding

Bindings always have two parts: a _target_ which will receive the bound value, and a _template expression_ which produces a value from the model.

## Syntax

Template expressions are similar to JavaScript expressions. Many JavaScript expressions are legal template expressions, with the following exceptions.

You can't use JavaScript expressions that have or promote side effects, including:

-   Assignments (`=`, `+=`, `-=`, `...`)

-   Operators such as `new`, `typeof`, or `instanceof`

-   Chaining expressions with <code>;</code> or <code>,</code>

-   Операторы инкремента и декремента `++` и `--`

-   Некоторые операторы ES2015+

Другие заметные отличия от синтаксиса JavaScript включают:

-   Отсутствие поддержки побитовых операторов, таких как `|` и `&`.

-   Новые [операторы шаблонных выражений](guide/template-expression-operators), такие как `|`.

## Контекст выражения

Интерполированные выражения имеют контекст &mdash; определенную часть приложения, к которой принадлежит выражение. Обычно таким контекстом является экземпляр компонента.

В следующем фрагменте выражение `recommended` и выражение `itemImageUrl2` относятся к свойствам `AppComponent`.

<code-example path="interpolation/src/app/app.component.html" region="component-context" header="src/app/app.component.html"></code-example>.

Выражение также может ссылаться на свойства контекста \_шаблона, такие как [входная переменная шаблона](guide/structural-directives#shorthand) или [переменная ссылки шаблона](guide/template-reference-variables).

В следующем примере используется входная переменная шаблона `customer`.

<code-example path="interpolation/src/app/app.component.html" region="template-input-variable" header="src/app/app.component.html (template input variable)"></code-example>

This next example features a template reference variable, `#customerInput`.

<code-example path="interpolation/src/app/app.component.html" region="template-reference-variable" header="src/app/app.component.html (template reference variable)"></code-example>

<div class="alert is-helpful">

Шаблонные выражения не могут ссылаться ни на что в глобальном пространстве имен, кроме `undefined`. Они не могут ссылаться на `window` или `document`. Кроме того, они не могут вызывать `console.log()` или `Math.max()` и ограничены ссылками на члены контекста выражения.

</div>

### Предотвращение столкновений имен

Контекст, по которому оценивается выражение, представляет собой объединение переменных шаблона, контекстного объекта директивы &mdash; если он есть&mdash; и членов компонента. Если вы ссылаетесь на имя, принадлежащее более чем одному из этих пространств имен, Angular применяет следующую логику старшинства для определения контекста:

1. Имя переменной шаблона.

1. Имя в контексте директивы.

1. Имена членов компонента.

Чтобы переменные не затеняли переменные в другом контексте, сохраняйте уникальность имен переменных. В следующем примере шаблон `AppComponent` приветствует `клиента`, Падму.

Затем `ngFor` перечисляет каждого `клиента` в массиве `customers`.

<code-example path="interpolation/src/app/app.component.1.ts" region="var-collision" header="src/app/app.component.ts"></code-example>.

Клиент `customer` в `ngFor` находится в контексте `<ng-template>` и поэтому ссылается на клиента `customer` в массиве `customers`, в данном случае Ebony и Chiho. В этом списке нет Падмы, потому что `customer` вне `ngFor` находится в другом контексте.

И наоборот, `customer` в `<h1>` не включает Ebony или Chiho, потому что контекстом для этого `customer` является класс, а значением класса для `customer` является Padma.

## Лучшие практики использования выражений

При использовании шаблонного выражения следуйте следующим рекомендациям:

-   **Используйте короткие выражения**.

Используйте имена свойств или вызовы методов, когда это возможно. Храните прикладную и бизнес-логику в компоненте, где она доступна для разработки и тестирования.

-   **Быстрое выполнение**.

Angular выполняет выражение шаблона после каждого цикла [обнаружения изменений](guide/glossary#change-detection). Многие асинхронные действия вызывают циклы обнаружения изменений, такие как выполнение обещаний, результаты HTTP, события таймера, нажатия клавиш и перемещения мыши.

Выражение должно завершаться быстро, чтобы обеспечить максимальную эффективность работы пользователя, особенно на медленных устройствах. Рассмотрите возможность кэширования значений, если их вычисление требует больших ресурсов.

## Отсутствие видимых побочных эффектов

Согласно [однонаправленной модели потока данных Angular] (guide/glossary#unidirectional-data-flow), выражение шаблона не должно изменять состояние приложения, кроме значения целевого свойства. Чтение значения компонента не должно изменять какое-либо другое отображаемое значение. Представление должно быть стабильным в течение одного прохода рендеринга.

  <div class="callout is-important">
     <header>Idempotent expressions reduce side effects</header>

Выражение [idempotent](https://en.wikipedia.org/wiki/Idempotence) не имеет побочных эффектов и улучшает производительность обнаружения изменений в Angular. В терминах Angular, идемпотентное выражение всегда возвращает _совершенно одно и то же_, пока одно из его зависимых значений не изменится.

Зависимые значения не должны меняться в течение одного оборота цикла событий. Если идемпотентное выражение возвращает строку или число, оно возвращает ту же строку или число, если вы вызываете его дважды подряд. Если выражение возвращает объект, включая `массив`, оно возвращает один и тот же объект _ссылка_, если вы вызываете его дважды подряд.

  </div>

## Что дальше

-   [Привязка свойств](руководство/привязка свойств)

-   [Связывание событий](guide/event-binding)

:date: 12.05.2022
