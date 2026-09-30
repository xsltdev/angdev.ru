---
description: "Декларативные ссылки ведут по маршрутам приложения без полной перезагрузки страницы."
---

# Переход к маршрутам {: #navigate-to-routes}

:date: 30.09.2026

Директива `RouterLink` — декларативный способ навигации в Angular. Через неё обычные якорные элементы (`<a>`) встраиваются в систему маршрутизации.

## Как использовать RouterLink {: #how-to-use-routerlink}

Вместо обычного элемента `<a>` с атрибутом `href` на ссылку вешают директиву `RouterLink` с нужным путём, и переход идёт через маршрутизацию Angular.

```ts
import {RouterLink} from '@angular/router';

@Component({
  template: `
    <nav>
      <a routerLink="/user-profile">User profile</a>
      <a routerLink="/settings">Settings</a>
    </nav>
  `,
  imports: [RouterLink],
  ...
})
export class App {}
```

### Абсолютные и относительные ссылки {: #using-absolute-or-relative-links}

**Относительные URL** в маршрутизации Angular задают путь от текущего положения маршрута. **Абсолютные URL** содержат полный путь вместе с протоколом (например, `http://`) и **корневым доменом** (например, `google.com`).

```html
<!-- Absolute URL -->
<a href="https://www.angular.dev/essentials">Angular Essentials Guide</a>

<!-- Relative URL -->
<a href="/essentials">Angular Essentials Guide</a>
```

В первом примере у страницы essentials явно указаны протокол (`https://`) и корневой домен (`angular.dev`). Во втором переход на `/essentials` рассчитан на то, что пользователь уже находится на нужном корневом домене.

Относительные URL проще сопровождать: им не нужно знать своё абсолютное место в иерархии маршрутов.

### Как устроены относительные URL {: #how-relative-urls-work}

Относительные URL в маршрутизации Angular задают двумя синтаксисами: строкой и массивом.

```html
<!-- Navigates user to /dashboard -->
<a routerLink="dashboard">Dashboard</a>
<a [routerLink]="['dashboard']">Dashboard</a>
```

!!! tip ""

    Строка — самый частый способ задать относительный URL.

Динамические параметры в относительном URL задают синтаксисом массива:

```html
<a [routerLink]="['user', currentUserId]">Current User</a>
```

Косая черта (`/`) в начале относительного пути привязывает его к корню домена. Без неё путь считается от текущего URL.

Если пользователь находится на `example.com/settings`, относительные пути для разных случаев выглядят так:

```html
<!-- Navigates to /settings/notifications -->
<a routerLink="notifications">Notifications</a>
<a routerLink="/settings/notifications">Notifications</a>

<!-- Navigates to /team/:teamId/user/:userId -->
<a routerLink="/team/123/user/456">User 456</a>
<a [routerLink]="['/team', teamId, 'user', userId]">Current User</a>
```

## Программный переход к маршрутам {: #programmatic-navigation-to-routes}

`RouterLink` закрывает декларативную навигацию в шаблонах. Программная навигация нужна, когда переход зависит от логики, действия пользователя или состояния приложения. Внедрив `Router`, из кода TypeScript переходят на маршруты, передают параметры и управляют поведением навигации.

### `router.navigate()` {: #routernavigate}

Метод `router.navigate()` выполняет программный переход между маршрутами по массиву сегментов URL.

```ts
import {Router} from '@angular/router';

@Component({
  selector: 'app-dashboard',
  template: ` <button (click)="navigateToProfile()">View Profile</button> `,
})
export class AppDashboard {
  private router = inject(Router);

  navigateToProfile() {
    // Standard navigation
    this.router.navigate(['/profile']);

    // With route parameters
    this.router.navigate(['/users', userId]);

    // With query parameters
    this.router.navigate(['/search'], {
      queryParams: {category: 'books', sort: 'price'},
    });

    // With matrix parameters
    this.router.navigate(['/products', {featured: true, onSale: true}]);
  }
}
```

