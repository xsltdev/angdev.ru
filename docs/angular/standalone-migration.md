# Миграция существующего проекта Angular на standalone

:date: 15.02.2023

Начиная с версии 15.2.0, Angular предлагает [схему](schematics.md), чтобы помочь авторам проектов перевести существующие проекты на [новые автономные API](standalone-components.md). Схема нацелена на автоматическое преобразование как можно большего количества кода, но может потребовать некоторых ручных исправлений со стороны автора проекта. Запустите схему с помощью следующей команды:

```shell
ng generate @angular/core:standalone
```

## Предварительные условия

Перед использованием схемы, пожалуйста, убедитесь, что проект:

1.  Используется Angular 15.2.0 или более поздняя версия.
2.  Собирается без ошибок компиляции.
3.  Находится на чистой ветке Git и вся работа сохраняется.

## Параметры схемы

| Опция  | Подробности                                                                                                                |
| :----- | :------------------------------------------------------------------------------------------------------------------------- |
| `mode` | Преобразование для выполнения. Подробности о доступных опциях см. в разделе "Режимы миграции" ниже.                        |
| `path` | Путь для миграции, относительно корня проекта. Вы можете использовать эту опцию для постепенной миграции разделов проекта. |

## Шаги миграции

Процесс миграции состоит из трех шагов. Вам придется запустить его несколько раз и вручную проверить, что проект собирается и ведет себя так, как ожидается.

!!!note ""

    Хотя схема может автоматически обновлять большинство кода, некоторые крайние случаи требуют вмешательства разработчика. Вам следует запланировать ручное исправление после каждого этапа миграции. Кроме того, новый код, сгенерированный схемой, может не соответствовать правилам форматирования вашего кода.

Выполните миграцию в перечисленном ниже порядке, проверяя, что ваш код собирается и запускается между каждым шагом:

1.  Запустите `ng g @angular/core:standalone` и выберите "Convert all components, directives and pipes to standalone".

2.  Запустите `ng g @angular/core:standalone` и выберите "Удалить ненужные классы NgModule".

3.  Запустите `ng g @angular/core:standalone` и выберите "Bootstrap проекта с использованием standalone API".

4.  Выполните все проверки линтинга и форматирования, исправьте все ошибки и зафиксируйте результат.

## После миграции

Поздравляем, ваше приложение было преобразовано в standalone 🎉. Вот некоторые необязательные последующие шаги, которые вы можете предпринять сейчас:

-   Найдите и удалите все оставшиеся объявления `NgModule`: поскольку шаг "Удалите ненужные модули NgModules" не может удалить все модули автоматически, возможно, вам придется удалить оставшиеся объявления вручную.
-   Запустите модульные тесты проекта и исправьте все ошибки.
-   Запустите все форматоры кода, если в проекте используется автоматическое форматирование.
-   Запустите все линтеры в вашем проекте и исправьте новые предупреждения. Некоторые линтеры поддерживают флаг `--fix`, который может устранить предупреждения автоматически.

## Режимы миграции

Миграция имеет следующие режимы:

1.  Преобразование деклараций в автономные.
2.  Удалить ненужные `NgModules`.
3.  Перейдите на автономный API для загрузки. Вы должны выполнить эти миграции в указанном порядке.

### Преобразование деклараций в автономный режим

В этом режиме миграция преобразует все компоненты, директивы и пайпы в автономные, устанавливая `standalone: true` и добавляя зависимости в их массив `imports`.

