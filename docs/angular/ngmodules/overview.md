---
description: "Модуль собирает компоненты, директивы и пайпы и настраивает для них инъекцию зависимостей; для нового кода лучше автономные компоненты."
---

# NgModules {: #ngmodules}

:date: 30.09.2026

!!! warning ""

    Для всего нового кода команда Angular рекомендует [автономные компоненты](../components/anatomy-of-components.md) вместо `NgModule`. Это руководство нужно, чтобы понимать уже написанный код на `@NgModule`.

NgModule — класс, помеченный декоратором `@NgModule`. Декоратор принимает _метаданные_: по ним Angular компилирует шаблоны компонентов и настраивает инъекцию зависимостей.

```ts
import {NgModule} from '@angular/core';

@NgModule({
  // Metadata goes here
})
export class CustomMenuModule {}
```

У NgModule две главные задачи:

-   объявляет компоненты, директивы и пайпы, которые принадлежат NgModule;
-   добавляет провайдеры в инжектор для компонентов, директив и пайпов, которые импортируют этот NgModule.

## Объявления {: #declarations}

Свойство `declarations` метаданных `@NgModule` перечисляет компоненты, директивы и пайпы этого NgModule.

```ts
@NgModule({
  /* ... */
  // CustomMenu and CustomMenuItem are components.
  declarations: [CustomMenu, CustomMenuItem],
})
export class CustomMenuModule {}
```

В примере выше компоненты `CustomMenu` и `CustomMenuItem` принадлежат `CustomMenuModule`.

Кроме того, `declarations` принимает _массивы_ компонентов, директив и пайпов. Внутри таких массивов могут быть другие массивы.

```ts
const MENU_COMPONENTS = [CustomMenu, CustomMenuItem];
const WIDGETS = [MENU_COMPONENTS, CustomSlider];

@NgModule({
  /* ... */
  // This NgModule declares all of CustomMenu, CustomMenuItem,
  // CustomSlider, and CustomCheckbox.
  declarations: [WIDGETS, CustomCheckbox],
})
export class CustomMenuModule {}
```

Если компонент, директива или пайп объявлены больше чем в одном NgModule, Angular сообщает об ошибке.

Чтобы объявить компонент, директиву или пайп в NgModule, их нужно явно пометить `standalone: false`.

```ts
@Component({
  // Mark this component as `standalone: false` so that it can be declared in an NgModule.
  standalone: false,
  /* ... */
})
export class CustomMenu {
  /* ... */
}
```

### Импорты {: #imports}

Компонент, объявленный в NgModule, может зависеть от других компонентов, директив и пайпов. Такие зависимости добавляют в свойство `imports` метаданных `@NgModule`.

```ts
@NgModule({
  /* ... */
  // CustomMenu and CustomMenuItem depend on the PopupTrigger and SelectorIndicator components.
  imports: [PopupTrigger, SelectionIndicator],
  declarations: [CustomMenu, CustomMenuItem],
})
export class CustomMenuModule {}
```

В массив `imports` входят другие NgModule, а также автономные компоненты, директивы и пайпы.

### Экспорты {: #exports}

NgModule может _экспортировать_ объявленные компоненты, директивы и пайпы. Тогда они доступны другим компонентам и NgModule.

```ts
@NgModule({
  imports: [PopupTrigger, SelectionIndicator],
  declarations: [CustomMenu, CustomMenuItem],

  // Make CustomMenu and CustomMenuItem available to
  // components and NgModules that import CustomMenuModule.
  exports: [CustomMenu, CustomMenuItem],
})
export class CustomMenuModule {}
```

Свойство `exports` не ограничено собственными объявлениями. NgModule может экспортировать и те компоненты, директивы, пайпы и NgModule, которые сам импортирует.

