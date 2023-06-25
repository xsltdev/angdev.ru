# Переходы и триггеры анимации

В этом руководстве подробно рассматриваются специальные состояния перехода, такие как `*` подстановочный знак и `void`. В нем показано, как эти специальные состояния используются для элементов, входящих и выходящих из представления. В этом разделе также рассматриваются триггеры анимации, обратные вызовы анимации и анимация на основе последовательности с использованием ключевых кадров.

## Предопределенные состояния и сопоставление подстановочных знаков

В Angular состояния перехода могут быть определены явно через функцию [`state()`](api/animations/state) или с помощью предопределенных `*` подстановочных знаков и `void` состояний.

### Состояние подстановочного знака

Звездочка `*` или _wildcard_ соответствует любому состоянию анимации. Это полезно для определения переходов, которые применяются независимо от начального или конечного состояния HTML-элемента.

Например, переход `open => *` применяется, когда состояние элемента меняется с открытого на любое другое.

<div class="lightbox">

<img alt="wildcard state expressions" src="generated/images/guide/animations/wildcard-state-500.png">

</div>

Ниже приведен еще один пример кода, использующий состояние с подстановочным знаком вместе с предыдущим примером, использующим состояния `открыто` и `закрыто`. Вместо определения каждой пары переходов из состояния в состояние, любой переход в `закрытое` занимает 1 секунду, а любой переход в `открытое` - 0,5 секунды.

Это позволяет добавлять новые состояния без необходимости включать отдельные переходы для каждого из них.

<code-example header="src/app/open-close.component.ts" path="animations/src/app/open-close.component.ts" region="trigger-wildcard1"></code-example>.

Используйте синтаксис двойной стрелки для указания переходов из состояния в состояние в обоих направлениях.

<code-example header="src/app/open-close.component.ts" path="animations/src/app/open-close.component.ts" region="trigger-wildcard2"></code-example>.

### Использование состояния подстановочного знака с несколькими состояниями перехода

В примере с кнопкой с двумя состояниями подстановочный знак не так полезен, потому что есть только два возможных состояния, `открыто` и `закрыто`. В целом, используйте подстановочный знак состояния, когда элемент имеет несколько потенциальных состояний, в которые он может перейти.

Если кнопка может переходить из состояния `открыто` в состояние `закрыто` или что-то вроде `в процессе`, использование подстановочного знака может сократить объем необходимой кодировки.

<div class="lightbox">

<img alt="wildcard state with 3 states" src="generated/images/guide/animations/wildcard-3-states.png">

</div>

<code-example header="src/app/open-close.component.ts" path="animations/src/app/open-close.component.ts" region="trigger-transition"></code-example>.

Переход `* => *` применяется, когда происходит изменение между двумя состояниями.

Переходы сопоставляются в том порядке, в котором они определены. Таким образом, вы можете применять другие переходы поверх перехода `* => *`.

Например, определите изменения стиля или анимации, которые будут применяться только к `открыто => закрыто`, а затем используйте `* => *` в качестве запасного варианта для пар состояний, которые иначе не называются.

Для этого перечислите более конкретные переходы _перед_ `* => *`.

### Использовать подстановочные знаки в стилях

Используйте подстановочный знак `*` со стилем, чтобы указать анимации использовать любое текущее значение стиля и анимировать в соответствии с ним. Wildcard - это запасное значение, которое используется, если анимируемое состояние не объявлено в триггере.

<code-example header="src/app/open-close.component.ts" path="animations/src/app/open-close.component.ts" region="transition4"></code-example>

### Состояние пустоты

