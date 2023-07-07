# Ленивая загрузка функциональных модулей

По умолчанию NgModules загружаются с нетерпением. Это означает, что как только приложение загружается, загружаются и все модули NgModules, независимо от того, нужны они сразу или нет. Для больших приложений с большим количеством маршрутов рассмотрите вариант ленивой загрузки &mdash; шаблон проектирования, который загружает NgModules по мере необходимости.

Ленивая загрузка помогает уменьшить размер начальных пакетов, что, в свою очередь, сокращает время загрузки.

<div class="alert is-helpful">

Окончательный пример приложения с двумя лениво загружаемыми модулями, который описан на этой странице, смотрите в <live-example></live-example>.

</div>

<a id="lazy-loading"></a>

## Основы ленивой загрузки

В этом разделе представлена основная процедура настройки маршрута с ленивой загрузкой. Пошаговый пример смотрите в разделе [пошаговая настройка](#step-by-step) на этой странице.

Для ленивой загрузки модулей Angular используйте `loadChildren`\ (вместо `component`\) в конфигурации `маршрутов` вашего `AppRoutingModule` следующим образом.

<code-example header="AppRoutingModule (excerpt)">

const routes: Маршруты = [ {
путь: 'items',

loadChildren: () =&gt; import('./items/items.module').then(m =&gt; m.ItemsModule)

}

];

</code-example>

В модуле маршрутизации модуля lazy-loaded добавьте маршрут для компонента.

<code-example header="Routing module for lazy loaded module (excerpt)">

const routes: Маршруты = [ {
путь: '',

компонент: ItemsComponent

}

];

</code-example>

Также не забудьте удалить `ItemsModule` из `AppModule`. Для получения пошаговых инструкций по ленивой загрузке модулей, продолжите следующие разделы этой страницы.

<a id="step-by-step"></a>

## Пошаговая настройка

Установка функционального модуля с ленивой загрузкой требует двух основных шагов:

1.  Создайте функциональный модуль с помощью Angular CLI, используя флаг `--route`.

1.  Настройте маршруты.

### Настройка приложения

Если у вас еще нет приложения, выполните следующие шаги, чтобы создать его с помощью Angular CLI. Если у вас уже есть приложение, перейдите к разделу [Настройка маршрутов](#config-routes).

<!-- vale Angular.Google_WordListWarnings = NO -->

Введите следующую команду, где `customer-app` - имя вашего приложения:

<!-- vale Angular.Google_WordListWarnings = YES -->

<code-example format="shell" language="shell">

ng new customer-app --routing

</code-example>

Это создает приложение под названием `customer-app`, а флаг `--routing` создает файл `app-routing.module.ts`. Это один из файлов, необходимых для настройки ленивой загрузки для вашего функционального модуля. Перейдите в проект, выполнив команду `cd customer-app`.

<div class="alert is-helpful">

Опция `--routing` требует Angular CLI версии 8.1 или выше. Смотрите [Keeping Up to Date](guide/updating).

</div>

### Создание функционального модуля с маршрутизацией

Далее вам понадобится функциональный модуль с компонентом для маршрутизации. Чтобы создать такой модуль, введите в командной строке следующую команду, где `customers` - имя функционального модуля.

Путь для загрузки функциональных модулей `customers` также `customers`, поскольку он указан с опцией `--route`:

<code-example format="shell" language="shell">

ng generate module customers --route customers --module app.module

</code-example>

Это создаст директорию `customers`, содержащую новый функциональный модуль `CustomersModule`, определяемый в файле `customers.module.ts`, и модуль маршрутизации `CustomersRoutingModule`, определяемый в файле `customers-routing.module.ts`. Команда автоматически объявляет `CustomersComponent` и импортирует `CustomersRoutingModule` внутри нового функционального модуля.

Поскольку новый модуль предназначен для ленивой загрузки, команда **не** добавляет ссылку на него в файл корневого модуля приложения, `app.module.ts`. Вместо этого она добавляет объявленный маршрут `customers` в массив `routes`, объявленный в модуле, предоставленном в качестве опции `--module`.

<code-example header="src/app/app-routing.module.ts" path="lazy-loading-ngmodules/src/app/app-routing.module.ts" region="routes-customers"></code-example>.

Обратите внимание, что синтаксис ленивой загрузки использует `loadChildren`, за которым следует функция, использующая встроенный в браузер синтаксис `import('...')` для динамического импорта. Путь импорта - это относительный путь к модулю.

<div class="callout is-helpful">

<header>String-based lazy loading</header>

В версии 8 Angular строковый синтаксис для спецификации маршрута `loadChildren` [был устаревшим] (guide/deprecations#loadchildren-string-syntax) в пользу синтаксиса `import()`. Вы можете отказаться от использования строковой ленивой загрузки\(`loadChildren: './path/to/module#Module'`\), включив маршруты с ленивой загрузкой в ваш файл `tsconfig`, который включает файлы с ленивой загрузкой в компиляцию.

По умолчанию Angular CLI генерирует проекты с более строгими включениями файлов, предназначенными для использования с синтаксисом `import()`.

</div>

### Добавьте еще один функциональный модуль

Используйте ту же команду для создания второго функционального модуля с ленивой загрузкой и маршрутизацией, а также его компонента-заглушки.

<code-example format="shell" language="shell">

ng generate module orders --route orders --module app.module

</code-example>

Это создает новый каталог `orders`, содержащий `OrdersModule` и `OrdersRoutingModule`, а также новые исходные файлы `OrdersComponent`. Маршрут `orders`, указанный с помощью опции `--route`, добавляется в массив `routes` внутри файла `app-routing.module.ts`, используя синтаксис ленивой загрузки.

<code-example header="src/app/app-routing.module.ts" path="lazy-loading-ngmodules/src/app/app-routing.module.ts" region="routes-customers-orders"></code-example>.

### Настройте пользовательский интерфейс

Хотя вы можете ввести URL в адресную строку, навигационный пользовательский интерфейс более прост для пользователя и более распространен. Замените стандартную разметку placeholder в `app.component.html` на пользовательскую навигацию, чтобы вы могли переходить к своим модулям в браузере:

<code-example header="app.component.html" path="lazy-loading-ngmodules/src/app/app.component.html" region="app-component-template" header="src/app/app.component.html"></code-example>.

Чтобы увидеть ваше приложение в браузере, введите следующую команду в окне инструмента командной строки:

<code-example format="shell" language="shell">

служить

</code-example>

<!-- vale Angular.Google_WordListWarnings = NO -->

Затем перейдите на `localhost:4200`, где вы должны увидеть "customer-app" и три кнопки.

<!-- vale Angular.Google_WordListWarnings = YES -->

<div class="lightbox">

<img alt="three buttons in the browser" src="generated/images/guide/lazy-loading-ngmodules/three-buttons.png" width="300">

</div>

Эти кнопки работают, потому что Angular CLI автоматически добавил маршруты к модулям функций в массив `routes` в файле `app-routing.module.ts`.

<a id="config-routes"></a>

### Импорт и конфигурация маршрутов

Angular CLI автоматически добавил каждый функциональный модуль в карту маршрутов на уровне приложения. Завершите это добавлением маршрута по умолчанию.

В файле `app-routing.module.ts` обновите массив `routes` следующим образом:

<code-example header="src/app/app-routing.module.ts" path="lazy-loading-ngmodules/src/app/app-routing.module.ts" id="app-routing.module.ts" region="const-routes"></code-example>.

Первые два пути - это маршруты к `CustomersModule` и `OrdersModule`. Последняя запись определяет маршрут по умолчанию.

Пустой путь соответствует всему, что не соответствует предыдущему пути.

### Внутри функционального модуля

Далее посмотрите на файл `customers.module.ts`. Если вы используете Angular CLI и следуете шагам, описанным на этой странице, вам не нужно ничего здесь делать.

<code-example header="src/app/customers/customers.module.ts" path="lazy-loading-ngmodules/src/app/customers/customers.module.ts" id="customers.module.ts" region="customers-module"></code-example>.

Файл `customers.module.ts` импортирует файлы `customers-routing.module.ts` и `customers.component.ts`. `CustomersRoutingModule` указан в массиве `@NgModule` `imports`, что дает `CustomersModule` доступ к собственному модулю маршрутизации.

`CustomersComponent` находится в массиве `declarations`, что означает, что `CustomersComponent` принадлежит `CustomersModule`.

Затем `app-routing.module.ts` импортирует функциональный модуль `customers.module.ts`, используя динамический импорт JavaScript.

Файл определения маршрута для конкретной функции `customers-routing.module.ts` импортирует свой компонент функции, определенный в файле `customers.component.ts`, вместе с другими операторами импорта JavaScript. Затем он сопоставляет пустой путь с `CustomersComponent`.

<code-example header="src/app/customers/customers-routing.module.ts" path="lazy-loading-ngmodules/src/app/customers/customers-routing.module.ts" id="customers-routing.module.ts" region="customers-routing-module"></code-example>.

Здесь `path` установлен в пустую строку, потому что путь в `AppRoutingModule` уже установлен в `customers`, поэтому этот маршрут в `CustomersRoutingModule` уже находится в контексте `customers`. Каждый маршрут в этом модуле маршрутизации является дочерним маршрутом.

Модуль маршрутизации другого функционального модуля настроен аналогично.

<code-example header="src/app/orders/orders-routing.module.ts (excerpt)" path="lazy-loading-ngmodules/src/app/orders/orders-routing.module.ts" id="orders-routing.module.ts" region="orders-routing-module-detail"></code-example>.

### Проверить ленивую загрузку

Вы можете проверить, действительно ли модуль загружается в ленивом режиме, с помощью инструментов разработчика Chrome. В Chrome откройте инструменты разработчика, нажав `Cmd+Option+i` на Mac или `Ctrl+Shift+j` на PC, и перейдите на вкладку Network.

<div class="lightbox">

<img alt="lazy loaded modules diagram" src="generated/images/guide/lazy-loading-ngmodules/network-tab.png" width="600">

</div>

Нажмите на кнопку "Заказы" или "Клиенты". Если появится фрагмент, значит, все подключено правильно и функциональный модуль загружается в ленивом режиме.
Кусок должен появиться для Заказов и для Клиентов, но только один раз для каждого.

<div class="lightbox">

<img alt="lazy loaded modules diagram" src="generated/images/guide/lazy-loading-ngmodules/chunk-arrow.png" width="600">

</div>

Чтобы увидеть его снова или проверить после внесения изменений, нажмите на круг с линией в верхней левой части вкладки Сеть:

<div class="lightbox">

<img alt="lazy loaded modules diagram" src="generated/images/guide/lazy-loading-ngmodules/clear.gif" width="200">

</div>

Затем перезагрузите с помощью `Cmd+r` или `Ctrl+r`, в зависимости от вашей платформы.

## `forRoot()` и `forChild()`.

Вы могли заметить, что Angular CLI добавляет `RouterModule.forRoot(routes)` в массив `импортов` модуля `AppRoutingModule`. Это дает Angular знать, что `AppRoutingModule` является модулем маршрутизации, а `forRoot()` указывает, что это корневой модуль маршрутизации.

Он настраивает все маршруты, которые вы ему передаете, дает вам доступ к директивам маршрутизации и регистрирует службу `Router`.

Используйте `forRoot()` только один раз в приложении, внутри `AppRoutingModule`.

Angular CLI также добавляет функцию `RouterModule.forChild(routes)` к модулям маршрутизации. Таким образом, Angular знает, что список маршрутов отвечает только за предоставление дополнительных маршрутов и предназначен для функциональных модулей.

Вы можете использовать `forChild()` в нескольких модулях.

Метод `forRoot()` заботится о конфигурации _глобального_ инжектора для маршрутизатора. Метод `forChild()` не имеет конфигурации инжектора.

Он использует такие директивы, как `RouterOutlet` и `RouterLink`.

Дополнительную информацию см. в разделе [шаблон `forRoot()`](guide/singleton-services#forRoot) руководства [Singleton Services](guide/singleton-services).

<a id="preloading"></a>

## Предварительная загрузка

Предварительная загрузка улучшает UX, загружая части вашего приложения в фоновом режиме. Вы можете предварительно загружать модули, отдельные компоненты или данные компонента.

### Предварительная загрузка модулей и отдельных компонентов

Предварительная загрузка модулей и отдельных компонентов улучшает UX, загружая части вашего приложения в фоновом режиме. Благодаря этому пользователям не нужно ждать загрузки элементов при активации маршрута.

Чтобы включить предварительную загрузку всех лениво загруженных модулей и автономных компонентов, импортируйте маркер `PreloadAllModules` из Angular `router`.

### Приложение на основе модулей

<code-example header="AppRoutingModule (excerpt)">

import { PreloadAllModules } from '&commat;angular/router';

</code-example>

Все еще в `AppRoutingModule`, укажите стратегию предварительной загрузки в `forRoot()`.

<code-example header="AppRoutingModule (excerpt)">

RouterModule.forRoot( appRoutes,
{

preloadingStrategy: PreloadAllModules

}

)

</code-example>

### Автономное приложение

Для автономных приложений настройте стратегии предварительной загрузки, добавив `withPreloading` к `provideRouter`s RouterFeatures в `app.config.ts`.

<code-example header="`app.config.ts`">

import { ApplicationConfig } from '@angular/core'; import {
PreloadAllModules,

provideRouter

withPreloading,

} из '@angular/router';

import { routes } from './app.routes';

export const appConfig: ApplicationConfig = { providers: [

provideRouter(

routes,

withPreloading(PreloadAllModules)

),

],

};

</code-example>

### Предварительная загрузка данных компонента

Чтобы предварительно загрузить данные компонента, используйте `резольвер`. Резольверы улучшают UX, блокируя загрузку страницы до тех пор, пока не будут доступны все необходимые данные для полного отображения страницы.

#### Резольверы

Создайте службу резольвера. С помощью Angular CLI команда для создания службы выглядит следующим образом:

<code-example format="shell" language="shell">

ng generate service &lt;service-name&gt;

</code-example>

Во вновь созданном сервисе реализуйте интерфейс `Resolve`, предоставляемый пакетом `@angular/router`:

<code-example header="Resolver service (excerpt)">

import { Resolve } from '&commat;angular/router';

&hellip;

/_ Интерфейс, представляющий вашу модель данных _/ export interface Crisis {

id: число;

name: string;

}

export class CrisisDetailResolverService implements Resolve&lt;Crisis&gt; { resolve(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable&lt;Crisis&gt; {

// ваша логика здесь

}

}

</code-example>

Импортируйте этот резольвер в модуль маршрутизации вашего модуля.

<code-example header="Feature module's routing module (excerpt)">

import { CrisisDetailResolverService } from './crisis-detail-resolver.service';

</code-example>

Добавьте объект `resolve` в конфигурацию `route` компонента.

<code-example header="Feature module's routing module (excerpt)">

{ path: '/your-path',
компонент: YourComponent,

resolve: {

кризис: CrisisDetailResolverService

}

}

</code-example>

В конструкторе компонента введите экземпляр класса `ActivatedRoute`, который представляет текущий маршрут.

<code-example header="Component's constructor (excerpt)">

import { ActivatedRoute } from '&commat;angular/router';

&commat;Component({ &hellip; }) class YourComponent {

constructor(private route: ActivatedRoute) {}

}

</code-example>

Используйте инжектированный экземпляр класса `ActivatedRoute` для доступа к `данным`, связанным с данным маршрутом.

<code-example header="Component's ngOnInit lifecycle hook (excerpt)">

import { ActivatedRoute } from '&commat;angular/router';

&commat;Component({ &hellip; }) class YourComponent {

constructor(private route: ActivatedRoute) {}

ngOnInit() { this.route.data

.subscribe(data =&gt; {

const crisis: Crisis = data.crisis;

// &hellip;

});

}

}

</code-example>

Для получения дополнительной информации и рабочего примера смотрите раздел [учебника по маршрутизации, посвященный предварительной загрузке] (guide/router-tutorial-toh#preloading-background-loading-of-feature-areas).

## Устранение неполадок при ленивой загрузке модулей

Распространенной ошибкой при ленивой загрузке модулей является импорт общих модулей в несколько мест в приложении. Для проверки этого условия сначала создайте модуль с помощью Angular CLI и включите параметр `--route route-name`, где `route-name` - это имя вашего модуля.

Затем создайте модуль без параметра `--route`.

Если `ng generate module` с параметром `--route` возвращает ошибку, а без него работает правильно, возможно, вы импортировали один и тот же модуль в нескольких местах.

Помните, что многие общие модули Angular должны быть импортированы в основу вашего приложения.

Для получения дополнительной информации о модулях Angular смотрите [NgModules](guide/ngmodules).

## Подробнее о NgModules и маршрутизации.

Вам также может быть интересно следующее:

-   [Маршрутизация и навигация](guide/router)

-   [Провайдеры](guide/providers)

-   [Типы модулей функций](guide/module-types)

-   [Разделение кода на уровне маршрутов в Angular](https://web.dev/route-level-code-splitting-in-angular)

-   [Стратегии предварительной загрузки маршрутов в Angular](https://web.dev/route-preloading-in-angular)

<!-- links -->

<!-- external links -->

<!-- end links -->

:date: 7.05.2022