```ts
@NgModule({
  imports: [PopupTrigger, SelectionIndicator],
  declarations: [CustomMenu, CustomMenuItem],

  // Also make PopupTrigger available to any component or NgModule that imports CustomMenuModule.
  exports: [CustomMenu, CustomMenuItem, PopupTrigger],
})
export class CustomMenuModule {}
```

## Провайдеры `NgModule` {: #ngmodule-providers}

!!! tip ""

    Про инъекцию зависимостей и провайдеры — в [руководстве по инъекции зависимостей](../di/overview.md).

`NgModule` задаёт `providers` для внедряемых зависимостей. Эти провайдеры доступны:

-   любому автономному компоненту, директиве и пайпу, которые импортируют этот NgModule;
-   объявлениям `declarations` и провайдерам `providers` любого другого NgModule, который импортирует этот.

```ts
@NgModule({
  imports: [PopupTrigger, SelectionIndicator],
  declarations: [CustomMenu, CustomMenuItem],

  // Provide the OverlayManager service
  providers: [OverlayManager],
  /* ... */
})
export class CustomMenuModule {}

@NgModule({
  imports: [CustomMenuModule],
  declarations: [UserProfile],
  providers: [UserDataClient],
})
export class UserProfileModule {}
```

В примере выше:

-   `CustomMenuModule` предоставляет сервис `OverlayManager`;
-   компоненты `CustomMenu` и `CustomMenuItem` могут внедрить `OverlayManager`, потому что объявлены в `CustomMenuModule`;
-   `UserProfile` может внедрить `OverlayManager`, потому что его NgModule импортирует `CustomMenuModule`;
-   `UserDataClient` может внедрить `OverlayManager`, потому что его NgModule импортирует `CustomMenuModule`.

### Паттерн `forRoot` и `forChild` {: #the-forroot-and-forchild-pattern}

У некоторых NgModule есть статический метод `forRoot`. Он принимает конфигурацию и возвращает массив провайдеров. Имя `forRoot` — соглашение: эти провайдеры добавляют только в _корень_ приложения, во время запуска.

Такие провайдеры загружаются сразу и увеличивают размер JavaScript первой загрузки страницы.

```ts
bootstrapApplication(MyApplicationRoot, {
  providers: [CustomMenuModule.forRoot(/* some config */)],
});
```

Статический метод `forChild` у части NgModule означает другое: провайдеры предназначены компонентам внутри иерархии приложения.

```ts
@Component({
  /* ... */
  providers: [CustomMenuModule.forChild(/* some config */)],
})
export class UserProfile {
  /* ... */
}
```

## Запуск приложения {: #bootstrapping-an-application}

!!! warning ""

    Для нового кода команда Angular рекомендует [bootstrapApplication](https://angular.dev/api/platform-browser/bootstrapApplication) вместо `bootstrapModule`. Здесь — как устроены приложения, которые по-прежнему запускают через `@NgModule`.

Декоратор `@NgModule` принимает необязательный массив `bootstrap` с одним или несколькими компонентами.

Приложение Angular запускают методом [`bootstrapModule`](https://angular.dev/api/core/PlatformRef#bootstrapModule) у [`platformBrowser`](https://angular.dev/api/platform-browser/platformBrowser) или [`platformServer`](https://angular.dev/api/platform-server/platformServer). При вызове функция находит на странице элементы, чей CSS-селектор совпадает с указанными компонентами, и отрисовывает эти компоненты.

```ts
import {platformBrowser} from '@angular/platform-browser';

@NgModule({
  bootstrap: [MyApplication],
})
export class MyApplicationModule {}

platformBrowser().bootstrapModule(MyApplicationModule);
```

Компоненты из `bootstrap` автоматически входят в объявления NgModule.

Когда приложение запускают из NgModule, собранные `providers` этого модуля и все `providers` из его `imports` загружаются сразу и доступны для инъекции во всём приложении.


---

Источник: [https://angular.dev/guide/ngmodules/overview](https://angular.dev/guide/ngmodules/overview)
