---
description: "По данным маршрута компоненты реагируют на текущий адрес и контекст."
---

# Чтение состояния маршрута {: #read-route-state}

:date: 30.09.2026

Angular Router позволяет читать данные, связанные с маршрутом, и строить компоненты, которые реагируют на контекст.

## Сведения о текущем маршруте через ActivatedRoute {: #get-information-about-the-current-route-with-activatedroute}

`ActivatedRoute` — сервис из `@angular/router`. В нём собраны все данные текущего маршрута.

```ts
import {Component} from '@angular/core';
import {ActivatedRoute} from '@angular/router';

@Component({
  selector: 'app-product',
})
export class Product {
  private activatedRoute = inject(ActivatedRoute);

  constructor() {
    console.log(this.activatedRoute);
  }
}
```

`ActivatedRoute` отдаёт разные сведения о маршруте. Часто используют такие свойства:

| Свойство      | Подробности                                                                                                                |
| :------------ | :------------------------------------------------------------------------------------------------------------------------- |
| `url`         | `Observable` путей маршрута: массив строк, по одной на каждую часть пути.                                                 |
| `data`        | `Observable` с объектом `data`, заданным для маршрута. Сюда же попадают значения, которые разрешил охранник `resolve`.    |
| `params`      | `Observable` обязательных и необязательных параметров именно этого маршрута.                                              |
| `queryParams` | `Observable` параметров запроса, доступных всем маршрутам.                                                                |
| `resources`   | Необязательная запись экземпляров `Resource`, объявленных на маршруте (когда включён `withRouterResources`).              |