!!!note ""

    Схема игнорирует `NgModules`, которые загружают компонент во время этого шага, потому что они, скорее всего, являются корневыми модулями, используемыми `bootstrapModule`, а не совместимым с standalone `bootstrapApplication`. Схема преобразует эти объявления автоматически в рамках шага ["Switch to standalone bootstrapping API"](#switch-to-standalone-bootstrapping-api).

**До:**

```typescript
// shared.module.ts
@NgModule({
    imports: [CommonModule],
    declarations: [GreeterComponent],
    exports: [GreeterComponent],
})
export class SharedModule {}
```

```typescript
// greeter.component.ts
@Component({
    selector: 'greeter',
    template: '<div *ngIf="showGreeting">Hello</div>',
})
export class GreeterComponent {
    showGreeting = true;
}
```

**После:**

```typescript
// shared.module.ts
@NgModule({
    imports: [CommonModule, GreeterComponent],
    exports: [GreeterComponent],
})
export class SharedModule {}
```

```typescript
// greeter.component.ts
@Component({
    selector: 'greeter',
    template: '<div *ngIf="showGreeting">Hello</div>',
    standalone: true,
    imports: [NgIf],
})
export class GreeterComponent {
    showGreeting = true;
}
```

### Удалите ненужные NgModules

После преобразования всех деклараций в автономные многие `NgModules` можно безопасно удалить. На этом шаге удаляются объявления таких модулей и как можно больше соответствующих ссылок. Если миграция не может удалить ссылку автоматически, она оставляет следующий комментарий TODO, чтобы вы могли удалить `NgModule` вручную:

```typescript
/* TODO(standalone-migration): clean up removed NgModule reference manually */
```

Миграция считает модуль безопасным для удаления, если этот модуль:

-   Не имеет `declarations`.
-   Не имеет `providers`.
-   Не имеет компонентов `bootstrap`.
-   Не имеет `imports`, которые ссылаются на символ `ModuleWithProviders` или модуль, который не может быть удален.
-   Не имеет членов класса. Пустые конструкторы игнорируются.

**До:**

```ts
// importer.module.ts
@NgModule({
    imports: [FooComponent, BarPipe],
    exports: [FooComponent, BarPipe],
})
export class ImporterModule {}
```

**После:**

```typescript
// importer.module.ts
// Does not exist!
```

### Переход к автономному API бутстрапинга {: #switch-to-standalone-bootstrapping-api}

Этот шаг преобразует любое использование `bootstrapModule` в новый, основанный на standalone `bootstrapApplication`. Он также переключает корневой компонент на `standalone: true` и удаляет корневой модуль `NgModule`. Если корневой модуль имеет какие-либо `providers` или `imports`, миграция пытается скопировать как можно больше этой конфигурации в новый вызов `bootstrap`.

**До:**

```ts
// ./app/app.module.ts
import { NgModule } from '@angular/core';
import { AppComponent } from './app.component';

@NgModule({
    declarations: [AppComponent],
    bootstrap: [AppComponent],
})
export class AppModule {}
```

```ts
// ./app/app.component.ts
@Component({ selector: 'app', template: 'hello' })
export class AppComponent {}
```

```ts
// ./main.ts
import { platformBrowser } from '@angular/platform-browser';
import { AppModule } from './app/app.module';

platformBrowser()
    .bootstrapModule(AppModule)
    .catch((e) => console.error(e));
```

**После:**

```typescript
// ./app/app.module.ts
// Does not exist!
```

```typescript
// ./app/app.component.ts
@Component({
    selector: 'app',
    template: 'hello',
    standalone: true,
})
export class AppComponent {}
```

```typescript
// ./main.ts
import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/app.component';

bootstrapApplication(AppComponent).catch((e) =>
    console.error(e)
);
```

## Общие проблемы

Некоторые общие проблемы, которые могут помешать правильной работе схемы, включают:

-   Ошибки компиляции — если проект имеет ошибки компиляции, Angular не сможет правильно проанализировать и мигрировать его.
-   Файлы, не включенные в tsconfig — схема определяет, какие файлы нужно перенести, анализируя файлы `tsconfig.json` вашего проекта. Схема исключает любые файлы, не захваченные `tsconfig`.
-   Код, который не поддается статическому анализу — схема использует статический анализ, чтобы понять ваш код и определить, где необходимо внести изменения. Миграция может пропустить классы с метаданными, которые не могут быть статически проанализированы во время сборки.

## Ограничения

Из-за размера и сложности миграции есть некоторые случаи, которые схема не может обработать:

-   Поскольку модульные тесты не компилируются заранее (AoT), `импорты`, добавленные к компонентам в модульных тестах, могут быть не совсем корректными.
-   Схема полагается на прямые вызовы API Angular. Схема не может распознать пользовательские обертки вокруг Angular API. Например, если вы определите пользовательскую функцию `customConfigureTestModule`, которая обертывает `TestBed.configureTestingModule`, объявленные в ней компоненты могут быть не распознаны.
