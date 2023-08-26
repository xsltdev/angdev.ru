# Общие задачи маршрутизации

:date: 28.02.2022

В этой теме описывается, как реализовать многие из общих задач, связанных с добавлением маршрутизатора Angular в ваше приложение.

## Генерация приложения с включенной маршрутизацией

Следующая команда использует Angular CLI для генерации базового приложения Angular с модулем маршрутизации приложения, называемым `AppRoutingModule`, который представляет собой NgModule, где вы можете настроить маршруты. Имя приложения в следующем примере — `routing-app`.

```shell
ng new routing-app --routing --defaults
```

### Добавление компонентов для маршрутизации

Чтобы использовать маршрутизатор Angular, приложение должно иметь как минимум два компонента, чтобы можно было переходить от одного к другому. Чтобы создать компонент с помощью CLI, введите в командной строке следующее, где `first` — имя вашего компонента:

```shell
ng generate component first
```

Повторите этот шаг для второго компонента, но дайте ему другое имя. Здесь новое имя будет `second`.

```shell
ng generate component second
```

CLI автоматически добавляет `Component`, поэтому если бы вы написали `first-component`, ваш компонент был бы `FirstComponentComponent`.

!!!note "&lt;base href&gt;"

    Это руководство работает с приложением Angular, созданным с помощью CLI. Если вы работаете вручную, убедитесь, что у вас есть `<base href="/">` в `<head>` вашего файла index.html.

    Это предполагает, что папка `app` является корнем приложения, и использует `"/"`.

### Импортирование новых компонентов

Чтобы использовать ваши новые компоненты, импортируйте их в `AppRoutingModule` в верхней части файла, как показано ниже:

```ts
import { FirstComponent } from './first/first.component';
import { SecondComponent } from './second/second.component';
```

## Определение базового маршрута

Создание маршрута состоит из трех основных компонентов.

Импортируйте `AppRoutingModule` в `AppModule` и добавьте его в массив `imports`.

Angular CLI выполнит этот шаг за вас. Однако если вы создаете приложение вручную или работаете с существующим приложением без CLI, проверьте правильность импорта и конфигурации.

Ниже приведен стандартный `AppModule`, использующий CLI с флагом `--routing`.

```ts
import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AppRoutingModule } from './app-routing.module'; // CLI imports AppRoutingModule
import { AppComponent } from './app.component';

@NgModule({
    declarations: [AppComponent],
    imports: [
        BrowserModule,
        AppRoutingModule, // CLI adds AppRoutingModule to the AppModule's imports array
    ],
    providers: [],
    bootstrap: [AppComponent],
})
export class AppModule {}
```

1.  Импортируйте `RouterModule` и `Routes` в ваш модуль маршрутизации.

    Angular CLI выполняет этот шаг автоматически.

    CLI также устанавливает массив `Routes` для ваших маршрутов и настраивает массивы `imports` и `exports` для `@NgModule()`.

    ```ts
    import { NgModule } from '@angular/core';
    import { Routes, RouterModule } from '@angular/router'; // CLI imports router

    const routes: Routes = []; // sets up routes constant where you define your routes

    // configures NgModule imports and exports
    @NgModule({
        imports: [RouterModule.forRoot(routes)],
        exports: [RouterModule],
    })
    export class AppRoutingModule {}
    ```

2.  Определите маршруты в массиве `Routes`.

    Каждый маршрут в этом массиве представляет собой объект JavaScript, который содержит два свойства.

    Первое свойство, `path`, определяет путь URL для маршрута.

    Второе свойство, `component`, определяет компонент, который Angular должен использовать для соответствующего пути.

    ```ts
    const routes: Routes = [
        {
            path: 'first-component',
            component: FirstComponent,
        },
        {
            path: 'second-component',
            component: SecondComponent,
        },
    ];
    ```

