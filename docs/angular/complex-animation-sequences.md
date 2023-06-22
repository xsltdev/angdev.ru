# Сложные анимационные последовательности

## Необходимые условия

Базовое понимание следующих концепций:

-   [Введение в анимации Angular](руководство/анимации)

-   [Переход и триггеры](guide/transition-and-triggers)

До сих пор мы изучали простые анимации отдельных элементов HTML. Angular также позволяет анимировать согласованные последовательности, например, всю сетку или список элементов, когда они входят и выходят со страницы.

Вы можете выбрать параллельный запуск нескольких анимаций или последовательный запуск отдельных анимаций, следующих одна за другой.

Функции, управляющие сложными анимационными последовательностями, следующие:

| Функции | Подробности | | :-------------------------------- | :------------------------------------------------------------- |.

| `query()` | Находит один или несколько внутренних элементов HTML. |

| `stagger()` | Применяет каскадную задержку к анимации для нескольких элементов. |

| [`group()`](api/animations/group) | Запускает несколько шагов анимации параллельно. |

| `sequence()` | Запускает шаги анимации один за другим. |

<a id="complex-sequence"></a>

## The query() function

Most complex animations rely on the `query()` function to find child elements and apply animations to them, basic examples of such are:

| Examples | Details | | :------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

| `query()` followed by `animate()` | Used to query simple HTML elements and directly apply animations to them. |

