# Введение в анимацию Angular

Анимация создает иллюзию движения: Элементы HTML меняют стиль с течением времени. Хорошо продуманные анимации могут сделать ваше приложение более интересным и простым в использовании, но они не только косметические.

Анимация может улучшить работу приложения и пользовательский опыт несколькими способами:

-   Без анимации переходы между веб-страницами могут казаться резкими и отрывистыми.

-   Движение значительно улучшает пользовательский опыт, поэтому анимация дает пользователям возможность определить реакцию приложения на их действия

-   Хорошая анимация интуитивно привлекает внимание пользователя к тому, что ему необходимо.

Как правило, анимация включает в себя несколько стилевых _преобразований_ во времени. Элемент HTML может перемещаться, менять цвет, увеличиваться или уменьшаться, исчезать или соскальзывать со страницы.

Эти изменения могут происходить одновременно или последовательно. Вы можете контролировать время каждого преобразования.

Система анимации Angular построена на функциональности CSS, что означает, что вы можете анимировать любое свойство, которое браузер считает анимируемым. Сюда входят позиции, размеры, трансформации, цвета, границы и многое другое.

W3C поддерживает список анимируемых свойств на своей странице [CSS Transitions](https://www.w3.org/TR/css-transitions-1).

## Об этом руководстве

В этом руководстве рассматриваются основные возможности анимации Angular, чтобы вы могли начать добавлять анимацию Angular в свой проект.

Функции, описанные в этом руководстве &mdash; и более продвинутые функции, описанные в соответствующих руководствах по анимации Angular&mdash; демонстрируются в примере приложения, доступном как <live-example></live-example>.

## Предварительные условия

Руководство предполагает, что вы знакомы с созданием базовых приложений Angular, как описано в следующих разделах:

-   [Учебник](tutorial)

-   [Обзор архитектуры](руководство/архитектура)

## Начало работы

Основными модулями Angular для анимации являются `@angular/animations` и `@angular/platform-browser`. Когда вы создаете новый проект с помощью CLI, эти зависимости автоматически добавляются в ваш проект.

Чтобы начать добавлять анимации Angular в свой проект, импортируйте модули, специфичные для анимации, вместе со стандартной функциональностью Angular.

### Шаг 1: Включение модуля анимации

Импортируйте `BrowserAnimationsModule`, который внедряет возможности анимации в ваш корневой модуль приложения Angular.

<code-example header="src/app/app.module.ts" path="animations/src/app/app.module.1.ts"></code-example>

<div class="alert is-helpful">

**NOTE**: <br /> When you use the CLI to create your app, the root application module `app.module.ts` is placed in the `src/app` folder.

</div>

### Шаг 2: Импорт функций анимации в файлы компонентов

Если вы планируете использовать определенные функции анимации в файлах компонентов, импортируйте эти функции из `@angular/animations`.

<code-example header="src/app/app.component.ts" path="animations/src/app/app/app.component.ts" region="imports"></code-example>

<div class="alert is-helpful">

**NOTE**: <br /> See a [summary of available animation functions](guide/animations#animation-api-summary) at the end of this guide.

</div>

### Шаг 3: Добавление свойства метаданных анимации

В файле компонента добавьте свойство метаданных `animations:` в декораторе `@Component()`. В свойство метаданных `animations` помещается триггер, определяющий анимацию.

<code-example header="src/app/app.component.ts" path="animations/src/app/app/app.component.ts" region="decorator"></code-example>.

## Анимация перехода

Давайте анимируем переход, который переводит один HTML-элемент из одного состояния в другое. Например, вы можете указать, что кнопка отображает либо **Открыто**, либо **Закрыто** в зависимости от последнего действия пользователя.

Когда кнопка находится в состоянии `открыто`, она видна и имеет желтый цвет.

Когда она находится в состоянии `закрыта`, она прозрачная и синяя.

В HTML эти атрибуты задаются с помощью обычных стилей CSS, таких как цвет и непрозрачность. В Angular используйте функцию `style()`, чтобы задать набор CSS-стилей для использования в анимации.

Соберите набор стилей в состояние анимации и дайте этому состоянию имя, например `открыто` или `закрыто`.

<div class="alert is-helpful">

Давайте создадим новый компонент `открыть-закрыть` для анимации с простыми переходами.

Выполните следующую команду в терминале, чтобы создать компонент:

<code-example format="shell" language="shell">

ng g компонент открыть-закрыть

</code-example>

Это создаст компонент в `src/app/open-close.component.ts`.

</div>

### Состояние и стили анимации

Используйте функцию Angular [`state()`](api/animations/state), чтобы определить различные состояния для вызова в конце каждого перехода. Эта функция принимает два аргумента:

Уникальное имя, например `открыто` или `закрыто`, и функцию `style()`.

Используйте функцию `style()` для определения набора стилей, которые будут ассоциироваться с данным именем состояния. Вы должны использовать [_camelCase_](guide/glossary#case-conventions) для атрибутов стиля, которые содержат тире, например `backgroundColor`, или обернуть их в кавычки, например `'background-color'`.

Давайте посмотрим, как функция Angular [`state()`](api/animations/state) работает с функцией `style()` для установки стилевых атрибутов CSS. В этом фрагменте кода для состояния одновременно устанавливается несколько атрибутов стиля.

В состоянии `открыто` кнопка имеет высоту 200 пикселей, непрозрачность 1 и желтый цвет фона.

<code-example header="src/app/open-close.component.ts" path="animations/src/app/open-close.component.ts" region="state1"></code-example>.

В следующем состоянии `closed` кнопка имеет высоту 100 пикселей, непрозрачность 0.8 и цвет фона синий.

<code-example header="src/app/open-close.component.ts" path="animations/src/app/open-close.component.ts" region="state2"></code-example>

### Переходы и синхронизация

В Angular вы можете установить несколько стилей без какой-либо анимации. Однако без дополнительной доработки кнопка мгновенно трансформируется без затухания, уменьшения или другого видимого индикатора того, что происходит изменение.

Чтобы сделать изменение менее резким, необходимо определить анимацию _transition_, чтобы указать изменения, которые происходят между одним состоянием и другим в течение определенного периода времени. Функция `transition()` принимает два аргумента:

Первый аргумент принимает выражение, определяющее направление между двумя состояниями перехода, а второй аргумент принимает один или серию шагов `animate()`.

Используйте функцию `animate()` для определения длины, задержки и смягчения перехода, а также для назначения функции style для определения стилей при переходе. Используйте функцию `animate()` для определения функции `keyframes()` для многошаговой анимации.

Эти определения помещаются во второй аргумент функции `animate()`.

#### Метаданные анимации: длительность, задержка и смягчение.

Функция `animate()` (второй аргумент функции перехода\) принимает входные параметры `timings` и `styles`.

Параметр `timings` принимает либо число, либо строку, состоящую из трех частей.

<code-example format="typescript" language="typescript">

одушевление (продолжительность)

</code-example>

или

<code-example format="typescript" language="typescript">

animate ('duration delay easing')

</code-example>

Первая часть, `duration`, является обязательной. Продолжительность может быть выражена в миллисекундах как число без кавычек или в секундах с кавычками и спецификатором времени.
Например, длительность в одну десятую секунды может быть выражена следующим образом:

-   В виде простого числа в миллисекундах:

    `100`

-   В строке, в миллисекундах:

    `100ms`.

-   В строке в виде секунд:

    `'0.1s'`

Второй аргумент, `delay`, имеет тот же синтаксис, что и `duration`. Например:

-   Подождать 100 мс, а затем выполнить 200 мс: `0.2s 100ms`.

Третий аргумент, `easing`, управляет тем, как анимация [ускоряется и замедляется](https://easings.net) во время выполнения. Например, `ease-in` заставляет анимацию начинаться медленно и набирать скорость по мере выполнения.

-   Подождите 100 мс, запустите 200 мс.

    Используйте кривую замедления, чтобы начать быстро и медленно замедляться до точки покоя:

    `0.2s 100ms ease-out`.

-   Запуск в течение 200 мс без задержки.

    Используйте стандартную кривую, чтобы начать медленно, ускориться в середине, а затем медленно замедлиться в конце:

    `0.2s ease-in-out`.

-   Запуск сразу, выполнение в течение 200 мс.

    Используйте кривую ускорения, чтобы начать медленно и закончить на полной скорости:

    `'0.2s ease-in'`.

<div class="alert is-helpful">

**NOTE**: <br /> See the Material Design website's topic on [Natural easing curves](https://material.io/design/motion/speed.html#easing) for general information on easing curves.

</div>

Этот пример обеспечивает переход из состояния `открыто` в `закрыто` с переходом между состояниями в течение 1 секунды.

<code-example header="src/app/open-close.component.ts" path="animations/src/app/open-close.component.ts" region="transition1"></code-example>.

В предыдущем фрагменте кода оператор `=>` обозначает однонаправленные переходы, а `<=>` - двунаправленные. Внутри перехода оператор `animate()` указывает, как долго длится переход.

В данном случае переход из состояния `открыто` в `закрыто` занимает 1 секунду, выраженную здесь как `1s`.

Этот пример добавляет переход состояния из состояния `закрыто` в состояние `открыто` с дугой анимации перехода 0,5 секунды.

<code-example header="src/app/open-close.component.ts" path="animations/src/app/open-close.component.ts" region="transition2"></code-example>

<div class="alert is-helpful">

**NOTE**: <br /> Some additional notes on using styles within [`state`](api/animations/state) and `transition` functions.

-   Use [`state()`](api/animations/state) to define styles that are applied at the end of each transition, they persist after the animation completes

-   Use `transition()` to define intermediate styles, which create the illusion of motion during the animation

-   When animations are disabled, `transition()` styles can be skipped, but [`state()`](api/animations/state) styles can't

-   Include multiple state pairs within the same `transition()` argument:

      <code-example format="typescript" language="typescript">

    transition( 'on =&gt; off, off =&gt; void' )

      </code-example>

</div>

### Запуск анимации

Анимация требует _триггера_, чтобы она знала, когда начинать. Функция `trigger()` собирает состояния и переходы и дает анимации имя, чтобы вы могли прикрепить его к запускающему элементу в шаблоне HTML.

Функция `trigger()` описывает имя свойства, которое нужно отслеживать на предмет изменений. Когда происходит изменение, триггер инициирует действия, указанные в его определении.

Эти действия могут быть переходами или другими функциями, как мы увидим позже.

В этом примере мы назовем триггер `openClose` и прикрепим его к элементу `button`. Триггер описывает открытое и закрытое состояния, а также тайминги для этих двух переходов.

<div class="alert is-helpful">

**NOTE**: <br /> Within each `trigger()` function call, an element can only be in one state at any given time.
However, it's possible for multiple triggers to be active at once.

</div>

### Определение анимаций и прикрепление их к шаблону HTML

Анимации определяются в метаданных компонента, который управляет анимируемым элементом HTML. Поместите код, определяющий анимацию, в свойство `animations:` в декораторе `@Component()`.

<code-example header="src/app/open-close.component.ts" path="animations/src/app/open-close.component.ts" region="component"></code-example>.

Когда вы определили триггер анимации для компонента, прикрепите его к элементу шаблона этого компонента, заключив имя триггера в скобки и предваряя его символом `@`. Затем вы можете привязать триггер к выражению шаблона, используя стандартный синтаксис привязки свойств Angular, как показано ниже, где `triggerName` - это имя триггера, а `expression` оценивает определенное состояние анимации.

<code-example format="typescript" language="typescript">

&lt;div [&commat;triggerName]="expression"&gt;&hellip;&lt;/div&gt;;

</code-example>

Анимация выполняется или запускается, когда значение выражения переходит в новое состояние.

Следующий фрагмент кода связывает триггер со значением свойства `isOpen`.

<code-example header="src/app/open-close.component.html" path="animations/src/app/open-close.component.1.html" region="trigger"></code-example>.

В этом примере, когда выражение `isOpen` оценивает определенное состояние `открыто` или `закрыто`, оно уведомляет триггер `openClose` об изменении состояния. Затем код `openClose` обрабатывает изменение состояния и запускает анимацию изменения состояния.

Для элементов, входящих или выходящих со страницы\(вставляемых или удаляемых из DOM\), вы можете сделать анимацию условной. Например, используйте `*ngIf` с триггером анимации в шаблоне HTML.

<div class="alert is-helpful">

**NOTE**: <br /> In the component file, set the trigger that defines the animations as the value of the `animations:` property in the `@Component()` decorator.

In the HTML template file, use the trigger name to attach the defined animations to the HTML element to be animated.

</div>

### Обзор кода

Вот файлы кода, рассмотренные в примере перехода.

<code-tabs> <code-pane header="src/app/open-close.component.ts" path="animations/src/app/open-close.component.ts" region="component"></code-pane>
<code-pane header="src/app/open-close.component.html" path="animations/src/app/open-close.component.1.html" region="trigger"></code-pane>
<code-pane header="src/app/open-close.component.css" path="animations/src/app/open-close.component.css"></code-pane>
</code-tabs>

### Резюме

Вы научились добавлять анимацию к переходу между двумя состояниями, используя `style()` и [`state()`](api/animations/state) вместе с `animate()` для синхронизации.

Узнайте о более продвинутых возможностях анимации в Angular в разделе Анимация, начиная с продвинутых техник в [transition and triggers](guide/transition-and-triggers).

<a id="animation-api-summary"></a>

## Краткое описание API анимации

Функциональный API, предоставляемый модулем `@angular/animations`, обеспечивает специфический язык \(DSL\) для создания и управления анимацией в приложениях Angular. Полный список и синтаксические подробности основных функций и связанных с ними структур данных см. в [API reference](api/animations).

| Function name | What it does | | :-------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `trigger()` | Kicks off the animation and serves as a container for all other animation function calls. HTML template binds to `triggerName`. Use the first argument to declare a unique trigger name. Uses array syntax. |
| `style()` | Defines one or more CSS styles to use in animations. Controls the visual appearance of HTML elements during animations. Uses object syntax. |
| [`state()`](api/animations/state) | Creates a named set of CSS styles that should be applied on successful transition to a given state. The state can then be referenced by name within other animation functions. |
| `animate()` | Specifies the timing information for a transition. Optional values for `delay` and `easing`. Can contain `style()` calls within. |
| `transition()` | Defines the animation sequence between two named states. Uses array syntax. |
| `keyframes()` | Allows a sequential change between styles within a specified time interval. Use within `animate()`. Can include multiple `style()` calls within each `keyframe()`. Uses array syntax. |
| [`group()`](api/animations/group) | Specifies a group of animation steps \(_inner animations_\) to be run in parallel. Animation continues only after all inner animation steps have completed. Used within `sequence()` or `transition()`. |
| `query()` | Finds one or more inner HTML elements within the current element. |
| `sequence()` | Specifies a list of animation steps that are run sequentially, one by one. |
| `stagger()` | Staggers the starting time for animations for multiple elements. |
| `animation()` | Produces a reusable animation that can be invoked from elsewhere. Used together with `useAnimation()`. |
| `useAnimation()` | Activates a reusable animation. Used with `animation()`. |
| `animateChild()` | Allows animations on child components to be run within the same timeframe as the parent. |

</table>

## Больше об анимации в Angular

Вам также может быть интересно следующее:

-   [Переходы и триггеры](guide/transition-and-triggers)

-   [Сложные анимационные последовательности](guide/complex-animation-sequences)

-   [Многоразовые анимации](guide/reusable-animations)

-   [Анимации перехода по маршруту](guide/route-animations)

<div class="alert is-helpful">

Посмотрите эту [презентацию](https://www.youtube.com/watch?v=rnTK9meY5us), показанную на конференции AngularConnect в ноябре 2017 года, и сопутствующий [исходный код](https://github.com/matsko/animationsftw.in).

</div>

<!-- links -->

<!-- external links -->

<!-- end links -->

:date: 28.02.2022
