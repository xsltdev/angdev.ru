---
description: В Angular-приложении должен быть хотя бы один модуль, который служит корневым. По мере добавления функций в приложение их можно добавлять в модули
---

# Часто используемые модули

:date: 28.02.2022

В Angular-приложении должен быть хотя бы один модуль, который служит корневым. По мере добавления функций в приложение их можно добавлять в модули. Ниже перечислены часто используемые модули Angular с примерами некоторых содержащихся в них функций:

| NgModule              | Импорт из                   | Зачем вы его используете                                       |
| :-------------------- | :-------------------------- | :------------------------------------------------------------- |
| `BrowserModule`       | `@angular/platform-browser` | Для запуска вашего приложения в браузере.                      |
| `CommonModule`        | `@angular/common`           | Для использования `NgIf` и `NgFor`.                            |
| `FormsModule`         | `@angular/forms`            | Для создания форм, управляемых шаблонами (включает `NgModel`). |
| `ReactiveFormsModule` | `@angular/forms`            | Для создания реактивных форм.                                  |
| `RouterModule`        | `@angular/router`           | Для использования `RouterLink`, `.forRoot()` и `.forChild()`.  |
| `HttpClientModule`    | `@angular/common/http`      | Для взаимодействия с сервером по протоколу HTTP.               |

## Импортирование модулей

Когда вы используете эти модули Angular, импортируйте их в `AppModule` или, в зависимости от ситуации, в ваш функциональный модуль и перечислите их в массиве `@NgModule` `imports`. Например, в базовом приложении, сгенерированном с помощью [Angular CLI](https://angular.io/cli), `BrowserModule` является первым импортом в верхней части `AppModule`, `app.module.ts`.

```ts
/* import modules so that AppModule can access them */
import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';

@NgModule({
    declarations: [AppComponent],
    imports: [
        /* add modules here so Angular knows to use them */
        BrowserModule,
    ],
    providers: [],
    bootstrap: [AppComponent],
})
export class AppModule {}
```

Импорты в верхней части массива — это операторы импорта JavaScript, а массив `imports` внутри `@NgModule` специфичен для Angular. Подробнее о различиях см. в [JavaScript Modules vs. NgModules](ngmodule-vs-jsmodule.md).

## `BrowserModule` и `CommonModule`

`BrowserModule` импортирует `CommonModule`, который предоставляет множество общих директив, таких как `ngIf` и `ngFor`. Кроме того, `BrowserModule` реэкспортирует `CommonModule`, делая все его директивы доступными для любого модуля, импортирующего `BrowserModule`.

Для приложений, работающих в браузере, импортируйте `BrowserModule` в корневой `AppModule`, поскольку он предоставляет сервисы, необходимые для запуска и работы браузерного приложения. Провайдеры `BrowserModule` предназначены для всего приложения, поэтому он должен находиться только в корневом модуле, а не в функциональных модулях. Функциональным модулям нужны только общие директивы в `CommonModule`; им не нужно переустанавливать общеприкладные провайдеры.

Если вы импортируете `BrowserModule` в функциональный модуль с ленивой загрузкой, Angular вернет ошибку и предложит использовать вместо него `CommonModule`.

![BrowserModule error](browser-module-error.gif)

## Подробнее о NgModules

Возможно, вас также заинтересует следующее:

-   [Bootstrapping](bootstrapping.md)
-   [NgModules](ngmodules.md)
-   [JavaScript Modules vs. NgModules](ngmodule-vs-jsmodule.md)

## Ссылки

-   [Frequently-used modules](https://angular.io/guide/frequent-ngmodules)
