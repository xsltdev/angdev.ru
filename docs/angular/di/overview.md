---
description: "Инъекция зависимостей — шаблон проектирования: классу передают зависимости снаружи, чтобы организовать и делить код по приложению"
---

# Инъекция зависимостей в Angular {: #dependency-injection-in-angular}

:date: 30.09.2026

Инъекция зависимостей (DI) — шаблон проектирования: так организуют и делят код по приложению, передавая зависимости в класс снаружи, а не создавая их внутри.

!!! tip ""

    Прежде чем читать это подробное руководство, загляните в [«Основы»](../essentials/dependency-injection.md) Angular.

По мере роста приложения одну и ту же функциональность приходится переиспользовать в разных частях кода. [Инъекция зависимостей](https://en.wikipedia.org/wiki/Dependency_injection) как раз для этого: зависимости передают классу, а не создают прямо внутри него. Части приложения проще переиспользовать и сопровождать.

Шаблон популярен, потому что закрывает типичные задачи:

-   **Проще сопровождать код.** Инъекция зависимостей разделяет ответственность: код легче рефакторить, повторов меньше.
-   **Масштаб.** Модульную функциональность можно переиспользовать в разных частях приложения, и расти проще.
-   **Удобнее тестировать.** В модульных тестах вместо настоящих реализаций при необходимости подставляют [тестовые двойники](https://en.wikipedia.org/wiki/Test_double).

## Как устроена инъекция зависимостей в Angular? {: #how-does-dependency-injection-work-in-angular}

Зависимость — любой объект, значение, функция или сервис, без которого класс не работает, но который он сам не создаёт. Его передают снаружи, и связь между частями приложения остаётся явной.

С системой инъекции зависимостей работают двумя способами:

-   Значения можно _предоставить_, то есть сделать доступными.
-   Эти значения можно _внедрить_, то есть запросить как зависимости.

Здесь «значения» — любые значения JavaScript: объекты, функции, экземпляры классов. Чаще всего внедряют такое:

-   **Значения конфигурации:** константы конкретного окружения, URL API, флаги функций и тому подобное.
-   **Фабрики:** функции, которые создают объекты или значения по условиям во время выполнения.
-   **Сервисы:** классы с общей функциональностью, бизнес-логикой или состоянием.

Компоненты и директивы Angular сами участвуют в DI: в них можно внедрять зависимости, и их самих можно отдавать для внедрения.

## Что такое сервисы? {: #what-are-services}

_Сервис_ в Angular — класс TypeScript с декоратором `@Service`. Экземпляр такого класса внедряют как зависимость. Через сервисы чаще всего делят данные и функциональность по приложению.

Обычные виды сервисов:

-   **Клиенты данных.** Скрывают подробности запросов к серверу: и чтение, и изменение.
-   **Управление состоянием.** Задаёт состояние, общее для нескольких компонентов или страниц.
-   **Аутентификация и авторизация.** Ведёт аутентификацию пользователя, хранение токенов и контроль доступа.
-   **Журнал и ошибки.** Задаёт общий API для записи в журнал и для сообщений пользователю об ошибках.
-   **События и рассылка.** Обрабатывает события и уведомления, не привязанные к конкретному компоненту, либо рассылает их компонентам по [паттерну «наблюдатель»](https://en.wikipedia.org/wiki/Observer_pattern).
-   **Вспомогательные функции.** Переиспользуемые утилиты: форматирование данных, проверка, вычисления.

В примере объявлен сервис `AnalyticsLogger`:

```ts
import {Service} from '@angular/core';

@Service()
export class AnalyticsLogger {
  trackEvent(category: string, value: string) {
    console.log('Analytics event logged:', {
      category,
      value,
      timestamp: new Date().toISOString(),
    });
  }
}
```

!!! info ""

    `@Service` делает этот сервис синглтоном на всё приложение. Для большинства сервисов так и стоит делать.

!!! tip ""

    Декоратор [`@Service`](creating-and-using-services.md#using-the-service-vs-injectable-decorator) — удобная краткая запись `@Injectable({providedIn: 'root'})`.

## Внедрение зависимостей через `inject()` {: #injecting-dependencies-with-inject}

Зависимости внедряют функцией `inject()` из Angular.

В примере панель навигации внедряет `AnalyticsLogger` и сервис `Router`: пользователь переходит на другую страницу, а событие при этом записывается.

```ts
import {Component, inject} from '@angular/core';
import {Router} from '@angular/router';
import {AnalyticsLogger} from './analytics-logger';

@Component({
  selector: 'app-navbar',
  template: `<a href="#" (click)="navigateToDetail($event)">Detail Page</a>`,
})
export class Navbar {
  private router = inject(Router);
  private analytics = inject(AnalyticsLogger);

  navigateToDetail(event: Event) {
    event.preventDefault();
    this.analytics.trackEvent('navigation', '/details');
    this.router.navigate(['/details']);
  }
}
```

### Где можно вызывать `inject()`? {: #where-can-inject-be-used}

Зависимости внедряют при создании компонента, директивы или сервиса. Вызов [`inject`](https://angular.dev/api/core/inject) стоит либо в `constructor`, либо в инициализаторе поля. Несколько обычных случаев:

```ts
@Component(/* ... */)
export class MyComponent {
  // ✅ In class field initializer
  private service = inject(MyService);

  // ✅ In constructor body
  private anotherService: MyService;

  constructor() {
    this.anotherService = inject(MyService);
  }
}
```

```ts
@Directive({...})
export class MyDirective {
  // ✅ In class field initializer
  private element = inject(ElementRef);
}
```

```ts
import {Service, inject} from '@angular/core';
import {HttpClient} from '@angular/common/http';

@Service()
export class MyService {
  // ✅ In a service
  private http = inject(HttpClient);
}
```

```ts
export const authGuard = () => {
  // ✅ In a route guard
  const auth = inject(AuthService);
  return auth.isAuthenticated();
};
```

«Контекстом инъекции» в Angular называют любое место в коде, где можно вызвать [`inject`](https://angular.dev/api/core/inject). Чаще всего это создание компонента, директивы или сервиса; подробнее — в разделе [контексты инъекции](https://angular.dev/guide/di/dependency-injection-context).

Подробнее — в [документации API `inject`](https://angular.dev/api/core/inject#usage-notes).

## Следующие шаги {: #next-steps}

Когда основы инъекции зависимостей в Angular ясны, можно создавать свои сервисы.

Следующее руководство, [Создание и использование сервисов](creating-and-using-services.md), разбирает:

-   как создать сервис через Angular CLI или вручную;
-   как работает шаблон `providedIn: 'root'`;
-   как внедрять сервисы в компоненты и другие сервисы.

Этого хватает для самого частого сценария сервисов в приложениях Angular.

---

Источник: [https://angular.dev/guide/di](https://angular.dev/guide/di)
