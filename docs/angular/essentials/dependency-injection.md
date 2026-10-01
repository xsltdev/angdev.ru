---
description: "Общий код и единое управление поведением в приложении и тестах."
---

# Инъекция зависимостей {: #dependency-injection}

:date: 30.09.2026

Общий код и единое управление поведением в приложении и тестах.

Когда логику нужно разделить между компонентами, Angular использует шаблон [инъекции зависимостей](../di/overview.md). На нём делают «сервис»: код внедряют в компоненты и ведут его из одного места.

## Что такое сервисы? {: #what-are-services}

Сервис — это переиспользуемый код, который можно внедрить.

Как и компонент, сервис состоит из следующего:

-   **Декоратор TypeScript**, который помечает класс как сервис Angular через `@Service` и позволяет описать сервис, доступный в любом месте приложения.
-   **Класс TypeScript** с кодом, который станет доступен после внедрения сервиса.

Пример сервиса `Calculator`.

```ts
import {Service} from '@angular/core';

@Service()
export class Calculator {
  add(x: number, y: number) {
    return x + y;
  }
}
```

## Как пользоваться сервисом {: #how-to-use-a-service}

Чтобы воспользоваться сервисом в компоненте, нужно:

1.  Импортировать сервис.
2.  Объявить поле класса, в которое внедряется сервис. Присвоить полю результат вызова встроенной функции [`inject`](https://angular.dev/api/core/inject): она создаёт сервис.

Так это выглядит в компоненте `Receipt`:

```ts
import {Component, inject} from '@angular/core';
import {Calculator} from './calculator';

@Component({
  selector: 'app-receipt',
  template: `<h1>The total is {{ totalCost }}</h1>`,
})
export class Receipt {
  private calculator = inject(Calculator);
  totalCost = this.calculator.add(50, 25);
}
```

В этом примере `Calculator` получают вызовом функции Angular [`inject`](https://angular.dev/api/core/inject) и передают в неё сервис.

## Следующий шаг {: #next-step}

-   [Что дальше после основ](next-steps.md)
-   [Подробное руководство по инъекции зависимостей](../di/overview.md)


---

Источник: [https://angular.dev/essentials/dependency-injection](https://angular.dev/essentials/dependency-injection)