3.  Добавьте маршруты в приложение.

    Теперь, когда вы определили маршруты, добавьте их в приложение.

    Сначала добавьте ссылки на два компонента.

    Присвойте тегу якоря, в который вы хотите добавить маршрут, атрибут `routerLink`.

    Установите значение атрибута для компонента, который будет отображаться, когда пользователь нажмет на каждую ссылку.

    Далее обновите шаблон компонента, включив в него `<router-outlet>`.

    Этот элемент сообщает Angular обновить представление приложения компонентом для выбранного маршрута.

    ```html
    <h1>Angular Router App</h1>
    <!-- This nav gives you links to click, which tells the router which route to use (defined in the routes constant in  AppRoutingModule) -->
    <nav>
        <ul>
            <li>
                <a
                    routerLink="/first-component"
                    routerLinkActive="active"
                    ariaCurrentWhenActive="page"
                    >First Component</a
                >
            </li>
            <li>
                <a
                    routerLink="/second-component"
                    routerLinkActive="active"
                    ariaCurrentWhenActive="page"
                    >Second Component</a
                >
            </li>
        </ul>
    </nav>
    <!-- The routed views render in the <router-outlet>-->
    <router-outlet></router-outlet>
    ```

### Порядок маршрутов

Порядок маршрутов важен, поскольку `Router` использует стратегию выигрыша по первому совпадению при подборе маршрутов, поэтому более конкретные маршруты должны располагаться выше менее конкретных. Сначала перечисляются маршруты со статическим путем, затем пустой маршрут, который соответствует маршруту по умолчанию.