`router.navigate()` покрывает и простые, и составные переходы: в вызов передают параметры маршрута, [параметры запроса](read-route-state.md#query-parameters) и настройки поведения навигации.

Динамический путь от положения компонента в дереве маршрутов собирают параметром `relativeTo`.

```ts
import {Router, ActivatedRoute} from '@angular/router';

@Component({
  selector: 'app-user-detail',
  template: `
    <button (click)="navigateToEdit()">Edit User</button>
    <button (click)="navigateToParent()">Back to List</button>
  `,
})
export class UserDetail {
  private route = inject(ActivatedRoute);
  private router = inject(Router);

  // Navigate to a sibling route
  navigateToEdit() {
    // From: /users/123
    // To:   /users/123/edit
    this.router.navigate(['edit'], {relativeTo: this.route});
  }

  // Navigate to parent
  navigateToParent() {
    // From: /users/123
    // To:   /users
    this.router.navigate(['..'], {relativeTo: this.route});
  }

  navigateToList() {
    // Angular resolves the commands array as a single navigation path relative to the current route.
    // From: /users/123
    // Result: /users/list
    this.router.navigate(['..', 'list'], {relativeTo: this.route});
  }
}
```

При подъёме на несколько уровней все сегменты `..` стоят в **первом элементе** массива команд. Маршрутизатор разбирает `..` только из первой строки команды, а следующие элементы массива считает буквальными сегментами пути.

```ts
// From: /team/123/users/456
// Result: /team/123/settings
this.router.navigate(['../../settings'], {relativeTo: this.route});
```

Вместе с `relativeTo` первую команду не начинают с `/`. Начальный `/` делает переход абсолютным, и `relativeTo` не учитывается.

```ts
// From: /team/123/users/456
// Result: /team/123/users/456/edit
this.router.navigate(['edit'], {relativeTo: this.route});
```

```ts
// From: /team/123/users/456
// Leading '/' causes absolute navigation — relativeTo is ignored
// Result: /edit
this.router.navigate(['/edit'], {relativeTo: this.route});
```

### `router.navigateByUrl()` {: #routernavigatebyurl}

Метод `router.navigateByUrl()` выполняет программный переход по строке пути, а не по массиву сегментов. Он удобен, когда есть полный путь и нужен абсолютный переход: внешние адреса и глубокие ссылки.

```ts
// Standard route navigation
router.navigateByUrl('/products');

// Navigate to nested route
router.navigateByUrl('/products/featured');

// Complete URL with parameters and fragment
router.navigateByUrl('/products/123?view=details#reviews');

// Navigate with query parameters
router.navigateByUrl('/search?category=books&sortBy=price');

// With matrix parameters
router.navigateByUrl('/sales-awesome;isOffer=true;showModal=false');
```

Чтобы заменить текущий URL в истории, в `navigateByUrl` передают объект конфигурации с параметром `replaceUrl`.

```ts
// Replace current URL in history
router.navigateByUrl('/checkout', {
  replaceUrl: true,
});
```

### Другой адрес в адресной строке {: #display-a-different-url-in-the-address-bar}

Параметр `browserUrl` метода `navigateByUrl` показывает в адресной строке браузера другой URL, не тот, по которому сопоставляется маршрут.

Так пользователя отправляют на другой маршрут, например на страницу ошибки, а в строке остаётся адрес, который он открывал изначально.

```ts
router.navigateByUrl('/not-found', {browserUrl: '/products/missing-item'});
```

Angular переходит на маршрут `/not-found` и отрисовывает его, а в адресной строке браузера остаётся `/products/missing-item`.

!!! info ""

    `browserUrl` меняет только то, что видно в адресной строке браузера.

## Адрес в браузере через RouterLink {: #customizing-the-browser-url-with-routerlink}

У директивы `RouterLink` тоже есть вход `browserUrl`. Он задаёт URL в адресной строке браузера при щелчке по ссылке отдельно от маршрута, на который переходит Angular.

```html
<!-- Navigates to /dashboard, but the address bar shows /home -->
<a [routerLink]="['/dashboard']" [browserUrl]="'/home'">Go to Dashboard</a>
```

Для более динамичных случаев привязывают `UrlTree`:

```ts
import {Component, inject} from '@angular/core';
import {Router, RouterLink, UrlTree} from '@angular/router';

@Component({
  template: `
    <a [routerLink]="['/products', product.id]" [browserUrl]="displayUrl">
      {{ product.name }}
    </a>
  `,
  imports: [RouterLink],
})
export class ProductList {
  private router = inject(Router);

  product = {id: 42, name: 'Widget'};

  // Create a UrlTree to display in the address bar
  displayUrl: UrlTree = this.router.createUrlTree(['/products', 'widget']);
}
```

## Что дальше {: #next-steps}

Как [читать состояние маршрута](read-route-state.md), чтобы компоненты реагировали на контекст.


---

Источник: [https://angular.dev/guide/routing/navigate-to-routes](https://angular.dev/guide/routing/navigate-to-routes)