Полный список того, что можно прочитать у маршрута, — в [документации API `ActivatedRoute`](https://angular.dev/api/router/ActivatedRoute).

## Снимки маршрута {: #understanding-route-snapshots}

Переходы между страницами — события во времени. Состояние маршрутизатора в конкретный момент даёт снимок маршрута.

В снимке — основные данные маршрута: параметры, данные и дочерние маршруты. Снимок статичен и не отражает последующие изменения.

Пример чтения снимка маршрута:

```ts
import {ActivatedRoute, ActivatedRouteSnapshot} from '@angular/router';

@Component(/* ... */)
export class UserProfile {
  readonly userId: string;
  private route = inject(ActivatedRoute);

  constructor() {
    // Example URL: https://www.angular.dev/users/123?role=admin&status=active#contact

    // Access route parameters from snapshot
    this.userId = this.route.snapshot.paramMap.get('id');

    // Access multiple route elements
    const snapshot = this.route.snapshot;
    console.log({
      url: snapshot.url, // https://www.angular.dev
      // Route parameters object: {id: '123'}
      params: snapshot.params,
      // Query parameters object: {role: 'admin', status: 'active'}
      queryParams: snapshot.queryParams, // Query parameters
    });
  }
}
```

Полный список свойств — в [документации API `ActivatedRoute`](https://angular.dev/api/router/ActivatedRoute) и [документации API `ActivatedRouteSnapshot`](https://angular.dev/api/router/ActivatedRouteSnapshot).

## Чтение параметров маршрута {: #reading-parameters-on-a-route}

Из маршрута читают два вида параметров: параметры маршрута и параметры запроса.

### Параметры маршрута {: #route-parameters}

Параметры маршрута передают данные в компонент через URL. Так показывают конкретное содержимое по идентификатору в адресе, например пользователя или товара.

[Параметры маршрута](define-routes.md#define-url-paths-with-route-parameters) задают, поставив перед именем двоеточие (`:`).

```ts
import {Routes} from '@angular/router';
import {Product} from './product';

const routes: Routes = [{path: 'product/:id', component: Product}];
```

Параметры читают подпиской на `route.params`.

```ts
import {Component, inject, signal} from '@angular/core';
import {ActivatedRoute} from '@angular/router';

@Component({
  selector: 'app-product-detail',
  template: `<h1>Product Details: {{ productId() }}</h1>`,
})
export class ProductDetail {
  productId = signal('');
  private activatedRoute = inject(ActivatedRoute);

  constructor() {
    // Access route parameters
    this.activatedRoute.params.subscribe((params) => {
      this.productId.set(params['id']);
    });
  }
}
```

### Параметры запроса {: #query-parameters}

[Параметры запроса](https://developer.mozilla.org/en-US/docs/Web/API/URLSearchParams) передают необязательные данные через URL и не меняют структуру маршрута. Они сохраняются между переходами и подходят для фильтрации, сортировки, постраничного вывода и других элементов интерфейса, у которых есть состояние.

```ts
// Single parameter structure
// /products?category=electronics
router.navigate(['/products'], {
  queryParams: {category: 'electronics'},
});

// Multiple parameters
// /products?category=electronics&sort=price&page=1
router.navigate(['/products'], {
  queryParams: {
    category: 'electronics',
    sort: 'price',
    page: 1,
  },
});
```

Параметры запроса читают через `route.queryParams`.

Ниже `ProductList` обновляет параметры запроса, от которых зависит показ списка товаров:

```ts
import {ActivatedRoute, Router} from '@angular/router';

@Component({
  selector: 'app-product-list',
  template: `
    <div>
      <select (change)="updateSort($event)">
        <option value="price">Price</option>
        <option value="name">Name</option>
      </select>
      <!-- Products list -->
    </div>
  `,
})
export class ProductList {
  private route = inject(ActivatedRoute);
  private router = inject(Router);

  constructor() {
    // Access query parameters reactively
    this.route.queryParams.subscribe((params) => {
      const sort = params['sort'] || 'price';
      const page = Number(params['page']) || 1;
      this.loadProducts(sort, page);
    });
  }

  updateSort(event: Event) {
    const sort = (event.target as HTMLSelectElement).value;
    // Update URL with new query parameter
    this.router.navigate([], {
      queryParams: {sort},
      queryParamsHandling: 'merge', // Preserve other query parameters
    });
  }
}
```

В примере список товаров сортируют по имени или цене через элемент `select`. Обработчик изменения пишет новые параметры запроса в URL, подписка читает их и обновляет список.

Подробнее — в [документации `QueryParamsHandling`](https://angular.dev/api/router/QueryParamsHandling).

### Матричные параметры {: #matrix-parameters}

Матричные параметры необязательны и принадлежат конкретному сегменту URL, а не всему маршруту. Параметры запроса стоят после `?` и действуют на весь адрес. Матричные параметры записывают через точку с запятой (`;`) и ограничивают одним сегментом пути.

Матричные параметры передают вспомогательные данные в конкретный сегмент маршрута и не влияют ни на определение маршрута, ни на сопоставление. Как и параметры запроса, их не объявляют в конфигурации маршрутов.

```ts
// URL format: /path;key=value
// Multiple parameters: /path;key1=value1;key2=value2

// Navigate with matrix parameters
this.router.navigate(['/awesome-products', {view: 'grid', filter: 'new'}]);
// Results in URL: /awesome-products;view=grid;filter=new
```

**Через ActivatedRoute**

```ts
import {Component, inject} from '@angular/core';
import {ActivatedRoute} from '@angular/router';

@Component(/* ... */)
export class AwesomeProducts {
  private route = inject(ActivatedRoute);

  constructor() {
    // Access matrix parameters via params
    this.route.params.subscribe((params) => {
      const view = params['view']; // e.g., 'grid'
      const filter = params['filter']; // e.g., 'new'
    });
  }
}
```

!!! info ""

    Матричные параметры также попадают во входы компонента, если включён `withComponentInputBinding`. Это вариант чтения помимо `ActivatedRoute`.

## Текущий активный маршрут через RouterLinkActive {: #detect-active-current-route-with-routerlinkactive}

Директива `RouterLinkActive` динамически оформляет элементы навигации по текущему активному маршруту. Так в меню видно, какой пункт сейчас открыт.

```html
<nav>
  <a
    class="button"
    routerLink="/about"
    routerLinkActive="active-button"
    ariaCurrentWhenActive="page"
  >
    About
  </a>
  |
  <a
    class="button"
    routerLink="/settings"
    routerLinkActive="active-button"
    ariaCurrentWhenActive="page"
  >
    Settings
  </a>
</nav>
```

В примере Angular Router добавляет класс `active-button` нужной ссылке и выставляет `ariaCurrentWhenActive` в `page`, когда URL совпадает с соответствующим `routerLink`.

Несколько классов задают строкой через пробел или массивом:

```html
<!-- Space-separated string syntax -->
<a routerLink="/user/bob" routerLinkActive="class1 class2">Bob</a>

<!-- Array syntax -->
<a routerLink="/user/bob" [routerLinkActive]="['class1', 'class2']">Bob</a>
```

Значение `routerLinkActive` одновременно становится значением `ariaCurrentWhenActive`. Так активную кнопку узнают и пользователи, которые не различают смену оформления.

Другое значение для aria задают явно директивой `ariaCurrentWhenActive`.

### Стратегия сопоставления маршрута {: #route-matching-strategy}

По умолчанию `RouterLinkActive` считает совпадением и предков маршрута.

```html
<a [routerLink]="['/user/jane']" routerLinkActive="active-link"> User </a>
<a [routerLink]="['/user/jane/role/admin']" routerLinkActive="active-link"> Role </a>
```

Когда пользователь открывает `/user/jane/role/admin`, класс `active-link` получают обе ссылки.

### RouterLinkActive только при точном совпадении {: #only-apply-routerlinkactive-on-exact-route-matches}

Чтобы класс появлялся только при точном совпадении, директиве `routerLinkActiveOptions` передают объект с `exact: true`.

```html
<a
  [routerLink]="['/user/jane']"
  routerLinkActive="active-link"
  [routerLinkActiveOptions]="{exact: true}"
>
  User
</a>
<a
  [routerLink]="['/user/jane/role/admin']"
  routerLinkActive="active-link"
  [routerLinkActiveOptions]="{exact: true}"
>
  Role
</a>
```

Если сопоставление нужно настроить точнее, `exact: true` раскрывается в полный набор параметров:

```ts
// `exact: true` is equivalent to
{
  paths: 'exact',
  fragment: 'ignored',
  matrixParams: 'ignored',
  queryParams: 'exact',
}

// `exact: false` is equivalent
{
  paths: 'subset',
  fragment: 'ignored',
  matrixParams: 'ignored',
  queryParams: 'subset',
}
```

Подробнее — в документации [isActiveMatchOptions](https://angular.dev/api/router/IsActiveMatchOptions).

### RouterLinkActive на элементе-предке {: #apply-routerlinkactive-to-an-ancestor}

Директиву `RouterLinkActive` вешают и на элемент-предок, чтобы оформить нужные элементы.

```html
<div routerLinkActive="active-link" [routerLinkActiveOptions]="{exact: true}">
  <a routerLink="/user/jim">Jim</a>
  <a routerLink="/user/bob">Bob</a>
</div>
```

Подробнее — в [документации API `RouterLinkActive`](https://angular.dev/api/router/RouterLinkActive).

## Проверка, активен ли адрес {: #check-if-a-url-is-active}

Функция `isActive` возвращает вычисляемый сигнал: активен ли заданный URL в маршрутизаторе. Сигнал обновляется сам, когда меняется состояние маршрутизатора.

```ts
import {Component, inject} from '@angular/core';
import {isActive, Router} from '@angular/router';

@Component({
  template: `
    <div [class.active]="isSettingsActive()">
      <h2>Settings</h2>
    </div>
  `,
})
export class Panel {
  private router = inject(Router);

  isSettingsActive = isActive('/settings', this.router, {
    paths: 'subset',
    queryParams: 'ignored',
    fragment: 'ignored',
    matrixParams: 'ignored',
  });
}
```


---

Источник: [https://angular.dev/guide/routing/read-route-state](https://angular.dev/guide/routing/read-route-state)
