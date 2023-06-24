# Справочник по маршрутизаторам

В следующих разделах рассматриваются некоторые основные концепции маршрутизаторов.

<a id="basics-router-imports"></a>

## Импорт маршрутизатора

Angular Router - это дополнительный сервис, который представляет определенный вид компонента для заданного URL. Он не является частью ядра Angular и поэтому находится в собственном библиотечном пакете `@angular/router`.

Импортируйте из него то, что вам нужно, как и из любого другого пакета Angular.

<code-example header="src/app/app.module.ts (import)" path="router/src/app/app.module.1.ts" region="import-router"></code-example>

<div class="alert is-helpful">

Подробнее о стилях URL браузера смотрите [`LocationStrategy` и стили URL браузера](guide/router#browser-url-styles).

</div>

<a id="basics-config"></a>

## Конфигурация

Маршрутизируемое приложение Angular имеет один экземпляр сервиса `Router`. Когда URL браузера изменяется, маршрутизатор ищет соответствующий `Route`, на основе которого он может определить компонент для отображения.

Маршрутизатор не имеет маршрутов, пока вы его не настроите. Следующий пример создает пять определений маршрутов, настраивает маршрутизатор с помощью метода `RouterModule.forRoot()` и добавляет результат в массив `imports` модуля `AppModule`.

<code-example header="src/app/app.module.ts (excerpt)" path="router/src/app/app.module.0.ts"></code-example>

<a id="example-config"></a>

Массив маршрутов `appRoutes` описывает способы навигации. Передайте его в метод `RouterModule.forRoot()` в модуле `imports` для настройки маршрутизатора.

Каждый `маршрут` сопоставляет URL `путь` с компонентом. В пути нет ведущих косых черт.

Маршрутизатор анализирует и формирует конечный URL, что позволяет использовать как относительные, так и абсолютные пути при навигации между представлениями приложения.

`:id` во втором маршруте является маркером для параметра маршрута. В URL, таком как `/hero/42`, "42" является значением параметра `id`.

Соответствующий компонент `HeroDetailComponent` использует это значение для поиска и представления героя, чей `id` равен 42.

Свойство `data` в третьем маршруте - это место для хранения произвольных данных, связанных с этим конкретным маршрутом. Свойство data доступно в каждом активированном маршруте.

Используйте его для хранения таких элементов, как заголовки страниц, текст хлебных крошек и других статических данных, доступных только для чтения.

Для получения динамических данных используйте [resolve guard](guide/router-tutorial-toh#resolve-guard).

Пустой путь в четвертом маршруте представляет собой путь по умолчанию для приложения &mdash; место, куда следует перейти, когда путь в URL пуст, как это обычно бывает в начале. Этот маршрут по умолчанию перенаправляет на маршрут для URL `/heroes` и, следовательно, отображает компонент `HeroesListComponent`.

Если вам нужно посмотреть, какие события происходят во время жизненного цикла навигации, в конфигурации маршрутизатора по умолчанию есть опция `enableTracing`. Она выводит в консоль браузера каждое событие маршрутизатора, произошедшее во время каждого жизненного цикла навигации.

Используйте `enableTracing` только в целях отладки.

Вы устанавливаете опцию `enableTracing: true` в объекте, передаваемом в качестве второго аргумента методу `RouterModule.forRoot()`.

<a id="basics-router-outlet"></a>

## Выход маршрутизатора

`RouterOutlet` - это директива из библиотеки маршрутизатора, которая используется подобно компоненту. Она действует как заполнитель, который отмечает место в шаблоне, где маршрутизатор должен отображать компоненты для данного аутлета.

<code-example format="html" language="html">

&lt;router-outlet&gt;&lt;/router-outlet&gt; &lt;!-- Маршрутизируемые компоненты идут сюда --&gt;

</code-example>

Учитывая предыдущую конфигурацию, когда URL браузера для этого приложения становится `/heroes`, маршрутизатор сопоставляет этот URL с маршрутным путем `/heroes` и отображает `HeroListComponent` в качестве дочернего элемента `RouterOutlet`, который вы поместили в шаблон главного компонента.

<a id="basics-router-links"></a> <a id="router-link"></a>

## Ссылки маршрутизатора

Для навигации в результате какого-либо действия пользователя, например, нажатия на тег якоря, используйте `RouterLink`.

Рассмотрим следующий шаблон:

<code-example header="src/app/app.component.html" path="router/src/app/app.component.1.html"></code-example>.

Директивы `RouterLink` в тегах якорей дают маршрутизатору контроль над этими элементами. Пути навигации фиксированы, поэтому вы можете назначить строку в качестве одноразовой привязки к `routerLink`.

Если бы путь навигации был более динамичным, можно было бы привязать к выражению шаблона, возвращающему массив параметров ссылки маршрута; то есть, массив [link parameters array](guide/router#link-parameters-array). Маршрутизатор преобразует этот массив в полный URL.

<a id="router-link-active"></a>

## Активные ссылки маршрутизатора

Директива `RouterLinkActive` переключает классы CSS для активных привязок `RouterLink` на основе текущего `RouterState`.

В каждом теге якоря вы видите [привязку свойства](guide/property-binding) к директиве `RouterLinkActive`, которая выглядит следующим образом

<code-example format="html" hideCopy language="html">

routerLinkActive="..."

</code-example>

Шаблонное выражение справа от знака равенства `=` содержит ограниченную пробелами строку CSS-классов, которые маршрутизатор добавляет, когда эта ссылка активна, и удаляет, когда ссылка неактивна. Вы устанавливаете директиву `RouterLinkActive` в строку классов, например `routerLinkActive="active fluffy"`, или связываете ее со свойством компонента, которое возвращает такую строку.
Например,

<code-example format="typescript" hideCopy language="typescript">

[routerLinkActive]="someStringProperty"

</code-example>

Активные ссылки маршрута каскадируют вниз через каждый уровень дерева маршрутов, поэтому родительские и дочерние ссылки маршрутизатора могут быть активны одновременно. Чтобы отменить это поведение, привяжитесь к входной привязке `[routerLinkActiveOptions]` с помощью выражения `{ exact: true }`.
При использовании `{ exact: true }`, данная `RouterLink` будет активна только в том случае, если ее URL точно совпадает с текущим URL.

`RouterLinkActive` также позволяет легко применить атрибут `aria-current` к активному элементу, обеспечивая тем самым более доступный опыт для всех пользователей. Для получения дополнительной информации см. раздел Accessibility Best Practices [Active links identification section](/guide/accessibility#active-links-identification).

<a id="basics-router-state"></a>

## Состояние маршрутизатора

После завершения каждого успешного жизненного цикла навигации маршрутизатор строит дерево объектов `ActivatedRoute`, которые составляют текущее состояние маршрутизатора. Вы можете получить доступ к текущему `RouterState` из любой точки приложения, используя службу `Router` и свойство `routerState`.

Каждый `ActivatedRoute` в `RouterState` предоставляет методы для перемещения вверх и вниз по дереву маршрутов для получения информации из родительских, дочерних и родственных маршрутов.

<a id="activated-route"></a>

## Активированный маршрут

Путь маршрута и параметры доступны через инжектируемый сервис маршрутизатора под названием [ActivatedRoute](api/router/ActivatedRoute). Он содержит много полезной информации, включая:

| Property | Details | | :-------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `url` | An `Observable` of the route paths, represented as an array of strings for each part of the route path. |
| `data` | An `Observable` that contains the `data` object provided for the route. Also contains any resolved values from the [resolve guard](guide/router-tutorial-toh#resolve-guard). |
| `params` | An `Observable` that contains the required and [optional parameters](guide/router-tutorial-toh#optional-route-parameters) specific to the route. |
| `paramMap` | An `Observable` that contains a [map](api/router/ParamMap) of the required and [optional parameters](guide/router-tutorial-toh#optional-route-parameters) specific to the route. The map supports retrieving single and multiple values from the same parameter. |
| `queryParamMap` | An `Observable` that contains a [map](api/router/ParamMap) of the [query parameters](guide/router-tutorial-toh#query-parameters) available to all routes. The map supports retrieving single and multiple values from the query parameter. |
| `queryParams` | An `Observable` that contains the [query parameters](guide/router-tutorial-toh#query-parameters) available to all routes. |
| `fragment` | An `Observable` of the URL [fragment](guide/router-tutorial-toh#fragment) available to all routes. |
| `outlet` | The name of the `RouterOutlet` used to render the route. For an unnamed outlet, the outlet name is primary. |
| `routeConfig` | The route configuration used for the route that contains the origin path. |
| `parent` | The route's parent `ActivatedRoute` when this route is a [child route](guide/router-tutorial-toh#child-routing-component). |
| `firstChild` | Contains the first `ActivatedRoute` in the list of this route's child routes. |
| `children` | Contains all the [child routes](guide/router-tutorial-toh#child-routing-component) activated under the current route. |

## События маршрутизатора

Во время каждой навигации `Router` издает навигационные события через свойство `Router.events`. Эти события показаны в следующей таблице.

| Router event | Details | | :-------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [`NavigationStart`](api/router/NavigationStart) | Triggered when navigation starts. |
| [`RouteConfigLoadStart`](api/router/RouteConfigLoadStart) | Triggered before the `Router` [lazy loads](guide/router-tutorial-toh#asynchronous-routing) a route configuration. |
| [`RouteConfigLoadEnd`](api/router/RouteConfigLoadEnd) | Triggered after a route has been lazy loaded. |
| [`RoutesRecognized`](api/router/RoutesRecognized) | Triggered when the Router parses the URL and the routes are recognized. |
| [`GuardsCheckStart`](api/router/GuardsCheckStart) | Triggered when the Router begins the Guards phase of routing. |
| [`ChildActivationStart`](api/router/ChildActivationStart) | Triggered when the Router begins activating a route's children. |
| [`ActivationStart`](api/router/ActivationStart) | Triggered when the Router begins activating a route. |
| [`GuardsCheckEnd`](api/router/GuardsCheckEnd) | Triggered when the Router finishes the Guards phase of routing successfully. |
| [`ResolveStart`](api/router/ResolveStart) | Triggered when the Router begins the Resolve phase of routing. |
| [`ResolveEnd`](api/router/ResolveEnd) | Triggered when the Router finishes the Resolve phase of routing successfully. |
| [`ChildActivationEnd`](api/router/ChildActivationEnd) | Triggered when the Router finishes activating a route's children. |
| [`ActivationEnd`](api/router/ActivationEnd) | Triggered when the Router finishes activating a route. |
| [`NavigationEnd`](api/router/NavigationEnd) | Triggered when navigation ends successfully. |
| [`NavigationCancel`](api/router/NavigationCancel) | Triggered when navigation is canceled. This can happen when a [Route Guard](guide/router-tutorial-toh#guards) returns false during navigation, or redirects by returning a `UrlTree`. |
| [`NavigationError`](api/router/NavigationError) | Triggered when navigation fails due to an unexpected error. |
| [`Scroll`](api/router/Scroll) | Represents a scrolling event. |

Когда вы включаете опцию `enableTracing`, Angular записывает эти события в консоль. Пример фильтрации событий навигации по маршрутизатору см. в разделе [router](guide/observables-in-angular#router) руководства [Observables in Angular](guide/observables-in-angular).

## Терминология маршрутизатора

Здесь приведены ключевые термины `Router` и их значения:

| Router part | Details | | :-------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Router` | Displays the application component for the active URL. Manages navigation from one component to the next. |
| `RouterModule` | A separate NgModule that provides the necessary service providers and directives for navigating through application views. |
| `Routes` | Defines an array of Routes, each mapping a URL path to a component. |
| `Route` | Defines how the router should navigate to a component based on a URL pattern. Most routes consist of a path and a component type. |
| `RouterOutlet` | The directive \(`<router-outlet>`\) that marks where the router displays a view. |
| `RouterLink` | The directive for binding a clickable HTML element to a route. Clicking an element with a `routerLink` directive that's bound to a _string_ or a _link parameters array_ triggers a navigation. |
| `RouterLinkActive` | The directive for adding/removing classes from an HTML element when an associated `routerLink` contained on or inside the element becomes active/inactive. It can also set the `aria-current` of an active link for better accessibility. |
| `ActivatedRoute` | A service that's provided to each route component that contains route specific information such as route parameters, static data, resolve data, global query parameters, and the global fragment. |
| `RouterState` | The current state of the router including a tree of the currently activated routes together with convenience methods for traversing the route tree. |
| Link parameters array | An array that the router interprets as a routing instruction. You can bind that array to a `RouterLink` or pass the array as an argument to the `Router.navigate` method. |
| Routing component | An Angular component with a `RouterOutlet` that displays views based on router navigations. |

<!-- links -->

<!-- external links -->

<!-- end links -->

:date: 28.02.2022
