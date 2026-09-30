---
description: "Сервисы — переиспользуемые части кода, общие для приложения Angular: загрузка данных, бизнес-логика и другая функциональность для нескольких компонентов"
---

# Создание и использование сервисов {: #creating-and-using-services}

:date: 30.09.2026

Сервисы — переиспользуемые куски кода, общие для приложения Angular. Обычно ими закрывают загрузку данных, бизнес-логику и другую функциональность, к которой обращаются несколько компонентов.

## Создание сервиса {: #creating-a-service}

Сервис можно создать через [Angular CLI](../tools/cli/overview.md) такой командой:

```bash
ng generate service CUSTOM_NAME
```

Команда создаёт отдельный файл `CUSTOM_NAME.ts` в каталоге `src`.

Сервис можно описать и вручную: декоратор `@Service()` на классе TypeScript говорит Angular, что класс годится как внедряемая зависимость.

В примере сервис даёт добавлять данные и читать их обратно.

_src/app/basic-data-store.ts_

```ts
import {Service} from '@angular/core';

@Service()
export class BasicDataStore {
  private data: string[] = [];

  addData(item: string): void {
    this.data.push(item);
  }

  getData(): string[] {
    return [...this.data];
  }
}
```

## Как сервис становится доступным {: #how-services-become-available}

По умолчанию сервисы предоставляются на корневом уровне. Если сервис предоставлен глобально, Angular даёт три гарантии:

-   **Один экземпляр.** На всё приложение создаётся один общий экземпляр.
-   **Доступен везде.** К нему можно обратиться откуда угодно, без ручной регистрации провайдера.
-   **Tree-shaking.** Если код нигде явно не использует сервис, тот не попадает в итоговый продакшен-бандл.

### Декоратор `@Service` и декоратор `@Injectable` {: #using-the-service-vs-injectable-decorator}

Декоратор `@Service` — современная удобная краткая запись привычного `@Injectable({ providedIn: 'root' })`.

Краткая шпаргалка, какой декоратор подходит:

| Возможность                                       | `@Service` | `@Injectable`                              |
| ------------------------------------------------- | ---------- | ------------------------------------------ |
| **Поддержка функции `inject()`**                  | Да         | Да                                         |
| **Инъекция через конструктор**                    | ❌ Нет     | Да                                         |
| **Неявный корневой провайдер-синглтон**           | Да         | ❌ Нет (нужен `{providedIn: 'root'}`)      |
| **Расширенные ключи провайдера (`useClass` и др.)** | ❌ Нет   | Да                                         |
| **Свои фабрики инициализации**                    | Да         | Да                                         |
| **Области не на корне (`platform` и др.)**        | ❌ Нет     | Да                                         |

### Подмена реализации фабрикой {: #replacing-the-implementation-with-a-factory}

Если нужно управлять созданием синглтона, например подставить другую реализацию в зависимости от окружения, передайте функцию `factory`.

Фабрика выполняется в [контексте инъекции](https://angular.dev/guide/di/dependency-injection-context), поэтому внутри можно вызвать [`inject()`](https://angular.dev/api/core/inject) и прочитать другие зависимости.

Сервис `Analytics` ниже локально ничего не делает: во время разработки события не засоряют консоль. В продакшене фабрика читает токен `ANALYTICS_ENABLED` и возвращает подкласс `GoogleAnalytics`, который передаёт события настоящему трекеру.

_src/app/analytics.ts_

```ts
import {inject, InjectionToken, Service} from '@angular/core';
import {ANALYTICS_ENABLED} from './token';

@Service({
  factory: () => (inject(ANALYTICS_ENABLED) ? new GoogleAnalytics() : new Analytics()),
})
export class Analytics {
  track(event: string, payload?: Record<string, unknown>) {
    // No-op by default.
  }
}

class GoogleAnalytics extends Analytics {
  override track(event: string, payload?: Record<string, unknown>) {
    // Dispatches an analytics event to Google Analytics
  }
}
```

!!! info ""

    Параметр `factory` заменяет у `@Injectable` параметры `useClass`, `useValue`, `useExisting` и `useFactory`. Если нужен любой из них, оставайтесь на `@Injectable`.

### Отказ от автоматического предоставления {: #opting-out-of-automatic-provisioning}

По умолчанию `@Service` предоставляет класс в корневом инжекторе. Чтобы предоставить его вручную, например ограничить конкретным маршрутом или компонентом, задайте `autoProvided: false`.

_src/app/analytics-logger.ts_

```ts
import {Service} from '@angular/core';

@Service({autoProvided: false})
export class AnalyticsLogger {
  trackEvent(name: string) {
    console.log('event:', name);
  }
}
```

Дальше сервис нужно самим добавить в массив `providers`, как и обычный `@Injectable()`:

### Когда брать `@Service`, а когда `@Injectable` {: #when-to-use-service-vs-injectable}

Берите `@Service`, когда создаёте новый класс-синглтон и зависимости берёте через `inject()`. Оставляйте `@Injectable`, если нужно что-то из списка:

-   **Инъекция зависимостей через конструктор.** `@Service` поддерживает только функцию [`inject()`](https://angular.dev/api/core/inject).
-   **Расширенная настройка провайдера**, например `useClass`, `useValue`, `useExisting` или `useFactory`. У `@Service` вместо этого один параметр `factory`.
-   **Области не на корне**, например `providedIn: 'platform'`.

## Внедрение сервиса {: #injecting-a-service}

Сервис с `providedIn: 'root'` внедряют в любом месте приложения функцией `inject()` из `@angular/core`.

### Внедрение в компонент {: #injecting-into-a-component}

```ts
import {Component, inject} from '@angular/core';
import {BasicDataStore} from './basic-data-store';

@Component({
  selector: 'app-example',
  template: `
    <div>
      <p>{{ dataStore.getData() }}</p>
      <button (click)="dataStore.addData('More data')">Add more data</button>
    </div>
  `,
})
export class Example {
  dataStore = inject(BasicDataStore);
}
```

### Внедрение в другой сервис {: #injecting-into-another-service}

```ts
import {inject, Service} from '@angular/core';
import {AdvancedDataStore} from './advanced-data-store';

@Service()
export class BasicDataStore {
  private advancedDataStore = inject(AdvancedDataStore);
  private data: string[] = [];

  addData(item: string): void {
    this.data.push(item);
  }

  getData(): string[] {
    return [...this.data, ...this.advancedDataStore.getData()];
  }
}
```

## Следующие шаги {: #next-steps}

`providedIn: 'root'` закрывает большинство случаев, но для более узких сценариев Angular даёт и другие способы настроить сервисы:

-   **Свой экземпляр у компонента.** Когда компоненту нужен отдельный экземпляр сервиса.
-   **Ручная настройка.** Для сервисов, которым конфигурация нужна во время выполнения.
-   **Провайдеры-фабрики.** Чтобы создавать сервис динамически, по условиям во время выполнения.
-   **Провайдеры значений.** Чтобы предоставить объект конфигурации или константу.

Подробнее об этих приёмах — в следующем руководстве: [определение провайдеров зависимостей](defining-dependency-providers.md).

---

Источник: [https://angular.dev/guide/di/creating-and-using-services](https://angular.dev/guide/di/creating-and-using-services)
