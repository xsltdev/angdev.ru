---
description: "Директива точки выхода отмечает место, где маршрутизатор отрисовывает компонент текущего адреса."
---

# Показ маршрутов в точках выхода {: #show-routes-with-outlets}

:date: 30.09.2026

Директива `RouterOutlet` — заполнитель. Она отмечает место, где маршрутизатор отрисовывает компонент текущего адреса.

```html
<app-header />
<!-- Angular inserts your route content here -->
<router-outlet />
<app-footer />
```

```ts
import {Component} from '@angular/core';
import {RouterOutlet} from '@angular/router';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App {}
```

Если в приложении заданы такие маршруты:

```ts
import {Routes} from '@angular/router';
import {Home} from './home';
import {Products} from './products';

const routes: Routes = [
  {
    path: '',
    component: Home,
    title: 'Home Page',
  },
  {
    path: 'products',
    component: Products,
    title: 'Our Products',
  },
];
```

Когда пользователь открывает `/products`, Angular отрисовывает:

```html
<app-header />
<app-products />
<app-footer />
```

Если пользователь возвращается на главную, Angular отрисовывает:

```html
<app-header />
<app-home />
<app-footer />
```

При показе маршрута элемент `<router-outlet>` остаётся в DOM и служит ориентиром для следующих переходов. Angular вставляет содержимое маршрута сразу после точки выхода, соседним узлом.

```html
<!-- Contents of the component's template -->
<app-header />
<router-outlet />
<app-footer />
```

```html
<!-- Content rendered on the page when the user visits /admin -->
<app-header />
<router-outlet />
<app-admin-page />
<app-footer />
```

## Вложенность через дочерние маршруты {: #nesting-routes-with-child-routes}

Когда приложение усложняется, маршруты привязывают не только к корневому компоненту. Тогда при смене URL меняется часть приложения, и у пользователя не возникает ощущения, что обновилась вся страница.

Такие вложенные маршруты называют дочерними. В приложение добавляют второй `<router-outlet>` — вдобавок к `<router-outlet>` в `AppComponent`.

В примере компонент `Settings` показывает нужную панель по выбору пользователя. У дочерних маршрутов в компоненте часто есть собственные `<nav>` и `<router-outlet>`.

```html
<h1>Settings</h1>
<nav>
  <ul>
    <li><a routerLink="profile">Profile</a></li>
    <li><a routerLink="security">Security</a></li>
  </ul>
</nav>
<router-outlet />
```

Дочернему маршруту, как и любому другому, нужны `path` и `component`. Его кладут в массив `children` родительского маршрута.

```ts
const routes: Routes = [
  {
    path: 'settings',
    component: Settings, // this is the component with the <router-outlet> in the template
    children: [
      {
        path: 'profile', // child route path
        component: Profile, // child route component that the router renders
      },
      {
        path: 'security',
        component: Security, // another child route component that the router renders
      },
    ],
  },
];
```

Когда `routes` и `<router-outlet>` настроены, приложение работает с вложенными маршрутами.

## Вторичные маршруты и именованные точки выхода {: #secondary-routes-with-named-outlets}

На странице может быть несколько точек выхода. Каждой задают имя, чтобы указать, какое содержимое куда попадает.

```html
<app-header />
<router-outlet />
<router-outlet name="read-more" />
<router-outlet name="additional-actions" />
<app-footer />
```

Имя каждой точки выхода уникально. Задать или изменить его динамически нельзя. По умолчанию имя — `'primary'`.

Angular сопоставляет имя точки выхода со свойством `outlet` маршрута:

```ts
{
  path: 'user/:id',
  component: UserDetails,
  outlet: 'additional-actions'
}
```

## События жизненного цикла точки выхода {: #outlet-lifecycle-events}

Точка выхода маршрутизатора порождает четыре события жизненного цикла:

| Событие      | Описание                                                                      |
| ------------ | ----------------------------------------------------------------------------- |
| `activate`   | Создаётся новый экземпляр компонента                                         |
| `deactivate` | Компонент уничтожается                                                        |
| `attach`     | `RouteReuseStrategy` указывает точке выхода присоединить поддерево           |
| `detach`     | `RouteReuseStrategy` указывает точке выхода отсоединить поддерево            |

Обработчики добавляют обычным синтаксисом привязки события:

```html
<router-outlet
  (activate)="onActivate($event)"
  (deactivate)="onDeactivate($event)"
  (attach)="onAttach($event)"
  (detach)="onDetach($event)"
/>
```

Подробнее — в [документации API `RouterOutlet`](https://angular.dev/api/router/RouterOutlet).

## Контекстные данные для компонентов маршрута {: #passing-contextual-data-to-routed-components}

Контекст для компонента маршрута часто тянет за собой глобальное состояние или сложную конфигурацию маршрутов. Чтобы обойтись без этого, у каждого `RouterOutlet` есть вход `routerOutletData`. Компонент маршрута и его потомки читают эти данные как сигнал через токен инъекции `ROUTER_OUTLET_DATA`. Настройка остаётся у точки выхода, и определения маршрутов менять не нужно.

```ts
import {Component} from '@angular/core';
import {RouterOutlet} from '@angular/router';

@Component({
  selector: 'app-dashboard',
  imports: [RouterOutlet],
  template: `
    <h2>Dashboard</h2>
    <router-outlet [routerOutletData]="{layout: 'sidebar'}" />
  `,
})
export class Dashboard {}
```

Компонент маршрута внедряет данные точки выхода через `ROUTER_OUTLET_DATA`:

```ts
import {Component, inject} from '@angular/core';
import {ROUTER_OUTLET_DATA} from '@angular/router';

@Component({
  selector: 'app-stats',
  template: `<p>Stats view (layout: {{ outletData().layout }})</p>`,
})
export class Stats {
  outletData = inject(ROUTER_OUTLET_DATA) as Signal<{layout: string}>;
}
```

Когда Angular активирует `Stats` в этой точке выхода, внедрённые данные равны `{ layout: 'sidebar' }`.

!!! info ""

    Если вход `routerOutletData` не задан, внедрённое значение по умолчанию равно `null`.

---

## Что дальше {: #next-steps}

Как [переходить к маршрутам](navigate-to-routes.md) с помощью Angular Router.


---

Источник: [https://angular.dev/guide/routing/show-routes-with-outlets](https://angular.dev/guide/routing/show-routes-with-outlets)