Маршрут [wildcard route](router.md#setting-up-wildcard-routes) идет последним, потому что он соответствует каждому URL, и `Router` выбирает его только в том случае, если ни один другой маршрут не подходит первым.

## Получение информации о маршруте

Часто, когда пользователь перемещается по вашему приложению, вы хотите передавать информацию от одного компонента к другому. Например, рассмотрим приложение, которое отображает список покупок продуктов.

Каждый элемент в списке имеет уникальный `id`.

Чтобы отредактировать элемент, пользователи нажимают кнопку Edit, которая открывает компонент `EditGroceryItem`.

Вы хотите, чтобы этот компонент получал `id` для бакалейного товара, чтобы он мог отображать правильную информацию пользователю.

Используйте маршрут для передачи такого типа информации компонентам приложения. Для этого вы используете функцию [withComponentInputBinding](https://angular.io/api/router/withComponentInputBinding) с `provideRouter` или опцию `bindToComponentInputs` в `RouterModule.forRoot`.

Чтобы получить информацию из маршрута:

1.  Добавьте функцию `withComponentInputBinding` к методу `provideRouter`.

    ```ts
    providers: [
        provideRouter(
            appRoutes,
            withComponentInputBinding()
        ),
    ];
    ```

2.  Обновите компонент, чтобы у него был `Input`, соответствующий имени параметра.

    ```ts
    @Input()
    set id(heroId: string) {
    	this.hero$ = this.service.getHero(heroId);
    }
    ```

    !!!note ""

        Вы можете привязать все данные маршрута с парами ключ-значение к входам компонента: статические или разрешенные данные маршрута, параметры пути, параметры матрицы и параметры запроса.

## Настройка маршрутов wildcard

Хорошо функционирующее приложение должно изящно обрабатывать попытки пользователей перейти к несуществующей части вашего приложения. Чтобы добавить эту функциональность в ваше приложение, вы устанавливаете маршрут `wildcard`.

Маршрутизатор Angular выбирает этот маршрут каждый раз, когда запрашиваемый URL не соответствует ни одному пути маршрутизатора.

Чтобы настроить маршрут с подстановочным знаком, добавьте следующий код в определение `routes`.

```ts
{ path: '**', component: <component-name> }
```

Две звездочки, `**`, указывают Angular, что это определение `routes` является маршрутом с подстановочным знаком. Для свойства component вы можете определить любой компонент в вашем приложении.

Обычно это `PageNotFoundComponent`, который можно определить как [отображение страницы 404](router.md#404-page-how-to) для ваших пользователей; или перенаправление на основной компонент вашего приложения.

Маршрут с подстановочным знаком — это последний маршрут, поскольку он соответствует любому URL.

Подробнее о том, почему порядок имеет значение для маршрутов, смотрите в разделе [Порядок маршрутов](router.md#route-order).

## Отображение страницы 404

Чтобы отобразить страницу 404, настройте [wildcard route](router.md#wildcard-route-how-to) со свойством `component`, установленным на компонент, который вы хотите использовать для страницы 404, следующим образом:

```ts
const routes: Routes = [
    { path: 'first-component', component: FirstComponent },
    {
        path: 'second-component',
        component: SecondComponent,
    },
    // Wildcard route for a 404 page
    { path: '**', component: PageNotFoundComponent },
];
```

Последний маршрут с `path` в `**` является маршрутом с подстановочным знаком. Маршрутизатор выбирает этот маршрут, если запрашиваемый URL не соответствует ни одному из предыдущих в списке путей, и отправляет пользователя на `PageNotFoundComponent`.

## Настройка перенаправлений

Чтобы настроить перенаправление, настройте маршрут с `путем`, с которого вы хотите перенаправить, `компонентом`, на который вы хотите перенаправить, и значением `pathMatch`, которое указывает маршрутизатору, как сопоставить URL.

```ts
const routes: Routes = [
    { path: 'first-component', component: FirstComponent },
    {
        path: 'second-component',
        component: SecondComponent,
    },
    {
        path: '',
        redirectTo: '/first-component',
        pathMatch: 'full',
    }, // redirect to `first-component`
    // Wildcard route for a 404 page
    { path: '**', component: PageNotFoundComponent },
];
```

В этом примере третий маршрут является перенаправлением, так что маршрутизатор по умолчанию переходит к маршруту `first-component`. Обратите внимание, что этот перенаправление предшествует маршруту с подстановочным знаком.

Здесь `path: ''` означает использование начального относительного URL (`''`).

Более подробно о `pathMatch` смотрите [Spotlight on `pathMatch`](router-tutorial-toh.md#pathmatch).

## Вложенные маршруты

По мере роста сложности вашего приложения вы можете захотеть создать маршруты, которые будут относиться к компоненту, отличному от корневого компонента. Такие типы вложенных маршрутов называются дочерними маршрутами.

Это означает, что вы добавляете второй `<router-outlet>` в ваше приложение, поскольку он является дополнением к `<router-outlet>` в `AppComponent`.

В этом примере есть два дополнительных дочерних компонента, `child-a` и `child-b`. Здесь `FirstComponent` имеет свою собственную `<nav>` и второй `<router-outlet>` в дополнение к тому, который находится в `AppComponent`.

```html
<h2>First Component</h2>

<nav>
    <ul>
        <li><a routerLink="child-a">Child A</a></li>
        <li><a routerLink="child-b">Child B</a></li>
    </ul>
</nav>

<router-outlet></router-outlet>
```

Дочерний маршрут подобен любому другому маршруту, так как ему нужны `путь` и `компонент`. Единственное отличие заключается в том, что дочерние маршруты размещаются в массиве `children` внутри родительского маршрута.

```ts
const routes: Routes = [
    {
        path: 'first-component',
        // this is the component with the <router-outlet> in the template
        component: FirstComponent,
        children: [
            {
                // child route path
                path: 'child-a',
                // child route component that the router renders
                component: ChildAComponent,
            },
            {
                path: 'child-b',
                // another child route component that the router renders
                component: ChildBComponent,
            },
        ],
    },
];
```

## Установка заголовка страницы {: #setting-the-page-title}

Каждая страница в вашем приложении должна иметь уникальный заголовок, чтобы ее можно было идентифицировать в истории браузера. Маршрутизатор `Router` устанавливает заголовок документа, используя свойство `title` из конфигурации `Route`.

```ts
const routes: Routes = [
    {
        path: 'first-component',
        title: 'First component',
        // this is the component with the <router-outlet> in the template
        component: FirstComponent,
        children: [
            {
                path: 'child-a', // child route path
                title: resolvedChildATitle,
                // child route component that the router renders
                component: ChildAComponent,
            },
            {
                path: 'child-b',
                title: 'child b',
                // another child route component that the router renders
                component: ChildBComponent,
            },
        ],
    },
];

const resolvedChildATitle: ResolveFn<string> = () =>
    Promise.resolve('child a');
```

!!!note ""

    Свойство `title` подчиняется тем же правилам, что и статические маршрутные `data` и динамические значения, реализующие `ResolveFn`.

Вы также можете создать собственную стратегию заголовка, расширив `TitleStrategy`.

```ts
@Injectable({providedIn: 'root'})
export class TemplatePageTitleStrategy extends TitleStrategy {
  constructor(private readonly title: Title) {
    super();
  }

  override updateTitle(routerState: RouterStateSnapshot) {
    const title = this.buildTitle(routerState);
    if (title !== undefined) {
      this.title.setTitle(`My Application | ${title}`);
    }
  }
}

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
  providers: [
    {provide: TitleStrategy, useClass: TemplatePageTitleStrategy},
  ]
})
export class AppRoutingModule {
}
```

## Использование относительных путей {: #using-relative-paths}

Относительные пути позволяют определять пути, которые являются относительными по отношению к текущему сегменту URL. Следующий пример показывает относительный путь к другому компоненту, `second-component`.

`FirstComponent` и `SecondComponent` находятся на одном уровне в дереве, однако ссылка на `SecondComponent` расположена внутри `FirstComponent`, что означает, что маршрутизатор должен подняться на один уровень вверх, а затем во второй каталог, чтобы найти `SecondComponent`.

Вместо того чтобы писать весь путь к `SecondComponent`, используйте обозначение `../` для перехода на уровень выше.

```html
<h2>First Component</h2>

<nav>
    <ul>
        <li>
            <a routerLink="../second-component"
                >Relative Route to second component</a
            >
        </li>
    </ul>
</nav>
<router-outlet></router-outlet>
```

В дополнение к `../`, используйте `./` или без ведущей косой черты для указания текущего уровня.

### Указание относительного маршрута

Чтобы указать относительный маршрут, используйте свойство `NavigationExtras` `relativeTo`. В классе компонента импортируйте `NavigationExtras` из `@angular/router`.

Затем используйте `relativeTo` в своем методе навигации. После массива параметров ссылки, который здесь содержит `items`, добавьте объект со свойством `relativeTo`, установленным на `ActivatedRoute`, которым является `this.route`.

```ts
goToItems() {
  this.router.navigate(['items'], { relativeTo: this.route });
}
```

Аргументы `navigate()` настраивают маршрутизатор на использование текущего маршрута в качестве основы для добавления `items`.

Метод `goToItems()` интерпретирует URI назначения как относительный к активированному маршруту и переходит к маршруту `items`.

## Доступ к параметрам запроса и фрагментам

Иногда функции вашего приложения требуют доступа к части маршрута, например, к параметру запроса или фрагменту. Приложение Tour of Heroes на данном этапе обучения использует представление списка, в котором вы можете нажать на героя, чтобы увидеть подробности.

Маршрутизатор использует `id` для отображения подробностей нужного героя.

Сначала импортируйте следующие члены в компонент, из которого вы хотите осуществлять навигацию.

```ts
import { ActivatedRoute } from '@angular/router';
import { Observable } from 'rxjs';
import { switchMap } from 'rxjs/operators';
```

Затем введите активированную службу маршрутизации:

```ts
constructor(private route: ActivatedRoute) {}
```

Настройте класс так, чтобы у вас была наблюдаемая `heroes$`, `selectedId` для хранения `id` номера героя, и герои в `ngOnInit()`, добавьте следующий код для получения `id` выбранного героя. Этот фрагмент кода предполагает, что у вас есть список героев, служба героев, функция для получения героев и HTML для отображения списка и деталей, как в примере Tour of Heroes.

```ts
heroes$: Observable<Hero[]>;
selectedId: number;
heroes = HEROES;

ngOnInit() {
  this.heroes$ = this.route.paramMap.pipe(
    switchMap(params => {
      this.selectedId = Number(params.get('id'));
      return this.service.getHeroes();
    })
  );
}
```

Затем в компоненте, на который вы хотите перейти, импортируйте следующие члены.

```ts
import {
    Router,
    ActivatedRoute,
    ParamMap,
} from '@angular/router';
import { Observable } from 'rxjs';
```

Вставьте `ActivatedRoute` и `Router` в конструктор класса компонента, чтобы они были доступны этому компоненту:

```ts
hero$: Observable<Hero>;

constructor(
  private route: ActivatedRoute,
  private router: Router  ) {}

ngOnInit() {
  const heroId = this.route.snapshot.paramMap.get('id');
  this.hero$ = this.service.getHero(heroId);
}

gotoItems(hero: Hero) {
  const heroId = hero ? hero.id : null;
  // Pass along the hero id if available
  // so that the HeroList component can select that item.
  this.router.navigate(['/heroes', { id: heroId }]);
}
```

## Ленивая загрузка {: #lazy-loading }

Вы можете настроить свои маршруты на ленивую загрузку модулей, что означает, что Angular загружает модули только по мере необходимости, а не загружает все модули при запуске приложения. Кроме того, можно предварительно загружать части приложения в фоновом режиме, чтобы улучшить качество работы пользователя.

Более подробную информацию о ленивой загрузке и предварительной загрузке можно найти в специальном руководстве [Ленивая загрузка NgModules](lazy-loading-ngmodules.md).

## Предотвращение несанкционированного доступа

Для предотвращения несанкционированного доступа пользователей к частям приложения используйте защитные экраны маршрутов. В Angular доступны следующие защиты маршрутов:

-   [`canActivate`](https://angular.io/api/router/CanActivateFn)
-   [`canActivateChild`](https://angular.io/api/router/CanActivateChildFn)
-   [`canDeactivate`](https://angular.io/api/router/CanDeactivateFn)
-   [`canMatch`](https://angular.io/api/router/CanMatchFn)
-   [`resolve`](https://angular.io/api/router/ResolveFn)
-   [`canLoad`](https://angular.io/api/router/CanLoadFn)

Чтобы использовать защиту маршрутов, используйте [component-less routes](https://angular.io/api/router/Route#componentless-routes), так как это облегчает защиту дочерних маршрутов.

Создайте файл для вашего охранника:

```shell
ng generate guard your-guard
```

В файле guard добавьте функции guard, которые вы хотите использовать. В следующем примере для защиты маршрута используется `canActivateFn`.

```ts
export const yourGuardFunction: CanActivateFn = (
    next: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
) => {
    // your  logic goes here
};
```

В модуле маршрутизации используйте соответствующее свойство в конфигурации `routes`.

В данном случае `canActivate` указывает маршрутизатору на необходимость посредничества в навигации по данному конкретному маршруту.

```ts
{
	path: '/your-path',
	component: YourComponent,
	canActivate: [yourGuardFunction],
}
```

Более подробную информацию с рабочим примером можно найти в разделе [учебника по маршрутизации, посвященном охранникам маршрутов](router-tutorial-toh.md#milestone-5-route-guards).

## Массив параметров ссылки

Массив параметров ссылки содержит следующие компоненты для навигации маршрутизатора:

-   Путь маршрута к компоненту назначения
-   Необходимые и необязательные параметры маршрута, которые входят в URL маршрута.

Привяжите директиву `RouterLink` к такому массиву следующим образом:

```ts
<a [routerLink]="['/heroes']">Heroes</a>
```

Ниже представлен двухэлементный массив при указании параметра маршрута:

```html
<a [routerLink]="['/hero', hero.id]">
    <span class="badge">{{ hero.id }}</span>{{ hero.name }}
</a>
```

Предоставьте необязательные параметры маршрута в объекте, как в `{ foo: 'foo' }`:

```ts
<a [routerLink]="['/crisis-center', { foo: 'foo' }]">Crisis Center</a>
```

Эти три примера покрывают потребности приложения с одним уровнем маршрутизации. Однако с дочерним маршрутизатором, как, например, в кризисном центре, вы создаете новые возможности массива ссылок.

Следующий минимальный пример `RouterLink` основан на заданном [дочернем маршруте по умолчанию](router-tutorial-toh.md#a-crisis-center-with-child-routes) для кризисного центра.

```ts
<a [routerLink]="['/crisis-center']">Crisis Center</a>
```

Рассмотрите следующее:

-   Первый элемент массива идентифицирует родительский маршрут (`/crisis-center`).
-   Для этого родительского маршрута нет параметров
-   Для дочернего маршрута нет параметров по умолчанию, поэтому вам нужно выбрать один из них.
-   Вы переходите к `CrisisListComponent`, путь маршрута которого `/`, но вам не нужно явно добавлять слеш.

Рассмотрим следующую ссылку маршрутизатора, которая ведет от корня приложения вниз к Кризису Дракона:

```ts
<a [routerLink]="['/crisis-center', 1]">Dragon Crisis</a>
```

-   Первый элемент массива идентифицирует родительский маршрут (`/crisis-center`).
-   Для этого родительского маршрута нет параметров
-   Второй элемент идентифицирует дочерний маршрут подробностей о конкретном кризисе (`/:id`)
-   Для дочернего маршрута подробностей требуется параметр маршрута `id`.
-   Вы добавили `id` кризиса Дракона в качестве второго элемента массива (`1`)
-   Получился путь `/crisis-center/1`.

Вы также можете переопределить шаблон `AppComponent` исключительно с маршрутами Кризисного центра:

```ts
template: `
  <h1 class="title">Angular Router</h1>
  <nav>
    <a [routerLink]="['/crisis-center']">Crisis Center</a>
    <a [routerLink]="['/crisis-center/1', { foo: 'foo' }]">Dragon Crisis</a>
    <a [routerLink]="['/crisis-center/2']">Shark Crisis</a>
  </nav>
  <router-outlet></router-outlet>
`;
```

В целом, вы можете писать приложения с одним, двумя или более уровнями маршрутизации. Массив параметров ссылок позволяет гибко представлять любую глубину маршрутизации и любую законную последовательность маршрутных путей, (требуется) параметров маршрутизатора и (необязательно) объектов параметров маршрута.

## `LocationStrategy` и стили URL браузера

Когда маршрутизатор переходит к новому представлению компонента, он обновляет местоположение и историю браузера с URL для этого представления.

Современные браузеры HTML5 поддерживают [history.pushState](https://developer.mozilla.org/docs/Web/API/History_API/Working_with_the_History_API#adding_and_modifying_history_entries), технику, которая изменяет местоположение и историю браузера, не вызывая запрос страницы на сервере. Маршрутизатор может составить "естественный" URL, неотличимый от того, который в противном случае потребовал бы загрузки страницы.

Вот URL Кризисного центра в этом стиле "HTML5 pushState":

```
localhost:3002/crisis-center
```

Старые браузеры отправляют запросы на сервер при изменении URL местоположения, если только изменение не происходит после "#" (называемого "хэшем"). Маршрутизаторы могут воспользоваться этим исключением, составляя URL маршрутов в приложении с помощью хэшей.
Вот "хэш URL", который направляет в Кризисный центр.

```
localhost:3002/src/#/crisis-center
```

Маршрутизатор поддерживает оба стиля с помощью двух провайдеров `LocationStrategy`:

| Провайдеры             | Подробности                           |
| :--------------------- | :------------------------------------ |
| `PathLocationStrategy` | Стиль по умолчанию "HTML5 pushState". |
| `HashLocationStrategy` | Стиль "хэш URL".                      |

Функция `RouterModule.forRoot()` устанавливает `LocationStrategy` в `PathLocationStrategy`, что делает ее стратегией по умолчанию. У вас также есть возможность переключиться на `HashLocationStrategy` с помощью переопределения во время процесса загрузки.

!!!note ""

    Более подробную информацию о провайдерах и процессе bootstrap смотрите в [Dependency Injection](dependency-injection-providers.md).

## Выбор стратегии маршрутизации

Вы должны выбрать стратегию маршрутизации на ранних этапах разработки проекта, потому что, как только приложение будет запущено в производство, посетители вашего сайта будут использовать и зависеть от ссылок URL приложения.

Почти все проекты Angular должны использовать стиль HTML5 по умолчанию. Он создает URL-адреса, которые легче понять пользователям, и сохраняет возможность рендеринга на стороне сервера.

Рендеринг критических страниц на сервере — это техника, которая может значительно улучшить воспринимаемую отзывчивость при первой загрузке приложения. Приложение, запуск которого в противном случае занял бы десять или более секунд, может быть отрисовано на сервере и доставлено на устройство пользователя менее чем за секунду.

Эта опция доступна только в том случае, если URL-адреса приложений выглядят как обычные веб-адреса без символов хэша (`#`) в середине.

## `<base href>`

Маршрутизатор использует [history.pushState](https://developer.mozilla.org/docs/Web/API/History_API/Working_with_the_History_API#adding_and_modifying_history_entries) браузера для навигации. `pushState` позволяет настраивать пути URL в приложении; например, `localhost:4200/crisis-center`.

URL-адреса внутри приложения могут быть неотличимы от URL-адресов сервера.

Современные браузеры HTML5 первыми стали поддерживать `pushState`, поэтому многие называют эти URL "URL в стиле HTML5".

!!!note ""

    Навигация в стиле HTML5 является маршрутизатором по умолчанию. В разделе [LocationStrategy и стили URL браузера](#browser-url-styles) вы узнаете, почему стиль HTML5 предпочтительнее, как настроить его поведение и как при необходимости переключиться на более старый стиль хэш (`#`).

Вы должны добавить элемент [`<base href>`](https://hcdev.ru/html/base/) в `index.html` приложения, чтобы маршрутизация `pushState` работала. Браузер использует значение `<base href>` для префиксации относительных URL при ссылке на файлы CSS, скрипты и изображения.

Добавьте элемент `<base>` сразу после тега `<head>`. Если папка `app` является корнем приложения, как это сделано для данного приложения, установите значение `href` в `index.html`, как показано здесь.

```html
<base href="/" />
```

### HTML5 URLs и `<base href>`

В последующих руководствах будут упоминаться различные части URL. На этой диаграмме показано, к чему относятся эти части:

```
foo://example.com:8042/over/there?name=ferret#nose
\_/   \______________/\_________/ \_________/ \__/
 |           |            |            |        |
scheme    authority      path        query   fragment
```

Хотя маршрутизатор по умолчанию использует стиль [HTML5 pushState](https://developer.mozilla.org/docs/Web/API/History_API#Adding_and_modifying_history_entries), вы должны настроить эту стратегию с помощью `<base href>`.

Предпочтительным способом настройки стратегии является добавление тега [`<base href>` element](https://hcdev.ru/html/base/) в `<head>` в `index.html`.

```html
<base href="/" />
```

Без этого тега браузер не сможет загрузить ресурсы (изображения, CSS, скрипты) при "глубокой ссылке" в приложение.

Некоторые разработчики могут не иметь возможности добавить элемент `<base>`, возможно, потому что у них нет доступа к `<head>` или `index.html`.

Такие разработчики все равно могут использовать HTML5 URL, выполнив следующие два шага:

1.  Предоставьте маршрутизатору соответствующее значение `APP_BASE_HREF`.

2.  Используйте корневые URL (URL с `авторитетом`) для всех веб-ресурсов: CSS, изображений, скриптов и HTML-файлов шаблона.

    -   Путь `<base href>` должен заканчиваться символом "/", так как браузеры игнорируют символы в `path`, следующие за крайним правым "`/`".
    -   Если `<base href>` включает часть `query`, то `query` используется только в том случае, если `path` ссылки на странице пуст и не содержит `query`.

        Это означает, что `query` в `<base href>` включается только при использовании `HashLocationStrategy`.

    -   Если ссылка на странице является корневым URL (имеет `авторитет`), то `<base href>` не используется.

        Таким образом, `APP_BASE_HREF` с авторитетом приведет к тому, что все ссылки, созданные Angular, будут игнорировать значение `<base href>`.

    -   Фрагмент в `<base href>` _никогда_ не сохраняется.

Для более полной информации о том, как `<base href>` используется для построения целевых URI, смотрите раздел [RFC](https://tools.ietf.org/html/rfc3986#section-5.2.2) о преобразовании ссылок.

### HashLocationStrategy {: #hashlocationstrategy }

Используйте `HashLocationStrategy`, предоставив `useHash: true` в объекте в качестве второго аргумента `RouterModule.forRoot()` в `AppModule`.

```ts
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { Routes, RouterModule } from '@angular/router';

import { AppComponent } from './app.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';

const routes: Routes = [];

@NgModule({
    imports: [
        BrowserModule,
        FormsModule,
        RouterModule.forRoot(routes, { useHash: true }), // .../#/crisis-center/
    ],
    declarations: [AppComponent, PageNotFoundComponent],
    providers: [],
    bootstrap: [AppComponent],
})
export class AppModule {}
```
