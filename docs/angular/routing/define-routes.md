---
description: "Маршруты задают основу навигации внутри приложения."
---

# Определение маршрутов {: #define-routes}

:date: 30.09.2026

Маршруты задают основу навигации внутри приложения Angular.

## Что такое маршруты? {: #what-are-routes}

В Angular **маршрут** — объект. Он задаёт, какой компонент отрисовать для конкретного пути или шаблона URL, и дополнительные параметры того, что происходит при переходе пользователя на этот адрес.

Базовый пример маршрута:

```ts
import {AdminPage} from './app-admin';

const adminPage = {
  path: 'admin',
  component: AdminPage,
};
```

Для этого маршрута при переходе на путь `/admin` приложение показывает компонент `AdminPage`.

### Как хранить маршруты в приложении {: #managing-routes-in-your-application}

В большинстве проектов маршруты выносят в отдельный файл, в имени которого есть `routes`.

Набор маршрутов выглядит так:

```ts
import {Routes} from '@angular/router';
import {HomePage} from './home-page';
import {AdminPage} from './admin-page';

export const routes: Routes = [
  {
    path: '',
    component: HomePage,
  },
  {
    path: 'admin',
    component: AdminPage,
  },
];
```

!!! tip ""

    Если проект создан через Angular CLI, маршруты заданы в `src/app/app.routes.ts`.

### Подключение маршрутизатора к приложению {: #adding-the-router-to-your-application}

При запуске приложения Angular без Angular CLI в конфигурацию передают объект с массивом `providers`.

В массив `providers` маршрутизатор добавляют вызовом `provideRouter` со списком маршрутов.

```ts
import {ApplicationConfig} from '@angular/core';
import {provideRouter} from '@angular/router';

import {routes} from './app.routes';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    // ...
  ],
};
```

## Пути URL маршрутов {: #route-url-paths}

### Статические пути URL {: #static-url-paths}

Статические пути — маршруты с заранее заданным адресом, который не меняется из-за динамических параметров. Такой маршрут точно совпадает со строкой `path` и всегда приводит к одному результату.

Примеры:

-   "/admin"
-   "/blog"
-   "/settings/account"

### Пути URL с параметрами маршрута {: #define-url-paths-with-route-parameters}

Параметризованные адреса задают динамические пути: на один компонент ведёт несколько адресов, а данные на экране зависят от параметров в адресе.

Такой шаблон задают параметрами в строке `path`: перед именем каждого параметра ставят двоеточие (`:`).