| `query()` followed by `animateChild()` | Used to query child elements, which themselves have animations metadata applied to them and trigger such animation \(which would be otherwise be blocked by the current/parent element's animation\). |

The first argument of `query()` is a [css selector](https://developer.mozilla.org/docs/Web/CSS/CSS_Selectors) string which can also contain the following Angular-specific tokens:

| Tokens | Details | | :------------------------- | :------------------------------------------- |

| `:enter` <br /> `:leave` | For entering/leaving elements. |

| `:animating` | For elements currently animating. |

| `@*` <br /> `@triggerName` | For elements with any—or a specific—trigger. |

| `:self` | The animating element itself. |

<div class="callout is-helpful">

<header>Entering and Leaving Elements</header>

Не все дочерние элементы на самом деле считаются входящими/выходящими; иногда это может быть нелогичным и запутанным. Пожалуйста, смотрите [query api docs](api/animations/query#entering-and-leaving-elements) для получения дополнительной информации.

Вы также можете увидеть иллюстрацию этого в живом примере анимации \(представленном в разделе анимации [введение](guide/animations#about-this-guide)\) на вкладке Querying.

</div>

## Анимация нескольких элементов с помощью функций query() и stagger()

После запроса дочерних элементов с помощью функции `query()`, функция `stagger()` позволяет определить временной промежуток между каждым анимируемым элементом и, таким образом, анимировать элементы с задержкой между ними.

Следующий пример демонстрирует, как использовать функции `query()` и `stagger()` для анимации списка \(героев\), добавляя каждый из них последовательно, с небольшой задержкой, сверху вниз.

-   Используйте функцию `query()` для поиска элемента на странице, который соответствует определенным критериям.

-   Для каждого из этих элементов используйте `style()`, чтобы установить одинаковый начальный стиль для элемента.

    Сделайте его прозрачным и с помощью `transform` переместите его из позиции в позицию, чтобы он мог встать на место.

-   Используйте `stagger()` для задержки каждой анимации на 30 миллисекунд.

-   Анимируйте каждый элемент на экране в течение 0,5 секунды, используя заданную кривую смягчения, одновременно затухая и разворачиваясь.

<code-example header="src/app/hero-list-page.component.ts" path="animations/src/app/hero-list-page.component.ts" region="page-animations"></code-example>.

## Параллельная анимация с помощью функции group()

Вы видели, как добавить задержку между каждой последующей анимацией. Но вы также можете захотеть настроить анимацию, которая будет происходить параллельно.

Например, вы можете захотеть анимировать два CSS-свойства одного и того же элемента, но использовать для каждого из них свою функцию `сглаживания`.

Для этого можно использовать функцию animation [`group()`](api/animations/group).

<div class="alert is-helpful">

**NOTE**: <br /> The [`group()`](api/animations/group) function is used to group animation _steps_, rather than animated elements.

</div>

Следующий пример использует [`group()`](api/animations/group)s на `:enter` и `:leave` для двух различных временных конфигураций, таким образом применяя две независимые анимации к одному и тому же элементу параллельно.

<code-example header="src/app/hero-list-groups.component.ts (excerpt)" path="animations/src/app/hero-list-groups.component.ts" region="animationdef"></code-example>.

## Последовательные и параллельные анимации

В сложных анимациях может происходить множество действий одновременно. Но что если вы хотите создать анимацию, включающую несколько анимаций, происходящих одна за другой? Ранее вы использовали [`group()`](api/animations/group), чтобы запустить несколько анимаций одновременно, параллельно.

Вторая функция под названием `sequence()` позволяет запускать те же анимации одну за другой. Внутри `sequence()` шаги анимации состоят из вызовов функций `style()` или `animate()`.

-   Используйте `style()` для немедленного применения предоставленных данных о стиле.

-   Используйте `animate()` для применения данных о стиле в течение заданного интервала времени.

## Пример анимации фильтра

Посмотрите на другую анимацию на странице живого примера. На вкладке Filter/Stagger введите текст в поле **Search Heroes**, например `Magnet` или `tornado`.

Фильтр работает в реальном времени по мере ввода текста. Элементы покидают страницу по мере ввода каждой новой буквы, а фильтр становится все более строгим.

Список героев постепенно возвращается на страницу по мере удаления каждой буквы в поле фильтра.

HTML-шаблон содержит триггер под названием `filterAnimation`.

<code-example header="src/app/hero-list-page.component.html" path="animations/src/app/hero-list-page.component.html" region="filter-animations"></code-example>.

Фильтр `filterAnimation` в декораторе компонента содержит три перехода.

<code-example header="src/app/hero-list-page.component.ts" path="animations/src/app/hero-list-page.component.ts" region="filter-animations"></code-example>.

Код в этом примере выполняет следующие задачи:

-   Пропускает анимацию, когда пользователь впервые открывает или переходит на эту страницу\(анимация фильтра сужает то, что уже есть, поэтому она работает только на элементах, которые уже существуют в DOM\)

-   Фильтрует героев, основываясь на значении поискового ввода.

Для каждого изменения:

-   Скрывает элемент, выходящий из DOM, устанавливая его непрозрачность и ширину на 0

-   Анимирует элемент, входящий в DOM в течение 300 миллисекунд.

    Во время анимации элемент принимает ширину и непрозрачность по умолчанию.

-   Если в DOM входят или выходят несколько элементов, каждая анимация начинается с верхней части страницы с задержкой в 50 миллисекунд между каждым элементом.

## Анимация элементов переупорядоченного списка

Хотя Angular правильно анимирует элементы списка `*ngFor` из коробки, он не сможет сделать это, если их порядок изменится. Это происходит потому, что он теряет представление о том, какой элемент является каким, что приводит к сбоям анимации.

Единственный способ помочь Angular отслеживать такие элементы - присвоить директиве `NgForOf` функцию `TrackByFunction`.

Благодаря этому Angular всегда будет знать, какой элемент каким является, что позволит ему постоянно применять правильную анимацию к правильным элементам.

<div class="alert is-important">

**ВАЖНО**: Если вам нужно анимировать элементы списка `*ngFor` и есть вероятность, что порядок этих элементов изменится во время выполнения, всегда используйте `TrackByFunction`.

</div>

## Animations and Component View Encapsulation

Angular animations are based on the components DOM structure and do not directly take [View Encapsulation](/guide/view-encapsulation) into account, this means that components using `ViewEncapsulation.Emulated` behave exactly as if they were using `ViewEncapsulation.None` (`ViewEncapsulation.ShadowDom` behaves differently as we'll discuss shortly).

For example if the `query()` function (which you'll see more of in the rest of the Animations guide) were to be applied at the top of a tree of components using the emulated view encapsulation, such query would be able to identify (and thus animate) DOM elements on any depth of the tree.

On the other hand the `ViewEncapsulation.ShadowDom` changes the component's DOM structure by "hiding" DOM elements inside [`ShadowRoot`](https://developer.mozilla.org/en-US/docs/Web/API/ShadowRoot) elements. Such DOM manipulations do prevent some of the animations implementation to work properly since it relies on simple DOM structures and doesn't take `ShadowRoot` elements into account. Therefore it is advised to avoid applying animations to views incorporating components using the ShadowDom view encapsulation.

## Animation sequence summary

Angular functions for animating multiple elements start with `query()` to find inner elements; for example, gathering all images within a `<div>`. The remaining functions, `stagger()`, [`group()`](api/animations/group), and `sequence()`, apply cascades or let you control how multiple animation steps are applied.

## Подробнее об анимации в Angular

Вам также может быть интересно следующее:

-   [Введение в анимации Angular](руководство/анимации)

-   [Переход и триггеры](guide/transition-and-triggers)

-   [Многоразовые анимации](руководство/reusable-animations)

-   [Анимации перехода по маршруту](guide/route-animations)

<!-- links -->

<!-- external links -->

<!-- end links -->

:дата: 28.02.2022