Используйте состояние `void` для настройки переходов для элемента, который входит или выходит со страницы. Смотрите [Анимация входа и выхода из представления](#enter-leave-view).

### Объединить состояния подстановочного знака и пустоты

Комбинируйте состояния wildcard и void в переходе, чтобы вызвать анимацию входа и выхода со страницы:

-   Переход `* => void` применяется, когда элемент покидает представление, независимо от того, в каком состоянии он находился до выхода.

-   Переход `void => *` применяется, когда элемент входит в представление, независимо от того, в каком состоянии он находится при входе.

-   Подстановочный знак состояния `*` соответствует _любому_ состоянию, включая `void`.

## Анимация входа и выхода из представления

В этом разделе показано, как анимировать элементы, входящие или выходящие со страницы.

Добавьте новое поведение:

-   Когда вы добавляете героя в список героев, он влетает на страницу слева.

-   Когда вы удаляете героя из списка, он вылетает справа.

<code-example header="src/app/hero-list-enter-leave.component.ts" path="animations/src/app/hero-list-enter-leave.component.ts" region="animationdef"></code-example>.

В предыдущем коде вы применили состояние `void`, когда HTML-элемент не прикреплен к представлению.

<a id="enter-leave-view"></a>

## Псевдонимы :enter и :leave

`:enter` и `:leave` являются псевдонимами для переходов `void => *` и `* => void`. Эти псевдонимы используются несколькими функциями анимации.

<code-example hideCopy language="typescript">

transition ( ':enter', [ &hellip; ] ); // псевдоним для void =&gt; \* transition ( ':leave', [ &hellip; ] ); // псевдоним для \* =&gt; void

</code-example>

Сложнее нацелиться на элемент, который входит в представление, поскольку он еще не находится в DOM. Используйте псевдонимы `:enter` и `:leave` для адресации HTML-элементов, которые вставляются или удаляются из представления.

### Используйте `*ngIf` и `*ngFor` с :enter и :leave

Переход `:enter` выполняется, когда на странице размещаются любые представления `*ngIf` или `*ngFor`, а `:leave` выполняется, когда эти представления удаляются со страницы.

<div class="alert is-important">

**NOTE**: <br /> Entering/leaving behaviors can sometime be confusing.
As a rule of thumb consider that any element being added to the DOM by Angular passes via the `:enter` transition. Only elements being directly removed from the DOM by Angular pass via the `:leave` transition. For example, an element's view is removed from the DOM because its parent is being removed from the DOM.

</div>

В этом примере есть специальный триггер для анимации входа и выхода под названием `myInsertRemoveTrigger`. HTML-шаблон содержит следующий код.

<code-example header="src/app/insert-remove.component.html" path="animations/src/app/insert-remove.component.html" region="insert-remove"></code-example>.

В файле компонента переход `:enter` устанавливает начальную непрозрачность 0. Затем он анимируется, чтобы изменить эту непрозрачность на 1, когда элемент вставляется в представление.

<code-example header="src/app/insert-remove.component.ts" path="animations/src/app/insert-remove.component.ts" region="enter-leave-trigger"></code-example>.

Обратите внимание, что в этом примере не нужно использовать [`state()`](api/animations/state).

## Переход :increment и :decrement

Функция `transition()` принимает другие значения селектора, `:increment` и `:decrement`. Используйте их для запуска перехода, когда числовое значение увеличивается или уменьшается.

<div class="alert is-helpful">

**NOTE**: <br /> The following example uses `query()` and `stagger()` methods.
For more information on these methods, see the [complex sequences](guide/complex-animation-sequences#complex-sequence) page.

</div>

<code-example header="src/app/hero-list-page.component.ts" path="animations/src/app/hero-list-page.component.ts" region="increment"></code-example>.

## Булевы значения в переходах

Если триггер содержит булево значение в качестве значения привязки, то это значение может быть сопоставлено с помощью выражения `transition()`, которое сравнивает `true` и `false`, или `1` и `0`.

<code-example header="src/app/open-close.component.html" path="animations/src/app/open-close.component.2.html" region="trigger-boolean"></code-example>

In the code snippet above, the HTML template binds a `<div>` element to a trigger named `openClose` with a status expression of `isOpen`, and with possible values of `true` and `false`. This pattern is an alternative to the practice of creating two named states like `open` and `close`.

Inside the `@Component` metadata under the `animations:` property, when the state evaluates to `true`, the associated HTML element's height is a wildcard style or default. In this case, the animation uses whatever height the element already had before the animation started.

When the element is `closed`, the element gets animated to a height of 0, which makes it invisible.

<code-example header="src/app/open-close.component.ts" path="animations/src/app/open-close.component.2.ts" region="trigger-boolean"></code-example>.

## Несколько триггеров анимации

Вы можете определить более одного триггера анимации для компонента. Прикрепите триггеры анимации к разным элементам, и отношения "родитель-потомок" между элементами будут влиять на то, как и когда запускается анимация.

### Анимация родительского и дочернего элементов

При каждом запуске анимации в Angular родительская анимация всегда получает приоритет, а дочерние анимации блокируются. Чтобы запустить дочернюю анимацию, родительская анимация должна запросить каждый из элементов, содержащих дочерние анимации. Затем она разрешает запуск анимации с помощью функции [`animateChild()`](api/animations/animateChild).

#### Отключение анимации на элементе HTML

Специальная привязка управления анимацией `@.disabled` может быть размещена на элементе HTML для отключения анимации на этом элементе, а также на любых вложенных элементах. При значении true привязка `@.disabled` предотвращает отрисовку всех анимаций.

Следующий пример кода показывает, как использовать эту функцию.

<code-tabs> <code-pane header="src/app/open-close.component.html" path="animations/src/app/open-close.component.4.html" region="toggle-animation"></code-pane>
<code-pane header="src/app/open-close.component.ts" path="animations/src/app/open-close.component.4.ts" region="toggle-animation" language="typescript"></code-pane>
</code-tabs>

Когда привязка `@.disabled` истинна, триггер `@childAnimation` не срабатывает.

Когда у элемента в HTML-шаблоне отключена анимация с помощью привязки `@.disabled`, анимация отключается и у всех внутренних элементов. Вы не можете выборочно отключить несколько анимаций на одном элементе.<!-- vale off -->.

Выборочная дочерняя анимация все еще может быть запущена на отключенном родительском элементе одним из следующих способов:

-   Родительская анимация может использовать функцию [`query()`](api/animations/query) для сбора внутренних элементов, расположенных в отключенных областях шаблона HTML.

Эти элементы все равно могут анимироваться.

<!-- vale on -->

-   Дочерняя анимация может быть запрошена родительской, а затем анимирована с помощью функции `animateChild()`.

#### Отключить все анимации

Чтобы отключить все анимации в приложении Angular, поместите привязку хоста `@.disabled` на самый верхний компонент Angular.

<code-example header="src/app/app.component.ts" path="animations/src/app/app.component.ts" region="toggle-app-animations"></code-example>

<div class="alert is-helpful">

**NOTE**: <br /> Disabling animations application-wide is useful during end-to-end \(E2E\) testing.

</div>

## Обратные вызовы анимации

Функция анимации `trigger()` испускает _обратные вызовы_, когда она начинается и когда она завершается. В следующем примере представлен компонент, содержащий триггер `openClose`.

<code-example header="src/app/open-close.component.ts" path="animations/src/app/open-close.component.ts" region="events1"></code-example>.

В шаблоне HTML событие анимации передается обратно через `$event`, как `@triggerName.start` и `@triggerName.done`, где `triggerName` - имя используемого триггера. В данном примере триггер `openClose` выглядит следующим образом.

<code-example header="src/app/open-close.component.html" path="animations/src/app/open-close.component.3.html" region="callbacks"></code-example>.

Потенциальное использование обратных вызовов анимации может быть связано с медленным вызовом API, таким как поиск в базе данных. Например, кнопка **InProgress** может быть настроена на зацикленную анимацию, пока завершается работа внутренней системы.

По завершении текущей анимации можно вызвать другую анимацию. Например, кнопка переходит из состояния `в процессе` в состояние `закрыто`, когда вызов API завершен.

Анимация может повлиять на конечного пользователя, чтобы он _воспринимал_ операцию как более быструю, даже если это не так.

Обратные вызовы могут служить в качестве инструмента отладки, например, в сочетании с `console.warn()` для просмотра хода выполнения приложения в JavaScript-консоли разработчика браузера. Следующий фрагмент кода создает вывод журнала консоли для исходного примера - кнопки с двумя состояниями `открыто` и `закрыто`.

<code-example header="src/app/open-close.component.ts" path="animations/src/app/open-close.component.ts" region="events"></code-example>

<a id="keyframes"></a>

## Ключевые кадры

Чтобы создать анимацию с несколькими последовательно выполняемыми шагами, используйте _ключевые кадры_.

Функция Angular `keyframe()` позволяет изменять несколько стилей в пределах одного временного сегмента. Например, кнопка, вместо того чтобы исчезать, может менять цвет несколько раз в течение одного 2-секундного отрезка времени.

<div class="lightbox">

<img alt="keyframes" src="generated/images/guide/animations/keyframes-500.png">

</div>

Код для этого изменения цвета может выглядеть следующим образом.

<code-example header="src/app/status-slider.component.ts" path="animations/src/app/status-slider.component.ts" region="keyframes"></code-example>

### Смещение

Ключевые кадры включают `смещение`, которое определяет точку в анимации, где происходит каждое изменение стиля. Смещение - это относительная величина от нуля до единицы, обозначающая начало и конец анимации. Они должны применяться к каждому из ключевых кадров, если используются хотя бы один раз.

Определение смещений для ключевых кадров необязательно. Если вы их не зададите, то равномерно расположенные смещения будут назначены автоматически.

Например, три ключевых кадра без заданных смещений получают смещения 0, 0,5 и 1.

Указание смещения 0,8 для среднего перехода в предыдущем примере может выглядеть следующим образом.

<div class="lightbox">

<img alt="keyframes with offset" src="generated/images/guide/animations/keyframes-offset-500.png">

</div>

Код с указанными смещениями будет выглядеть следующим образом.

<code-example header="src/app/status-slider.component.ts" path="animations/src/app/status-slider.component.ts" region="keyframesWithOffsets"></code-example>.

Вы можете комбинировать ключевые кадры с `длительностью`, `задержкой` и `сглаживанием` в рамках одной анимации.

### Ключевые кадры с пульсацией

Используйте ключевые кадры для создания эффекта пульсации в анимации, определяя стили с определенным смещением на протяжении всей анимации.

Вот пример использования ключевых кадров для создания эффекта пульсации:

-   Исходные состояния `открыто` и `закрыто` с оригинальными изменениями высоты, цвета и непрозрачности, происходящими в течение 1 секунды.

-   Последовательность ключевых кадров, вставленная в середине, которая заставляет кнопку пульсировать неравномерно в течение того же 1 секунды.

<div class="lightbox">

<img alt="keyframes with irregular pulsation" src="generated/images/guide/animations/keyframes-pulsation.png">

</div>

Фрагмент кода для этой анимации может выглядеть следующим образом.

<code-example header="src/app/open-close.component.ts" path="animations/src/app/open-close.component.1.ts" region="trigger"></code-example>.

### Анимируемые свойства и единицы

Поддержка анимации в Angular основана на веб-анимации, поэтому вы можете анимировать любое свойство, которое браузер считает анимируемым. Сюда входят позиции, размеры, трансформации, цвета, границы и многое другое.

W3C поддерживает список анимируемых свойств на странице [CSS Transitions](https://www.w3.org/TR/css-transitions-1).

Для свойств с числовым значением определите единицу измерения, указав значение в виде строки в кавычках с соответствующим суффиксом:

-   50 пикселей:

    `'50px'`.

-   Относительный размер шрифта:

    `3em`.

-   Процент:

    `'100%'`

Вы также можете указать значение в виде числа. В таких случаях Angular принимает единицу измерения по умолчанию - пиксели, или `px`. Выразить 50 пикселей как `50` - то же самое, что сказать `'50px'`.

<div class="alert is-helpful">

**NOTE**: <br /> The string `"50"` would instead not be considered valid\).

</div>

### Автоматическое вычисление свойств с помощью подстановочных знаков

Иногда значение свойства размерного стиля не известно до момента выполнения. Например, элементы часто имеют ширину и высоту, которые зависят от их содержимого или размера экрана.

Эти свойства часто сложно анимировать с помощью CSS.

В таких случаях можно использовать специальный подстановочный знак `*` в свойстве `style()`. Значение этого конкретного свойства стиля вычисляется во время выполнения и затем вставляется в анимацию.

В следующем примере есть триггер `shrinkOut`, который используется, когда элемент HTML покидает страницу. Анимация берет высоту элемента перед его уходом и анимируется от этой высоты до нуля.

<code-example header="src/app/hero-list-auto.component.ts" path="animations/src/app/hero-list-auto.component.ts" region="auto-calc"></code-example>

### Краткое описание ключевых кадров

Функция `keyframes()` в Angular позволяет задать несколько промежуточных стилей в рамках одного перехода. Необязательное `смещение` может быть использовано для определения точки в анимации, в которой должно произойти изменение каждого стиля.

## Подробнее об анимации в Angular

Вам также может быть интересно следующее:

-   [Введение в анимации Angular](руководство/анимации)

-   [Сложные анимационные последовательности](guide/complex-animation-sequences)

-   [Многоразовые анимации](руководство/reusable-animations)

-   [Анимации перехода по маршруту](guide/route-animations)

:date: 11.10.2022
