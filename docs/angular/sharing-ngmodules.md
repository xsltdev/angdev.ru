---
description: Создание общих модулей позволяет упорядочить и оптимизировать код. Вы можете поместить часто используемые директивы, пайпы и компоненты в один модуль, а затем импортировать этот модуль в другие части приложения
---

# Совместное использование модулей

:date: 28.02.2022

Создание общих модулей позволяет упорядочить и оптимизировать код. Вы можете поместить часто используемые директивы, пайпы и компоненты в один модуль, а затем импортировать этот модуль в другие части приложения.

Рассмотрим следующий модуль из воображаемого приложения:

```ts
import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CustomerComponent } from './customer.component';
import { NewItemDirective } from './new-item.directive';
import { OrdersPipe } from './orders.pipe';

@NgModule({
    imports: [CommonModule],
    declarations: [
        CustomerComponent,
        NewItemDirective,
        OrdersPipe,
    ],
    exports: [
        CustomerComponent,
        NewItemDirective,
        OrdersPipe,
        CommonModule,
        FormsModule,
    ],
})
export class SharedModule {}
```

Обратите внимание на следующее:

-   Он импортирует `CommonModule`, поскольку компоненту модуля нужны общие директивы
-   Объявляются и экспортируются классы пайпов, директив и компонентов
-   Он реэкспортирует `CommonModule` и `FormsModule`.

В результате реэкспорта `CommonModule` и `FormsModule` любой другой модуль, импортирующий этот `SharedModule`, получает доступ к директивам `NgIf` и `NgFor` из `CommonModule` и может связываться со свойствами компонента с помощью `[(ngModel)]`, директивы в `FormsModule`.

Даже если компоненты, объявленные `SharedModule`, могут не связываться с `[(ngModel)]` и нет необходимости в импорте `FormsModule`, `SharedModule` может экспортировать `FormsModule`, не указывая его среди своих `импортов`.
Таким образом, вы можете предоставить другим модулям доступ к `FormsModule` без необходимости импортировать его непосредственно в декоратор `@NgModule`.

## Подробнее о NgModules

Возможно, вас также заинтересует следующее:

-   [Провайдеры](providers.md)
-   [Типы функциональных модулей](module-types.md)

## Ссылки

-   [Sharing modules](https://angular.io/guide/sharing-ngmodules)