!!! warning ""

    Параметры пути и сведения в [строке запроса](https://en.wikipedia.org/wiki/Query_string) — разные вещи. Подробнее о [параметрах запроса в Angular](read-route-state.md#query-parameters).

В примере ниже компонент профиля показывается по идентификатору пользователя из адреса.

```ts
import {Routes} from '@angular/router';
import {UserProfile} from './user-profile/user-profile';

const routes: Routes = [{path: 'user/:id', component: UserProfile}];
```

Адреса вроде `/user/leeroy` и `/user/jenkins` отрисовывают компонент `UserProfile`. Компонент читает параметр `id` и выполняет дальнейшую работу, например загрузку данных. Как читать параметры маршрута, описано в разделе [Чтение состояния маршрута](read-route-state.md).

Допустимое имя параметра маршрута начинается с буквы (a-z, A-Z) и содержит только:

-   буквы (a-z, A-Z)
-   цифры (0-9)
-   подчёркивание (\_)
-   дефис (-)

Путь может содержать и несколько параметров:

```ts
import {Routes} from '@angular/router';
import {UserProfile} from './user-profile';
import {SocialMediaFeed} from './social-media-feed';

const routes: Routes = [
  {path: 'user/:id/:social-media', component: SocialMediaFeed},
  {path: 'user/:id/', component: UserProfile},
];
```

С таким путём по адресам `/user/leeroy/youtube` и `/user/leeroy/bluesky` открывается лента соответствующей соцсети для пользователя leeroy.

Как читать параметры маршрута, описано в разделе [Чтение состояния маршрута](read-route-state.md).

### Подстановочные маршруты {: #wildcards}

Чтобы поймать все адреса для заданного пути, используют подстановочный маршрут: его задают двойной звёздочкой (`**`).

Частый пример — компонент страницы «не найдено».

```ts
import {Home} from './home/home';
import {UserProfile} from './user-profile';
import {NotFound} from './not-found';

const routes: Routes = [
  {path: 'home', component: Home},
  {path: 'user/:id', component: UserProfile},
  {path: '**', component: NotFound},
];
```

В этом массиве приложение показывает компонент `NotFound`, когда пользователь открывает любой путь, кроме `home` и `user/:id`.

!!! tip ""

    Подстановочные маршруты обычно ставят в конец массива маршрутов.

## Как Angular сопоставляет URL {: #how-angular-matches-urls}

Порядок маршрутов важен: Angular берёт первое совпадение. Как только URL совпал с `path` маршрута, остальные маршруты уже не проверяются. Более конкретные маршруты ставьте раньше менее конкретных.

В примере маршруты идут от самого конкретного к самому общему:

```ts
const routes: Routes = [
  {path: '', component: Home}, // Empty path
  {path: 'users/new', component: NewUser}, // Static, most specific
  {path: 'users/:id', component: UserDetail}, // Dynamic
  {path: 'users', component: Users}, // Static, less specific
  {path: '**', component: NotFound}, // Wildcard - always last
];
```

Если пользователь открывает `/users/new`, маршрутизатор Angular проходит такие шаги:

1.  Проверяет `''` — совпадения нет
1.  Проверяет `users/new` — есть совпадение, проверка останавливается
1.  До `users/:id` дело не доходит, хотя этот путь тоже мог бы совпасть
1.  До `users` дело не доходит
1.  До `**` дело не доходит

## Перенаправления {: #redirects}

Маршрут может перенаправлять на другой маршрут и не отрисовывать компонент:

```ts
import {Blog} from './home/blog';

const routes: Routes = [
  {
    path: 'articles',
    redirectTo: '/blog',
  },
  {
    path: 'blog',
    component: Blog,
  },
];
```

Если маршрут изменили или удалили, часть пользователей всё ещё откроет устаревшую ссылку или закладку. Перенаправление отправит их на подходящий маршрут, а не на страницу «не найдено».

## Заголовки страниц {: #page-titles}

Каждому маршруту можно задать **заголовок**. При активации маршрута Angular сам обновляет [заголовок страницы](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/title). Задавайте осмысленные заголовки: они нужны, чтобы приложение оставалось доступным.

```ts
import {Routes} from '@angular/router';
import {Home} from './home';
import {About} from './about';
import {Products} from './products';

const routes: Routes = [
  {
    path: '',
    component: Home,
    title: 'Home Page',
  },
  {
    path: 'about',
    component: About,
    title: 'About Us',
  },
];
```

Свойство `title` страницы можно задать динамически функцией-резолвером через [`ResolveFn`](https://angular.dev/api/router/ResolveFn).

```ts
const titleResolver: ResolveFn<string> = (route) => route.queryParams['id'];
const routes: Routes = [
  ...{
    path: 'products',
    component: Products,
    title: titleResolver,
  },
];
```

Заголовки маршрутов также задаёт сервис, который расширяет абстрактный класс [`TitleStrategy`](https://angular.dev/api/router/TitleStrategy). По умолчанию Angular использует [`DefaultTitleStrategy`](https://angular.dev/api/router/DefaultTitleStrategy).

### Заголовки страниц через TitleStrategy {: #using-titlestrategy-for-page-titles}

Когда состав заголовка документа нужно собирать в одном месте, реализуйте `TitleStrategy`.

`TitleStrategy` — токен, которым подменяют стратегию заголовков Angular по умолчанию. Своя реализация задаёт соглашения: суффикс приложения, заголовок из хлебных крошек или заголовок из данных маршрута.

```ts
import {inject, Injectable} from '@angular/core';
import {Title} from '@angular/platform-browser';
import {TitleStrategy, RouterStateSnapshot} from '@angular/router';

@Injectable()
export class AppTitleStrategy extends TitleStrategy {
  private readonly title = inject(Title);

  updateTitle(snapshot: RouterStateSnapshot): void {
    // PageTitle is equal to the "Title" of a route if it's set
    // If its not set it will use the "title" given in index.html
    const pageTitle = this.buildTitle(snapshot) || this.title.getTitle();
    this.title.setTitle(`MyAwesomeApp - ${pageTitle}`);
  }
}
```

Чтобы подключить свою стратегию, зарегистрируйте её по токену `TitleStrategy` на уровне приложения:

```ts
import {provideRouter, TitleStrategy} from '@angular/router';
import {AppTitleStrategy} from './app-title.strategy';

export const appConfig = {
  providers: [provideRouter(routes), {provide: TitleStrategy, useClass: AppTitleStrategy}],
};
```

## Провайдеры маршрута для инъекции зависимостей {: #route-level-providers-for-dependency-injection}

У каждого маршрута есть свойство `providers`: через него зависимости содержимого этого маршрута регистрируют с помощью [инъекции зависимостей](../di/overview.md).

Так удобно, когда набор сервисов зависит от того, администратор ли пользователь.

```ts
export const ROUTES: Route[] = [
  {
    path: 'admin',
    providers: [AdminService, {provide: ADMIN_API_KEY, useValue: '12345'}],
    children: [
      {path: 'users', component: AdminUsers},
      {path: 'teams', component: AdminTeams},
    ],
  },
  // ... other application routes that don't
  //     have access to ADMIN_API_KEY or AdminService.
];
```

В примере у пути `admin` есть защищённое значение `ADMIN_API_KEY`. Оно доступно только дочерним маршрутам этого раздела. Остальные пути к данным через `ADMIN_API_KEY` не обращаются.

Подробнее о провайдерах и инъекции в Angular — в [руководстве по инъекции зависимостей](../di/overview.md).

## Данные, связанные с маршрутами {: #associating-data-with-routes}

Данные маршрута — дополнительные сведения, которые крепят к маршруту. По ним настраивают поведение компонентов.

Данные маршрута бывают статическими, они не меняются, и динамическими, они зависят от условий во время выполнения.

### Статические данные {: #static-data}

Произвольные статические данные крепят к маршруту через свойство `data`. Так в одном месте собирают метаданные маршрута: идентификатор аналитики, права и тому подобное.

```ts
import {Routes} from '@angular/router';
import {Home} from './home';
import {About} from './about';
import {Products} from './products';

const routes: Routes = [
  {
    path: 'about',
    component: About,
    data: {analyticsId: '456'},
  },
  {
    path: '',
    component: Home,
    data: {analyticsId: '123'},
  },
];
```

В примере у главной страницы и у страницы «о нас» задан свой `analyticsId`. Компоненты этих страниц используют его в аналитике просмотров.

Эти статические данные читают, внедрив `ActivatedRoute`. Подробности — в разделе [Чтение состояния маршрута](read-route-state.md).

### Динамические данные: ресурсы и резолверы {: #dynamic-data-with-resources-and-resolvers}

Чтобы загрузить данные для маршрута, Angular Router поддерживает реактивные ресурсы маршрута и резолверы данных:

-   [Загрузка данных через ресурсы](https://angular.dev/guide/routing/data-fetching-with-resources): реактивная загрузка через API сигналов `Resource`.
-   [Резолверы данных маршрута](https://angular.dev/guide/routing/data-resolvers): загрузка данных до активации маршрута функциями-резолверами.

## Вложенные маршруты {: #nested-routes}

Вложенные маршруты, их ещё называют дочерними, применяют для сложной навигации: у компонента есть вложенное представление, которое меняется вместе с URL.

Дочерние маршруты добавляют в любое определение через свойство `children`:

```ts
const routes: Routes = [
  {
    path: 'product/:id',
    component: Product,
    children: [
      {
        path: 'info',
        component: ProductInfo,
      },
      {
        path: 'reviews',
        component: ProductReviews,
      },
    ],
  },
];
```

В примере страница товара переключает сведения о товаре и отзывы в зависимости от адреса.

Свойство `children` принимает массив объектов `Route`.

Чтобы показать дочерние маршруты, родительский компонент (в примере это `Product`) содержит собственный `<router-outlet>`.

```html
<!-- Product -->
<article>
  <h1>Product {{ id }}</h1>
  <router-outlet />
</article>
```

Когда дочерние маршруты есть в конфигурации, а в компоненте есть `<router-outlet>`, переход между адресами дочерних маршрутов обновляет только вложенную точку выхода.

## Что дальше {: #next-steps}

-   [Стратегии загрузки маршрутов](https://angular.dev/guide/routing/loading-strategies)
-   [Показ содержимого маршрутов в точках выхода](show-routes-with-outlets.md)


---

Источник: [https://angular.dev/guide/routing/define-routes](https://angular.dev/guide/routing/define-routes)
