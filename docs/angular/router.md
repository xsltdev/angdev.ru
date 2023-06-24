# Общие задачи маршрутизации

В этой теме описывается, как реализовать многие из общих задач, связанных с добавлением маршрутизатора Angular в ваше приложение.

<a id="basics"></a>

## Генерация приложения с включенной маршрутизацией

Следующая команда использует Angular CLI для генерации базового приложения Angular с модулем маршрутизации приложения, называемым `AppRoutingModule`, который представляет собой NgModule, где вы можете настроить маршруты. Имя приложения в следующем примере - `routing-app`.

<code-example format="shell" language="shell">

ng new routing-app --routing --defaults

</code-example>

### Добавление компонентов для маршрутизации

Чтобы использовать маршрутизатор Angular, приложение должно иметь как минимум два компонента, чтобы можно было переходить от одного к другому. Чтобы создать компонент с помощью CLI, введите в командной строке следующее, где `first` - имя вашего компонента:

<code-example format="shell" language="shell">

ng сначала создайте компонент

</code-example>

Повторите этот шаг для второго компонента, но дайте ему другое имя. Здесь новое имя будет `second`.

<code-example format="shell" language="shell">

ng генерировать второй компонент

</code-example>

CLI автоматически добавляет `Component`, поэтому если бы вы написали `first-component`, ваш компонент был бы `FirstComponentComponent`.

<a id="basics-base-href"></a>

<div class="alert is-helpful">

<header><code>&lt;base href&gt;</code></header>

Это руководство работает с приложением Angular, созданным с помощью CLI. Если вы работаете вручную, убедитесь, что у вас есть `<base href="/">` в `<head>` вашего файла index.html.
Это предполагает, что папка `app` является корнем приложения, и использует `"/"`.

</div>

### Импортирование новых компонентов

Чтобы использовать ваши новые компоненты, импортируйте их в `AppRoutingModule` в верхней части файла, как показано ниже:

<code-example header="AppRoutingModule (excerpt)">

import { FirstComponent } from './first/first.component'; import { SecondComponent } from './second/second.component';

</code-example>

<a id="basic-route"></a>

## Определение базового маршрута

Создание маршрута состоит из трех основных компонентов.

Импортируйте `AppRoutingModule` в `AppModule` и добавьте его в массив `imports`.

Angular CLI выполнит этот шаг за вас. Однако если вы создаете приложение вручную или работаете с существующим приложением без CLI, проверьте правильность импорта и конфигурации.

Ниже приведен стандартный `AppModule`, использующий CLI с флагом `--routing`.

<code-example header="Default CLI AppModule with routing" path="router/src/app/app.module.8.ts"></code-example>.

1.  Импортируйте `RouterModule` и `Routes` в ваш модуль маршрутизации.

    Angular CLI выполняет этот шаг автоматически.

    CLI также устанавливает массив `Routes` для ваших маршрутов и настраивает массивы `imports` и `exports` для `@NgModule()`.

    <code-example header="Модуль маршрутизации приложений CLI" path="router/src/app/app-routing.module.7.ts"></code-example>.

1.  Определите маршруты в массиве `Routes`.

    Каждый маршрут в этом массиве представляет собой объект JavaScript, который содержит два свойства.

    Первое свойство, `path`, определяет путь URL для маршрута.

    Второе свойство, `component`, определяет компонент, который Angular должен использовать для соответствующего пути.

    <code-example header="AppRoutingModule (excerpt)" path="router/src/app/app-routing.module.8.ts" region="routes"></code-example>.

1.  Добавьте маршруты в приложение.

    Теперь, когда вы определили маршруты, добавьте их в приложение.

    Сначала добавьте ссылки на два компонента.

    Присвойте тегу якоря, в который вы хотите добавить маршрут, атрибут `routerLink`.

    Установите значение атрибута для компонента, который будет отображаться, когда пользователь нажмет на каждую ссылку.

    Далее обновите шаблон компонента, включив в него `<router-outlet>`.

    Этот элемент сообщает Angular обновить представление приложения компонентом для выбранного маршрута.

    <code-example header="Шаблон с routerLink и router-outlet" path="router/src/app/app.component.7.html"></code-example>.

