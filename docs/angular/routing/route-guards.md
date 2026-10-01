---
description: "Охранники маршрута решают, можно ли перейти на маршрут или покинуть его."
---

# Контроль доступа к маршрутам охранниками {: #control-route-access-with-guards}

:date: 30.09.2026

!!! danger ""

    Клиентские охранники нельзя считать единственным контролем доступа. Любой JavaScript, который выполняется в браузере, пользователь этого браузера может изменить. Авторизацию всегда проверяйте на сервере, в дополнение к охранникам на клиенте.

Охранники маршрута — функции, которые решают, может ли пользователь перейти на маршрут или покинуть его. Это контрольные точки доступа к конкретным маршрутам. Чаще всего ими закрывают аутентификацию и разграничение доступа.

## Создание охранника маршрута {: #creating-a-route-guard}

Охранник маршрута генерируют через Angular CLI:

```bash
ng generate guard CUSTOM_NAME
```

Команда предложит выбрать [тип охранника маршрута](#types-of-route-guards) и создаст файл `CUSTOM_NAME-guard.ts`.

!!! tip ""

    Охранник можно написать и вручную: отдельный файл TypeScript в проекте Angular. Обычно в имени оставляют суффикс `-guard.ts`, чтобы файл было проще отличить от остальных.

## Типы возврата охранника маршрута {: #route-guard-return-types}

У всех охранников маршрута одинаковый набор возможных типов возврата. От типа зависит, как именно управляют навигацией:

| Типы возврата                   | Описание                                                                              |
| ------------------------------- | ------------------------------------------------------------------------------------- |
| `boolean`                       | `true` разрешает переход, `false` блокирует его (см. примечание об охраннике `CanMatch`) |
| `UrlTree` или `RedirectCommand` | Перенаправляет на другой маршрут вместо блокировки                                   |
| `Promise<T>` или `Observable<T>` | Маршрутизатор берёт первое выданное значение и отписывается                          |

!!! info ""

    У `CanMatch` поведение другое: при возврате `false` Angular пробует остальные подходящие маршруты, а не блокирует навигацию целиком.

## Типы охранников маршрута {: #types-of-route-guards}

В Angular четыре типа охранников маршрута, и у каждого своя задача:

-   [CanActivate](#canactivate)
-   [CanActivateChild](#canactivatechild)
-   [CanDeactivate](#candeactivate)
-   [CanMatch](#canmatch)

Каждый охранник видит [сервисы, предоставленные на уровне маршрута](../di/defining-dependency-providers.md#route-providers), и данные конкретного маршрута через аргумент `route`.

### CanActivate {: #canactivate}

Охранник `CanActivate` решает, может ли пользователь открыть маршрут. Чаще всего его ставят на аутентификацию и авторизацию.

По умолчанию ему доступны такие аргументы:

-   `route`: `ActivatedRouteSnapshot` — сведения об активируемом маршруте
-   `state`: `RouterStateSnapshot` — текущее состояние маршрутизатора

Вернуть можно [стандартные типы возврата охранника](#route-guard-return-types).

```ts
export const authGuard: CanActivateFn = (
  route: ActivatedRouteSnapshot,
  state: RouterStateSnapshot,
) => {
  const authService = inject(AuthService);
  return authService.isAuthenticated();
};
```

!!! tip ""

    Если пользователя нужно перенаправить, верните [`URLTree`](https://angular.dev/api/router/UrlTree) или [`RedirectCommand`](https://angular.dev/api/router/RedirectCommand). **Не** возвращайте `false` и следом не вызывайте `navigate` программно.

Подробнее — в [документации API `CanActivateFn`](https://angular.dev/api/router/CanActivateFn).

### CanActivateChild {: #canactivatechild}

Охранник `CanActivateChild` решает, может ли пользователь открыть дочерние маршруты конкретного родителя. Им защищают целый раздел вложенных маршрутов. `canActivateChild` выполняется для _всех_ дочерних маршрутов. Если у дочернего компонента есть свой дочерний компонент, `canActivateChild` выполнится по одному разу для обоих компонентов.

По умолчанию ему доступны такие аргументы:

-   `childRoute`: `ActivatedRouteSnapshot` — «будущий» снимок активируемого дочернего маршрута, то есть состояние, в которое маршрутизатор пытается перейти
-   `state`: `RouterStateSnapshot` — текущее состояние маршрутизатора

Вернуть можно [стандартные типы возврата охранника](#route-guard-return-types).

```ts
export const adminChildGuard: CanActivateChildFn = (
  childRoute: ActivatedRouteSnapshot,
  state: RouterStateSnapshot,
) => {
  const authService = inject(AuthService);
  return authService.hasRole('admin');
};
```

Подробнее — в [документации API `CanActivateChildFn`](https://angular.dev/api/router/CanActivateChildFn).

### CanDeactivate {: #candeactivate}

Охранник `CanDeactivate` решает, может ли пользователь покинуть маршрут. Частый сценарий — не дать уйти с формы, пока в ней есть несохранённые изменения.

По умолчанию ему доступны такие аргументы:

-   `component`: `T` — экземпляр деактивируемого компонента
-   `currentRoute`: `ActivatedRouteSnapshot` — сведения о текущем маршруте
-   `currentState`: `RouterStateSnapshot` — текущее состояние маршрутизатора
-   `nextState`: `RouterStateSnapshot` — следующее состояние маршрутизатора, куда идёт переход

Вернуть можно [стандартные типы возврата охранника](#route-guard-return-types).

```ts
export const unsavedChangesGuard: CanDeactivateFn<Form> = (
  component: Form,
  currentRoute: ActivatedRouteSnapshot,
  currentState: RouterStateSnapshot,
  nextState: RouterStateSnapshot,
) => {
  return component.hasUnsavedChanges()
    ? confirm('You have unsaved changes. Are you sure you want to leave?')
    : true;
};
```

Подробнее — в [документации API `CanDeactivateFn`](https://angular.dev/api/router/CanDeactivateFn).

### CanMatch {: #canmatch}

Охранник `CanMatch` решает, подходит ли маршрут при сопоставлении пути. Если маршрут отклонён, сопоставление переходит к другим подходящим маршрутам, а не останавливает навигацию целиком. Так делают флаги функций, A/B-тестирование и условную загрузку маршрутов.

По умолчанию ему доступны такие аргументы:

-   `route`: `Route` — проверяемая конфигурация маршрута
-   `segments`: `UrlSegment[]` — сегменты URL, которые ещё не разобраны при проверке родительских маршрутов
-   `currentSnapshot: PartialMatchRouteSnapshot` — снимок маршрута на текущем шаге сопоставления

Вернуть можно [стандартные типы возврата охранника](#route-guard-return-types), но при `false` Angular пробует другие подходящие маршруты и не блокирует навигацию целиком.

```ts
export const featureToggleGuard: CanMatchFn = (
  route: Route,
  segments: UrlSegment[],
  currentSnapshot: PartialMatchRouteSnapshot,
) => {
  const featureService = inject(FeatureService);
  return featureService.isFeatureEnabled('newDashboard');
};
```

На один и тот же путь можно повесить разные компоненты.

_routes.ts_

```ts
const routes: Routes = [
  {
    path: 'dashboard',
    component: AdminDashboard,
    canMatch: [adminGuard],
  },
  {
    path: 'dashboard',
    component: UserDashboard,
    canMatch: [userGuard],
  },
];
```

Когда пользователь открывает `/dashboard`, берётся первый маршрут, чей охранник разрешил совпадение.

Подробнее — в [документации API `CanMatchFn`](https://angular.dev/api/router/CanMatchFn).

## Подключение охранников к маршрутам {: #applying-guards-to-routes}

Созданные охранники подключают в определениях маршрутов.

В конфигурации охранники задают массивом: на один маршрут можно повесить несколько. Они выполняются в том порядке, в каком стоят в массиве.

```ts
import {Routes} from '@angular/router';
import {authGuard} from './guards/auth.guard';
import {adminGuard} from './guards/admin.guard';
import {canDeactivateGuard} from './guards/can-deactivate.guard';
import {featureToggleGuard} from './guards/feature-toggle.guard';

const routes: Routes = [
  // Basic CanActivate - requires authentication
  {
    path: 'dashboard',
    component: Dashboard,
    canActivate: [authGuard],
  },

  // Multiple CanActivate guards - requires authentication AND admin role
  {
    path: 'admin',
    component: Admin,
    canActivate: [authGuard, adminGuard],
  },

  // CanActivate + CanDeactivate - protected route with unsaved changes check
  {
    path: 'profile',
    component: Profile,
    canActivate: [authGuard],
    canDeactivate: [canDeactivateGuard],
  },

  // CanActivateChild - protects all child routes
  {
    path: 'users', // /user - NOT protected
    canActivateChild: [authGuard],
    children: [
      // /users/list - PROTECTED
      {path: 'list', component: UserList},
      // /users/detail/:id - PROTECTED
      {path: 'detail/:id', component: UserDetail},
    ],
  },

  // CanMatch - conditionally matches route based on feature flag
  {
    path: 'beta-feature',
    component: BetaFeature,
    canMatch: [featureToggleGuard],
  },

  // Fallback route if beta feature is disabled
  {
    path: 'beta-feature',
    component: ComingSoon,
  },
];
```


---

Источник: [https://angular.dev/guide/routing/route-guards](https://angular.dev/guide/routing/route-guards)
