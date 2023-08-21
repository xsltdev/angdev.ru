---
description: Модули функций - это NgModules, предназначенные для организации кода
---

# Feature modules

:date: 28.02.2022

**Модули функций** - это NgModules, предназначенные для организации кода.

Последний пример приложения с функциональным модулем, который описывается на этой странице, приведен в [живом примере](https://angular.io/generated/live-examples/feature-modules/stackblitz.html).

По мере роста приложения можно организовать код, относящийся к конкретной функции. Это помогает установить четкие границы между функциями. С помощью модулей функций можно отделить код, относящийся к конкретной функциональности или функции, от остального кода. Разграничение областей приложения помогает наладить сотрудничество между разработчиками и командами, разделить директивы и управлять размером корневого модуля.

## Функциональные модули и корневые модули

Функциональный модуль - это лучшая организационная практика, а не концепция основного API Angular. Функциональный модуль представляет собой целостный набор функциональных возможностей, ориентированных на конкретные потребности приложения, такие как рабочий процесс пользователя, маршрутизация или формы. В то время как в корневом модуле можно сделать все, что угодно, функциональные модули помогают разделить приложение на отдельные области. Функциональный модуль взаимодействует с корневым модулем и другими модулями через предоставляемые им сервисы, а также компоненты, директивы и пайпы, которые он совместно использует.

## Как создать функциональный модуль

Предполагая, что у вас уже есть приложение, созданное с помощью [Angular CLI](https://angular.io/cli), создайте функциональный модуль с помощью CLI, введя следующую команду в корневом каталоге проекта. Замените `CustomerDashboard` на название вашего модуля. Суффикс "Module" в имени можно не указывать, так как CLI добавит его:

```shell
ng generate module CustomerDashboard
```

В результате CLI создаст папку `customer-dashboard` с файлом внутри `customer-dashboard.module.ts` со следующим содержимым:

```ts
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

@NgModule({
    imports: [CommonModule],
    declarations: [],
})
export class CustomerDashboardModule {}
```

Структура NgModule одинакова независимо от того, является ли он корневым или функциональным модулем. В функциональном модуле, сгенерированном CLI, в верхней части файла находятся два оператора импорта JavaScript: первый импортирует `NgModule`, который, как и корневой модуль, позволяет использовать декоратор `@NgModule`; второй импортирует `CommonModule`, который вносит множество общих директив, таких как `ngIf` и `ngFor`. Модули функций импортируют `CommonModule` вместо `BrowserModule`, который импортируется только один раз в корневом модуле. `CommonModule` содержит информацию только для общих директив, таких как `ngIf` и `ngFor`, которые необходимы в большинстве шаблонов, в то время как `BrowserModule` конфигурирует приложение Angular для браузера, что необходимо сделать только один раз.

Массив `declarations` доступен для добавления декларируемых компонентов, директив и пайпов, которые принадлежат только данному модулю. Чтобы добавить компонент, введите в командную строку следующую команду, где `customer-dashboard` - каталог, в котором CLI сгенерировал функциональный модуль, а `CustomerDashboard` - имя компонента:

```shell
ng generate component customer-dashboard/CustomerDashboard
```

При этом создается папка для нового компонента в папке `customer-dashboard` и обновляется функциональный модуль с информацией `CustomerDashboardComponent`:

```ts
// import the new component
import { CustomerDashboardComponent } from './customer-dashboard/customer-dashboard.component';

@NgModule({
  imports: [
    CommonModule,
  ],
  declarations: [
    CustomerDashboardComponent,
  ],
})
```

Компонент `CustomerDashboardComponent` теперь находится в списке импорта JavaScript в верхней части и добавлен в массив `declarations`, что дает Angular знать, что нужно связать этот новый компонент с данным функциональным модулем.

## Импорт функционального модуля

Чтобы включить функциональный модуль в свое приложение, необходимо сообщить о нем корневому модулю `app.module.ts`. Обратите внимание на экспорт `CustomerDashboardModule` в нижней части `customer-dashboard.module.ts`. Это раскрывает его, чтобы другие модули могли обращаться к нему. Чтобы импортировать его в модуль `AppModule`, добавьте его в импорт в `app.module.ts` и в массив `imports`:

```ts
import { HttpClientModule } from '@angular/common/http';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
// import the feature module here so you can add it to the imports array below
import { CustomerDashboardModule } from './customer-dashboard/customer-dashboard.module';

@NgModule({
    declarations: [AppComponent],
    imports: [
        BrowserModule,
        FormsModule,
        HttpClientModule,
        CustomerDashboardModule, // add the feature module here
    ],
    providers: [],
    bootstrap: [AppComponent],
})
export class AppModule {}
```

Теперь `AppModule` знает о функциональном модуле. Если к функциональному модулю добавить поставщиков услуг, то `AppModule` будет знать и о них, как и о любых других функциональных модулях. Однако по умолчанию NgModules не раскрывает свои компоненты.

## Рендеринг шаблона компонента функционального модуля

Когда CLI сгенерировал компонент `CustomerDashboardComponent` для функционального модуля, он включил в него шаблон `customer-dashboard.component.html` со следующей разметкой:

```html
<p>customer-dashboard works!</p>
```

Чтобы увидеть этот HTML в `AppComponent`, необходимо сначала экспортировать `CustomerDashboardComponent` в `CustomerDashboardModule`. В файле `customer-dashboard.module.ts`, сразу под массивом `declarations`, добавьте массив `exports`, содержащий `CustomerDashboardComponent`:

```ts
exports: [CustomerDashboardComponent];
```

Далее в `AppComponent`, `app.component.html`, добавьте тег `<app-customer-dashboard>`:

```html
<h1>{{title}}</h1>

<!-- add the selector from the CustomerDashboardComponent -->
<app-customer-dashboard></app-customer-dashboard>
```

Теперь, помимо заголовка, который отображается по умолчанию, отображается и шаблон `CustomerDashboardComponent`:

![feature module component](feature-module.png)

## Подробнее о NgModules

Возможно, вас также заинтересует следующее:

-   [Ленивая загрузка модулей с помощью Angular Router](lazy-loading-ngmodules.md)
-   [Провайдеры](providers.md)
-   [Типы функциональных модулей](module-types.md)

## Ссылки

-   [Feature modules](https://angular.io/guide/feature-modules)