<a id="route-order"></a>

### Порядок маршрутов

Порядок маршрутов важен, поскольку `Router` использует стратегию выигрыша по первому совпадению при подборе маршрутов, поэтому более конкретные маршруты должны располагаться выше менее конкретных. Сначала перечисляются маршруты со статическим путем, затем пустой маршрут, который соответствует маршруту по умолчанию.

Маршрут [wildcard route](guide/router#setting-up-wildcard-routes) идет последним, потому что он соответствует каждому URL, и `Router` выбирает его только в том случае, если ни один другой маршрут не подходит первым.

<a id="getting-route-information"></a>

## Получение информации о маршруте

Часто, когда пользователь перемещается по вашему приложению, вы хотите передавать информацию от одного компонента к другому. Например, рассмотрим приложение, которое отображает список покупок продуктов.

Каждый элемент в списке имеет уникальный `id`.

Чтобы отредактировать элемент, пользователи нажимают кнопку Edit, которая открывает компонент `EditGroceryItem`.

Вы хотите, чтобы этот компонент получал `id` для бакалейного товара, чтобы он мог отображать правильную информацию пользователю.

Используйте маршрут для передачи такого типа информации компонентам приложения. Для этого вы используете функцию [withComponentInputBinding](api/router/withComponentInputBinding) с `provideRouter` или опцию `bindToComponentInputs` в `RouterModule.forRoot`.

Чтобы получить информацию из маршрута:

1.  Добавьте функцию `withComponentInputBinding` к методу `provideRouter`.

    <code-example header="provideRouter feature" path="router/src/app/app-routing.module.11.ts" region="withComponentInputBinding"></code-example>.

1.  Обновите компонент, чтобы у него был `Input`, соответствующий имени параметра.

    <code-example header="The component input (excerpt)" path="router/src/app/heroes/hero-detail/hero-detail.component.4.ts" region="id-input"></code-example>

    <div class="alert is-helpful">

    **NOTE:** <br>

    You can bind all route data with key, value pairs to component inputs: static or resolved route data, path parameters, matrix parameters, and query parameters.

    </div>

<a id="wildcard-route-how-to"></a>

## Настройка маршрутов wildcard

Хорошо функционирующее приложение должно изящно обрабатывать попытки пользователей перейти к несуществующей части вашего приложения. Чтобы добавить эту функциональность в ваше приложение, вы устанавливаете маршрут wildcard.

Маршрутизатор Angular выбирает этот маршрут каждый раз, когда запрашиваемый URL не соответствует ни одному пути маршрутизатора.

Чтобы настроить маршрут с подстановочным знаком, добавьте следующий код в определение `routes`.

<code-example header="AppRoutingModule (excerpt)">

{ path: '\*\*', component: &lt;component-name&gt; }

</code-example>

Две звездочки, `**`, указывают Angular, что это определение `routes` является маршрутом с подстановочным знаком. Для свойства component вы можете определить любой компонент в вашем приложении.
Обычно это `PageNotFoundComponent`, который можно определить как [отображение страницы 404](guide/router#404-page-how-to) для ваших пользователей; или перенаправление на основной компонент вашего приложения.

Маршрут с подстановочным знаком - это последний маршрут, поскольку он соответствует любому URL.

Подробнее о том, почему порядок имеет значение для маршрутов, смотрите в разделе [Порядок маршрутов](guide/router#route-order).

<a id="404-page-how-to"></a>

## Отображение страницы 404

Чтобы отобразить страницу 404, настройте [wildcard route](guide/router#wildcard-route-how-to) со свойством `component`, установленным на компонент, который вы хотите использовать для страницы 404, следующим образом:

<code-example header="AppRoutingModule (excerpt)" path="router/src/app/app-routing.module.8.ts" region="routes-with-wildcard"></code-example>.

Последний маршрут с `путем` в `**` является маршрутом с подстановочным знаком. Маршрутизатор выбирает этот маршрут, если запрашиваемый URL не соответствует ни одному из предыдущих в списке путей, и отправляет пользователя на `PageNotFoundComponent`.

## Настройка перенаправлений

Чтобы настроить перенаправление, настройте маршрут с `путем`, с которого вы хотите перенаправить, `компонентом`, на который вы хотите перенаправить, и значением `pathMatch`, которое указывает маршрутизатору, как сопоставить URL.

<code-example header="AppRoutingModule (excerpt)" path="router/src/app/app-routing.module.8.ts" region="redirect"></code-example>.

В этом примере третий маршрут является перенаправлением, так что маршрутизатор по умолчанию переходит к маршруту `первого компонента`. Обратите внимание, что этот перенаправление предшествует маршруту с подстановочным знаком.

Здесь `path: ''` означает использование начального относительного URL \(`''`\).

Более подробно о `pathMatch` смотрите [Spotlight on `pathMatch`](guide/router-tutorial-toh#pathmatch).

<a id="nesting-routes"></a>

## Вложенные маршруты

По мере роста сложности вашего приложения вы можете захотеть создать маршруты, которые будут относиться к компоненту, отличному от корневого компонента. Такие типы вложенных маршрутов называются дочерними маршрутами.

Это означает, что вы добавляете второй `<router-outlet>` в ваше приложение, поскольку он является дополнением к `<router-outlet>` в `AppComponent`.

В этом примере есть два дополнительных дочерних компонента, `child-a` и `child-b`. Здесь `FirstComponent` имеет свою собственную `<nav>` и второй `<router-outlet>` в дополнение к тому, который находится в `AppComponent`.

<code-example header="В шаблоне" path="router/src/app/app.component.8.html" region="child-routes"></code-example>.

Дочерний маршрут подобен любому другому маршруту, так как ему нужны `путь` и `компонент`. Единственное отличие заключается в том, что дочерние маршруты размещаются в массиве `children` внутри родительского маршрута.

<code-example header="AppRoutingModule (excerpt)" path="router/src/app/app-routing.module.9.ts" region="child-routes"></code-example>.

<a id="setting-the-page-title"></a>

## Установка заголовка страницы

Каждая страница в вашем приложении должна иметь уникальный заголовок, чтобы ее можно было идентифицировать в истории браузера. Маршрутизатор `Router` устанавливает заголовок документа, используя свойство `title` из конфигурации `Route`.

<code-example header="AppRoutingModule (excerpt)" path="router/src/app/app-routing.module.10.ts" region="page-title"></code-example>.

<div class="alert is-helpful">

**NOTE**: <br /> The `title` property follows the same rules as static route `data` and dynamic values that implement `ResolveFn`.

</div>

Вы также можете создать собственную стратегию заголовка, расширив `TitleStrategy`.

<code-example header="AppRoutingModule (excerpt)" path="router/src/app/app-routing.module.10.ts" region="custom-page-title"></code-example>.

<a id="using-relative-paths"></a>

## Использование относительных путей

Относительные пути позволяют определять пути, которые являются относительными по отношению к текущему сегменту URL. Следующий пример показывает относительный путь к другому компоненту, `second-component`.

`FirstComponent` и `SecondComponent` находятся на одном уровне в дереве, однако ссылка на `SecondComponent` расположена внутри `FirstComponent`, что означает, что маршрутизатор должен подняться на один уровень вверх, а затем во второй каталог, чтобы найти `SecondComponent`.

Вместо того чтобы писать весь путь к `SecondComponent`, используйте обозначение `../` для перехода на уровень выше.

<code-example header="В шаблоне" path="router/src/app/app.component.8.html" region="relative-route"></code-example>.

В дополнение к `../`, используйте `./` или без ведущей косой черты для указания текущего уровня.

### Указание относительного маршрута

Чтобы указать относительный маршрут, используйте свойство `NavigationExtras` `relativeTo`. В классе компонента импортируйте `NavigationExtras` из `@angular/router`.

Затем используйте `relativeTo` в своем методе навигации. После массива параметров ссылки, который здесь содержит `items`, добавьте объект со свойством `relativeTo`, установленным на `ActivatedRoute`, которым является `this.route`.

<code-example header="RelativeTo" path="router/src/app/app.component.4.ts" region="relative-to">

Аргументы `navigate()` настраивают маршрутизатор на использование текущего маршрута в качестве основы для добавления `элементов`.

</code-example>

Метод `goToItems()` интерпретирует URI назначения как относительный к активированному маршруту и переходит к маршруту `items`.

## Доступ к параметрам запроса и фрагментам

Иногда функции вашего приложения требуют доступа к части маршрута, например, к параметру запроса или фрагменту. Приложение Tour of Heroes на данном этапе обучения использует представление списка, в котором вы можете нажать на героя, чтобы увидеть подробности.

Маршрутизатор использует `id` для отображения подробностей нужного героя.

Сначала импортируйте следующие члены в компонент, из которого вы хотите осуществлять навигацию.

<code-example header="Component import statements (excerpt)">

import { ActivatedRoute } from '&commat;angular/router'; import { Observable } from 'rxjs';
import { switchMap } from 'rxjs/operators';

</code-example>

Затем введите активированную службу маршрутизации:

<code-example header="Component (excerpt)">

constructor(private route: ActivatedRoute) {}

</code-example>

Настройте класс так, чтобы у вас была наблюдаемая `heroes$`, `selectedId` для хранения `id` номера героя, и герои в `ngOnInit()`, добавьте следующий код для получения `id` выбранного героя. Этот фрагмент кода предполагает, что у вас есть список героев, служба героев, функция для получения героев и HTML для отображения списка и деталей, как в примере Tour of Heroes.

<code-example header="Component 1 (excerpt)">

герои\$: Observable&lt;Hero[]&gt;; selectedId: number;
heroes = HEROES;

ngOnInit() { this.heroes\$ = this.route.paramMap.pipe(

switchMap(params =&gt; {

this.selectedId = Number(params.get('id'));

return this.service.getHeroes();

})

);

}

</code-example>

Затем в компоненте, на который вы хотите перейти, импортируйте следующие члены.

<code-example header="Component 2 (excerpt)">

import { Router, ActivatedRoute, ParamMap } from '&commat;angular/router'; import { Observable } from 'rxjs';

</code-example>

Вставьте `ActivatedRoute` и `Router` в конструктор класса компонента, чтобы они были доступны этому компоненту:

<code-example header="Component 2 (excerpt)">

герой\$: Observable&lt;Hero&gt;;

constructor( private route: ActivatedRoute,

private router: Router ) {}

ngOnInit() { const heroId = this.route.snapshot.paramMap.get('id');

this.hero\$ = this.service.getHero(heroId);

}

gotoItems(hero: Hero) { const heroId = hero ? hero.id : null;

// Передаем идентификатор героя, если он доступен

// чтобы компонент HeroList мог выбрать этот элемент.

this.router.navigate(['/heroes', { id: heroId }]);

}

</code-example>

<a id="lazy-loading"></a>

## Ленивая загрузка

Вы можете настроить свои маршруты на ленивую загрузку модулей, что означает, что Angular загружает модули только по мере необходимости, а не загружает все модули при запуске приложения. Кроме того, можно предварительно загружать части приложения в фоновом режиме, чтобы улучшить качество работы пользователя.

Более подробную информацию о ленивой загрузке и предварительной загрузке можно найти в специальном руководстве [Ленивая загрузка NgModules] (guide/lazy-loading-ngmodules).

## Предотвращение несанкционированного доступа

Для предотвращения несанкционированного доступа пользователей к частям приложения используйте защитные экраны маршрутов. В Angular доступны следующие защиты маршрутов:

-   [`canActivate`](api/router/CanActivateFn)

-   [`canActivateChild`](api/router/CanActivateChildFn)

-   [`canDeactivate`](api/router/CanDeactivateFn)

-   [`canMatch`](api/router/CanMatchFn)

-   [`resolve`](api/router/ResolveFn)

-   [`canLoad`](api/router/CanLoadFn)

Чтобы использовать защиту маршрутов, используйте [component-less routes](api/router/Route#componentless-routes), так как это облегчает защиту дочерних маршрутов.

Создайте файл для вашего охранника:

<code-example format="shell" language="shell">

ng generate guard your-guard

</code-example>

В файле guard добавьте функции guard, которые вы хотите использовать. В следующем примере для защиты маршрута используется `canActivateFn`.

<code-example header="guard (excerpt)">

export const yourGuardFunction: CanActivateFn = ( next: ActivatedRouteSnapshot,
состояние: RouterStateSnapshot) => {

// ваша логика здесь

}

</code-example>

В модуле маршрутизации используйте соответствующее свойство в конфигурации `routes`.

В данном случае `canActivate` указывает маршрутизатору на необходимость посредничества в навигации по данному конкретному маршруту.

<code-example header="Модуль маршрутизации (выдержка)">

{

путь: '/ваш путь',

компонент: YourComponent,

canActivate: [yourGuardFunction],

}

</code-example>

Более подробную информацию с рабочим примером можно найти в разделе [учебника по маршрутизации, посвященном охранникам маршрутов] (guide/router-tutorial-toh#milestone-5-route-guards).

## Массив параметров ссылки

Массив параметров ссылки содержит следующие компоненты для навигации маршрутизатора:

-   Путь маршрута к компоненту назначения

-   Необходимые и необязательные параметры маршрута, которые входят в URL маршрута.

Привяжите директиву `RouterLink` к такому массиву следующим образом:

<code-example header="src/app/app.component.ts (h-anchor)" path="router/src/app/app.component.3.ts" region="h-anchor"></code-example>.

Ниже представлен двухэлементный массив при указании параметра маршрута:

<code-example header="src/app/heroes/hero-list/hero-list.component.html (nav-to-detail)" path="router/src/app/heroes/hero-list/hero-list.component.1.html" region="nav-to-detail"></code-example>.

Предоставьте необязательные параметры маршрута в объекте, как в `{ foo: 'foo' }`:

<code-example header="src/app/app.component.ts (cc-query-params)" path="router/src/app/app.component.3.ts" region="cc-query-params"></code-example

Эти три примера покрывают потребности приложения с одним уровнем маршрутизации. Однако с дочерним маршрутизатором, как, например, в кризисном центре, вы создаете новые возможности массива ссылок.

Следующий минимальный пример `RouterLink` основан на заданном [дочернем маршруте по умолчанию](guide/router-tutorial-toh#a-crisis-center-with-child-routes) для кризисного центра.

<code-example header="src/app/app.component.ts (cc-anchor-w-default)" path="router/src/app/app/app.component.3.ts" region="cc-anchor-w-default"></code-example>.

Рассмотрите следующее:

-   Первый элемент массива идентифицирует родительский маршрут \(`/crisis-center`\).

-   Для этого родительского маршрута нет параметров

-   Для дочернего маршрута нет параметров по умолчанию, поэтому вам нужно выбрать один из них.

-   Вы переходите к `CrisisListComponent`, путь маршрута которого `/`, но вам не нужно явно добавлять слеш.

Рассмотрим следующую ссылку маршрутизатора, которая ведет от корня приложения вниз к Кризису Дракона:

<code-example header="src/app/app.component.ts (Dragon-anchor)" path="router/src/app/app.component.3.ts" region="Dragon-anchor"></code-example>

-   Первый элемент массива идентифицирует родительский маршрут \(`/crisis-center`\).

-   Для этого родительского маршрута нет параметров

-   Второй элемент идентифицирует дочерний маршрут подробностей о конкретном кризисе \(`/:id`\)

-   Для дочернего маршрута подробностей требуется параметр маршрута `id`.

-   Вы добавили `id` кризиса Дракона в качестве второго элемента массива \(`1`\)

-   Получился путь `/crisis-center/1`.

Вы также можете переопределить шаблон `AppComponent` исключительно с маршрутами Кризисного центра:

<code-example header="src/app/app.component.ts (template)" path="router/src/app/app.component.3.ts" region="template"></code-example>

В целом, вы можете писать приложения с одним, двумя или более уровнями маршрутизации. Массив параметров ссылок позволяет гибко представлять любую глубину маршрутизации и любую законную последовательность маршрутных путей, \(требуется\) параметров маршрутизатора и \(необязательно\) объектов параметров маршрута.

<a id="browser-url-styles"></a> <a id="location-strategy"></a>

## `LocationStrategy` и стили URL браузера

Когда маршрутизатор переходит к новому представлению компонента, он обновляет местоположение и историю браузера с URL для этого представления.

Современные браузеры HTML5 поддерживают [history.pushState](https://developer.mozilla.org/docs/Web/API/History_API/Working_with_the_History_API#adding_and_modifying_history_entries 'HTML5 browser history push-state'), технику, которая изменяет местоположение и историю браузера, не вызывая запрос страницы на сервере. Маршрутизатор может составить "естественный" URL, неотличимый от того, который в противном случае потребовал бы загрузки страницы.

Вот URL Кризисного центра в этом стиле "HTML5 pushState":

<code-example format="none" language="http">

localhost:3002/crisis-center

</code-example>

Старые браузеры отправляют запросы на сервер при изменении URL местоположения, если только изменение не происходит после "#" \(называемого "хэшем"\). Маршрутизаторы могут воспользоваться этим исключением, составляя URL маршрутов в приложении с помощью хэшей.
Вот "хэш URL", который направляет в Кризисный центр.

<code-example format="none" language="http">

localhost:3002/src/#/crisis-center

</code-example>

Маршрутизатор поддерживает оба стиля с помощью двух провайдеров `LocationStrategy`:

| Провайдеры | Подробности | | :--------------------- | :----------------------------------- |.

| `PathLocationStrategy` | Стиль по умолчанию "HTML5 pushState". |

| | `HashLocationStrategy` | Стиль "хэш URL". |

Функция `RouterModule.forRoot()` устанавливает `LocationStrategy` в `PathLocationStrategy`, что делает ее стратегией по умолчанию. У вас также есть возможность переключиться на `HashLocationStrategy` с помощью переопределения во время процесса загрузки.

<div class="alert is-helpful">

Более подробную информацию о провайдерах и процессе bootstrap смотрите в [Dependency Injection](guide/dependency-injection-providers).

</div>

## Выбор стратегии маршрутизации

Вы должны выбрать стратегию маршрутизации на ранних этапах разработки проекта, потому что, как только приложение будет запущено в производство, посетители вашего сайта будут использовать и зависеть от ссылок URL приложения.

Почти все проекты Angular должны использовать стиль HTML5 по умолчанию. Он создает URL-адреса, которые легче понять пользователям, и сохраняет возможность рендеринга на стороне сервера.

Рендеринг критических страниц на сервере - это техника, которая может значительно улучшить воспринимаемую отзывчивость при первой загрузке приложения. Приложение, запуск которого в противном случае занял бы десять или более секунд, может быть отрисовано на сервере и доставлено на устройство пользователя менее чем за секунду.

Эта опция доступна только в том случае, если URL-адреса приложений выглядят как обычные веб-адреса без символов хэша \(`#`\) в середине.

## `<base href>`.

Маршрутизатор использует [history.pushState](https://developer.mozilla.org/docs/Web/API/History_API/Working_with_the_History_API#adding_and_modifying_history_entries 'HTML5 browser history push-state') браузера для навигации. `pushState` позволяет настраивать пути URL в приложении; например, `localhost:4200/crisis-center`.

URL-адреса внутри приложения могут быть неотличимы от URL-адресов сервера.

Современные браузеры HTML5 первыми стали поддерживать `pushState`, поэтому многие называют эти URL "URL в стиле HTML5".

<div class="alert is-helpful">

Навигация в стиле HTML5 является маршрутизатором по умолчанию. В разделе [LocationStrategy и стили URL браузера](#browser-url-styles) вы узнаете, почему стиль HTML5 предпочтительнее, как настроить его поведение и как при необходимости переключиться на более старый стиль хэш \(`#`\).

</div>

Вы должны добавить элемент [`<base href>`](https://developer.mozilla.org/docs/Web/HTML/Element/base 'base href') в `index.html` приложения, чтобы маршрутизация `pushState` работала. Браузер использует значение `<base href>` для префиксации относительных URL при ссылке на файлы CSS, скрипты и изображения.

Добавьте элемент `<base>` сразу после тега `<head>`. Если папка `app` является корнем приложения, как это сделано для данного приложения, установите значение `href` в `index.html`, как показано здесь.

<code-example header="src/index.html (base-href)" path="router/src/index.html" region="base-href"></code-example>.

### HTML5 URLs и `<base href>`

В последующих руководствах будут упоминаться различные части URL. На этой диаграмме показано, к чему относятся эти части:

<code-example format="output" hideCopy language="none">

foo://example.com:8042/over/there?name=ferret#nose &bsol;\_/ &bsol;\_\_\_\_\_\_\_\_\_\_\_\_\_\_/&bsol;\_\_\_\_\_\_\_\_\_/ &bsol;\_\_\_\_\_\_\_\_\_/ &bsol;\_\_/
&verbar; &verbar; &verbar; &verbar; &verbar; &verbar;

схема авторитет путь фрагмент запроса

</code-example>

Хотя маршрутизатор по умолчанию использует стиль [HTML5 pushState](https://developer.mozilla.org/docs/Web/API/History_API#Adding_and_modifying_history_entries 'Browser history push-state'), вы должны настроить эту стратегию с помощью `<base href>`.

Предпочтительным способом настройки стратегии является добавление тега [`<base href>` element](https://developer.mozilla.org/docs/Web/HTML/Element/base 'base href') в `<head>` в `index.html`.

<code-example header="src/index.html (base-href)" path="router/src/index.html" region="base-href"></code-example>.

Без этого тега браузер не сможет загрузить ресурсы\(изображения, CSS, скрипты\) при "глубокой ссылке" в приложение.

Некоторые разработчики могут не иметь возможности добавить элемент `<base>`, возможно, потому что у них нет доступа к `<head>` или `index.html`.

Такие разработчики все равно могут использовать HTML5 URL, выполнив следующие два шага:

1.  Предоставьте маршрутизатору соответствующее значение `APP_BASE_HREF`.

1.  Используйте корневые URL \(URL с `авторитетом`\) для всех веб-ресурсов: CSS, изображений, скриптов и HTML-файлов шаблона.

    -   Путь `<base href>` должен заканчиваться символом "/", так как браузеры игнорируют символы в `пути`, следующие за крайним правым "`/`".

    -   Если `<base href>` включает часть `query`, то `query` используется только в том случае, если `путь` ссылки на странице пуст и не содержит `query`.

        Это означает, что `query` в `<base href>` включается только при использовании `HashLocationStrategy`.

    -   Если ссылка на странице является корневым URL\(имеет `авторитет`\), то `<базовый href>` не используется.

        Таким образом, `APP_BASE_HREF` с авторитетом приведет к тому, что все ссылки, созданные Angular, будут игнорировать значение `<base href>`.

    -   Фрагмент в `<base href>` _никогда_ не сохраняется.

Для более полной информации о том, как `<base href>` используется для построения целевых URI, смотрите раздел [RFC](https://tools.ietf.org/html/rfc3986#section-5.2.2) о преобразовании ссылок.

<a id="hashlocationstrategy"></a>

### `HashLocationStrategy`.

Используйте `HashLocationStrategy`, предоставив `useHash: true` в объекте в качестве второго аргумента `RouterModule.forRoot()` в `AppModule`.

<code-example header="src/app/app.module.ts (стратегия хэш URL)" path="router/src/app/app.module.6.ts"></code-example>

<!-- links -->

<!-- external links -->

<!-- end links -->

:date: 28.02.2022
